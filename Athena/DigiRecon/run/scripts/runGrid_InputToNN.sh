pathena \
--inDS=mc15_13TeV:mc15_13TeV.361026.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6W.merge.HITS.e3569_s2608_s2183 \
--outDS=user.qzeng.mc15_13TeV.361026.JZ6W.DigiRecon.v00-01-00_blayerON_pixelON_FastBichselON_NoPU_NN \
--nFilesPerJob=1 \
--nFiles=800 \
--trf "Reco_tf.py --pileupFinalBunch '6' --jobNumber %RNDM:0 --conditionsTag 'default:OFLCOND-MC15c-SDR-05' --maxEvents '400' --preInclude 'SimulationJobOptions/preInclude.PileUpBunchTrainsMC15_2015_25ns_Config1.py' --postExec 'all:CfgMgr.MessageSvc().setError+=[\"HepMcParticleLink\"]' 'HITtoRDO:job.StandardPileUpToolsAlg.PileUpTools[\"MdtDigitizationTool\"].LastXing=150' 'HITtoRDO:from AthenaCommon.AppMgr import ToolSvc;ToolSvc.PixelDigitizationTool.LVL1Latency=[16,150,255,255,255,16];ToolSvc.PixelDigitizationTool.ApplyDupli=[True,True,True,True,True,True];ToolSvc.PixelDigitizationTool.LowTOTduplication=[0,5,7,7,7,0]' 'HITtoRDO:from AthenaCommon.AlgSequence import AlgSequence;job=AlgSequence();StreamRDO=job.StreamRDO;StreamRDO.ItemList+=[\"SiHitCollection#*\"];StreamRDO.ForceRead=TRUE;' 'RAWtoESD:from AthenaCommon.AlgSequence import AlgSequence;job=AlgSequence();StreamESD=job.StreamESD;StreamESD.ItemList+=[\"SiHitCollection#*\"];StreamESD.ItemList+=[\"InDetSimDataCollection#*\"];StreamESD.ForceRead=TRUE;' --outputESDFile %OUT.ESD.pool.root --outputRDOFile %OUT.RDO.pool.root --digiSeedOffset2 %RNDM:2 --postInclude 'default:RecJobTransforms/UseFrontier.py' --digiSeedOffset1 %RNDM:1 --skipEvents %SKIPEVENTS --triggerConfig 'MCRECO:DBF:TRIGGERDBMC:2037,14,39' --autoConfiguration 'everything' --inputHITSFile %IN --preExec 'all:rec.Commissioning.set_Value_and_Lock(True);from AthenaCommon.BeamFlags import jobproperties;jobproperties.Beam.numberOfCollisions.set_Value_and_Lock(20.0);from LArROD.LArRODFlags import larRODFlags;larRODFlags.NumberOfCollisions.set_Value_and_Lock(20);larRODFlags.nSamples.set_Value_and_Lock(4);larRODFlags.doOFCPileupOptimization.set_Value_and_Lock(True);larRODFlags.firstSample.set_Value_and_Lock(0);larRODFlags.useHighestGainAutoCorr.set_Value_and_Lock(True)' 'RAWtoESD:from CaloRec.CaloCellFlags import jobproperties;jobproperties.CaloCellFlags.doLArCellEmMisCalib=False' 'ESDtoAOD:TriggerFlags.AODEDMSet=\"AODFULL\"' 'RAWtoESD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.doSlimming.set_Value_and_Lock(False)' 'ESDtoAOD:from InDetRecExample.InDetJobProperties import InDetFlags; InDetFlags.doSlimming.set_Value_and_Lock(False)' 'all:from SiLorentzAngleSvc.SiLorentzAngleSvcConf import SiLorentzAngleSvc;SiLorentzAngleSvc.OutputLevel=VERBOSE; print SiLorentzAngleSvc;from IOVDbSvc.CondDB import conddb;conddb.addOverride(\"/PIXEL/DCS/HV\",\"PixDCSHV-SIMU-RUN2-BL250\");conddb.addOverride(\"/PIXEL/DCS/TEMPERATURE\",\"PixDCSTEMP-SIMU-RUN12-0000-00\");conddb.addOverride(\"/PIXEL/PixCalib\",\"PixCalib-SIM-RUN12-000-04\")' --numberOfCavernBkg '0' " \
--skipScout 

