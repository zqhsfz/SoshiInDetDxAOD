///////////////////////////////////////////////////////////////////
// SurfaceChargesTool.cxx
//   Implementation file for class SurfaceChargesTool
///////////////////////////////////////////////////////////////////
// (c) ATLAS Detector software
///////////////////////////////////////////////////////////////////

#include "SurfaceChargesTool.h"
#include "InDetReadoutGeometry/SiDetectorElement.h"
#include "InDetReadoutGeometry/PixelModuleDesign.h"
#include "InDetSimEvent/SiHit.h"
#include "InDetIdentifier/PixelID.h"
#include "GeneratorObjects/HepMcParticleLink.h"
#include "SiPropertiesSvc/SiliconProperties.h"

#include "HepMC/GenEvent.h"
#include "HepMC/GenVertex.h"
#include "HepMC/GenParticle.h"
#include "AtlasCLHEP_RandomGenerators/RandGaussZiggurat.h"
#include "AthenaKernel/errorcheck.h"

#include "PixelBarrelChargeTool.h"
#include "PixelECChargeTool.h"
#include "IblPlanarChargeTool.h"
#include "Ibl3DChargeTool.h"
#include "DBMChargeTool.h"

#include <chrono>
#include "TFile.h"

using namespace InDetDD;

static const InterfaceID IID_ISurfaceChargesTool("SurfaceChargesTool", 1, 0);
const InterfaceID& SurfaceChargesTool::interfaceID( ){ return IID_ISurfaceChargesTool; }

// Constructor with parameters:
SurfaceChargesTool::SurfaceChargesTool(const std::string& type, const std::string& name,const IInterface* parent):
  AthAlgTool(type,name,parent),
  m_module(0),
  m_IBLabsent(true),
  m_PixelBarrelChargeTool("PixelBarrelChargeTool"),
  m_PixelECChargeTool("PixelECChargeTool"),
  m_DBMChargeTool("DBMChargeTool"),
  m_IblPlanarChargeTool("IblPlanarChargeTool"),
  m_Ibl3DChargeTool("Ibl3DChargeTool"),
  m_IBLParameterSvc("IBLParameterSvc",name)
  { 
	declareInterface< SurfaceChargesTool >( this );
	declareProperty("PixelBarrelChargeTool", m_PixelBarrelChargeTool,   "PixelBarrelChargeTool");
	declareProperty("PixelECChargeTool", m_PixelECChargeTool,   "PixelECChargeTool");
	declareProperty("IblPlanarChargeTool", m_IblPlanarChargeTool,   "IblPlanarChargeTool");
	declareProperty("Ibl3DChargeTool", m_Ibl3DChargeTool,   "Ibl3DChargeTool");
	declareProperty("DBMChargeTool", m_DBMChargeTool,   "DBMChargeTool");
}

class DetCondCFloat;

// Destructor:
SurfaceChargesTool::~SurfaceChargesTool()
{
}

//----------------------------------------------------------------------
// Initialize
//----------------------------------------------------------------------
StatusCode SurfaceChargesTool::initialize() {
 StatusCode sc = AthAlgTool::initialize();
 if (sc.isFailure()) {
	ATH_MSG_FATAL("SurfaceChargesTool::initialize() failed");
	return sc;
 } 
 if (m_IBLParameterSvc.retrieve().isFailure()) {
	ATH_MSG_WARNING("Could not retrieve IBLParameterSvc");
 }
 else {
	m_IBLParameterSvc->setBoolParameters(m_IBLabsent,"IBLAbsent");
 }
  CHECK(initTools());
  ATH_MSG_DEBUG ( "SurfaceChargesTool::initialize()");
  return sc ;
}

