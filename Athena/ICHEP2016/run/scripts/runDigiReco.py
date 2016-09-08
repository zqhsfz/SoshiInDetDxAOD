import sys
sys.path.append("../../../scripts")

import runUtils
import os
from copy import deepcopy

##########################
# specifically for r7772 #
##########################

# common part for both local and grid job
AMITag = "r7772"
TrfOptions = runUtils.GetOptions(AMITag)

extraTrfOptions_kernel = {
                          "steering": None,                                  # no RDO_TRIG step
                          "triggerConfig": None,                             # Remove --triggerConfig 'RDOtoRDOTrigger=MCRECO:DBF:TRIGGERDBMC:2046,20,56'
                          "preInclude": [
                                          'HITtoRDO:Digitization/ForceUseOfPileUpTools.py,SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py,RunDependentSimData/configLumi_run284500_v2.py',
                                          #'RDOtoRDOTrigger:RecExPers/RecoOutputMetadataList_jobOptions.py',        # Remove RDOtoRDOTrigger
                                        ]
                         }


##############################
# Control over Bichsel model #
##############################

_doBichsel = True # touch


####################################
# Control over DAOD Job (ESD->AOD) #
####################################

_doDAOD = True   # touch


############################################
# Whether we match pixel condition to data #
############################################

_matchData = True # touch

##########################
# Whether we turn off NN #
##########################

_turnOffNN = True # touch


##############################
# Control over official VOMS #
##############################

_useOfficialVOMS = True # touch


def config_default():
	updateConfig = {}

	if 'preExec' not in updateConfig.keys():
		updateConfig['preExec'] = []
	updateConfig['preExec'] += [
	                             'RAWtoESD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.doSlimming.set_Value_and_Lock(False);',
	                             'ESDtoAOD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.doSlimming.set_Value_and_Lock(False);',
	                           ]

	if _doDAOD:
		if 'preExec' not in updateConfig.keys():
			updateConfig['preExec'] = []
		updateConfig['preExec'] += [
		                             'ESDtoDPD:from InDetPrepRawDataToxAOD.InDetDxAODJobProperties import InDetDxAODFlags;InDetDxAODFlags.DumpPixelInfo.set_Value_and_Lock(True);InDetDxAODFlags.DumpPixelRdoInfo.set_Value_and_Lock(True);InDetDxAODFlags.DumpPixelNNInfo.set_Value_and_Lock(False);InDetDxAODFlags.DumpSctInfo.set_Value_and_Lock(False);InDetDxAODFlags.DumpTrtInfo.set_Value_and_Lock(False);InDetDxAODFlags.ThinHitsOnTrack.set_Value_and_Lock(False);print "Printing of InDetDxAODFlags below ...";print InDetDxAODFlags;'
		                           ]

		if 'postExec' not in updateConfig.keys():
			updateConfig['postExec'] = []
		updateConfig['postExec'] += [
		                             'ESDtoDPD:IDTRKVALIDStream.AddItem("xAOD::TauJetContainer#TauJets");IDTRKVALIDStream.AddItem("xAOD::TauJetAuxContainer#TauJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt4EMTopoJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt4EMTopoJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt2PV0TrackJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt2PV0TrackJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt3PV0TrackJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt3PV0TrackJetsAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt4EMTopo");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt4EMTopoAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt2Track");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt2TrackAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt3Track");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt3TrackAux.");'
		                            ]

	if _doBichsel:
		if 'preExec' not in updateConfig.keys():
			updateConfig['preExec'] = []
		updateConfig['preExec'] += [
		                             'HITtoRDO:ftemp_Bichsel=open("addBichselJobProperty.py", "w");ftemp_Bichsel.write("from AthenaCommon.JobProperties import JobProperty\\nfrom Digitization.DigitizationFlags import digitizationFlags\\n\\nprint \\\"addBichselJobProperty being loaded ... \\\"\\n\\nclass doBichselSimulation(JobProperty):\\n\\tstatusOn = True\\n\\tallowedTypes = [\\\"bool\\\"]\\n\\tStoredValue = False\\n\\ndigitizationFlags.add_JobProperty(doBichselSimulation)\\n\\ndigitizationFlags.doBichselSimulation.set_Value_and_Lock(True)\\n");ftemp_Bichsel.close();include("addBichselJobProperty.py");'
		                           ]

	if _matchData:
		if 'preExec' not in updateConfig.keys():
			updateConfig['preExec'] = []
		updateConfig['preExec'] += [
		                            'all:from IOVDbSvc.CondDB import conddb;conddb.addOverride(\"/PIXEL/DCS/HV\",\"PixDCSHV-SIM-MC16a-000-01\");conddb.addOverride(\"/PIXEL/DCS/TEMPERATURE\",\"PixDCSTemp-SIM-MC16a-000-02\");conddb.addOverride(\"/PIXEL/PixCalib\",\"PixCalib-SIM-MC16a-000-02\");conddb.addOverride(\"/PIXEL/PixMapOverlay\",\"PixMapOverlay-SIM-MC16a-000-01\");',
		                           ]

		if 'postExec' not in updateConfig.keys():
			updateConfig['postExec'] = []
		updateConfig['postExec'] += [
		                              # 'HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[False,False,False,False,False,False];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0];ToolSvc.PixelDigitizationTool.ToTMinCut=[0,6,6,6,6,0];ToolSvc.PixelCellDiscriminator.TimingTune=2015;',
		                              'HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[False,False,False,False,False,False];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0];ToolSvc.PixelDigitizationTool.ToTMinCut=[0,6,6,6,6,0];',
		                              'all:from PixelConditionsServices.PixelConditionsServicesConf import PixelOfflineCalibSvc;ServiceMgr+=PixelOfflineCalibSvc();ServiceMgr.PixelOfflineCalibSvc.OverrideIBLToToverflowBin=16;',
		                            ]


	if _turnOffNN:
		if 'preExec' not in updateConfig.keys():
			updateConfig['preExec'] = []
		updateConfig['preExec'] += [
		                             'RAWtoESD:InDetFlags.doPixelClusterSplitting.set_Value_and_Lock(False);InDetFlags.doTIDE_Ambi.set_Value_and_Lock(False)',
		                           ]

	return updateConfig


