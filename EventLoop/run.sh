# local test
# xAH_run.py --files filelists/filelist_data.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct
# xAH_run.py --files filelists/filelist_mc_BichselON.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct
xAH_run.py --files filelist_test.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct

# batch
# xAH_run.py --files filelists/filelist_data.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 0 lsf --optSubmitFlags='-q atlas-t3 -W 10:00' --optFilesPerWorker=1