//----------------------------------------------------------------------
// finalize
//----------------------------------------------------------------------
StatusCode SurfaceChargesTool::finalize() {

  // store timing histograms //
  TFile* fOutput = new TFile("Timer_SurfaceChargesTool.root", "RECREATE");

  std::vector<SurfaceChargesTool::Technology> ListToLoop = {
    IBL3D,
    IBLPLANAR,
    PIXELEC,
    PIXELBARREL,
    DBM
  };

  for(auto Tech : ListToLoop){
    fOutput->WriteTObject(TechTimer[Tech], TechTimer[Tech]->GetName(), "Overwrite");
  }
  fOutput->WriteTObject(m_timer_execute, m_timer_execute->GetName(), "Overwrite");

  fOutput->Close();

  StatusCode sc = AthAlgTool::finalize();
  if (sc.isFailure()) {
    ATH_MSG_FATAL ( "SurfaceChargesTool::finalize() failed");
    return sc ;
  }
  ATH_MSG_DEBUG ( "SurfaceChargesTool::finalize()");
  return sc ;
}

// create a list of surface charges from a hit
// this is a copy of Laurent's routine SensorStage::process
StatusCode SurfaceChargesTool::process(const TimedHitPtr<SiHit> & phit,
                                 SiChargedDiodeCollection& chargedDiodes,
                                 InDetDD::SiDetectorElement &Module)
{
 m_module = &Module;
 SurfaceChargesTool::Technology tech = getTechnology();
 ATH_MSG_DEBUG ("Technology = " << tech);

 auto timer_execute_start = std::chrono::high_resolution_clock::now();
 auto result = TechChargeTools[tech]->charge(phit,chargedDiodes,Module);
 auto timer_execute_end = std::chrono::high_resolution_clock::now();

 std::chrono::duration<double, std::micro> timer_execute_elapse =  timer_execute_end - timer_execute_start;
 TechTimer[tech]->Fill( timer_execute_elapse.count() );
 m_timer_execute->Fill( timer_execute_elapse.count() );

 return result;
}

StatusCode SurfaceChargesTool::initTools()
{
  if (!m_DBMChargeTool.retrieve()) {
	ATH_MSG_ERROR("Can't get tool DBMChargeTool");
	return StatusCode::FAILURE;
  }
  StatusCode sc = m_PixelBarrelChargeTool.retrieve();
  if (sc != StatusCode::SUCCESS) {
	ATH_MSG_ERROR("Can't get tool PixelBarrelChargeTool");
	return sc;
  }
  sc = m_PixelECChargeTool.retrieve();
  if (sc != StatusCode::SUCCESS) {
	ATH_MSG_ERROR("Can't get tool PixelECChargeTool");
	return sc;
  }
  sc = m_Ibl3DChargeTool.retrieve();
  if (sc != StatusCode::SUCCESS) {
	ATH_MSG_ERROR("Can't get tool Ibl3DChargeTool");
	return sc;
  }
  sc = m_IblPlanarChargeTool.retrieve();
  if (sc != StatusCode::SUCCESS) {
	ATH_MSG_ERROR("Can't get tool IblPlanarChargeTool");
	return sc;
  }

 storeTool(DBM,&(*m_DBMChargeTool));
 storeTool(PIXELEC,&(*m_PixelECChargeTool));
 storeTool(PIXELBARREL,&(*m_PixelBarrelChargeTool));
 storeTool(IBLPLANAR,&(*m_IblPlanarChargeTool));
 storeTool(IBL3D,&(*m_Ibl3DChargeTool));

 m_timer_execute = new TH1D("timer_SurfaceChargeTool_execute", "timer_SurfaceChargeTool_execute", 20000, 0, 20000);

 return sc;

}

//Returns the technology of the current module. The enum type Technology is defined in SurfaceChargesTool.h
SurfaceChargesTool::Technology SurfaceChargesTool::getTechnology()
{
	const PixelID* pixelId = static_cast<const PixelID *>(m_module->getIdHelper());
	PixelModuleDesign *design = (PixelModuleDesign*)(&(m_module->design()));
	Identifier iden = m_module->identify();
	int barrel_ec = pixelId->barrel_ec(iden);
	int layer_disk = pixelId->layer_disk(iden);
//Not including IBL	
	if (barrel_ec == 4 || barrel_ec == -4) return DBM;
	if (barrel_ec == 2 || barrel_ec == -2) return PIXELEC;
	if (layer_disk>0) return PIXELBARREL;
	if (design->length()<30) return IBL3D; //temporary fix until newer version of InDetReadoutGeometry is used 
	if (!m_IBLabsent) return IBLPLANAR;
	return PIXELBARREL;
}
