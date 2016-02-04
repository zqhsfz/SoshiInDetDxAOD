import sys
sys.path.append("../../../scripts")

import runUtils
import os



AMITag = "r7534"
Options = runUtils.GetOptions(AMITag)
extraOptions = {
                 "preExec": Options["preExec"] + ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc; SiLorentzAngleSvc.usePixelDefaults=True; SiLorentzAngleSvc.OutputLevel = VERBOSE; print SiLorentzAngleSvc'],
                 "preInclude": ['HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_v1.py'],
                 "geometryVersion": "ATLAS-R2-2015-03-15-00",
                 "steering": None,
                 "maxEvents": "20",
                 "jobNumber": "1",
                 "inputHITSFile": "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/20.7.3.3/sample/user.stsuno.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7335511.EXT0._001325.HITS.pool.root",
                 "inputLowPtMinbiasHitsFile": "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/20.7.3.3/sample/user.stsuno.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7392209.EXT0._000001.HITS.pool.root",
                 "inputHighPtMinbiasHitsFile": "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/20.7.3.3/sample/user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7392273.EXT0._000745.HITS.pool.root",
                 "outputRDOFile": "MyRDO.pool.root",
                 "outputESDFile": "MyESD.pool.root",
               }
cmd = runUtils.GetCmd(Options, extraOptions, doNewLine=False)
print
os.system(cmd)

# print runUtils.GetPathenaCmd({}, Options, extraOptions, doNewLine=True)