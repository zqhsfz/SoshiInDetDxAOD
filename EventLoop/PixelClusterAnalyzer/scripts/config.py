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
	                              "m_triggerSelection"      : "",
	                              "m_applyTriggerCut"       : False,
	                              "m_storeTrigDecisions"    : False,
	                            } )

c.setalg("MuonCalibrator", {
	                         "m_name"                : "Muons",
	                         "m_debug"               : False,
	                         "m_inContainerName"     : "Muons",
	                         "m_outContainerName"    : "Muons_Calib",
	                         "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
	                       })

# muon selection following https://twiki.cern.ch/twiki/bin/view/AtlasProtected/VHFAnalysis2015#Event_selection
c.setalg("MuonSelector", {
	                       "m_name"                    : "MuonSelector",
	                       "m_debug"                   : False,
	                       "m_useCutFlow"              : True,
	                       "m_inContainerName"         : "Muons_Calib",
	                       "m_outContainerName"        : "Muons_Selected",
	                       "m_createSelectedContainer" : True,
	                       "m_pT_min"                  : 25e3,
	                       "m_eta_max"                 : 2.4,
	                       "m_muonType"                : "Combined",
	                       "m_muonQualityStr"          : "Medium",
	                       "m_d0sig_max"               : 3,
	                       "m_z0sintheta_max"          : 0.5,
	                       "m_IsoWPList"               : "FixedCutTightTrackOnly",
	                       "m_MinIsoWPCut"             : "FixedCutTightTrackOnly",
	                     })

# todo: muon efficiency SF, calo-jet and jet-muon OR

c.setalg("ZmumuSelector", {
	                        "m_debug"                  : False,
	                        "m_inMuonContainerName"    : "Muons_Calib",
	                        "m_outMuonContainerName"   : "Muons_Zmumu",
	                        "m_outTrackContainerName"  : "Tracks_Zmumu",
	                      })

















