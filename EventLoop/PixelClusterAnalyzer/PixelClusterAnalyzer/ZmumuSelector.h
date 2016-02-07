#ifndef PixelClusterAnalyzer_ZmumuSelector_H
#define PixelClusterAnalyzer_ZmumuSelector_H

// Infrastructure include(s):
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"

// EL include(s):
#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>

// package include(s):
#include "AutoHists/Analysis_AutoHists.h"
#include "MuonSelectorTools/MuonSelectionTool.h"

// EDM include(s):
#include "xAODTracking/VertexContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "xAODTracking/TrackMeasurementValidationContainer.h"
#include "xAODTracking/TrackStateValidationContainer.h"
#include "xAODMuon/MuonContainer.h"
#include "xAODEventInfo/EventInfo.h"
#include "AsgTools/StatusCode.h"

class ZmumuSelector : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  bool        m_debug;

  std::string m_inMuonContainerName;
  std::string m_outMuonContainerName;

  std::string m_inJetContainerName;
  std::string m_inTrackContainerName;

  std::string m_outTrackContainerName_Zmumu;
  std::string m_outTrackContainerName_Jet;
  std::string m_outTrackContainerName_Other; 

  std::string m_outputName;

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!



  // this is a standard constructor
  ZmumuSelector ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(ZmumuSelector, 1);

  // standard tools
  // muon selection has to be done here, instead of xAH
  CP::MuonSelectionTool *m_muonSelection;  //!

  // sort
  static bool sort_pt(const xAOD::IParticle* A, const xAOD::IParticle* B){ return (A->pt() > B->pt()); }

private:

  xAOD::TEvent* m_event; //!
  xAOD::TStore* m_store; //!

  const xAOD::EventInfo* m_eventInfo; //!

  bool HistSvcInit();

  Analysis_AutoHists* m_histsvc_cutflow;  //!
  Analysis_AutoHists* m_histsvc_event;  //!
  Analysis_AutoHists* m_histsvc_muons;  //!
  Analysis_AutoHists* m_histsvc_tracks; //!
  Analysis_AutoHists* m_histsvc_pixelclusters; //!

  double m_EvtWeight; //!

  // histogram filling

  bool FillCutflow(std::string cutname);

  StatusCode FillHistogramTracks(std::string TrackContainerName);

  bool BookHistogramPixelCluster(Analysis_AutoHists* histsvc);
  bool FillHistogramPixelCluster(std::string TrackContainerName, const xAOD::TrackStateValidation* msos, const xAOD::TrackMeasurementValidation* PixelCluster, const xAOD::TrackParticle* Track);

  // auxiliary functions

  const xAOD::Vertex* m_PrimaryVertex;  //!

  bool TrackSelection(const xAOD::TrackParticle* track);
  std::vector<const xAOD::TrackStateValidation*> GetPixelMeasurements(const xAOD::TrackParticle* track);  // return a vector of measurement objects on pixel layers from a track
  const xAOD::TrackMeasurementValidation* GetPixelCluster(const xAOD::TrackStateValidation* msos);        // return the pixel cluster object. This function also includes necessary element link checking
  bool SelectGoodPixelCluster(const xAOD::TrackMeasurementValidation* PixelCluster);

  int numberOfSiHits(const xAOD::TrackParticle* Track);

};

#endif