# local job
def runLocal(config, printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	updateTrfOptions = config()
	for key,item in updateTrfOptions.items():
		extraTrfOptions[key] = TrfOptions[key] + item

	extraTrfOptions["maxEvents"] = "100"
	extraTrfOptions["jobNumber"] = "1"
	extraTrfOptions["inputHITSFile"]              = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.merge.HITS.e3601_s2576_s2132/HITS.05260138._001411.pool.root.1"
	extraTrfOptions["inputLowPtMinbiasHitsFile"]  = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.merge.HITS.e3581_s2578_s2195/HITS.05608147._000306.pool.root.1"
	extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.merge.HITS.e3581_s2578_s2195/HITS.05608152._001169.pool.root.1"

	extraTrfOptions["outputRDOFile"] = "MyRDO.pool.root"
	extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

	if _doDAOD:
		extraTrfOptions["outputDAOD_IDTRKVALIDFile"] = "MyInDetDxAOD.pool.root"

	# extraTrfOptions["athenaopts"] = "-l VERBOSE"

	cmd = runUtils.GetCmd(TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

	return cmd

def runGrid(config, printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	updateTrfOptions = config()
	for key,item in updateTrfOptions.items():
		extraTrfOptions[key] = TrfOptions[key] + item

	extraTrfOptions["maxEvents"] = "100"                    # touch
	extraTrfOptions["skipEvents"] = "%SKIPEVENTS"

	if _doDAOD:
		extraTrfOptions["inputESDFile"] = "%IN"
		extraTrfOptions["outputDAOD_IDTRKVALIDFile"] = "%OUT.InDetDxAOD.pool.root"

		pathenaOptions = {
		                   "nFilesPerJob": "1",
		                   "skipScout": None,
		                   "inDS": "group.det-indet.mc15_13TeV.361107.Zmumu.DigiRecon.e3601.v00-02-00.BichselON_EXT0",
		                   "outDS": "group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601.v00-02-00.BichselON",
		                 }
	else:
		extraTrfOptions["jobNumber"] = "%RNDM:0"
		extraTrfOptions["inputHITSFile"] = "%IN"
		extraTrfOptions["inputLowPtMinbiasHitsFile"] = "%LOMBIN"
		extraTrfOptions["inputHighPtMinbiasHitsFile"] = "%HIMBIN"
		extraTrfOptions["outputRDOFile"] = "%OUT.RDO.pool.root"
		extraTrfOptions["outputESDFile"] = "%OUT.ESD.pool.root"
		extraTrfOptions["digiSeedOffset1"] = "%RNDM:1"
		extraTrfOptions["digiSeedOffset2"] = "%RNDM:2"

		pathenaOptions = {
		                  "nFilesPerJob": "1",
		                  "nLowMin": "5",
		                  "nHighMin": "5",
		                  "skipScout": None,
		                  "inDS"     : "user.qzeng:user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0",
		                  "lowMinDS" : "user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0",
		                  "highMinDS": "user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0",
		                  "outDS": "group.det-indet.mc15_13TeV.361107.Zmumu.DigiRecon.e3601.v00-02-00.Nominal.try1",
		                 }

	if _useOfficialVOMS:
		pathenaOptions["official"] = None
		pathenaOptions["voms"] = "atlas:/atlas/det-indet/Role=production"

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

################

def OrganizeCommand(inputCmd):
	# convert command into 
	inputCmdLines = inputCmd.split("\n")
	inputCmdFirstLine = inputCmdLines[0]
	inputCmdLines = inputCmdLines[1:]

	inputCmdDict = {}
	for line in inputCmdLines:		
		if line == "": continue

		startIndex = line.find("--")+2
		endIndex = line.find(" ")

		key = line[startIndex:endIndex]
		value = line

		inputCmdDict[key] = value

		if key == "":
			print "******************************"
			print " *** ERROR *** line "
			print "******************************"

	targetListOrdred = [

	                     # some basic configuration
	                     'autoConfiguration',
	                     'digiSteeringConf',
	                     'geometryVersion',
	                     'conditionsTag',
	                     'ignorePatterns',

	                     # work-flow
	                     'preInclude',
	                     'preExec',
	                     'postInclude',
	                     'postExec',

	                     # pile-up
	                     'pileupFinalBunch',
	                     'numberOfLowPtMinBias',
	                     'numberOfHighPtMinBias',
	                     'numberOfCavernBkg',

	                     # inputs
	                     'inputHITSFile',
	                     'inputLowPtMinbiasHitsFile',
	                     'inputHighPtMinbiasHitsFile',

	                     # outputs
	                     'outputRDOFile',
	                     'outputESDFile',
	                     'outputDAOD_IDTRKVALIDFile',

	                     # job specification
	                     'jobNumber',
	                     'maxEvents',
	                   ]

	if sorted(targetListOrdred) != sorted(inputCmdDict.keys()):
		print "\n"
		print "*** ERROR ***"
		print "Some lines are missing. Hint:", list(set(targetListOrdred).symmetric_difference(set(inputCmdDict.keys())))
		print "targetListOrdred:",targetListOrdred
		print "originalList:",inputCmdDict.keys()
		print "\n"

	newcmd = "\n".join([inputCmdFirstLine] + [inputCmdDict[key] for key in targetListOrdred])
	return newcmd

if __name__ == "__main__":
	cmd = runLocal(config_default, True)

	print "\n"
	print "Reorganizing ... "
	print "\n"

	print OrganizeCommand(cmd)


	# runGrid(config_default, False)














