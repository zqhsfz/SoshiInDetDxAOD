#--------------------------------------------------------------
# some xAOD specific things
#--------------------------------------------------------------
useBeamConstraint = InDetFlags.useBeamConstraint()

#  Build xAODPrd objects
from TRT_ConditionsServices.TRT_ConditionsServicesConf import TRT_StrawNeighbourSvc
TRTStrawNeighbourSvc=TRT_StrawNeighbourSvc()
ServiceMgr += TRTStrawNeighbourSvc

from TRT_ConditionsServices.TRT_ConditionsServicesConf import TRT_CalDbSvc
TRTCalibDBSvc=TRT_CalDbSvc()
ServiceMgr += TRTCalibDBSvc

from InDetPrepRawDataToxAOD.InDetPrepRawDataToxAODConf import TRT_PrepDataToxAOD
xAOD_TRT_PrepDataToxAOD = TRT_PrepDataToxAOD( name = "xAOD_TRT_PrepDataToxAOD")
xAOD_TRT_PrepDataToxAOD.OutputLevel=INFO
print "Add TRT xAOD PrepRawData:"
print xAOD_TRT_PrepDataToxAOD
#topSequence += xAOD_TRT_PrepDataToxAOD

from InDetPrepRawDataToxAOD.InDetPrepRawDataToxAODConf import SCT_PrepDataToxAOD
xAOD_SCT_PrepDataToxAOD = SCT_PrepDataToxAOD( name = "xAOD_SCT_PrepDataToxAOD")
xAOD_SCT_PrepDataToxAOD.OutputLevel=INFO
xAOD_SCT_PrepDataToxAOD.UseTruthInfo = True
print "Add SCT xAOD PrepRawData:"
print xAOD_SCT_PrepDataToxAOD
topSequence += xAOD_SCT_PrepDataToxAOD

from InDetPrepRawDataToxAOD.InDetPrepRawDataToxAODConf import PixelPrepDataToxAOD
xAOD_PixelPrepDataToxAOD = PixelPrepDataToxAOD( name = "xAOD_PixelPrepDataToxAOD")
xAOD_PixelPrepDataToxAOD.OutputLevel=INFO
xAOD_PixelPrepDataToxAOD.UseTruthInfo = True
print "Add SCT xAOD PrepRawData:"
print xAOD_PixelPrepDataToxAOD
topSequence += xAOD_PixelPrepDataToxAOD


from AthenaCommon import CfgMgr

# DerivationJob is COMMON TO ALL DERIVATIONS
DerivationFrameworkJob = CfgMgr.AthSequencer("MySeq2")

# Set up stream auditor
from AthenaCommon.AppMgr import ServiceMgr as svcMgr
if not hasattr(svcMgr, 'DecisionSvc'):
        svcMgr += CfgMgr.DecisionSvc()
svcMgr.DecisionSvc.CalcStats = True


# Add the track dressing alg
streamName = "IDTIDE"

from DerivationFrameworkInDet.DerivationFrameworkInDetConf import DerivationFramework__TrackParametersForTruthParticles
TruthDecor = DerivationFramework__TrackParametersForTruthParticles( name = "TruthTPDecor",
                                                                    TruthParticleContainerName = "TruthParticles")
ToolSvc +=TruthDecor

augmentationTools = [TruthDecor]

from DerivationFrameworkInDet.DerivationFrameworkInDetConf import DerivationFramework__TrackStateOnSurfaceDecorator
DFTSOS = DerivationFramework__TrackStateOnSurfaceDecorator(name = "DFTrackStateOnSurfaceDecorator",
                                                          ContainerName = InDetKeys.xAODTrackParticleContainer(),
                                                          DecorationPrefix = "",
                                                          StoreTRT = False,
                                                          OutputLevel =INFO)
ToolSvc += DFTSOS
augmentationTools += [DFTSOS]


if InDetFlags.doPseudoTracking():
  from DerivationFrameworkInDet.DerivationFrameworkInDetConf import DerivationFramework__TrackStateOnSurfaceDecorator
  DFPTSOS = DerivationFramework__TrackStateOnSurfaceDecorator(name = "DFPseudoTrackStateOnSurfaceDecorator",
                                                          ContainerName = InDetKeys.xAODPseudoTrackParticleContainer(),
                                                          DecorationPrefix = streamName,
   PixelMsosName = "PseudoPixelMSOSs",
	 SctMsosName = "PseudoSctMSOSs",   
	 TrtMsosName = "PseudoTrtMSOSs",
   StoreTRT = False,
                                                          OutputLevel =INFO)
  ToolSvc += DFPTSOS
  augmentationTools += [ DFPTSOS]

from OutputStreamAthenaPool.MultipleStreamManager import MSMgr

fileName   = "AOD.TIDE.pool.root"

TestStream = MSMgr.NewPoolRootStream( streamName, fileName)
TestStream.AddItem("xAOD::EventInfo#*")
TestStream.AddItem("xAOD::EventAuxInfo#*")
TestStream.AddItem("xAOD::TrackParticleContainer#*")
TestStream.AddItem("xAOD::TrackParticleAuxContainer#*")
TestStream.AddItem("xAOD::VertexContainer#PrimaryVerticesAux")
TestStream.AddItem("xAOD::VertexAuxContainer#PrimaryVerticesAux")
TestStream.AddItem("xAOD::TrackMeasurementValidationContainer#*")
TestStream.AddItem("xAOD::TrackMeasurementValidationAuxContainer#*")
TestStream.AddItem("xAOD::TrackStateValidationContainer#*")
TestStream.AddItem("xAOD::TrackStateValidationAuxContainer#*")
TestStream.AddItem("xAOD::TruthParticleContainer#*")
TestStream.AddItem("xAOD::TruthParticleAuxContainer#*")
TestStream.AddItem("xAOD::TruthVertexContainer#*")
TestStream.AddItem("xAOD::TruthVertexAuxContainer#*")
TestStream.AddItem("xAOD::TruthEventContainer#*")
TestStream.AddItem("xAOD::TruthEventAuxContainer#*")
TestStream.ForceRead = True

from DerivationFrameworkCore.ThinningHelper import ThinningHelper
IDTIDEThinningHelper = ThinningHelper( "IDTIDEThinningHelper" )
IDTIDEThinningHelper.AppendToStream( TestStream )


thinningTools = []

# TrackParticles directly
from DerivationFrameworkInDet.DerivationFrameworkInDetConf import DerivationFramework__TrackParticleThinning
IDTIDE1ThinningTool = DerivationFramework__TrackParticleThinning(name = "IDTIDE1ThinningTool",
	                                                         ThinningService         = IDTIDEThinningHelper.ThinningSvc(),
	                                                         SelectionString         = "InDetTrackParticles.pt >= 0",
	                                                         InDetTrackParticlesKey  = "InDetTrackParticles",
	                                                         ThinHitsOnTrack = True,
                                                                 OutputLevel = INFO)
ToolSvc += IDTIDE1ThinningTool
thinningTools.append(IDTIDE1ThinningTool)

DerivationFrameworkJob += CfgMgr.DerivationFramework__DerivationKernel("DFTSOS_KERN",
	                                                               AugmentationTools = augmentationTools,
	                                                               ThinningTools = thinningTools,
	                                                               OutputLevel =INFO)

topSequence += DerivationFrameworkJob

print("dumping alg sequence")
from AthenaCommon.AlgSequence import *
dumpSequence(topSequence)
