import os
from copy import deepcopy
import time

# local test #
# cmd = "xAH_run.py --files filelists/00-01-02/filelist_mc_BichselON_RetrainNN.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-00-02/filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.v00-00-02_blayerON_pixelON_FastBichselON_ECOffPUOn_nCols5_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-00-01/filelist_data_reference.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-01-03/filelist_mc_BichselON_RetrainNN.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-01-03/filelist_data_RetrainNN.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-02-00/filelist_group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.OldVersion.e3601.v00-02-00.BichselON_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-02-00/filelist_group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601.v00-02-00.BichselON_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 1000 direct"
# os.system(cmd)

# batch #

SUBMITFLAG='-q atlas-t3 -W 10:00'
# SUBMITFLAG='-W 2:00'

Configs = [
            # {'filelist': 'filelist_mc_BichselON_RetrainNN.txt', 'shortname': 'mc_BichselON_RetrainNN', 'nFilesPerWorker': 20},
            # {'filelist': 'filelist_data_RetrainNN.txt', 'shortname': 'data_RetrainNN', 'nFilesPerWorker': 1},

            # {'filelist': 'filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.v00-00-02_blayerON_pixelON_FastBichselON_ECOffPUOn_nCols5_EXT0.txt', 'shortname': 'mc_2016LHCCPublicPlots_BichselON', 'nFilesPerWorker': 20},
            # {'filelist': 'filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_blayerON_pixelON_Nominal_EXT0.txt', 'shortname': 'mc_2016LHCCPublicPlots_Nominal', 'nFilesPerWorker': 10},
            # {'filelist': 'filelist_data_reference.txt', 'shortname': 'data_2016LHCCPublicPlots', 'nFilesPerWorker': 1},

            # {'filelist': 'filelist_group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.OldVersion.e3601.v00-02-00.BichselON_EXT0.txt', 'shortname': 'mc_BichselON_RetrainNN_DigiRecon20p7p5p8_OldVersionDAOD', 'nFilesPerWorker': 20},
            {'filelist': 'filelist_group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.OldVersion.e3601.v00-02-00.Nominal_EXT0.txt', 'shortname': 'mc_Nominal_DigiRecon20p7p5p8_OldVersionDAOD', 'nFilesPerWorker': 20},
          ]

for config in Configs:
	config_copy = deepcopy(config)
	config_copy['SUBMITFLAG'] = SUBMITFLAG
	# cmd = "xAH_run.py --files filelists/00-01-02/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)
	# cmd = "xAH_run.py --files filelists/00-00-01/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)
	# cmd = "xAH_run.py --files filelists/00-01-03/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)
	cmd = "xAH_run.py --files filelists/00-02-00/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)

	print cmd
	time.sleep(1)

	os.system(cmd)
