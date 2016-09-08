import os

f = open("filelist_user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_blayerON_pixelON_Nominal_EXT0.txt", "r")
pattern = "root://atlprf01.slac.stanford.edu:11094/"

for line in f.readlines():
	startIndex = line.find(pattern) + len(pattern)
	file_source = line[startIndex:-1]
	cmd = "cp %s /u/gl/zengq/nfs2/Atlas/dataset_tmp/user.qzeng.mc15_13TeV.361107.Zmumu.InDetDxAOD.e3601_ATLAS-R2-2015-03-15-00.v00-00-01_blayerON_pixelON_Nominal_EXT0/" % (file_source)

	print cmd,"..."
	os.system(cmd)
