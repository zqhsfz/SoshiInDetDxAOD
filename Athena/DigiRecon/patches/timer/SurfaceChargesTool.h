///////////////////////////////////////////////////////////////////
// SurfaceChargesTool.h
//   Header file for class SurfaceChargesTool
///////////////////////////////////////////////////////////////////
// (c) ATLAS Detector software
///////////////////////////////////////////////////////////////////

#ifndef PIXELDIGITIZATION_SurfaceChargesTool_H
#define PIXELDIGITIZATION_SurfaceChargesTool_H

#include "AthenaBaseComps/AthAlgTool.h"
#include "SiDigitization/SiChargedDiodeCollection.h"
#include "InDetReadoutGeometry/SiDetectorElement.h"
#include "GaudiKernel/ToolHandle.h"
#include "HitManagement/TimedHitPtr.h"
#include "PixelGeoModel/IBLParameterSvc.h"

#include "TH1D.h"
#include "TString.h"

// Base class
class PixelID;

class SubChargesTool;
class PixelBarrelChargeTool;
class PixelECChargeTool;
class IblPlanarChargeTool;
class Ibl3DChargeTool;
class DBMChargeTool;

namespace InDetDD {
  class SiDetectorElement;
}

namespace CLHEP {
  class HepRandomEngine;
}

class SurfaceChargesTool : public AthAlgTool {

public:
  //Defines the Technology variable type, used for labeling the different tools.  
  enum Technology {IBL3D,IBLPLANAR,PIXELEC,PIXELBARREL,DBM};
 
  // Constructor:
  SurfaceChargesTool( const std::string& type, const std::string& name,const IInterface* parent);

  /** AlgTool InterfaceID */
  static const InterfaceID& interfaceID() ;

  /** AlgTool initialize */
  virtual StatusCode initialize();

  /** AlgTool finalize */
  virtual StatusCode finalize();

  /** Destructor */
  virtual ~SurfaceChargesTool();
  StatusCode initTools();
  
  /** create a list of surface charges from a hit
      @param phit hit information
      @param charges reference to vector of charges to be filled
   */
  virtual StatusCode process(const TimedHitPtr<SiHit> &phit,
                       SiChargedDiodeCollection& chargedDiodes,
		       InDetDD::SiDetectorElement &Module);

private:
  /** empty constructor, make private */
  SurfaceChargesTool();
  Technology getTechnology();  
  void storeTool(Technology tech,SubChargesTool *techTool) {
    TechChargeTools[tech]=techTool;

    char histogramName[100];
    sprintf(histogramName, "timer_SurfaceChargeTool%d_execute", (int)tech);
    TechTimer[tech] = new TH1D(histogramName, histogramName, 20000, 0, 20000);
  }

private:
  //This is only used in the getTechnology function. Perhaps it should be 
  //eliminated and have getTechnology() become getTechnology(Module);
  InDetDD::SiDetectorElement * m_module;   
  bool m_IBLabsent;
  /** Tool handles for the technology-specific tools for generating 
    * surface charges. 
    */ 
  ToolHandle<PixelBarrelChargeTool> m_PixelBarrelChargeTool;
  ToolHandle<PixelECChargeTool> m_PixelECChargeTool;
  ToolHandle<DBMChargeTool> m_DBMChargeTool;
  ToolHandle<IblPlanarChargeTool> m_IblPlanarChargeTool;
  ToolHandle<Ibl3DChargeTool> m_Ibl3DChargeTool;
  ServiceHandle<IBLParameterSvc> m_IBLParameterSvc;
  
  /** map connecting Technology to the relevant tool */
  std::map<Technology,SubChargesTool*> TechChargeTools; 

  /** timer for each technology **/
  std::map<Technology,TH1D*> TechTimer;
  TH1D* m_timer_execute;
 
 };


#endif //PIXELDIGITIZATION_SurfaceChargesTool_H
