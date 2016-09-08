// EL include(s)
#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include "EventLoop/OutputStream.h"

// package include(s)
#include "xAODAnaHelpers/HelperClasses.h"
#include "xAODAnaHelpers/HelperFunctions.h"
#include <xAODAnaHelpers/tools/ReturnCheck.h>
#include <PixelClusterAnalyzer/ZmumuSelector.h>

// EDM include(s)
#include "AthContainers/ConstDataVector.h"

// ROOT include(s)
#include "TLorentzVector.h"

// C++ Standards
#include <iostream>
#include <algorithm>
#include <vector>

// this is needed to distribute the algorithm to the workers
ClassImp(ZmumuSelector)

// Copy of enum MeasurementType from Athena: Tracking/TrkEvent/TrkEventPrimitives/TrkEventPrimitives/TrackStateDefs.h
namespace TrackState {
  enum MeasurementType {
    unidentified = 0,
    Pixel      = 1,
    SCT        = 2,
    TRT        = 3,
    MDT        = 4,
    CSC        = 5,
    RPC        = 6,
    TGC        = 7,
    Pseudo     = 8,
    Vertex     = 9,
    Segment    = 10,
    SpacePoint = 11,
    LArCal     = 12,
    TileCal    = 13,
    STGC       = 14,
    MM         = 15,
    NumberOfMeasurementTypes=16
  };
}

// Copy of enum TrackStateOnSurfaceType from Athena: Tracking/TrkEvent/TrkTrack/TrkTrack/TrackStateOnSurface.h
namespace TrackStateOnSurface {
  enum TrackStateOnSurfaceType {
    /** This is a measurement, and will at least contain a Trk::MeasurementBase*/
    Measurement=0,
 
    /** This represents inert material, and so will contain MaterialEffectsBase */
    InertMaterial=1, 
            
    /** This represents a brem point on the track,
     * and so will contain TrackParameters and MaterialEffectsBase */
    BremPoint=2, 
         
    /** This represents a scattering point on the track,
     * and so will contain TrackParameters and MaterialEffectsBase */
    Scatterer=3, 
          
    /** This represents a perigee, and so will contain a Perigee
     * object only*/
    Perigee=4, 
         
    /** This TSoS contains an outlier, that is, it contains a
     * MeasurementBase/RIO_OnTrack which was not used in the track
     * fit*/
    Outlier=5,
          
    /** A hole on the track - this is defined in the following way.
     * A hole is a missing measurement BETWEEN the first and last
     * actual measurements. i.e. if your track starts in the SCT,
     * you should not consider a missing b-layer hit as a hole.*/
    Hole=6,
    /** For some reason this does not fall into any of the other categories
     * PLEASE DO NOT USE THIS - DEPRECATED!*/
    Unknown=7,
           
    /** This TSOS contains a CaloEnergy object*/
    CaloDeposit=8,
              
    /**
     * This TSOS contains a Trk::MeasurementBase
     */
    Parameter=9,
            
    /**
     * This TSOS contains a Trk::FitQualityOnSurface
     */
    FitQuality=10,
    NumberOfTrackStateOnSurfaceTypes=11
  };
}

ZmumuSelector :: ZmumuSelector ()
{
  // Here you put any code for the base initialization of variables,
  // e.g. initialize all pointers to 0.  Note that you should only put
  // the most basic initialization here, since this method will be
  // called on both the submission and the worker node.  Most of your
  // initialization code will go into histInitialize() and
  // initialize().

  Info("ZmumuSelector()", "Calling constructor");

  m_muonSelection = 0;

  m_event = 0;
  m_store = 0;

  m_eventInfo = 0;

  m_debug = false;

  m_inMuonContainerName = "";
  m_outMuonContainerName = "";

  m_inJetContainerName = "";
  m_inTrackContainerName = "";

  m_outTrackContainerName_PVTrack = "";
  m_outTrackContainerName_Zmumu = "";
  m_outTrackContainerName_Jet = "";
  m_outTrackContainerName_Other = "";

  m_outputName = "ZmumuSelector";

  m_histsvc_cutflow = 0;
  m_histsvc_event = 0;
  m_histsvc_muons = 0;
  m_histsvc_tracks = 0;
  m_histsvc_pixelclusters = 0;

  m_EvtWeight = 1.;

  m_PrimaryVertex = 0;

}



