pathena \
--trf "Reco_tf.py \
--autoConfiguration 'everything' \
--inputESDFile %IN \
--outputDAOD_IDTRKVALIDFile %OUT.InDetDxAOD.pool.root \
--skipEvents %SKIPEVENTS \
--maxEvents '100'" \
--nFilesPerJob=1 \
--skipScout \
--inDS=group.det-indet.mc15_13TeV.361107.Zmumu.DigiRecon.e3601.v00-02-00.Nominal.try1_EXT0/ \
--outDS=group.det-indet.mc15_13TeV.361107.Zmumu.InDetDxAOD.OldVersion.e3601.v00-02-00.Nominal \
--official \
--voms=atlas:/atlas/det-indet/Role=production
