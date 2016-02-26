# checkout necessary packges
pkgco.py PixelDigitization-02-00-22

# apply patching
echo "Applying patches ..."
cp patches/*Bichsel*.cxx InnerDetector/InDetDigitization/PixelDigitization/src
cp patches/*Bichsel*.h InnerDetector/InDetDigitization/PixelDigitization/src
cp patches/PixelDigitizationConfig.py InnerDetector/InDetDigitization/PixelDigitization/python

# in case you want to do timing study, do one more step
# cp patches/timer/* InnerDetector/InDetDigitization/PixelDigitization/src
