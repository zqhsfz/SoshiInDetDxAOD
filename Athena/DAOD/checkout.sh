# checkout packges
pkgco.py DerivationFrameworkInDet-00-00-47
pkgco.py InDetPrepRawDataToxAOD-00-01-23

# apply patches
echo "Applying patches ..."
cp patches/PixelPrepDataToxAOD.cxx InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/src
cp patches/PixelPrepDataToxAOD.h InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/src
cp patches/TrackStateOnSurfaceDecorator.cxx PhysicsAnalysis/DerivationFramework/DerivationFrameworkInDet/src
cp patches/InDetDxAOD.py InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/share
