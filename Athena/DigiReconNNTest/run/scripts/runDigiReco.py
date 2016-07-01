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
                          "geometryVersion": "ATLAS-R2-2015-03-15-00",       # specific to the samples you are using
                          "steering": None,                                  # no RDO_TRIG step
                         }


####################################
# Control over DAOD Job (ESD->AOD) #
####################################

_doDAOD = True   # touch

##############################
# Control over official VOMS #
##############################

_useOfficialVOMS = True # touch


##############################
# Control over re-trained NN #
##############################

_useRetrainNN = True    # touch


def config_default():
	updateConfig = {}

	if _useRetrainNN:
		if _doDAOD:
			updateConfig['preInclude'] = ['ESDtoDPD:GridCatalogTrick.py']
		else:
			updateConfig['preInclude'] = ['HITtoRDO:GridCatalogTrick.py']
		updateConfig['preExec'] = ['all:from IOVDbSvc.CondDB import conddb;conddb.blockFolder("/PIXEL/PixelClustering/PixelClusNNCalib");conddb.addFolder("", "<dbConnection>sqlite://X;schema=NewPixelNNdb.db;dbname=OFLP200</dbConnection> /PIXEL/PixelClustering/PixelClusNNCalib <tag>PixelClusNNCalib-SIM-RUN2-Bichsel-00-00-00</tag>", force=True)']

	if _doDAOD:
		if 'preExec' not in updateConfig.keys():
			updateConfig['preExec'] = []
		updateConfig['preExec'] += ['ESDtoDPD:from InDetPrepRawDataToxAOD.InDetDxAODJobProperties import InDetDxAODFlags;InDetDxAODFlags.DumpPixelInfo.set_Value_and_Lock(True);InDetDxAODFlags.DumpPixelRdoInfo.set_Value_and_Lock(True);InDetDxAODFlags.DumpPixelNNInfo.set_Value_and_Lock(False);InDetDxAODFlags.DumpSctInfo.set_Value_and_Lock(False);InDetDxAODFlags.DumpTrtInfo.set_Value_and_Lock(False);InDetDxAODFlags.ThinHitsOnTrack.set_Value_and_Lock(False);print "Hahahahaha";print InDetDxAODFlags']

		if 'postExec' not in updateConfig.keys():
			updateConfig['postExec'] = []
		updateConfig['postExec'] += ['ESDtoDPD:IDTRKVALIDStream.AddItem("xAOD::TauJetContainer#TauJets");IDTRKVALIDStream.AddItem("xAOD::TauJetAuxContainer#TauJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt4EMTopoJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt4EMTopoJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt2PV0TrackJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt2PV0TrackJetsAux.");IDTRKVALIDStream.AddItem("xAOD::JetContainer#AntiKt3PV0TrackJets");IDTRKVALIDStream.AddItem("xAOD::JetAuxContainer#AntiKt3PV0TrackJetsAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt4EMTopo");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt4EMTopoAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt2Track");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt2TrackAux.");IDTRKVALIDStream.AddItem("xAOD::BTaggingContainer#BTagging_AntiKt3Track");IDTRKVALIDStream.AddItem("xAOD::BTaggingAuxContainer#BTagging_AntiKt3TrackAux.");']

	return updateConfig


# local job
def runLocal(config, printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	updateTrfOptions = config()
	for key,item in updateTrfOptions.items():
		extraTrfOptions[key] = TrfOptions[key] + item

	extraTrfOptions["maxEvents"] = "20"


	if _doDAOD:
		extraTrfOptions["inputESDFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/group.det-indet.mc15_13TeV.361107.Zmumu.DigiRecon.e3601.v00-02-00.BichselON_EXT0/group.det-indet.8652772.EXT0._000291.ESD.pool.root"
		extraTrfOptions["outputDAOD_IDTRKVALIDFile"] = "MyInDetDxAOD.pool.root"
	else:
		extraTrfOptions["jobNumber"] = "1"
		
		extraTrfOptions["inputHITSFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7335511.EXT0._000518.HITS.pool.root"
		extraTrfOptions["inputLowPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0/user.qzeng.7485559.EXT0._000332.HITS.pool.root"
		extraTrfOptions["inputHighPtMinbiasHitsFile"] = "/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7392273.EXT0._000241.HITS.pool.root"

		extraTrfOptions["outputRDOFile"] = "MyRDO.pool.root"
		extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

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
		                  "inDS": "user.qzeng:user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0",
		                  "lowMinDS": "user.qzeng.mc15_13TeV.361034.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_low.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1.try1_EXT0",
		                  "highMinDS": "user.stsuno.mc15_13TeV.361035.Pythia8EvtGen_A2MSTW2008LO_minbias_inelastic_high.evgen.EVNT.e3581_ATLAS-R2-2015-03-15-00.v1_EXT0",
		                  "outDS": "group.det-indet.mc15_13TeV.361107.Zmumu.DigiRecon.e3601.v00-02-00.Nominal.try1",
		                 }

	if _useRetrainNN:
		pathenaOptions["extFile"] = "GridCatalogTrick.py,NewPixelNNdb.db,NNCalibFinal_NNTrained_20160513_LGTide_JZ6W.root"

	if _useOfficialVOMS:
		pathenaOptions["official"] = None
		pathenaOptions["voms"] = "atlas:/atlas/det-indet/Role=production"

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)


if __name__ == "__main__":
	# runLocal(config_default, False)

	runGrid(config_default, False)














