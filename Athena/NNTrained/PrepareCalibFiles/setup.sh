setupATLAS
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasoff/InnerDetector/InDetCalibAlgs/PixelCalibAlgs/tags/PixelCalibAlgs-00-07-02/NNClusteringCalibration_RunII

# what to do after this?
# cd NNClusteringCalibration_RunII
# open setupROOT.sh, and replace "TestArea" with the your working directory 
# source setupROOT.sh
# make
# rm prepareCalibration.C
# ln -s ../prepareCalibration.C
# root
# .x doCalibration.C
