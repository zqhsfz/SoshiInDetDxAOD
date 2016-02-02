# xAH_run.py --files filelist_data_test.txt --inputList  --config PixelClusterAnalyzer/scripts/config.py -f --nevents 5000 direct

# xAH_run.py --files filelist_data.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 5000 direct
xAH_run.py --files filelist_data.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 0 lsf --optSubmitFlags='-q atlas-t3 -W 10:00' --optFilesPerWorker=10
