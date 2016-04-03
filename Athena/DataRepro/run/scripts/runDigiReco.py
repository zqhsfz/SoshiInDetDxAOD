import sys
sys.path.append("../../../scripts")

import runUtils
import os
from copy import deepcopy

# common part for both local and grid job
AMITag = "r7562"
TrfOptions = runUtils.GetOptions(AMITag)
extraTrfOptions_kernel = {
                         }

##############################
# Control over re-trained NN #
##############################

_doRetrainNN = False #True  # touch
if _doRetrainNN:
	# preInclude
	extraTrfOptions_kernel["preInclude"] = ['RAWtoESD:GridCatalogTrick.py']
	# postExec -- make sure it is the same as default without _RetrainNNAppendix
	_RetrainNNAppendix = 'conddb.blockFolder("/PIXEL/PixelClustering/PixelClusNNCalib");conddb.addFolder("", "<dbConnection>sqlite://X;schema=NewPixelNNdb.db;dbname=CONDBR2</dbConnection> /PIXEL/PixelClustering/PixelClusNNCalib <tag>PixelClusNNCalib-DATA-RUN2-Bichsel-00-00-00</tag>", force=True);'
	extraTrfOptions_kernel["postExec"] = ['ESDtoDPD:from AthenaCommon.AppMgr import ServiceMgr;import MuonRPC_Cabling.MuonRPC_CablingConfig;ServiceMgr.MuonRPC_CablingSvc.RPCMapfromCool=False;ServiceMgr.MuonRPC_CablingSvc.CorrFileName="LVL1confAtlasRUN2_ver016.corr";ServiceMgr.MuonRPC_CablingSvc.ConfFileName="LVL1confAtlasRUN2_ver016.data";', 'RAWtoESD:ToolSvc.MuidRefitTool.DeweightEEL1C05=True;ToolSvc.OutwardsRefitTool.DeweightEEL1C05=True;', 'all:from IOVDbSvc.CondDB import conddb;conddb.addFolderSplitOnline("INDET","/Indet/Onl/IBLDist","/Indet/IBLDist");'+_RetrainNNAppendix]

def runLocal(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "20"
	# extraTrfOptions["inputBSFile"] = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453._0036.1"
	extraTrfOptions["inputBSFile"] = "/afs/cern.ch/user/q/qzeng/eos/atlas/user/q/qzeng/Pixel/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453._0069.1"
	extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

	cmd = runUtils.GetCmd(TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

def runGrid(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "200"
	extraTrfOptions["inputBSFile"] = "%IN"
	extraTrfOptions["outputESDFile"] = "%OUT.ESD.pool.root"
	extraTrfOptions["skipEvents"] = "%SKIPEVENTS"

	pathenaOptions = { 
	                  "nEventsPerJob": "200",
	                  "skipScout": None,
	                  "inDS": "data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453",
	                  # "outDS": "user.qzeng.data15_13TeV.00281411.physics_Main.merge.Recon_ZMUMU.f629_m1453_r7562_v00-01-00_RetrainNN",
	                  "outDS": "user.qzeng.data15_13TeV.00281411.physics_Main.merge.Recon_ZMUMU.f629_m1453_r7562_v00-01-00",

	                  # touch
	                  # "nFilesPerJob": "1",
	                  # "nFiles": "20",
	                  # "outDS": "user.qzeng.data15_13TeV.00281411.physics_Main.merge.Recon_ZMUMU.f629_m1453_r7562.GridTest.Try1",
	                 }

	if _doRetrainNN:
		pathenaOptions["extFile"] = "GridCatalogTrick.py,NewPixelNNdb.db,NNCalibBichselFinal.root"

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

if __name__ == "__main__":
	# runLocal(False)
	runGrid(False)








