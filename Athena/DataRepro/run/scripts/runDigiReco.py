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

def runLocal(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "20"
	extraTrfOptions["inputBSFile"] = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453/data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453._0036.1"
	extraTrfOptions["outputESDFile"] = "MyESD.pool.root"

	cmd = runUtils.GetCmd(TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

def runGrid(printOnly=False):
	extraTrfOptions = deepcopy(extraTrfOptions_kernel)

	extraTrfOptions["maxEvents"] = "300"
	extraTrfOptions["inputBSFile"] = "%IN"
	extraTrfOptions["outputESDFile"] = "%OUT.ESD.pool.root"
	extraTrfOptions["skipEvents"] = "%SKIPEVENTS"

	pathenaOptions = {
	                  "nEventsPerJob": "300",
	                  "skipScout": None,
	                  "inDS": "data15_13TeV.00281411.physics_Main.merge.DRAW_ZMUMU.f629_m1453",
	                  "outDS": "user.qzeng.data15_13TeV.00281411.physics_Main.merge.Recon_ZMUMU.f629_m1453_r7562",
	                 }

	cmd = runUtils.GetPathenaCmd(pathenaOptions, TrfOptions, extraTrfOptions, doNewLine=printOnly)
	print cmd

	if not printOnly:
		os.system(cmd)

if __name__ == "__main__":
	# runLocal(False)
	runGrid(False)








