import os
from copy import deepcopy
import time

# local test #
# cmd = "xAH_run.py --files filelists/00-01-00/filelist_user.qzeng.data15_13TeV.00281411.physics_Main.merge.InDetDxAOD_ZMUMU.f629_m1453_r7562_v00-01-00_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-01-00/filelist_user.qzeng.data15_13TeV.00281411.physics_Main.merge.InDetDxAOD_ZMUMU.f629_m1453_r7562_v00-01-00_RetrainNN_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-01-00/filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-01-00_blayerON_pixelON_FastBichselON_RetrainNN_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# os.system(cmd)

# batch for 00-01-00

SUBMITFLAG='-q atlas-t3 -W 10:00'

Configs = [
            {'filelist': 'filelist_user.qzeng.data15_13TeV.00281411.physics_Main.merge.InDetDxAOD_ZMUMU.f629_m1453_r7562_v00-01-00_EXT0.txt', 'shortname': 'data_reference', 'nFilesPerWorker': 20},
            {'filelist': 'filelist_user.qzeng.data15_13TeV.00281411.physics_Main.merge.InDetDxAOD_ZMUMU.f629_m1453_r7562_v00-01-00_RetrainNN_EXT0.txt', 'shortname': 'data_RetrainNN', 'nFilesPerWorker': 20},
            {'filelist': 'filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-01-00_blayerON_pixelON_FastBichselON_RetrainNN_EXT0.txt', 'shortname': 'mc_FastBichselOn_RetrainNN', 'nFilesPerWorker': 20},
          ]

for config in Configs:
	config_copy = deepcopy(config)
	config_copy['SUBMITFLAG'] = SUBMITFLAG
	cmd = "xAH_run.py --files filelists/00-01-00/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)

	print cmd
	time.sleep(1)

	os.system(cmd)
