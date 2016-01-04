import runUtils
import os

#################
# Local Version #
#################

# AMITag = "f643"
# Options = runUtils.GetOptions(AMITag)
# extraOptions = {'maxEvents': '20', 'inputBSFile': '/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/20.1.8.4/data/data15_13TeV.00283780.physics_Main.merge.DRAW_ZMUMU.f643_m1453/data15_13TeV.00283780.physics_Main.merge.DRAW_ZMUMU.f643_m1453._0097.1', 'outputDAOD_IDTRKVALIDFile': 'InDetDxAOD.pool.root'}
# cmd = runUtils.GetCmd(Options, extraOptions, doNewLine=False)

# print cmd
# os.system(cmd)

################
# Grid Version #
################

AMITag = "f643"
TrfOptions = runUtils.GetOptions(AMITag)
TrfExtraOptions = {'maxEvents': '2000', 'inputBSFile': '%IN', 'outputDAOD_IDTRKVALIDFile': '%OUT.InDetDxAOD.pool.root', 'skipEvents': '%SKIPEVENTS'}
PathenaOptions = {'inDS': 'data15_13TeV.periodJ.physics_Main.PhysCont.DRAW_ZMUMU.t0pro19_v01', 'outDS': 'user.qzeng.data15_13TeV.periodJ.physics_Main.DRAW_ZMUMU.t0pro19_v01.SoshiInDetDxAOD-v00-00-00', 'dbRelease': 'LATEST', 'skipScout': None, 'nEventsPerJob': 2000}
cmd = runUtils.GetPathenaCmd(PathenaOptions, TrfOptions, TrfExtraOptions, doNewLine=False)

print cmd
os.system(cmd)