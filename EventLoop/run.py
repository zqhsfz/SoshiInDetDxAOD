import os
from copy import deepcopy
import time

# local test #
cmd = "xAH_run.py --files filelists/00-01-01/filelist_data_reference_nn.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --mode class --nevents 2000 direct"
os.system(cmd)

# batch for 00-01-01

# SUBMITFLAG='-q atlas-t3 -W 10:00'

# Configs = [
#             # {'filelist': 'filelist_data_reference_nn.txt', 'shortname': 'data_reference_RetrainNN', 'nFilesPerWorker': 1},
#             {'filelist': 'filelist_mc_BichselON_RetrainNN.txt', 'shortname': 'mc_BichselON_RetrainNN', 'nFilesPerWorker': 10},
#           ]

# for config in Configs:
# 	config_copy = deepcopy(config)
# 	config_copy['SUBMITFLAG'] = SUBMITFLAG
# 	cmd = "xAH_run.py --files filelists/00-01-01/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)

# 	print cmd
# 	time.sleep(1)

# 	os.system(cmd)
