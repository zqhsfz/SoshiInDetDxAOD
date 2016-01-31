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

// EDM include(s):
#include "xAODTracking/VertexContainer.h"
#include "xAODTracking/TrackParticleContainer.h"
#include "xAODTracking/TrackMeasurementValidationContainer.h"
#include "xAODTracking/TrackStateValidationContainer.h"


class ZmumuSelector : public EL::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  bool        m_debug;

  std::string m_inMuonContainerName;
  std::string m_outMuonContainerName;
  std::string m_outTrackContainerName;

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

private:

  xAOD::TEvent* m_event; //!
  xAOD::TStore* m_store; //!

  bool HistSvcInit();

  Analysis_AutoHists* m_histsvc_event;  //!
  Analysis_AutoHists* m_histsvc_muons;  //!
  Analysis_AutoHists* m_histsvc_tracks; //!
  Analysis_AutoHists* m_histsvc_pixelclusters; //!

  double m_EvtWeight; //!

  // histogram filling

  bool BookHistogramPixelCluster(Analysis_AutoHists* histsvc);
  bool FillHistogramPixelCluster(const xAOD::TrackStateValidation* msos, const xAOD::TrackMeasurementValidation* PixelCluster, const xAOD::TrackParticle* Track);

  // auxiliary functions

  const xAOD::Vertex* m_PrimaryVertex;  //!

  std::vector<const xAOD::TrackStateValidation*> GetPixelMeasurements(const xAOD::TrackParticle* track);  // return a vector of measurement objects on pixel layers from a track
  const xAOD::TrackMeasurementValidation* GetPixelCluster(const xAOD::TrackStateValidation* msos);        // return the pixel cluster object. This function also includes necessary element link checking
  bool SelectGoodPixelCluster(const xAOD::TrackMeasurementValidation* PixelCluster);

};

#endif
