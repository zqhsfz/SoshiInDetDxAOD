import os
import subprocess

def GetListOfFiles(datasetname):
	rawRucio = subprocess.check_output(["rucio", "list-files", datasetname])
	rawRucioList = rawRucio.split("\n")

	fileList = []
	for line in rawRucioList:
		if "pool.root" not in line: continue

		filename_withspace = line.split("|")[1]
		filename = filename_withspace.replace(" ", "")

		fileList.append( filename )

	return fileList

def GetExistingHITSFiles():
	f = open("ExistingHITS_Soshi270.txt", "w")
	fileList = GetListOfFiles("user.stsuno:user.stsuno.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0")

	for filename in fileList:
		f.write(filename+"\n")

	f.close()

def GetNewUploadHITSFiles():
	f = open("NewUploadHITS.txt", "w")

	rawFileList = subprocess.check_output(["ls", "/u/gl/zengq/nfs2/Atlas/dataset_tmp/HITSUpload/"]).split("\n")
	for item in rawFileList:
		if "pool.root" not in item: continue
		f.write("user.qzeng:"+item+"\n")

	f.close()


def TransferUnregisteredHITSFiles():
	local_sourcebase = "/atlas/local/zengq/PixelCluster/SoshiInDetDxAOD/HITS/user.stsuno.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0/"
	local_targetbase = "/u/gl/zengq/nfs2/Atlas/dataset_tmp/HITSUpload/"

	fileList_registered = GetListOfFiles("user.stsuno:user.stsuno.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.EVNT.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0")
	fileList_alllocal = subprocess.check_output(["ls", local_sourcebase]).split("\n")

	count = 0
	for fileName in fileList_alllocal:
		fileName_tocheck = "user.stsuno:"+fileName
		if fileName_tocheck in fileList_registered: continue
		if "pool.root" not in fileName: continue

		count += 1

		print "Transferring file:",fileName,"..."
		cmd = "xrdcp root://atlprf01:1094/%s/%s %s" % (local_sourcebase, fileName, local_targetbase)
		os.system(cmd)

	print "Files to be uploaded:",count


def test():
	fileList = GetListOfFiles("user.qzeng.mc15_13TeV.361107.PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu.evgen.HITS.e3601_ATLAS-R2-2015-03-15-00.v1_EXT0")

	n_qzeng = 0
	n_soshi = 0

	for filename in fileList:
		scope = filename.split(":")[0]
		if "qzeng" in scope: n_qzeng += 1
		if "stsuno" in scope: n_soshi += 1

	print "qzeng:",n_qzeng
	print "soshi:",n_soshi

# This file only provides some auxiliary functions
# Two important steps to be done by hand
# "rucio attach" the existing files to your dataset
# "rucio upload" the un-registered local files to your dataset 
if __name__ == "__main__":
	# test()

	# GetExistingHITSFiles()
	# TransferUnregisteredHITSFiles()
	GetNewUploadHITSFiles()








