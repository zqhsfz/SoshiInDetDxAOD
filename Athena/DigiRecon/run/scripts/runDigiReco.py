import sys
sys.path.append("../../../scripts")

import runUtils
import os
from copy import deepcopy

# this script is only applicable to r7534 tag
# This is because we are assuming the updated configuration has never been shown in the default configuration. So instead of overwrite, they are simply appended to the original configuration

# common part for both local and grid job
AMITag = "r7534"
TrfOptions = runUtils.GetOptions(AMITag)
extraTrfOptions_kernel = {
                          "preInclude": ['HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_v1.py'],
                          "geometryVersion": "ATLAS-R2-2015-03-15-00",
                          "steering": None,
                         }

# configuration for version 00-00-00
def config_v00_00_00():
	updateConfig = {
	  "postExec": [],
	  "preExec": ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc; SiLorentzAngleSvc.usePixelDefaults=True; SiLorentzAngleSvc.OutputLevel = VERBOSE; print SiLorentzAngleSvc'],
	}
	return updateConfig

# configuration for 00-00-01:
# new charge calibration for b-layer (ToT18)
# Correct HV in b-layer (250 V)
# Vary LowTOTduplication setting

def config_blayerON_pixelON():
	updateConfig = {
	  "postExec": ['HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[True,True,True,True,True,True];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0]'],
	  "preExec": ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc;SiLorentzAngleSvc.OutputLevel=VERBOSE; print SiLorentzAngleSvc;from IOVDbSvc.CondDB import conddb;conddb.addOverride("/PIXEL/DCS/HV","PixDCSHV-SIMU-RUN2-BL250");conddb.addOverride("/PIXEL/DCS/TEMPERATURE","PixDCSTEMP-SIMU-RUN12-0000-00");conddb.addOverride("/PIXEL/PixCalib","PixCalib-SIM-RUN12-000-04")'],
	}
	return updateConfig

def config_blayerOFF_pixelON():
	updateConfig = {
	  "postExec": ['HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[True,False,True,True,True,True];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0]'],
	  "preExec": ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc;SiLorentzAngleSvc.OutputLevel=VERBOSE; print SiLorentzAngleSvc;from IOVDbSvc.CondDB import conddb;conddb.addOverride("/PIXEL/DCS/HV","PixDCSHV-SIMU-RUN2-BL250");conddb.addOverride("/PIXEL/DCS/TEMPERATURE","PixDCSTEMP-SIMU-RUN12-0000-00");conddb.addOverride("/PIXEL/PixCalib","PixCalib-SIM-RUN12-000-04")'],
	}
	return updateConfig

def config_blayerOFF_pixelOFF():
	updateConfig = {
	  "postExec": ['HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[True,False,False,False,False,True];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0]'],
	  "preExec": ['all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc;SiLorentzAngleSvc.OutputLevel=VERBOSE; print SiLorentzAngleSvc;from IOVDbSvc.CondDB import conddb;conddb.addOverride("/PIXEL/DCS/HV","PixDCSHV-SIMU-RUN2-BL250");conddb.addOverride("/PIXEL/DCS/TEMPERATURE","PixDCSTEMP-SIMU-RUN12-0000-00");conddb.addOverride("/PIXEL/PixCalib","PixCalib-SIM-RUN12-000-04")'],
	}
	return updateConfig

################################################################

def runLocal(config, printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)
	updateTrfOptions = config()

	for key,item in updateTrfOptions.items():
		extraTrfOptions[key] = TrfOptions[key] + item

	extraTrfOptions["maxEvents"] = "200"
	extraTrfOptions["jobNumber"] = "1"
	
	# extraTrfOptions["inputHITSFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7335511.EXT0._000518.HITS.pool.root"
	# extraTrfOptions["inputLowPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0/user.qzeng.7485559.EXT0._000332.HITS.pool.root"
	# extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7392273.EXT0._000241.HITS.pool.root"
	
	# extraTrfOptions["inputHITSFile"] = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.simul.HITS.e4398_s2608/HITS.06476735._000007.pool.root.1"
	# extraTrfOptions["inputLowPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.simul.HITS.e3581_s2806/HITS.07591856._013487.pool.root.1"
	# extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.simul.HITS.e3581_s2806/HITS.07591861._004380.pool.root.1"

	extraTrfOptions["inputHITSFile"] = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/Pixel/mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.simul.HITS.e4398_s2608/HITS.06476735._000007.pool.root.1"
	extraTrfOptions["inputLowPtMinbiasHitsFile"] = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/Pixel/mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.simul.HITS.e3581_s2806/HITS.07591856._013426.pool.root.1"
	extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/Pixel/mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.simul.HITS.e3581_s2806/HITS.07591861._007384.pool.root.1"

	extraTrfOptions["outputRDOFile"] = "MyRDO.pool.root"
	# extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

	# extraTrfOptions["athenaopts"] = "-l VERBOSE"

	cmd = runUtils.GetCmd(TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

def runGrid(config, printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)
	updateTrfOptions = config()

	for key,item in updateTrfOptions.items():
		extraTrfOptions[key] = TrfOptions[key] + item

	configName = config.__name__
	configSkipID = "config_"
	configName = configName[configName.find(configSkipID)+len(configSkipID):]

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
	                  "inDS": "user.qzeng:user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0",
	                  "lowMinDS": "user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0",
	                  "highMinDS": "user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0",
	                  "outDS": "user.qzeng.mc15_13TeV.361107.Zmumu.DigiRecon.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_%s_BichselON" % (configName),
	                 }

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

if __name__ == "__main__":
	runLocal(config_blayerON_pixelON, False)

	# runGrid(config_blayerON_pixelON, False)
	# runGrid(config_blayerOFF_pixelON, False)
	# runGrid(config_blayerOFF_pixelOFF, False)








