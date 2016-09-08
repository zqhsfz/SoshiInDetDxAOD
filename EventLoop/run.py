import os
from copy import deepcopy
import time

# local test #
# cmd = "xAH_run.py --files filelists/ICHEP2016/filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8188.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 1000 direct"
# cmd = "xAH_run.py --files filelists/ICHEP2016/filelist_data16_13TeV.00301973.physics_Main.recon.DAOD_IDTRKVALID.f709_m1616_r8184.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 1000 direct"
# cmd = "xAH_run.py --files filelists/ICHEP2016/filelist_group.perf-idtracking.valid4c_totmin6.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.e3601.XAOD_v6_EXT0.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 1000 direct"
# cmd = "xAH_run.py --files filelists/ICHEP2016/filelist_mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.recon.DAOD_IDTRKVALID.e4135_s2608_s2183_r8242.txt --inputList --config PixelClusterAnalyzer/scripts/config.py -f --nevents 1000 direct"
# os.system(cmd)

# batch #

SUBMITFLAG='-q atlas-t3 -W 10:00'

Configs = [
            # {'filelist': 'filelist_data16_13TeV.00301973.physics_Main.recon.DAOD_IDTRKVALID.f709_m1616_r8184.txt', 'shortname': 'data16_13TeV_00301973_r8184', 'nFilesPerWorker': 5},

            # {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8188.txt', 'shortname': 'mc_Zmumu_r8188', 'nFilesPerWorker': 3},
            # {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8192.txt', 'shortname': 'mc_Zmumu_r8192', 'nFilesPerWorker': 3},
            # {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8193.txt', 'shortname': 'mc_Zmumu_r8193', 'nFilesPerWorker': 3},
            # {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8206.txt', 'shortname': 'mc_Zmumu_r8206', 'nFilesPerWorker': 6},

            # {'filelist': 'filelist_group.perf-idtracking.valid4c_totmin6.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.e3601.XAOD_v6_EXT0.txt', 'shortname': 'mc_Zmumu_valid4c_totmin6_XAODv6', 'nFilesPerWorker': 1},

            {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8242.txt', 'shortname': 'mc_Zmumu_r8242', 'nFilesPerWorker': 5},
            {'filelist': 'filelist_mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.recon.DAOD_IDTRKVALID.e3601_s2576_s2132_r8243.txt', 'shortname': 'mc_Zmumu_r8243', 'nFilesPerWorker': 5},
            {'filelist': 'filelist_mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.recon.DAOD_IDTRKVALID.e4135_s2608_s2183_r8242.txt', 'shortname': 'mc_ttbar_r8242', 'nFilesPerWorker': 5},
            {'filelist': 'filelist_mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.recon.DAOD_IDTRKVALID.e4135_s2608_s2183_r8243.txt', 'shortname': 'mc_ttbar_r8243', 'nFilesPerWorker': 5},
            {'filelist': 'filelist_mc16_valid.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.recon.DAOD_IDTRKVALID.e4135_s2608_s2183_r8241.txt', 'shortname': 'mc_ttbar_r8241', 'nFilesPerWorker': 5},

          ]

for config in Configs:
	config_copy = deepcopy(config)
	config_copy['SUBMITFLAG'] = SUBMITFLAG
	cmd = "xAH_run.py --files filelists/ICHEP2016/{filelist} --inputList --config PixelClusterAnalyzer/scripts/config.py -f --submitDir 'submitDir_{shortname}' --nevents 0 lsf --optSubmitFlags='{SUBMITFLAG}' --optBatchSharedFileSystem true --optFilesPerWorker={nFilesPerWorker}".format(**config_copy)

	print cmd
	time.sleep(1)

	os.system(cmd)
