cp /cvmfs/atlas-condb.cern.ch/repo/conditions/poolcond/PoolFileCatalog.xml .

coolHist_insertFileToCatalog.py NNCalibBichselFinal.root

AtlCoolCopy.exe "COOLOFL_PIXEL/CONDBR2" "sqlite://X;schema=NewPixelNNdb.db;dbname=CONDBR2" -f /PIXEL/PixelClustering/PixelClusNNCalib -nd -rdo -c

coolHist_setReference.py 'sqlite://X;schema=NewPixelNNdb.db;dbname=CONDBR2' /PIXEL/PixelClustering/PixelClusNNCalib 1 PixelClusNNCalib-DATA-RUN2-Bichsel-00-00-00 NNCalibBichselFinal.root
