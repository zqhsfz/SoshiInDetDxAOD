# local test
# xAH_run.py --files filelists/filelist_data_r20.1.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct
# xAH_run.py --files filelists/filelist_data_r20.7.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct
# xAH_run.py --files filelists/filelist_mc_BichselON.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct
# xAH_run.py --files filelists/filelist_test.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 2000 direct

# batch
xAH_run.py --files filelists/filelist_data_r20.1.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir "submitDir_data" --nevents 0 lsf --optSubmitFlags='-q atlas-t3 -W 10:00' --optFilesPerWorker=1
# xAH_run.py --files filelists/filelist_mc_BichselON.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir "submitDir_mc_bichsel" --nevents 0 lsf --optSubmitFlags='-q atlas-t3 -W 10:00' --optFilesPerWorker=10
# xAH_run.py --files filelists/filelist_mc_Nominal.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir "submitDir_mc_nominal" --nevents 0 lsf --optSubmitFlags='-q atlas-t3 -W 10:00' --optFilesPerWorker=10
