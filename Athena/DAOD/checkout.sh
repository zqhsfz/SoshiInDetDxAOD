# checkout packges
pkgco.py DerivationFrameworkInDet
pkgco.py InDetPrepRawDataToxAOD
pkgco.py xAODTracking-00-13-24

# apply patches
echo "Applying patches ..."
cp patches/PixelPrepDataToxAOD.cxx InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/src
cp patches/PixelPrepDataToxAOD.h InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/src
cp patches/requirements InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/cmt
cp patches/InDetDxAOD.py InnerDetector/InDetEventCnv/InDetPrepRawDataToxAOD/share
cp patches/TrackStateOnSurfaceDecorator.cxx PhysicsAnalysis/DerivationFramework/DerivationFrameworkInDet/src
