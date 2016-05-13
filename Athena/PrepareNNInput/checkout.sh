cmt checkout svn+ssh://svn.cern.ch/reps/atlasperf/CombPerf/Tracking/TrackingInDenseEnvironments/SimpleSamples 
git clone https://:@gitlab.cern.ch:8443/lgagnon/pixel-configurable-matrix-size.git
cd SimpleSamples && patch -p0 -i ../pixel-configurable-matrix-size/TIDExAODAnalysis_track-thinning.patch && cd ..
pkgco.py PixelDigitization
cp patches/PixelDigitizationConfig.py InnerDetector/InDetDigitization/PixelDigitization/python/

setupWorkArea.py
cd WorkArea/cmt && cmt bro cmt config && cmt bro gmake

cd ../../run/scripts
cp ../../SimpleSamples/GenerateRunII/scripts/mcHitInfo.py .                                                              
cp ../../SimpleSamples/GenerateRunII/scripts/TIDExAODAnalysis.py _TIDExAODAnalysis.py
svn export svn+ssh://svn.cern.ch/reps/atlasoff/Simulation/ISF/ISF_Example/trunk/share/preInclude.IDonly_reconstruction.py
