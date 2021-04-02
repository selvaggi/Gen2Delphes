#### python -u submitCondor_gen.py 200PU >& submit.log &

import os,datetime,time,subprocess
from listFiles import *

runDir=os.getcwd()

os.system('xrdcp -f root://cmseos.fnal.gov//store/user/snowmass/DelphesSubmissionLPCcondor/scripts/EOSSafeUtils.py '+runDir)
execfile(runDir+'/EOSSafeUtils.py')

start_time = time.time()
pileup = str(sys.argv[1])

#IO directories must be full paths
outputDir='/store/group/upgrade/RTB/Delphes343pre07/v08/'  ## For CERN condor

#condorDir='/uscms_data/d3/jmanagan/Validation2019/delphes343pre01/' # Change username, helps to match log directory to the ROOT file directory, adding "_logs" (for compatibility with error checker)
condorDir='condor' # Change username, helps to match log directory to the ROOT file directory, adding "_logs" (for compatibility with error checker)

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

print fileList


for sample in fileList:
    if '_'+pileup not in sample: continue
    with open(os.path.abspath(sample),'r') as rootlist:
        rootfiles = []
        rootfiles_bare = []
        for line in rootlist:
            rootfiles.append('root://xrootd-cms.infn.it/'+line.strip())
            rootfiles_bare.append(line.strip())
 

    '''
    rootlist = open(sample)
    rootfiles = []
    rootfiles_bare = []
    for line in rootlist:
        rootfiles.append('root://xrootd-cms.infn.it/'+line.strip())
        rootfiles_bare.append(line.strip())
        # OPTIONAL: use a more exact accessor for certain samples at CERN:
        #if(sample != 'WprimeToWZToWhadZinv_narrow_M-600_13TeV-madgraph.txt'): rootfiles.append('root://eoscms.cern.ch/'+line.strip())
        #else: rootfiles.append('root://cmsxrootd.fnal.gov/'+line.strip())
    rootlist.close()
    '''


    relPath = sample.replace('.txt','').replace('fileLists/','')
    if '_'+pileup in relPath: relPath = relPath.replace('_'+pileup,'')

    os.system('eos root://eoscms.cern.ch/ mkdir -p '+outputDir+relPath+'_'+pileup) # For running @ CERN
    ## os.system('eos root://cmseos.fnal.gov/ mkdir -p '+outputDir+relPath+'_'+pileup) #For FNAL
    ## os.system('gfal-mkdir -p srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2'+outputDir+relPath+'_'+pileup) ## DESY???
    #os.system('mkdir -p '+condorDir+relPath+'_'+pileup)

    condor_dir='%s/%s/%s_%s'%(runDir,condorDir,relPath,pileup)
    os.system('mkdir -p {}'.format(condor_dir))

    os.chdir(condor_dir)

    print condor_dir, relPath

    cmdfile="""# here goes your shell script
use_x509userproxy = true
x509userproxy = {}
universe = vanilla
+JobFlavour = tomorrow
+AccountingGroup = "group_u_CMST3.all"
Executable = {}/GENtoDelphes.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
#output  = condor.$(ClusterId).$(ProcId).out
#error   = condor.$(ClusterId).$(ProcId).err
#log     = condor.$(ClusterId).log
output = /dev/null
error= /dev/null
log = /dev/null
Notification = Never
""".format(proxyPath,runDir)


    tempcount = 0;
    for ifile, file in enumerate(rootfiles):
        infile = file

        #print infile
        tempcount+=1
        #if tempcount == 1: continue   # OPTIONAL to submit a test job

        fname_bare = rootfiles_bare[ifile]
        #print fname_bare

        #count+=1
        ### usual submitter if no splitting
        if not maxEvtsPerJob > -1:
            outfile = relPath+'_'+str(tempcount)
            dict={'RUNDIR':runDir, 'RELPATH':relPath, 'PILEUP':pileup, 'FILEIN':infile, 'FILEOUT':outfile, 'OUTPUTDIR':outputDir, 'PROXY':proxyPath}

        #----------------
        def file_exist(myfile):
            import os.path
            if os.path.isfile(myfile): return True
            else: return False

        eosfile='/eos/cms/{}/{}_{}/{}.root'.format(outputDir, relPath, pileup, outfile)

        if not file_exist(eosfile):
           count+=1
           print 'did not find: ', eosfile
           print '  --> (re-)submitting ... '

           argstr="Arguments = %(FILEIN)s %(OUTPUTDIR)s/%(RELPATH)s_%(PILEUP)s %(FILEOUT)s.root %(PILEUP)s\n"%dict
           cmdfile += argstr
           cmdfile += 'queue\n'

           #os.system('condor_submit %(FILEOUT)s.jdl'%dict)
           #os.system('sleep 0.5')

	   #print str(count), "jobs submitted!!!"


    with open('condor_delphes.sub' , "w") as f:
        f.write(cmdfile)


    # submitting jobs
    print 'submitting {} jobs ... '.format(relPath)
    os.system('condor_submit condor_delphes.sub')

    ## go back to run dir 
    os.chdir('%s'%(runDir))

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))

