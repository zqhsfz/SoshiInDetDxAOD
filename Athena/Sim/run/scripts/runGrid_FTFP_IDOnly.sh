pathena \
--trf "Sim_tf.py --conditionsTag 'default:OFLCOND-MC15c-SDR-02' --geometryVersion 'default:ATLAS-R2-2015-03-15-00_VALIDATION' --physicsList FTFP_BERT_LIV_VALIDATION --truthStrategy 'MC12' --simulator 'MC12G4' --DataRunNumber '284500' --DBRelease 'default:current' --postInclude 'default:PyJobTransforms/UseFrontier.py' --preInclude 'EVNTtoHITS:SimulationJobOptions/preInclude.BeamPipeKill.py,SimulationJobOptions/preInclude.CaloOffDigitConfig.py,SimulationJobOptions/preInclude.MuonOffDigitConfig.py,SimulationJobOptions/preInclude.ForwardOffDigitConfig.py' --maxEvents 100 --inputEVNTFile %IN --outputHITSFile %OUT.HITS.pool.root" \
--nJobs=1000 \
--nFilesPerJob=1 \
--skipScout \
--inDS mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601 \
--outDS user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_FTFP_IDOnly
