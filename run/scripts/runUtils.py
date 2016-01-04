from copy import deepcopy
import ast
import os

import pyAMI.client
import pyAMI.atlas.api as AtlasAPI
client = pyAMI.client.Client('atlas')
AtlasAPI.init()

# get option dictionary given AMITag
# Make sure you setup pyami before
def GetOptions(AMITag):
	fullInfo_unicode = pyAMI.atlas.api.get_ami_tag(client, AMITag)[0]
	phconfig_unicode = fullInfo_unicode[u'phconfig']
	phconfig = ast.literal_eval(phconfig_unicode)
	return phconfig

# generate local trf command line given AMI options
def GetCmd(Options, extraOptions, doNewLine=False):
	# make deepy copy first
	Options_in = deepcopy(Options)
	extraOptions_in = deepcopy(extraOptions)

	# merge two options, extraOption should overwrite option
	for key,value in extraOptions_in.items():
		Options_in[key] = value

	# now generate command
	cmd = "Reco_tf.py "
	for key,value in Options_in.items():
		contentList = []

		if type(value) == list:
			if len(value) > 1:
				print "ERROR: Unrecognized value!",value
				return None
			else:
				contentList.append( value[0] )
		elif type(value) == dict:
			for stage, exp in value.items():
				if type(exp) == list:
					if len(exp) > 1:
						print "ERROR: Unrecognized value!",exp
					else:
						contentList.append( "%s:%s" % (stage, exp[0]) )
				elif type(exp) == str:
					contentList.append( "%s:%s" % (stage, exp) )
				else:
					print "ERROR: Unrecognized value!",exp
		elif type(value) == str:
			contentList.append( value )
		elif type(value) == bool:
			contentList.append( str(value) )
		else:
			print 'ERROR: Unrecognized value!',value
			return None

		cmd += ("--%s " % (key))
		for content in contentList:
			if "%" in content:   # only appears in pathena case
				cmd += ("%s " % (content))
			else:
				cmd += ("\'%s\' " % (content))

		if doNewLine:
			cmd += ("\n")

	return cmd

# generate pathena command 
def GetPathenaCmd(PathenaOptions, TrfOptions, TrfExtraOptions, doNewLine=False):
	trfCmd = GetCmd(TrfOptions, TrfExtraOptions, False)
	trfCmd = trfCmd.replace('\"', '\\\"')

	PathenaOptions_in = deepcopy(PathenaOptions)
	PathenaOptions_in['trf'] = trfCmd

	pathenaCmd = "pathena "

	if doNewLine:
		pathenaCmd += ("\n")

	for key,value in PathenaOptions_in.items():
		pathenaCmd += ("--%s" % (key))

		if key == "trf":
			pathenaCmd += (" \"%s\" " % (value))
		elif value is None:
			pathenaCmd += " "
		else:
			pathenaCmd += ("=%s " % (value))

		if doNewLine:
			pathenaCmd += ("\n")

	return pathenaCmd

# running example
if __name__ == "__main__":
	# f643
	# Options = {'conditionsTag': {'all': 'CONDBR2-BLKPA-2015-14'}, 'ignorePatterns': ['ToolSvc.InDetSCTRodDecoder.+ERROR.+Unknown.+offlineId.+for.+OnlineId'], 'ignoreErrors': True, 'autoConfiguration': ['everything'], 'maxEvents': '-1', 'AMITag': 'f629', 'postExec': {'e2d': ['from AthenaCommon.AppMgr import ServiceMgr; import MuonRPC_Cabling.MuonRPC_CablingConfig ; ServiceMgr.MuonRPC_CablingSvc.RPCMapfromCool=False ; ServiceMgr.MuonRPC_CablingSvc.CorrFileName="LVL1confAtlasRUN2_ver016.corr"; ServiceMgr.MuonRPC_CablingSvc.ConfFileName="LVL1confAtlasRUN2_ver016.data" ']}, 'preExec': {'all': ['from MuonRecExample.MuonRecFlags import muonRecFlags;muonRecFlags.useLooseErrorTuning.set_Value_and_Lock(True);DQMonFlags.doCTPMon=False;jobproperties.Beam.bunchSpacing.set_Value_and_Lock(25)']}, 'geometryVersion': {'all': 'ATLAS-R2-2015-03-01-00'}}
	Options = GetOptions('f643')
	extraOptions = {'maxEvents': '20', 'inputBSFile': '/afs/cern.ch/user/q/qzeng/Work/PixelCluster/SoshiZmumuFramework/20.1.8.4/data/data15_13TeV.00283780.physics_Main.merge.DRAW_ZMUMU.f643_m1453/data15_13TeV.00283780.physics_Main.merge.DRAW_ZMUMU.f643_m1453._0097.1', 'outputDAOD_IDTRKVALIDFile': 'InDetDxAOD.pool.root'}
	cmd = GetCmd(Options, extraOptions, doNewLine=False)
	print cmd





















