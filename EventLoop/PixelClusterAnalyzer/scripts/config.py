import ROOT
from xAH_config import xAH_config
import sys,os

sys.path.insert(0, os.environ['ROOTCOREBIN']+"/user_scripts/PixelClusterAnalyzer/")

c = xAH_config()

c.setalg("BasicEventSelection", {
	                              "m_name"                  : "basicEventSel",
	                              "m_debug"                 : False,
	                              "m_truthLevelOnly"        : False,
	                              # "m_derivationName"        : 
	                              "m_useMetaData"           : False,
	                              "m_applyGRLCut"           : True,
	                              "m_GRLxml"                : '$ROOTCOREBIN/data/PixelClusterAnalyzer/data15_13TeV.periodAllYear_DetStatus-v73-pro19-08_DQDefects-00-01-02_PHYS_StandardGRL_All_Good_25ns.xml',
	                              "m_doPUreweighting"       : False,
	                              "m_applyEventCleaningCut" : True,
	                              "m_applyCoreFlagsCut"     : True,
	                              "m_vertexContainerName"   : "PrimaryVertices",
	                              "m_applyPrimaryVertexCut" : True,
	                              "m_PVNTrack"              : 2,
	                              "m_triggerSelection"      : "HLT_mu20_iloose_L1MU15,HLT_mu50",
	                              "m_applyTriggerCut"       : False,
	                              "m_storeTrigDecisions"    : True,
	                            } )

c.setalg("MuonCalibrator", {
	                         "m_name"                : "Muons",
	                         "m_debug"               : False,
	                         "m_inContainerName"     : "Muons",
	                         "m_outContainerName"    : "Muons_Calib",
	                         "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
	                       })

c.setalg("JetCalibrator", { "m_name"                   : "AntiKt4TopoEM", 
	                        "m_inContainerName"        : "AntiKt4EMTopoJets",
	                        "m_outContainerName"       : "AntiKt4EMTopoJets_Calib", 
	                        "m_sort"                   : True,
	                        "m_jetAlgo"                : "AntiKt4EMTopo",
	                        "m_outputAlgo"             : "AntiKt4EMTopoJets_Calib_Algo",
	                        "m_calibSequence"          : "JetArea_Residual_Origin_EtaJES_GSC",
	                        "m_calibConfigFullSim"     : "JES_MC15Prerecommendation_April2015.config",
	                        "m_calibConfigData"        : "JES_MC15Prerecommendation_April2015.config",
	                        "m_calibConfigAFII"        : "JES_MC15Prerecommendation_AFII_June2015.config",
	                        "m_jetCleanCutLevel"       : "LooseBad",
	                        "m_JESUncertConfig"        : "$ROOTCOREBIN/data/JetUncertainties/JES_2015/Prerec/PrerecJES2015_3NP_Scenario1_25ns.config",
	                        "m_JESUncertMCType"        : "MC15",
	                        "m_saveAllCleanDecisions"  : True,                         
	                        "m_setAFII"                : False,
	                        "m_JERUncertConfig"        : "JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root",
	                        "m_JERApplyNominal"        : False,
	                        "m_redoJVT"                : True,
	                        "m_systName"               : "",
	                        "m_systVal"                : 0,
	                       })

c.setalg("JetSelector", {
	                      "m_name"                    : "SelectAntiKt4TopoEM",
	                      "m_inContainerName"         : "AntiKt4EMTopoJets_Calib",
	                      "m_inputAlgo"               : "AntiKt4EMTopoJets_Calib_Algo",
	                      "m_outContainerName"        : "AntiKt4EMTopoJets_Calib_Selected",
	                      "m_outputAlgo"              : "AntiKt4EMTopoJets_Calib_Selected_Algo",
	                      "m_decorateSelectedObjects" : False,
	                      "m_createSelectedContainer" : True,
	                      "m_cleanJets"               : False,
	                      "m_pT_min"                  : 25e3,
	                      "m_eta_max"                 : 2.5,
	                      "m_useCutFlow"              : True,
	                      "m_doJVT"                   : True,
	                      "m_jetScaleType"            : "JetConstitScaleMomentum",
	                    })

# todo: muon efficiency SF, calo-jet and jet-muon OR

c.setalg("ZmumuSelector", {
	                        "m_debug"                        : False,

	                        "m_inMuonContainerName"          : "Muons_Calib",
	                        "m_outMuonContainerName"         : "Muons_Zmumu",

	                        "m_inJetContainerName"           : "AntiKt4EMTopoJets_Calib_Selected",
	                        "m_inTrackContainerName"         : "InDetTrackParticles",

	                        "m_outTrackContainerName_Zmumu"  : "Tracks_Zmumu",
	                        "m_outTrackContainerName_Jet"    : "Tracks_Jet",
	                        "m_outTrackContainerName_Other"  : "Tracks_Other",
	                      })















