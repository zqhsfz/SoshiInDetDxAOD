Reco_tf.py \
--maxEvents 20 \
--autoConfiguration='everything' \
--inputHITSFile=/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/samples/user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/user.stsuno.7335511.EXT0._000518.HITS.pool.root \
--outputESDFile=MyESD.pool.root \
--preInclude 'RAWtoESD:preInclude.IDonly_reconstruction.py' \
--postInclude 'HITtoRDO:mcHitInfo.py' 'RAWtoESD:_TIDExAODAnalysis.py'
