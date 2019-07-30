import os,sys

samplelist = [

    # '/WpWpJJ_QCD_TuneCP5_14TeV-madgraph-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/WpWpJJ_EWK_TuneCP5_14TeV-madgraph-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/WZTo3LNu_TuneCP5_14TeV-amcatnloFXFX-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/WToLNu_14TeV_TuneCP5_pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/WToLNu_14TeV_TuneCP5_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/VBF_HToInvisible_M125_14TeV_powheg_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/VBFHToBB_M-125_14TeV_powheg_pythia8_weightfix/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/VBFHToBB_M-125_14TeV_powheg_pythia8_weightfix/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/TTbar_14TeV_TuneCP5_pilot_PhaseIITDRSpring19/PhaseIITDRSpring19MiniAOD-PU200_pilot_106X_upgrade2023_realistic_v3_ext1-v3/MINIAODSIM',
    # '/TTbar_14TeV_TuneCP5_pilot_PhaseIITDRSpring19/PhaseIITDRSpring19MiniAOD-NoPU_pilot_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/TTbar_14TeV_TuneCP5_Pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3_ext1-v3/MINIAODSIM',
    # '/TTbar_14TeV_TuneCP5_Pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/SinglePion_PT2to100/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/SinglePion_PT2to100/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    '/SinglePion0_FlatPt-8to100/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    '/SinglePion0_FlatPt-8to100/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/SingleElectron_PT2to100/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/SingleElectron_PT2to100/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/QCD_Pt_0_1000_14TeV_TuneCUETP8M1/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/QCD_Pt_0_1000_14TeV_TuneCUETP8M1/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    '/PhotonFlatPt8To150/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    '/PhotonFlatPt8To150/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/Nu_E10-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v3/MINIAODSIM',
    # '/Muplus_Pt500-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muplus_Pt1000-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muplus_Pt100-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muminus_Pt500-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muminus_Pt50-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muminus_Pt1000-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Muminus_Pt100-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/Mu_FlatPt2to100-pythia8-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/JPsiToMuMu_Pt0to100-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/JPsiToMuMu_Pt0to100-pythia8-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/HSCPppstau_M_871_TuneCUETP8M1_14TeV_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    '/GluGluHToGG_M125_14TeV_amcatnloFXFX_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DoubleElectron_FlatPt-1To100/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v2/MINIAODSIM',
    # '/DisplacedMuons_Pt30to100_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DisplacedMuons_Pt30to100_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DisplacedMuons_Pt2to10_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DisplacedMuons_Pt2to10_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DisplacedMuons_Pt10to30_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DisplacedMuons_Pt10to30_Dxy0to3000-pythia8-gun/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DYToMuMuorEleEle_M-20_14TeV_pythia8/PhaseIITDRSpring19MiniAOD-PU200_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/DYToMuMuorEleEle_M-20_14TeV_pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
    # '/BsToPhiPhi_4K_TuneCP5_14TeV-pythia8/PhaseIITDRSpring19MiniAOD-NoPU_106X_upgrade2023_realistic_v3-v1/MINIAODSIM',
]
   
if not os.path.exists(os.getcwd()+'/fileLists'): os.system('mkdir fileLists')
    
for sample in samplelist:
    print '------------------------------------------'
    print 'Listing',sample

    # print file list to a .txt                                                                              
    if 'PU200' in sample:
        if '_ext' not in sample:
            os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" > fileLists/'+sample.split('/')[1]+'_200PU.txt')
        else:
            os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >> fileLists/'+sample.split('/')[1]+'_200PU.txt')
    elif 'NoPU' in sample:
        if '_ext' not in sample:
            os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" > fileLists/'+sample.split('/')[1]+'_0PU.txt')
        else:
            os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+sample+'" >> fileLists/'+sample.split('/')[1]+'_0PU.txt')

    # check if this sample is on a T2...                                                                     
    #os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="site dataset = '+sample+'"')        

    # print number of events                                                                                 
    #os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="dataset = '+sample+' | grep dataset.nevents" ')                       
