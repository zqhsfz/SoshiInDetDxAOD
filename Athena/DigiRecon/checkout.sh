# checkout necessary packges
pkgco.py PixelDigitization-02-00-22

# apply patching
echo "Applying patches ..."
cp patches/*Bichsel*.cxx InnerDetector/InDetDigitization/PixelDigitization/src