EL::StatusCode ZmumuSelector :: setupJob (EL::Job& job)
{
  // Here you put code that sets up the job on the submission object
  // so that it is ready to work with your algorithm, e.g. you can
  // request the D3PDReader service or add output files.  Any code you
  // put here could instead also go into the submission script.  The
  // sole advantage of putting it here is that it gets automatically
  // activated/deactivated when you add/remove the algorithm from your
  // job, which may or may not be of value to you.

  Info("setupJob()", "Calling setupJob");

  job.useXAOD ();
  xAOD::Init("ZmumuSelector").ignore(); // call before opening first file

  EL::OutputStream OutputStream_ZmumuSelector(m_outputName);
  job.outputAdd(OutputStream_ZmumuSelector);

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: histInitialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.

  if(!HistSvcInit()) return EL::StatusCode::FAILURE;

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: changeInput (bool firstFile)
{
  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: initialize ()
{
  // Here you do everything that you need to do after the first input
  // file has been connected and before the first event is processed,
  // e.g. create additional histograms based on which variables are
  // available in the input files.  You can also create all of your
  // histograms and trees in here, but be aware that this method
  // doesn't get called if no events are processed.  So any objects
  // you create here won't be available in the output if you have no
  // input events.

  Info("initialize()", "Initializing ZmumuSelector Interface ...");
  
  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  m_muonSelection = new CP::MuonSelectionTool("MuonSelection_Zmumu");
  m_muonSelection->msg().setLevel(MSG::ERROR);
  // does not matter what initialization we use, since we will do explicit cut later
  m_muonSelection->setProperty("MaxEta", 2.5);
  m_muonSelection->setProperty("MuQuality", 2); // Medium
  m_muonSelection->initialize();

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: execute ()
{
  // Here you do everything that needs to be done on every single
  // events, e.g. read input variables, apply cuts, and fill
  // histograms and trees.  This is where most of your actual analysis
  // code will go.

  if(m_debug) Info("execute()", "Running ZmumuSelector ...");

  // reset hist svc
  m_histsvc_cutflow->Reset();
  m_histsvc_event->Reset();
  m_histsvc_muons->Reset();
  m_histsvc_tracks->Reset();
  m_histsvc_pixelclusters->Reset();

  // get primary vertex
  std::string PrimaryVertexContainerName("PrimaryVertices");
  const xAOD::VertexContainer* PrimaryVertices(nullptr);
  RETURN_CHECK("ZmumuSelector::execute()", HelperFunctions::retrieve(PrimaryVertices, PrimaryVertexContainerName, m_event, m_store, m_debug), "");
  m_PrimaryVertex = HelperFunctions::getPrimaryVertex(PrimaryVertices);

  // set weight
  m_EvtWeight = 1.;

  // Initial of cut-flow
  FillCutflow("Initial");

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Triggers 
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  if(m_debug) Info("execute()", "Passing Triggers");

  RETURN_CHECK("ZmumuSelector::execute()", HelperFunctions::retrieve(m_eventInfo, "EventInfo", m_event, m_store, m_debug), "");

  std::vector<std::string> passTriggers = m_eventInfo->auxdata<std::vector<std::string> >("passTriggers");
  bool pass_HLT_mu20_iloose_L1MU15 = (std::find(passTriggers.begin(), passTriggers.end(), "HLT_mu20_iloose_L1MU15") != passTriggers.end());
  bool pass_HLT_mu50 = (std::find(passTriggers.begin(), passTriggers.end(), "HLT_mu50") != passTriggers.end());

  if( !pass_HLT_mu20_iloose_L1MU15 && !pass_HLT_mu50 ) return EL::StatusCode::SUCCESS;

  FillCutflow("PassTrigger");

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Jet Cleaning
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  if(m_debug) Info("execute()", "Passing Jet Cleaning");

  const xAOD::JetContainer* inJets(nullptr);
  RETURN_CHECK("ZmumuSelector::execute()", HelperFunctions::retrieve(inJets, m_inJetContainerName, m_event, m_store, m_debug), "");

  bool passJetCleaning = true;
  for(auto jet : *inJets){
    passJetCleaning = (passJetCleaning && jet->auxdata<char>("cleanJet"));
  }

  if(!passJetCleaning) return EL::StatusCode::SUCCESS;

  FillCutflow("PassJetCleaning");

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Muon Selection, and Z->mumu event selection
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // read input muons
  const xAOD::MuonContainer* inMuons(nullptr);
  RETURN_CHECK("ZmumuSelector::execute()", HelperFunctions::retrieve(inMuons, m_inMuonContainerName, m_event, m_store, m_debug) ,"");

  if(m_debug) Info("execute()", "Passing Muon Selection");

  // muon selection
  std::vector<const xAOD::Muon*> selectMuons;
  for(auto muon : *inMuons){
    // pT, eta
    if(muon->pt() < 25e3) continue;
    if(abs(muon->eta()) > 2.4) continue;

    // quality
    if(m_muonSelection->getQuality(*muon) > xAOD::Muon::Loose) continue;

    // IDCut
    // if(!m_muonSelection->passedIDCuts(*muon)) continue; // this one will kill all muons ... 
    if(!muon->passesIDCuts()) continue;

    selectMuons.push_back(muon);
  }

  // sort muons by pT
  std::sort(selectMuons.begin(), selectMuons.end(), ZmumuSelector::sort_pt);

  // create output muons
  ConstDataVector<xAOD::MuonContainer>* outMuons_Zmumu(nullptr);
  outMuons_Zmumu = new ConstDataVector<xAOD::MuonContainer>(SG::VIEW_ELEMENTS);

  if(m_debug) Info("execute()", "Passing Z->mumu event selection");

  // Z->mumu event selection
  // only two leading selected muons are considered
  // Zmumu selection reference https://twiki.cern.ch/twiki/bin/view/AtlasProtected/VHFAnalysis2015#Event_selection
  // Also following Soshi's code: https://svnweb.cern.ch/trac/atlasperf/browser/CombPerf/Tracking/TrackingInDenseEnvironments/SimpleAnaxAOD/trunk/ParticleAnalysis/Root/ZmumuAnalysis.cxx

  if(selectMuons.size() < 2) return EL::StatusCode::SUCCESS;

  FillCutflow("PassAtLeastTwoMuons");

  const xAOD::Muon* Muon1_Zmumu = selectMuons[0];
  const xAOD::Muon* Muon2_Zmumu = selectMuons[1];

  if(Muon1_Zmumu->charge() * Muon2_Zmumu->charge() >= 0) return EL::StatusCode::SUCCESS;

  FillCutflow("PassOppositeMuons");

  TLorentzVector Zboson = Muon1_Zmumu->p4() + Muon2_Zmumu->p4();
  double Zboson_mass = Zboson.M();
  if( (Zboson_mass <= 76e3) || (Zboson_mass >= 106e3) ) return EL::StatusCode::SUCCESS;

  FillCutflow("PassZMassWindow");

  // store output muons
  outMuons_Zmumu->push_back(Muon1_Zmumu);
  outMuons_Zmumu->push_back(Muon2_Zmumu);
  RETURN_CHECK("ZmumuSelector::execute()", m_store->record(outMuons_Zmumu, m_outMuonContainerName), "Failed to store muons from Zmumu");

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // extract tracks
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////  

  if(m_debug) Info("execute()", "Extracting tracks");

  const xAOD::TrackParticleContainer* inTracks(nullptr);
  RETURN_CHECK("ZmumuSelector::execute()", HelperFunctions::retrieve(inTracks, m_inTrackContainerName, m_event, m_store, m_debug) ,"");

  // PV-track
  if(m_debug) Info("execute()", "Storing PV-tracks");

  ConstDataVector<xAOD::TrackParticleContainer>* outTracks_PV(nullptr);
  outTracks_PV = new ConstDataVector<xAOD::TrackParticleContainer>(SG::VIEW_ELEMENTS);

  for(auto Track : *inTracks){
    // must from PV
    if(Track->vertex() != m_PrimaryVertex) continue;

    // track selection
    if(!TrackSelection(Track)) continue;

    outTracks_PV->push_back(Track);
  }

  RETURN_CHECK("ZmumuSelector::execute()", m_store->record(outTracks_PV, m_outTrackContainerName_PVTrack), "Failed to store tracks from PV");

  // muon-tracks
  if(m_debug) Info("execute()", "Storing muon-tracks");

  ConstDataVector<xAOD::TrackParticleContainer>* outTracks_Zmumu(nullptr);
  outTracks_Zmumu = new ConstDataVector<xAOD::TrackParticleContainer>(SG::VIEW_ELEMENTS);

  for(auto Muon : *outMuons_Zmumu){
    auto el_tp = Muon->inDetTrackParticleLink();
    if((!el_tp.isValid()) || !(*el_tp)){
      if(m_debug) Warning("execute()", "Invalid link to InnerDetectorTrackParticle from Muon!");
      continue;
    }

    if(!TrackSelection(*el_tp)) continue;

    outTracks_Zmumu->push_back(*el_tp);
  }

  RETURN_CHECK("ZmumuSelector::execute()", m_store->record(outTracks_Zmumu, m_outTrackContainerName_Zmumu), "Failed to store Zmumu tracks");

  // jet-tracks
  if(m_debug) Info("execute()", "Storing jet-tracks");

  ConstDataVector<xAOD::TrackParticleContainer>* outTracks_jet(nullptr);
  outTracks_jet = new ConstDataVector<xAOD::TrackParticleContainer>(SG::VIEW_ELEMENTS);

  for(auto Jet : *inJets){
    // // take tracks for b-tagging
    // auto v_el_tp = Jet->btagging()->auxdata<std::vector<ElementLink<xAOD::TrackParticleContainer> > >("BTagTrackToJetAssociator");
    // for(auto el_tp : v_el_tp){
    //   if( (!el_tp.isValid()) || (!(*el_tp)) ){
    //     if(m_debug) Warning("execute()", "Invalid link to InnerDetectorTrackParticle from Jet b-tagging \"BTagTrackToJetAssociator\" decoration!");
    //     continue;
    //   }

    //   if(!TrackSelection(*el_tp)) continue;

    //   outTracks_jet->push_back(*el_tp);
    // }

    auto v_tracks = Jet->getAssociatedObjects<xAOD::TrackParticle>("GhostTrack");
    for(auto track : v_tracks){
      if(!track){
        Warning("execute()", "Invalid link to InnerDetectorTrackParticle from Jet \"GhostTrack\" decoration! This track will be skipped");
        continue;
      }

      if(!TrackSelection(track)) continue;

      outTracks_jet->push_back(track);
    }
  }

  RETURN_CHECK("ZmumuSelector::execute()", m_store->record(outTracks_jet, m_outTrackContainerName_Jet), "Failed to store tracks inside jet");

  // other-tracks
  if(m_debug) Info("execute()", "Storing other-tracks");

  ConstDataVector<xAOD::TrackParticleContainer>* outTracks_other(nullptr);
  outTracks_other = new ConstDataVector<xAOD::TrackParticleContainer>(SG::VIEW_ELEMENTS);

  for(auto Track : *inTracks){
    // anything that is left
    if(std::find(outTracks_Zmumu->begin(), outTracks_Zmumu->end(), Track) != outTracks_Zmumu->end()) continue;
    if(std::find(outTracks_jet->begin(), outTracks_jet->end(), Track) != outTracks_jet->end()) continue;

    if(!TrackSelection(Track)) continue;

    outTracks_other->push_back(Track);
  }

  RETURN_CHECK("ZmumuSelector::execute()", m_store->record(outTracks_other, m_outTrackContainerName_Other), "Failed to store tracks from other places");

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Fill Histograms
  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  if(m_debug) Info("execute()", "Begin filling histograms");

  // event histograms
  if(m_debug) Info("execute()", "Filling event histograms");
  m_histsvc_event->Reset();

  m_histsvc_event->Set("nJets", inJets->size());
  m_histsvc_event->Set("nTracks_Zmumu", outTracks_Zmumu->size());
  m_histsvc_event->Set("nTracks_jet", outTracks_jet->size());
  m_histsvc_event->Set("nTracks_other", outTracks_other->size());

  m_histsvc_event->MakeHists("GoodEvents", "");

  // muon histograms
  if(m_debug) Info("execute()", "Filling muon histograms");
  for(auto Muon : *outMuons_Zmumu){
    m_histsvc_muons->Reset();

    m_histsvc_muons->Set("Pt", Muon->pt()/1000.);
    m_histsvc_muons->Set("Eta", Muon->eta());
    m_histsvc_muons->Set("Quality_DAOD", Muon->quality());

    m_histsvc_muons->MakeHists("GoodEvents", "_Muons_Zmumu");
  }

  // track histograms
  if(m_debug) Info("execute()", "Filling track histograms");
  RETURN_CHECK("ZmumuSelector::execute()", FillHistogramTracks(m_outTrackContainerName_PVTrack), "Failure when filling track histograms");
  RETURN_CHECK("ZmumuSelector::execute()", FillHistogramTracks(m_outTrackContainerName_Zmumu), "Failure when filling track histograms");
  RETURN_CHECK("ZmumuSelector::execute()", FillHistogramTracks(m_outTrackContainerName_Jet), "Failure when filling track histograms");
  RETURN_CHECK("ZmumuSelector::execute()", FillHistogramTracks(m_outTrackContainerName_Other), "Failure when filling track histograms");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: postExecute ()
{
  // Here you do everything that needs to be done after the main event
  // processing.  This is typically very rare, particularly in user
  // code.  It is mainly used in implementing the NTupleSvc.

  if(m_debug) Info("postExecute()", "Calling postExecute");

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.  This is different from histFinalize() in that it only
  // gets called on worker nodes that processed input events.

  Info("finalize()", "Deleting tool instance ...");

  if(m_muonSelection) {m_muonSelection = 0; delete m_muonSelection;}
  if(m_histsvc_cutflow) {m_histsvc_cutflow = 0; delete m_histsvc_cutflow;}
  if(m_histsvc_event) {m_histsvc_event = 0; delete m_histsvc_event;}
  if(m_histsvc_muons) {m_histsvc_muons = 0; delete m_histsvc_muons;}
  if(m_histsvc_tracks) {m_histsvc_tracks = 0; delete m_histsvc_tracks;}
  if(m_histsvc_pixelclusters) {m_histsvc_pixelclusters = 0; delete m_histsvc_pixelclusters;}

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode ZmumuSelector :: histFinalize ()
{
  // This method is the mirror image of histInitialize(), meaning it
  // gets called after the last event has been processed on the worker
  // node and allows you to finish up any objects you created in
  // histInitialize() before they are written to disk.  This is
  // actually fairly rare, since this happens separately for each
  // worker node.  Most of the time you want to do your
  // post-processing on the submission node after all your histogram
  // outputs have been merged.  This is different from finalize() in
  // that it gets called on all worker nodes regardless of whether
  // they processed input events.

  Info("histFinalize()", "Calling histFinalize");

  return EL::StatusCode::SUCCESS;
}

bool ZmumuSelector :: HistSvcInit()
{
  if(m_debug) Info("HistSvcInit()", "Entering HistSvcInit.");

  m_histsvc_cutflow = new Analysis_AutoHists(wk()->getOutputFile(m_outputName));

  m_histsvc_event = new Analysis_AutoHists(wk()->getOutputFile(m_outputName));
  m_histsvc_event->Book("nJets", "nJets", &m_EvtWeight, 50, -0.5, 49.5);
  m_histsvc_event->Book("nTracks_Zmumu", "nTracks_Zmumu", &m_EvtWeight, 20, -0.5, 19.5);
  m_histsvc_event->Book("nTracks_jet", "nTracks_jet", &m_EvtWeight, 2000, -0.5, 1999.5);
  m_histsvc_event->Book("nTracks_other", "nTracks_other", &m_EvtWeight, 2000, -0.5, 1999.5);

  m_histsvc_muons = new Analysis_AutoHists(wk()->getOutputFile(m_outputName));
  m_histsvc_muons->Book("Pt", "Pt", &m_EvtWeight, 500, 0, 500);
  m_histsvc_muons->Book("Eta", "Eta", &m_EvtWeight, 60, -3, 3);
  m_histsvc_muons->Book("Quality_DAOD", "Quality_DAOD", &m_EvtWeight, 10, -1.5, 8.5);

  m_histsvc_tracks = new Analysis_AutoHists(wk()->getOutputFile(m_outputName));
  m_histsvc_tracks->Book("Pt", "Pt", &m_EvtWeight, 500, 0, 500);
  m_histsvc_tracks->Book("Eta", "Eta", &m_EvtWeight, 60, -3, 3);
  m_histsvc_tracks->Book("Pt_d0", "Pt", "d0", &m_EvtWeight, 500, 0, 500, 200, -1, 1);
  m_histsvc_tracks->Book("Pt_z0", "Pt", "z0", &m_EvtWeight, 500, 0, 500, 400, -2, 2);
  m_histsvc_tracks->Book("Pt_z0sintheta", "Pt", "z0sintheta", &m_EvtWeight, 500, 0, 500, 400, -2, 2);

  m_histsvc_pixelclusters = new Analysis_AutoHists(wk()->getOutputFile(m_outputName));
  BookHistogramPixelCluster(m_histsvc_pixelclusters);

  if(m_debug) Info("HistSvcInit()", "Leaving HistSvcInit.");

  return true;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Cutflow
///////////////////////////////////////////////////////////////////////////////////////////////////

bool ZmumuSelector :: FillCutflow(std::string cutname)
{
  m_histsvc_cutflow->AutoFill("Cutflow", "", "CountEntry_"+cutname, 0, 1, 1, -0.5, 0.5);
  m_histsvc_cutflow->AutoFill("Cutflow", "", "CountWeight_"+cutname, 0, m_EvtWeight, 1, -0.5, 0.5);

  return true;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Fill Tracks
///////////////////////////////////////////////////////////////////////////////////////////////////

StatusCode ZmumuSelector :: FillHistogramTracks(std::string TrackContainerName)
{
  if(m_debug) Info("FillHistogramTracks()", "Begin fill track container %s", TrackContainerName.c_str());

  // fetch track collection
  const xAOD::TrackParticleContainer* TracksToFill(nullptr);
  RETURN_CHECK("ZmumuSelector::FillHistogramTracks()", HelperFunctions::retrieve(TracksToFill, TrackContainerName, m_event, m_store, m_debug), "");

  for(auto Track : *TracksToFill){
    // tracks
    m_histsvc_tracks->Reset();

    m_histsvc_tracks->Set("Pt", Track->pt()/1000.);
    m_histsvc_tracks->Set("Eta", Track->eta());
    m_histsvc_tracks->Set("d0", Track->d0());

    double dz = Track->z0() + Track->vz() - m_PrimaryVertex->z();
    m_histsvc_tracks->Set("z0", dz);
    m_histsvc_tracks->Set("z0sintheta", dz * TMath::Sin(Track->theta()));

    m_histsvc_tracks->MakeHists("GoodEvents", "_"+TrackContainerName);

    // pixel clusters
    auto msosVector = GetPixelMeasurements(Track);
    for(auto msos : msosVector){
      auto PixelCluster = GetPixelCluster(msos);
      if(!SelectGoodPixelCluster(PixelCluster)) continue;
      if(!FillHistogramPixelCluster(TrackContainerName, msos, PixelCluster, Track)) continue;
    }
  }

  return StatusCode::SUCCESS;
}

///////////////////////////////////////////////////////////////////////////////////////////////////
// Pixel Clusters
///////////////////////////////////////////////////////////////////////////////////////////////////

bool ZmumuSelector :: BookHistogramPixelCluster(Analysis_AutoHists* histsvc)
{
  // Hit Summary
  histsvc->Book("Charge", "Charge", &m_EvtWeight, 100, 0., 5e5);
  histsvc->Book("Charge90", "Charge90", &m_EvtWeight, 100, 0., 5e5);
  histsvc->Book("SumCharge", "SumCharge", &m_EvtWeight, 100, 0., 5e5);
  histsvc->Book("EnergyLoss", "EnergyLoss", &m_EvtWeight, 100, 0, 1000.);
  histsvc->Book("SumEnergyLoss", "SumEnergyLoss", &m_EvtWeight, 100, 0, 1000.);
  histsvc->Book("ToT", "ToT", &m_EvtWeight, 200, 0., 1000.);
  histsvc->Book("ToTNonZero", "ToTNonZero", &m_EvtWeight, 200, 0., 1000.);
  histsvc->Book("LogCharge", "LogCharge", &m_EvtWeight, 500, -8., 8.);
  histsvc->Book("isFake", "isFake", &m_EvtWeight, 2, -0.5, 1.5);
  histsvc->Book("isGanged", "isGanged", &m_EvtWeight, 2, -0.5, 1.5);
  histsvc->Book("isSplit", "isSplit", &m_EvtWeight, 2, -0.5, 1.5);
  histsvc->Book("splitProb1", "splitProb1", &m_EvtWeight, 50, 0., 1.1);
  histsvc->Book("splitProb2", "splitProb2", &m_EvtWeight, 50, 0., 1.1);

  // Cluster Position
  histsvc->Book("Layer", "Layer", &m_EvtWeight, 5, -0.5, 4.5);
  histsvc->Book("Bec", "Bec", &m_EvtWeight, 11, -5.5, 5.5);
  histsvc->Book("LocalX", "LocalX", &m_EvtWeight, 200, -10., 10.);
  histsvc->Book("LocalY", "LocalY", &m_EvtWeight, 200, -100., 100.);
  histsvc->Book("GlobalZ", "GlobalZ", &m_EvtWeight, 1000, -600., 600.);
  histsvc->Book("GlobalR", "GlobalR", &m_EvtWeight, 150, 0., 150.);
  histsvc->Book("InciPhi", "InciPhi", &m_EvtWeight, 70, 0., 0.7);
  histsvc->Book("InciTheta", "InciTheta", &m_EvtWeight, 200, -2., 2.);
  histsvc->Book("trkPhi", "trkPhi", &m_EvtWeight, 100, -TMath::Pi()-1, TMath::Pi()+1);
  histsvc->Book("trkEta", "trkEta", &m_EvtWeight, 50, -2.5, 2.5); 
  histsvc->Book("trkPt", "trkPt", &m_EvtWeight, 100, 0., 50.);
  histsvc->Book("trkPt_long", "trkPt", &m_EvtWeight, 400, 0., 200.);
  histsvc->Book("trkP", "trkP", &m_EvtWeight, 100, 0., 50.);
  histsvc->Book("trkd0_InciPhi", "trkd0", "InciPhi", &m_EvtWeight, 250, -1., 1., 70, 0, 0.7);
  histsvc->Book("trkz0_InciPhi", "trkz0", "InciPhi", &m_EvtWeight, 500, -2., 2., 70, 0, 0.7);

  // Cluster Shape
  histsvc->Book("Size", "Size", &m_EvtWeight, 10, -0.5, 9.5);
  histsvc->Book("Size_long", "Size", &m_EvtWeight, 100, -0.5, 99.5);
  histsvc->Book("SizePhi", "SizePhi", &m_EvtWeight, 10, -0.5, 9.5);
  histsvc->Book("SizePhi_long", "SizePhi", &m_EvtWeight, 100, -0.5, 99.5);
  histsvc->Book("SizeZ", "SizeZ", &m_EvtWeight, 10, -0.5, 9.5); 
  histsvc->Book("SizeZ_long", "SizeZ", &m_EvtWeight, 100, -0.5, 99.5);
  histsvc->Book("MeanCharge", "MeanCharge", &m_EvtWeight, 1000, 0., 5e5);
  histsvc->Book("MedianCharge", "MedianCharge", &m_EvtWeight, 1000, 0., 5e5);
  histsvc->Book("RMSCharge", "RMSCharge", &m_EvtWeight, 1000, 0., 5e4);
  histsvc->Book("LogRMSCharge", "LogRMSCharge", &m_EvtWeight, 500, -8., 8.); 
  histsvc->Book("MaxChargeProp", "MaxChargeProp", &m_EvtWeight, 55, 0., 1.1);
  histsvc->Book("MaxToTProp", "MaxToTProp", &m_EvtWeight, 55, 0, 1.1);
  histsvc->Book("AboveMeanRdoNProp", "AboveMeanRdoNProp", &m_EvtWeight, 11, 0., 1.1);
  histsvc->Book("AboveMedianRdoNProp", "AboveMedianRdoNProp", &m_EvtWeight, 11, 0., 1.1);

  // correlation between cluster shape and incident angle
  histsvc->Book("InciTheta_Size", "InciTheta", "Size", &m_EvtWeight, 200, -2., 2., 10, -0.5, 9.5);
  histsvc->Book("InciPhi_Size", "InciPhi", "Size", &m_EvtWeight, 150, 0., 1.5, 10, -0.5, 9.5);
  histsvc->Book("InciTheta_SizePhi", "InciTheta", "SizePhi", &m_EvtWeight, 200, -2., 2., 10, -0.5, 9.5);
  histsvc->Book("InciPhi_SizePhi", "InciPhi", "SizePhi", &m_EvtWeight, 70, 0., 0.7, 10, -0.5, 9.5);
  histsvc->Book("InciTheta_SizeZ", "InciTheta", "SizeZ", &m_EvtWeight, 200, -2., 2., 10, -0.5, 9.5);
  histsvc->Book("InciPhi_SizeZ", "InciPhi", "SizeZ", &m_EvtWeight, 70, 0., 0.7, 10, -0.5, 9.5);

  // correlation between cluster shape and track kinematic
  histsvc->Book("trkPt_SizePhi", "trkPt", "SizePhi", &m_EvtWeight, 100, 0, 50, 10, -0.5, 9.5);
  histsvc->Book("trkEta_SizePhi", "trkEta", "SizePhi", &m_EvtWeight, 25, -2.5, 2.5, 10, -0.5, 9.5);

  // correlation between cluster shape in r-phi and z direction
  histsvc->Book("SizePhi_SizeZ", "SizePhi", "SizeZ", &m_EvtWeight, 6, -0.5, 5.5, 6, -0.5, 5.5);

  // correlation between track kinematic and incident angle
  histsvc->Book("trkEta_InciPhi", "trkEta", "InciPhi", &m_EvtWeight, 25, -2.5, 2.5, 70, 0, 0.7);

  // correlation between Flatness and Size
  histsvc->Book("Size_AboveMeanRdoNProp", "Size", "AboveMeanRdoNProp", &m_EvtWeight, 10, -0.5, 9.5, 11, 0., 1.1);
  histsvc->Book("SizeZ_AboveMeanRdoNProp", "SizeZ", "AboveMeanRdoNProp", &m_EvtWeight, 10, -0.5, 9.5, 11, 0., 1.1);
  histsvc->Book("SizePhi_AboveMeanRdoNProp", "SizePhi", "AboveMeanRdoNProp", &m_EvtWeight, 10, -0.5, 9.5, 11, 0., 1.1);

  // correlation between Flatness and Incident Angle
  histsvc->Book("InciTheta_AboveMeanRdoNProp", "InciTheta", "AboveMeanRdoNProp", &m_EvtWeight, 200, -2., 2., 11, 0., 1.1);
  histsvc->Book("InciPhi_AboveMeanRdoNProp", "InciPhi", "AboveMeanRdoNProp", &m_EvtWeight, 70, 0, 0.7, 11, 0., 1.1);
  histsvc->Book("InciPhi_MaxChargeProp", "InciPhi", "MaxChargeProp", &m_EvtWeight, 70, 0, 0.7, 55, 0, 1.1);
  histsvc->Book("InciPhi_MaxToTProp", "InciPhi", "MaxToTProp", &m_EvtWeight, 70, 0, 0.7, 55, 0, 1.1);

  // charge <-> tot calibration
  histsvc->Book("Charge_ToT", "Charge", "ToT", &m_EvtWeight, 1000, 0, 5e5, 200, 0, 1000);
  histsvc->Book("trkPt_Charge", "trkPt", "Charge", &m_EvtWeight, 100, 0, 50, 1000, 0, 5e5);
  histsvc->Book("trkEta_Charge", "trkEta", "Charge", &m_EvtWeight, 25, -2.5, 2.5, 1000, 0, 5e5);
  histsvc->Book("InciPhi_Charge", "InciPhi", "Charge", &m_EvtWeight, 70, 0, 0.7, 1000, 0, 5e5);
  histsvc->Book("trkPt_ToT", "trkPt", "ToT", &m_EvtWeight, 100, 0, 50, 200, 0, 1000);
  histsvc->Book("trkEta_ToT", "trkEta", "ToT", &m_EvtWeight, 25, -2.5, 2.5, 200, 0, 1000);
  histsvc->Book("InciPhi_ToT", "InciPhi", "ToT", &m_EvtWeight, 70, 0, 0.7, 200, 0, 1000);

  /*
  // G4 information
  histsvc->Book("truth_size", "truth_size", &m_EvtWeight, 10, -0.5, 9.5);
  histsvc->Book("sdo_size", "sdo_size", &m_EvtWeight, 10, -0.5, 9.5);
  histsvc->Book("sihit_size", "sihit_size", &m_EvtWeight, 10, -0.5, 9.5);

  histsvc->Book("G4_Number", "G4_Number", &m_EvtWeight, 5, -0.5, 4.5);
  histsvc->Book("G4_ResLocX", "G4_ResLocX", &m_EvtWeight, 100, -0.2, 0.2);
  histsvc->Book("G4_ResLocY", "G4_ResLocY", &m_EvtWeight, 100, -1., 1.);
  histsvc->Book("G4_EnergyLoss", "G4_EnergyLoss", &m_EvtWeight, 100, 0., 1000.);
  histsvc->Book("G4_EnergyLossDiff", "G4_EnergyLossDiff", &m_EvtWeight, 60, -30, 30.);
  histsvc->Book("G4_SumEnergyLossDiff", "G4_SumEnergyLossDiff", &m_EvtWeight, 60, -30, 30.);
  histsvc->Book("G4_InciPhi", "G4_InciPhi", &m_EvtWeight, 70, 0, 0.7);
  histsvc->Book("G4_InciPhi_ResLocX", "InciPhi", "G4_ResLocX", &m_EvtWeight, 70, 0, 0.7, 100, -0.2, 0.2);
  histsvc->Book("G4_InciPhi_ResLocY", "InciPhi", "G4_ResLocY", &m_EvtWeight, 70, 0, 0.7, 100, -1, 1);
  histsvc->Book("G4_InciPhi_EnergyLoss", "InciPhi", "G4_EnergyLoss", &m_EvtWeight, 70, 0, 0.7, 100, 0, 1000);
  histsvc->Book("G4_InciPhi_InciPhi", "InciPhi", "G4_InciPhi", &m_EvtWeight, 70, 0, 0.7, 70, 0, 0.7);
  */
  
  // recon residual
  histsvc->Book("InciPhi_trklocUnbiasedResidualX", "InciPhi", "trklocUnbiasedResidualX", &m_EvtWeight, 70, 0, 0.7, 100, -0.1, 0.1);
  histsvc->Book("InciPhi_trklocUnbiasedResidualY", "InciPhi", "trklocUnbiasedResidualY", &m_EvtWeight, 70, 0, 0.7, 100, -0.5, 0.5);
  histsvc->Book("EtaModule_trklocUnbiasedResidualX", "EtaModule", "trklocUnbiasedResidualX", &m_EvtWeight, 21, -10.5, 10.5, 100, -0.1, 0.1);
  histsvc->Book("EtaModule_trklocUnbiasedResidualY", "EtaModule", "trklocUnbiasedResidualY", &m_EvtWeight, 21, -10.5, 10.5, 100, -0.5, 0.5);

  return true;
}

bool ZmumuSelector :: FillHistogramPixelCluster(std::string TrackContainerName, const xAOD::TrackStateValidation* msos, const xAOD::TrackMeasurementValidation* PixelCluster, const xAOD::TrackParticle* Track)
{
  if(m_debug) Info("FillHistogramPixelCluster()", "Filling histograms for Pixel Cluster");

  // Reset
  m_histsvc_pixelclusters->Reset();

  // detector info
  m_histsvc_pixelclusters->Set("EtaModule", PixelCluster->auxdata<int>("eta_module"));

  // hit summary
  m_histsvc_pixelclusters->Set("Charge", PixelCluster->auxdata<float>("charge"));
  m_histsvc_pixelclusters->Set("Charge90", 0.9 * PixelCluster->auxdata<float>("charge"));
  m_histsvc_pixelclusters->Set("EnergyLoss", PixelCluster->auxdata<float>("charge")*3.62/1000.);   // corresponding energy loss (in keV) to produce such amount of charge
  m_histsvc_pixelclusters->Set("ToT", PixelCluster->auxdata<int>("ToT"));
  if(PixelCluster->auxdata<int>("ToT") > 0.01) m_histsvc_pixelclusters->Set("ToTNonZero", PixelCluster->auxdata<int>("ToT"));
  m_histsvc_pixelclusters->Set("LogCharge", TMath::Log10(PixelCluster->auxdata<float>("charge")));
  m_histsvc_pixelclusters->Set("isFake", PixelCluster->auxdata<char>("isFake"));
  m_histsvc_pixelclusters->Set("isGanged", PixelCluster->auxdata<char>("gangedPixel"));
  m_histsvc_pixelclusters->Set("isSplit", PixelCluster->auxdata<int>("isSplit"));
  m_histsvc_pixelclusters->Set("splitProb1", PixelCluster->auxdata<float>("splitProbability1"));
  m_histsvc_pixelclusters->Set("splitProb2", PixelCluster->auxdata<float>("splitProbability2"));

  // Cluster Position
  m_histsvc_pixelclusters->Set("Layer", PixelCluster->auxdata<int>("layer"));
  m_histsvc_pixelclusters->Set("Bec", PixelCluster->auxdata<int>("bec"));
  m_histsvc_pixelclusters->Set("LocalX", PixelCluster->localX());
  m_histsvc_pixelclusters->Set("LocalY", PixelCluster->localY());
  m_histsvc_pixelclusters->Set("GlobalZ", PixelCluster->globalZ());
  m_histsvc_pixelclusters->Set("GlobalR", TMath::Sqrt(TMath::Power(PixelCluster->globalX(), 2) + TMath::Power(PixelCluster->globalY(), 2)));
  m_histsvc_pixelclusters->Set("InciPhi", msos->auxdata<float>("localPhi"));
  m_histsvc_pixelclusters->Set("InciTheta", msos->auxdata<float>("localTheta"));
  m_histsvc_pixelclusters->Set("trkPhi", Track->phi());
  m_histsvc_pixelclusters->Set("trkEta", Track->eta());
  m_histsvc_pixelclusters->Set("trkPt", Track->pt()/1000.);
  m_histsvc_pixelclusters->Set("trkP", Track->p4().P()/1000.);

  double dz = Track->z0() + Track->vz() - m_PrimaryVertex->z();
  m_histsvc_pixelclusters->Set("trkd0", Track->d0());
  m_histsvc_pixelclusters->Set("trkz0", dz);

  // residual
  m_histsvc_pixelclusters->Set("trklocUnbiasedResidualX", msos->auxdata<float>("unbiasedResidualX"));
  m_histsvc_pixelclusters->Set("trklocUnbiasedResidualY", msos->auxdata<float>("unbiasedResidualY"));

  // Cluster Shapes
  if(PixelCluster->isAvailable<int>("size")){
    m_histsvc_pixelclusters->Set("Size", PixelCluster->auxdata<int>("size"));
  }
  else{
    // std::cout << "-----------" << std::endl;
    // std::cout << "size from tot: " << PixelCluster->auxdata< std::vector<int> >("rdo_tot").size() << std::endl;
    // std::cout << "size from charge: " << PixelCluster->auxdata< std::vector<float> >("rdo_charge").size() << std::endl;
    // std::cout << "size from eta index: " << PixelCluster->auxdata< std::vector<int> >("rdo_eta_pixel_index").size() << std::endl;
    // std::cout << "size from phi index: " << PixelCluster->auxdata< std::vector<int> >("rdo_phi_pixel_index").size() << std::endl;

    m_histsvc_pixelclusters->Set("Size", PixelCluster->auxdata< std::vector<int> >("rdo_tot").size());
  }
  
  m_histsvc_pixelclusters->Set("SizePhi", PixelCluster->auxdata<int>("sizePhi"));
  m_histsvc_pixelclusters->Set("SizeZ", PixelCluster->auxdata<int>("sizeZ"));

  // cluster fluctuation information
  int maxToT = -1;
  float maxCharge = -1.;

  // try{
    std::vector<int>   rdo_tot = PixelCluster->auxdata< std::vector<int> >("rdo_tot");
    std::vector<float> rdo_charge = PixelCluster->auxdata< std::vector<float> >("rdo_charge");
    std::vector<int>   rdo_eta_pixel_index = PixelCluster->auxdata< std::vector<int> >("rdo_eta_pixel_index");
    std::vector<int>   rdo_phi_pixel_index = PixelCluster->auxdata< std::vector<int> >("rdo_phi_pixel_index");

    float sumToT = 0.;
    for(unsigned int irdo = 0; irdo < rdo_tot.size(); irdo++){
      if(rdo_tot[irdo] > maxToT) maxToT = rdo_tot[irdo];
      sumToT += rdo_tot[irdo];
    }

    float sumCharge = 0.;
    for(unsigned int irdo = 0; irdo < rdo_charge.size(); irdo++){
      // don't ask me, I don't know why some (exterme rare case) pixel could have negative charge ... 
      // This would eliminte the >1 overflow
      if(rdo_charge[irdo] < 0.) continue;

      if(rdo_charge[irdo] > maxCharge) maxCharge = rdo_charge[irdo];
      sumCharge += rdo_charge[irdo];
    }

    // It is important that the denominator is the sum of charge here, since cluster charge is converted from cluster ToT, which is the sum of pixel ToT, instead of the sum of charge on each pixel, which is converted from pixel ToT. These two things (sum of charge, or cluster charge) can potentially be different, since the charge<->tot calibration is non-linear
    m_histsvc_pixelclusters->Set("MaxChargeProp", 1.0*maxCharge/sumCharge);
    m_histsvc_pixelclusters->Set("MaxToTProp", 1.0*maxToT/sumToT);

    m_histsvc_pixelclusters->Set("SumCharge", sumCharge);
    m_histsvc_pixelclusters->Set("SumEnergyLoss", sumCharge*3.62/1000.);
  // }
  // catch(...){
  //   Info("FillHistogramPixelCluster()", "Hmm, why you cannot get rdo information?!");
  // }

  // G4 information (MC ONLY) --> not available for now
  // if(isMC){
  //   // size of each truth container
  //   m_histsvc_pixelclusters->Set("truth_size", PixelCluster->auxdata< std::vector<int> >("truth_barcode").size());
  //   m_histsvc_pixelclusters->Set("sdo_size", PixelCluster->auxdata< std::vector<int> >("sdo_words").size());
  //   m_histsvc_pixelclusters->Set("sihit_size", PixelCluster->auxdata< std::vector<int> >("sihit_barcode").size());

  //   // G4 HIT
  //   m_histsvc_pixelclusters->Set("G4_Number", m_histsvc_pixelclusters->Get("sihit_size"));
  //   if(m_histsvc_pixelclusters->Get("sihit_size") == 1){
  //     float G4_startPosX = PixelCluster->auxdata< std::vector<float> >("sihit_startPosX")[0];   // xEta
  //     float G4_endPosX = PixelCluster->auxdata< std::vector<float> >("sihit_endPosX")[0];
  //     float G4_posX = (G4_startPosX + G4_endPosX)/2.;

  //     float G4_startPosY = PixelCluster->auxdata< std::vector<float> >("sihit_startPosY")[0];   // xPhi
  //     float G4_endPosY = PixelCluster->auxdata< std::vector<float> >("sihit_endPosY")[0];
  //     float G4_posY = (G4_startPosY + G4_endPosY)/2.;

  //     float G4_startPosZ = PixelCluster->auxdata< std::vector<float> >("sihit_startPosZ")[0];   // Radius
  //     float G4_endPosZ = PixelCluster->auxdata< std::vector<float> >("sihit_endPosZ")[0];
  //     float G4_posZ = (G4_startPosZ + G4_endPosZ)/2.;

  //     float G4_EnergyLoss = PixelCluster->auxdata< std::vector<float> >("sihit_energyDeposit")[0] * 1e+3;  // MeV -> keV

  //     m_histsvc_pixelclusters->Set("G4_ResLocX", m_histsvc_pixelclusters->Get("LocalX") - G4_posX);
  //     m_histsvc_pixelclusters->Set("G4_ResLocY", m_histsvc_pixelclusters->Get("LocalY") - G4_posY);
  //     m_histsvc_pixelclusters->Set("G4_EnergyLoss", G4_EnergyLoss);
  //     m_histsvc_pixelclusters->Set("G4_EnergyLossDiff", m_histsvc_pixelclusters->Get("EnergyLoss") - m_histsvc_pixelclusters->Get("G4_EnergyLoss"));
  //     m_histsvc_pixelclusters->Set("G4_SumEnergyLossDiff", m_histsvc_pixelclusters->Get("SumEnergyLoss") - m_histsvc_pixelclusters->Get("G4_EnergyLoss"));
  //   }
  // }

  ///////////////////////////////////////////////////////////////
  // finalize
  ///////////////////////////////////////////////////////////////

  TString ContainerTag = "GoodEvents_"+TrackContainerName;
  TString PixelClusterTag = "_PixelCluster";

  // bec
  TString BecTag = "_At";
  if(m_histsvc_pixelclusters->Get("Bec") == 0)
    BecTag += "Barrel";
  else if( fabs(m_histsvc_pixelclusters->Get("Bec")) == 2 )
    BecTag += "EndCap";
  else{
    std::cout << "Undefined BEC code " << m_histsvc_pixelclusters->Get("Bec") << " !" << std::endl;
    BecTag += "Non";
  }

  // layer
  TString LayerTag = "_Layer";
  if( (m_histsvc_pixelclusters->Get("Bec") == 0) && (PixelCluster->auxdata<int>("layer") == 0) ){
    int etaModule = PixelCluster->auxdata<int>("eta_module");

    if( ((etaModule >= -10) && (etaModule <= -7)) || ((etaModule >= 6) && (etaModule <= 9)) ) 
      LayerTag += "IBL3D";
    else if( (etaModule >= -6) && (etaModule <= 5) ) 
      LayerTag += "IBLPlanar";
    else 
      LayerTag += "IBLUnknown";
  }
  else{
    LayerTag += "Pixel";
    LayerTag += TString::Itoa(PixelCluster->auxdata<int>("layer"), 10);
  }

  // pt
  TString PtTag = "_Pt";
  if( (m_histsvc_pixelclusters->Get("trkPt") >= 0.5) && (m_histsvc_pixelclusters->Get("trkPt") < 1.) )
    PtTag += "-1";
  else if( (m_histsvc_pixelclusters->Get("trkPt") >= 1.) && (m_histsvc_pixelclusters->Get("trkPt") < 5.) )
    PtTag += "0";
  else if( (m_histsvc_pixelclusters->Get("trkPt") >= 5.) && (m_histsvc_pixelclusters->Get("trkPt") < 10.) )
    PtTag += "1";
  else if( (m_histsvc_pixelclusters->Get("trkPt") >= 10.) && (m_histsvc_pixelclusters->Get("trkPt") < 25.) )
    PtTag += "2";
  else if(m_histsvc_pixelclusters->Get("trkPt") >= 25.)
    PtTag += "3";
  else
    PtTag += "None";

  // eta
  TString EtaTag = "_Eta";
  if(fabs(m_histsvc_pixelclusters->Get("trkEta")) < 1.5)
    EtaTag += "0";
  else if(fabs(m_histsvc_pixelclusters->Get("trkEta")) < 2.5)
    EtaTag += "1";
  else
    EtaTag += "None";

  // cluster size
  TString SizeTag = "_N";
  if(m_histsvc_pixelclusters->Get("Size") == 1)
    SizeTag += "1";
  else if(m_histsvc_pixelclusters->Get("Size") > 1)
    SizeTag += "1p";
  else
    SizeTag += "None";

  // filling histograms
  m_histsvc_pixelclusters->MakeHists(ContainerTag, PixelClusterTag);
  m_histsvc_pixelclusters->MakeHists(ContainerTag, PixelClusterTag + BecTag + LayerTag + PtTag + EtaTag + SizeTag);

  // end
  return true;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Auxiliary Functions 
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

bool ZmumuSelector :: TrackSelection(const xAOD::TrackParticle* Track)
{
  // kinematic cuts
  // if(Track->pt() < 1e3) return false;
  if(Track->pt() < 500.) return false;
  if(abs(Track->eta()) > 2.5) return false;

  // quality cut
  uint8_t getInt(0);
  int nSiHits = numberOfSiHits(Track);
  Track->summaryValue(getInt,xAOD::numberOfPixelSharedHits);
  int nPixSharedHits = getInt;
  Track->summaryValue(getInt,xAOD::numberOfSCTSharedHits);
  int nSCTSharedHits = getInt;
  Track->summaryValue(getInt,xAOD::numberOfPixelHoles);
  int nPixHoles = getInt;
  Track->summaryValue(getInt,xAOD::numberOfSCTHoles);
  int nSCTHoles = getInt;

  if (!( (nSiHits >= 7) && (nPixSharedHits + nSCTSharedHits <= 1) && (nPixHoles + nSCTHoles <= 2) && (nPixHoles <= 1) )) return false;

  // good to go
  return true;
}

std::vector<const xAOD::TrackStateValidation*> ZmumuSelector :: GetPixelMeasurements(const xAOD::TrackParticle* Track)
{
  if(m_debug) Info("GetPixelMeasurements()", "Begin retrieving pixel measurements ...");

  std::vector<const xAOD::TrackStateValidation*> output;

  std::string msosLink("msosLink");
  auto msosLinkVector = Track->auxdata< std::vector<ElementLink< xAOD::TrackStateValidationContainer > > >(msosLink);

  for(auto msosLink : msosLinkVector){
    // make sure the link is valid
    if( (!msosLink.isValid()) || ((*msosLink) == 0) ){
      Warning("GetPixelMeasurements()", "Invalid link to msos of track.");
      continue;
    }

    const xAOD::TrackStateValidation* msos = (*msosLink);

    // make sure it is a measurement on pixel detector (pixel + IBL)
    if( (msos->detType() != TrackState::Pixel)  ||  (msos->type() != TrackStateOnSurface::Measurement) ) continue;

    // done
    output.push_back(msos);
  }

  if(m_debug) Info("GetPixelMeasurements()", "Leaving GetPixelMeasurements ...");

  return output;
}

const xAOD::TrackMeasurementValidation* ZmumuSelector :: GetPixelCluster(const xAOD::TrackStateValidation* msos)
{
  auto el_PixelCluster = msos->trackMeasurementValidationLink();

  if(!el_PixelCluster.isValid()){
    Warning("GetPixelCluster()", "Invalid track measurement validation link.");
    return 0;
  }

  if((*el_PixelCluster) == 0){
    Warning("GetPixelCluster()", "Null pointer returned for pixel cluster.");
    return 0;
  }

  return (*el_PixelCluster);
}

bool ZmumuSelector :: SelectGoodPixelCluster(const xAOD::TrackMeasurementValidation* PixelCluster)
{
  if(PixelCluster == 0) return false;
  if(PixelCluster->auxdata<char>("gangedPixel") != 0) return false;
  if(PixelCluster->auxdata<char>("isFake") != 0) return false;
  if(PixelCluster->auxdata<int>("isSplit") == 1) return false;

  return true;
}

// copy from https://svnweb.cern.ch/trac/atlasperf/browser/CombPerf/Tracking/TrackingInDenseEnvironments/SimpleAnaxAOD/trunk/HistManager/Root/TrackHelper.cxx
int ZmumuSelector :: numberOfSiHits(const xAOD::TrackParticle* trkPart)
{
  if(!trkPart) { return 0; }

  uint8_t tmp(0);
  int nSiHits(0);

  if( trkPart->summaryValue(tmp, xAOD::numberOfPixelHits) ) { nSiHits += tmp; }
  else {
    Info("ZmumuSelector::numberOfSiHits", "numberOfPixelHits is not stored in TrackParticle object");
    return -1;
  }
  if( trkPart->summaryValue(tmp, xAOD::numberOfSCTHits   ) ) { nSiHits += tmp; }
  else {
    Info("ZmumuSelector::numberOfSiHits", "numberOfSCTHits is not stored in TrackParticle object");
    return -1;
  }

  return nSiHits;
}
