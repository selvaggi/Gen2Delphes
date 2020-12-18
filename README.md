# RTB Gen2Delphes

These scripts facilitate submitting HTCondor jobs that process a defined set of LHE or GEN input files through Delphes.

 * Current CMSSW = CMSSW_10_0_5
 * Current Delphes tag = 3.4.3pre07
 * Current Delphes card = CMS_Phase2_200PU_v07VAL.tcl

## To change the CMSSW or Delphes settings

First, prepare a delphes tarball that has your desired changes to the code and/or the card:
 * Cards should be placed in the CMS_Phase2/ folder
 * Optimally, name the card: CMS_Phase2_200PU_SomeNewLabelHere.tcl
 * **In the PileupMerger section, choose the MinBias_100k line, NOT the /eos/ path!**

Tar your delphes area like this, updating the name of the tarball. This tarball should be put in the DelphesSubmissionLPCcondor area in FNAL eos.
```
tar -zcf Delphes343pre07.tar delphes/
xrdcp Delphes343pre07.tar root://cmseos.fnal.gov//store/user/snowmass/DelphesSubmissionLPCcondor/Delphes343pre07.tar
```

Edit `GENtoDelphes.sh` to reflect these changes. In particular:
 * Line 8: architecture, if needed.
 * Line 33: delphes card name
 * Line 35: delphes tag (for metadata only)
 * Lines 42-43: CMSSW version
 * Line 48: delphes tarball name

## To submit condor jobs at the FNAL LPC:

Currently all ROOT files are directed to CERN's /eos/ system! Check GENtoDelphes.sh to change that if desired.

```
cd ~/nobackup
mkdir DelphesProduction
cd DelphesProduction
git clone https://github.com/recotoolsbenchmarks/Gen2Delphes.git 
cd Gen2Delphes

voms-proxy-init -voms cms -valid 168:00
python -u listFiles.py ## after editing it to select/add your samples!

vi/emacs/nano submitCondor_gen.py ## Edit blocks at line 12 (paths) and sample list at line 27
python -u submitCondor_gen.py 200PU >& submit.log &

tail -f submit.log ## watch and see
```

## To submit condor jobs on lxplus HTCondor:

```
mkdir DelphesProduction
cd DelphesProduction
git clone https://github.com/recotoolsbenchmarks/Gen2Delphes.git 
cd Gen2Delphes

source environment.(c)sh
voms-proxy-init -voms cms -valid 168:00
python -u listFiles.py ## after editing it to select/add your samples!

vi/emacs/nano submitCondor_genCERN.py ## Edit blocks at line 12 (paths) and sample list at line 32
python -u submitCondor_genCERN.py 200PU >& submit.log &

tail -f submit.log ## watch and see
```


## Checking for errors (not checked since 2018!)

To check output of jobs, edit CheckErrorsDelphesGEN.py (check ROOT file directory path & month for zero size test)

python -u CheckErrorsDelphes.py /path/to/logs/ --pileup <0,200>PU --verbose <0,1> --resubmit <0,1> --resub_num <-1,0,1,2,3>

*Note: the final slash on the log file directory path is important*

This will check for four types of failures (give as resub_num argument)

0. Explicit failure of xrdcp, printed in the log file

1. Job went over the 2-day walltime limit on the LPC cluster

1. ROOT file in EOS with zero size. NOTE: have to hardcode the month expected in ls -l

2. No ROOT file with the expected name in EOS. NOTE: hardcode the path if its name differs from the log directory

-1 will resubmit all types of failures.

Logs can be deleted after jobs are successful.


## Post-processing options (not checked since 2018!)

Post-processing scripts are available to hadd and xrdcp files

python -u haddOnCondor.py <0,200>PU

Set up to hadd files and copy to another LPC EOS directory. 

python -u xrdcpOnCondor.py <0,200>PU

Set up to xrdcp files from LPC EOS to CERN EOS.

