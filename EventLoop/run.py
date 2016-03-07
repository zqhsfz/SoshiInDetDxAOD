import os
from copy import deepcopy
import time

# local test #
# cmd = "AH_run.py --files filelists/00-00-01/filelist_data_reference.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct"
# cmd = "xAH_run.py --files filelists/00-00-01/filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_blayerOFF_pixelON_BichselON_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct"
# os.system(cmd)

# batch jobs #

SUBMITFLAG='-q atlas-t3 -W 10:00'
# SUBMITFLAG='-W 0:30'

# data
DataConfigs = [
               {'config': 'reference'},
               {'config': 'IBLToT8_BLayDubOFF'},
               {'config': 'IBLToT8_PixDubOFF'},
              ]

for configDict in DataConfigs:
	configDict_copy = deepcopy(configDict)
	configDict_copy["SUBMITFLAG"] = SUBMITFLAG

	cmd = "xAH_run.py --files filelists/00-00-01/filelist_data_{config}.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_data_{config}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker=1".format(**configDict_copy)
	print cmd
	os.system(cmd)

	time.sleep(1)

# MC
# MCConfigs = [
#               # {"blayer": "ON", "pixel": "ON", "bichsel": False, "nWorkers": 10},
#               # {"blayer": "OFF", "pixel": "ON", "bichsel": False, "nWorkers": 10},
#               # {"blayer": "OFF", "pixel": "OFF", "bichsel": False, "nWorkers": 10},

#               # {"blayer": "ON", "pixel": "ON", "bichsel": True, "nWorkers": 20},
#               # {"blayer": "OFF", "pixel": "ON", "bichsel": True, "nWorkers": 20},
#               # {"blayer": "OFF", "pixel": "OFF", "bichsel": True, "nWorkers": 20},
#             ]

# for configDict in MCConfigs:
# 	configDict_copy = deepcopy(configDict)

# 	configDict_copy["BichselStr_filelist"] = ("BichselON" if configDict_copy["bichsel"] else "Nominal")
# 	configDict_copy["BichselStr_submitdir"] = ("bichsel" if configDict_copy["bichsel"] else "nominal")
# 	configDict_copy["SUBMITFLAG"] = SUBMITFLAG

# 	cmd = "xAH_run.py --files filelists/00-00-01/filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_blayer{blayer}_pixel{pixel}_{BichselStr_filelist}_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_mc_{BichselStr_submitdir}_blayer{blayer}_pixel{pixel}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nWorkers}".format(**configDict_copy)
# 	print cmd
# 	os.system(cmd)

# 	time.sleep(1)
