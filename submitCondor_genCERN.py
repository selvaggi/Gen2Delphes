#### python -u submitCondor_gen.py 200PU >& submit.log &

import os,datetime,time,subprocess
runDir=os.getcwd()

os.system('xrdcp -f root://cmseos.fnal.gov//store/user/snowmass/DelphesSubmissionLPCcondor/scripts/EOSSafeUtils.py '+runDir)
execfile(runDir+'/EOSSafeUtils.py')

start_time = time.time()
pileup = str(sys.argv[1])

#IO directories must be full paths
outputDir='/store/group/upgrade/RTB/Delphes343pre07/v07VALclosure/'  ## For CERN condor

condorDir='/uscms_data/d3/jmanagan/Validation2019/delphes343pre01/' # Change username, helps to match log directory to the ROOT file directory, adding "_logs" (for compatibility with error checker)

maxEvtsPerJob = -1 #50000 for production ## -1 --> do not make splitting (1 job per file)

## Proxy settings differ between CERN and Fermilab...
print 'Getting proxy'
proxyPath=os.popen('voms-proxy-info -path')
proxyPath=proxyPath.readline().strip()
print 'ProxyPath:',proxyPath
if 'tmp' in proxyPath: 
    print 'Run source environment.(c)sh and make a new proxy!'
    exit(1)

print 'Starting submission'
cTime=datetime.datetime.now()
count=0

fileList = [  # CHOOSE SAMPLES, you MUST have listed the file names with listFiles.py

    #'TT_TuneCP5_14TeV-powheg-pythia8_200PU.txt',
    #'GluGluHToTauTau_M125_14TeV_powheg_pythia8_TuneCP5_200PU.txt',
    'GluGluToHHTo2B2G_node_SM_TuneCP5_14TeV-madgraph_pythia8_200PU.txt',
    'QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_200PU.txt',
    'DYToLL_M-50_TuneCP5_14TeV-pythia8_200PU.txt',

    ]

for sample in fileList:
    if '_'+pileup not in sample: continue

    rootlist = open('fileLists/'+sample)
    rootfiles = []
    rootfiles_bare = []
    for line in rootlist:
        rootfiles.append('root://xrootd-cms.infn.it/'+line.strip())
        rootfiles_bare.append(line.strip())
        # OPTIONAL: use a more exact accessor for certain samples at CERN:
        #if(sample != 'WprimeToWZToWhadZinv_narrow_M-600_13TeV-madgraph.txt'): rootfiles.append('root://eoscms.cern.ch/'+line.strip())
        #else: rootfiles.append('root://cmsxrootd.fnal.gov/'+line.strip())
    rootlist.close()

    relPath = sample.replace('.txt','')
    if '_'+pileup in relPath: relPath = relPath.replace('_'+pileup,'')

    os.system('eos root://eoscms.cern.ch/ mkdir -p '+outputDir+relPath+'_'+pileup) # For running @ CERN
    ## os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outputDir+relPath+'_'+pileup) #For FNAL
    ## os.system('gfal-mkdir -p srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2'+outputDir+relPath+'_'+pileup) ## DESY???
    os.system('mkdir -p '+condorDir+relPath+'_'+pileup)

    tempcount = 0;
    for ifile, file in enumerate(rootfiles):
        infile = file

        tempcount+=1
        #if tempcount == 1: continue   # OPTIONAL to submit a test job

        fname_bare = rootfiles_bare[ifile]
        n_jobs = 1
        if maxEvtsPerJob > -1: ## just query DAS if necessary
            command = '/cvmfs/cms.cern.ch/common/dasgoclient --query="file='+fname_bare+' | grep file.nevents" '
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            try: nevents = int(out.split('\n')[0])
            except:
                try: nevents = int(out.split('\n')[1])
                except: print 'ERROR: couldnt isolate the number of events'

            n_jobs = int(nevents) / int(maxEvtsPerJob)
            if int(nevents) % int(maxEvtsPerJob) > 0:
                n_jobs += 1 ## and extra one to account for the remainder

        ### split based on the number of events
        for i_split in range(n_jobs):

            count+=1
            ### usual submitter if no splitting
            if not maxEvtsPerJob > -1:
                outfile = relPath+'_'+str(tempcount)

                dict={'RUNDIR':runDir, 'RELPATH':relPath, 'PILEUP':pileup, 'FILEIN':infile, 'FILEOUT':outfile, 'OUTPUTDIR':outputDir, 'PROXY':proxyPath}
                jdfName=condorDir+'/%(RELPATH)s_%(PILEUP)s/%(FILEOUT)s.jdl'%dict
                # print jdfName
                jdf=open(jdfName,'w')
                jdf.write(
                    """use_x509userproxy = true
x509userproxy = %(PROXY)s
universe = vanilla
+JobFlavour = tomorrow
Executable = %(RUNDIR)s/GENtoDelphes.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Output = %(FILEOUT)s.out
Error = %(FILEOUT)s.err
Log = %(FILEOUT)s.log
Notification = Never
Arguments = %(FILEIN)s %(OUTPUTDIR)s/%(RELPATH)s_%(PILEUP)s %(FILEOUT)s.root %(PILEUP)s

Queue 1"""%dict)  ##Requirements = (TARGET.TotalCpus == 8)
            else:
                outfile = relPath+'_'+str(tempcount)+'_'+str(i_split)
                maxEvents = int(maxEvtsPerJob)
                skipEvents = int(maxEvtsPerJob*i_split)
                if i_split == n_jobs-1:
                   maxEvents = nevents - maxEvtsPerJob*(n_jobs-1) ## up to the last event

                dict={'RUNDIR':runDir, 'RELPATH':relPath, 'PILEUP':pileup, 'FILEIN':infile, 'FILEOUT':outfile, 'OUTPUTDIR':outputDir, 'SKIPEVENTS':str(skipEvents), 'MAXEVENTS':str(maxEvents), 'ISPLIT':str(i_split), 'PROXY':proxyPath}
                jdfName=condorDir+'/%(RELPATH)s_%(PILEUP)s/%(FILEOUT)s.jdl'%dict ## note: i_split is contained in FILEOUT
                jdf=open(jdfName,'w')
                jdf.write(
                    """use_x509userproxy = true
x509userproxy = %(PROXY)s
universe = vanilla
+JobFlavor = nextweek
Executable = %(RUNDIR)s/GENtoDelphes.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Output = %(FILEOUT)s.out
Error = %(FILEOUT)s.err
Log = %(FILEOUT)s.log
Notification = Never
Arguments = %(FILEIN)s %(OUTPUTDIR)s/%(RELPATH)s_%(PILEUP)s %(FILEOUT)s.root %(PILEUP)s %(SKIPEVENTS)s %(MAXEVENTS)s

Queue 1"""%dict) ## Requirements = (TARGET.TotalCpus == 8)

            jdf.close()
            os.chdir('%s/%s_%s'%(condorDir,relPath,pileup))
            os.system('condor_submit %(FILEOUT)s.jdl'%dict)
            os.system('sleep 0.5')
            os.chdir('%s'%(runDir))
            print str(count), "jobs submitted!!!"

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))



