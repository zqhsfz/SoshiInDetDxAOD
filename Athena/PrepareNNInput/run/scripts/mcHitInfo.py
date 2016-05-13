### Add Pixel and SCT SiHitCollections to outputStream, if required
if hasattr(topSequence, 'StreamRDO'):
    outStream = topSequence.StreamRDO
else:
    outStreams = AlgSequence( "Streams" )
    if hasattr(outStreams, 'StreamRDO'):
        outStream = outStreams.StreamRDO
        print "********************outStream"

if 'outStream' in dir():
    outStream.ItemList+=["SiHitCollection#PixelHits"]
    outStream.ItemList+=["SiHitCollection#SCT_Hits"]
    print "********************outStream"
else:
    print "NO DICE AGAIN"
