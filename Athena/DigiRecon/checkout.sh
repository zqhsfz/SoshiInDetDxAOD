# checkout necessary packges
pkgco.py PixelDigitization-02-00-22

# check out NN only if you want to apply a special patch below (change sigmoid function)
# pkgco.py TrkNeuralNetworkUtils

# apply patching
echo "Applying patches ..."
cp patches/*Bichsel*.cxx InnerDetector/InDetDigitization/PixelDigitization/src
cp patches/*Bichsel*.h InnerDetector/InDetDigitization/PixelDigitization/src
cp patches/PixelDigitizationConfig.py InnerDetector/InDetDigitization/PixelDigitization/python
cp patches/data/*.dat InnerDetector/InDetDigitization/PixelDigitization/share
# cp patches/TTrainedNetwork.cxx Tracking/TrkUtilityPackages/TrkNeuralNetworkUtils/src

# in case you want to do timing study, do one more step
# cp patches/timer/* InnerDetector/InDetDigitization/PixelDigitization/src
