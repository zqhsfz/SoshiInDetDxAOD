import sys
sys.path.append("../../../scripts")

import runUtils
import os
from copy import deepcopy

# common part for both local and grid job
AMITag = "r7534"
TrfOptions = runUtils.GetOptions(AMITag)
extraTrfOptions_kernel = {
                          "preExec": TrfOptions["preExec"] + ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc; SiLorentzAngleSvc.usePixelDefaults=True; SiLorentzAngleSvc.OutputLevel = VERBOSE; print SiLorentzAngleSvc'],
                          "preInclude": ['HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_v1.py'],
                          "geometryVersion": "ATLAS-R2-2015-03-15-00",
                          "steering": None,
                         }

def runLocal(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "1"
	extraTrfOptions["jobNumber"] = "1"
	extraTrfOptions["inputHITSFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7335511.EXT0._000518.HITS.pool.root"
	extraTrfOptions["inputLowPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0/user.qzeng.7485559.EXT0._000332.HITS.pool.root"
	extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7392273.EXT0._000241.HITS.pool.root"
	extraTrfOptions["outputRDOFile"] = "MyRDO.pool.root"
	# extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

	cmd = runUtils.GetCmd(TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

def runGrid(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "100"
	extraTrfOptions["jobNumber"] = "%RNDM:0"
	extraTrfOptions["inputHITSFile"] = "%IN"
	extraTrfOptions["inputLowPtMinbiasHitsFile"] = "%LOMBIN"
	extraTrfOptions["inputHighPtMinbiasHitsFile"] = "%HIMBIN"
	extraTrfOptions["outputRDOFile"] = "%OUT.RDO.pool.root"
	extraTrfOptions["outputESDFile"] = "%OUT.ESD.pool.root"
	extraTrfOptions["digiSeedOffset1"] = "%RNDM:1"
	extraTrfOptions["digiSeedOffset2"] = "%RNDM:2"
	extraTrfOptions["skipEvents"] = "%SKIPEVENTS"

	pathenaOptions = {
	                  "nFilesPerJob": "1",
	                  "nLowMin": "5",
	                  "nHighMin": "5",
	                  "skipScout": None,
	                  "inDS": "user.stsuno.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0",
	                  "lowMinDS": "user.stsuno.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0",
	                  "highMinDS": "user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0",
	                  "outDS": "user.qzeng.mc15_13TeV.361107.Zmumu.DigiRecon.e3601_ATLAS-R2-2015-03-15-00.v1_Nominal",
	                 }

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

if __name__ == "__main__":
	runLocal(False)
	# runGrid(False)








