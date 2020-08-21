#!/bin/bash

#################################### Wrapper submit script for Upgrade production 
#Written by Alexis Kalogeropoulos - July 2014
#Adapted by Julie Hogan - summer 2016, jmhogan@fnal.gov

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700

startTime=`date +%s`

# Condor arguments
# Arguments = %(FILEIN)s %(OUTPUTDIR)s/%(RELPATH)s_%(PILEUP)s %(FILEOUT)s.root %(PILEUP)s
FILEIN=$1
OUTPUT=$2
FILEOUT=$3
PILEUP=$4
SKIPEVT=$5
MAXEVT=$6

echo "Starting job on " `date`
echo "Running on " `uname -a`
echo "System release " `cat /etc/redhat-release`

if [[ $# -eq 4 ]] ; then
    echo "Setting SkipEvents to 0, no argument given"
    SKIPEVT=0
    echo "Setting MaxEvents to -1, no argument given"
    MAXEVT=-1
fi

# Set variables
detCard=CMS_PhaseII_${PILEUP}_v05VAL.tcl
energy=14
DelphesVersion=tags/3.4.3pre01
nPU=`echo $detCard | cut -d '_' -f 2 | cut -d '.' -f 1`
process=`echo $FILEIN | cut -d '_' -f 1-2`
configuration=`echo $detCard | cut -d '_' -f 1-2`
DelphesOutput=CMSP2_${nPU}_`echo $FILEIN`.root

# make the CMSSW release, compile, and copy
scram project CMSSW_10_0_5
cd CMSSW_10_0_5/src
eval `scram runtime -sh`
cd -

echo "xrdcp source tarball and pileup file"
xrdcp -f root://cmseos.fnal.gov//store/user/snowmass/DelphesSubmissionLPCcondor/Delphes343pre01_v05VAL.tar tarball.tar #CHECK ME!
XRDEXIT=$?
if [[ $XRDEXIT -ne 0 ]]; then
    echo "exit code $XRDEXIT, failure in xrdcp of Delphes.tar"
    exit $XRDEXIT
fi

tar -xf tarball.tar
rm -f tarball.tar 
cd delphes
# Delphes is already compiled in the tarball

xrdcp -f root://cmseos.fnal.gov//store/user/snowmass/DelphesSubmissionLPCcondor/MinBias_100k.pileup .
XRDEXIT=$?
if [[ $XRDEXIT -ne 0 ]]; then
    echo "exit code $XRDEXIT, failure in xrdcp of MinBias_100k.pileup"
    exit $XRDEXIT
fi

# echo "xrdcp input miniAOD"
# filein should already be in root://eoscms.cern.ch//store/mc/... format
# xrdcp -f ${FILEIN} delphesinput.root
# XRDEXIT=$?
# if [[ $XRDEXIT -ne 0 ]]; then
#     echo "exit code $XRDEXIT, failure in xrdcp of GEN file"
#     exit $XRDEXIT
# fi

setupTime=`date +%s`

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#run MiniAOD through Delphes

sed -i "s|MAXEVENTS|${MAXEVT}|g" cards/CMS_PhaseII/$detCard
sed -i "s|SKIPEVENTS|${SKIPEVT}|g" cards/CMS_PhaseII/$detCard

./DelphesCMSFWLite cards/CMS_PhaseII/$detCard ${FILEOUT} ${FILEIN}
DELPHESEXIT=$?
if [[ $DELPHESEXIT -ne 0 ]]; then
    echo "exit code $DELPHESEXIT, failure in DelphesCMSFWLite (maybe from xrootd)"
    exit $DELPHESEXIT
fi

DelphesTime=`date +%s`

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#metadata

echo "User: " `eval whoami`
echo "Date: " `date` 
echo 

echo "Process: " $process 
echo "Pileup Conditions: " $nPU 
echo "Configuration: " $configuration 
echo "Energy: " $energy 
echo 

echo "Input MiniAOD: " $FILEIN
echo "Skipped Events: " $SKIPEVT 
echo "Run Events: " $MAXEVT 
echo 

echo "Delphes Output: " $FILEOUT
echo "Delphes Version: " $DelphesVersion 
echo "Detector Card: " $detCard 
echo 

echo "Minutes spent setting up job: " `expr $setupTime / 60 - $startTime / 60` 
echo "Minutes spent running Delphes: " `expr $DelphesTime / 60 - $setupTime / 60` 
echo 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# copy output to eos
# Running @CERN this should be fine with the root://eoscms.cern.ch eosOutDir
# Running @DESY likely need to change this copy command!
echo "xrdcp -f ${FILEOUT} root://eoscms.cern.ch/${OUTPUT}/${FILEOUT}"
#xrdcp -f ${FILEOUT} root://cmseos.fnal.gov/${OUTPUT}/${FILEOUT} 2>&1
xrdcp -f ${FILEOUT} root://eoscms.cern.ch/${OUTPUT}/${FILEOUT} 2>&1
#gfal-cp ${FILEOUT} srm://dcache-se-cms.desy.de/pnfs/desy.de/cms/tier2/${OUTPUT}/${FILEOUT} 2>&1 ## Maybe??
XRDEXIT=$?
if [[ $XRDEXIT -ne 0 ]]; then
    echo "exit code $XRDEXIT, failure in xrdcp of ROOT"
    exit $XRDEXIT
fi

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
endTime=`date +%s`
echo "Time spent copying output (s): " `expr $endTime - $DelphesTime`
echo "Total runtime (m): " `expr $endTime / 60 - $startTime / 60`

echo "removing inputs from condor"
rm -f ${FILEOUT}
rm -f *.root MinBias_100k.pileup
