cp /cvmfs/atlas-condb.cern.ch/repo/conditions/poolcond/PoolFileCatalog.xml .

coolHist_insertFileToCatalog.py NNCalibFinal_NNTrained_20160513_LGTide_JZ6W.root

AtlCoolCopy.exe "COOLOFL_PIXEL/OFLP200" "sqlite://X;schema=NewPixelNNdb.db;dbname=OFLP200" -f /PIXEL/PixelClustering/PixelClusNNCalib -nd -rdo -c

coolHist_setReference.py 'sqlite://X;schema=NewPixelNNdb.db;dbname=OFLP200' /PIXEL/PixelClustering/PixelClusNNCalib 1 PixelClusNNCalib-SIM-RUN2-Bichsel-00-00-00 NNCalibFinal_NNTrained_20160513_LGTide_JZ6W.root
