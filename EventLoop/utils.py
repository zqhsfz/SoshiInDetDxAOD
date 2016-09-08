###################################################################################################################################################
# Generate a file-list for a data-set that is transferred to SLAC-ATLAS-T3_GRIDFTP
# Make sure you have rucio setup before running these
###################################################################################################################################################

def GetGridFileList(datasetname):
	import subprocess

	outputList = []
	rawRucioOutput = subprocess.check_output(["rucio", "list-files", datasetname]).split("\n")
	for line in rawRucioOutput:
		if "pool.root" not in line: continue
		GridFileName = line.split("|")[1].replace(" ","")
		outputList.append(GridFileName)

	return outputList

def GenerateFileListR2D2(datasetname, RSE, outputFileName):
	import subprocess

	rucio = subprocess.Popen(('rucio', 'list-file-replicas', datasetname), stdout=subprocess.PIPE)
	GridFileList = subprocess.check_output(('grep', RSE), stdin=rucio.stdout).split("\n")
	LocalFileList = []
	for GridFileName in GridFileList:
		if "pool.root" not in GridFileName: continue
		if RSE not in GridFileName:
			print "Warning! %s not found in line %s" % (RSE, GridFileName)
			continue

		FilePathAndName = GridFileName.split("|")[5].split(":")[-1]
		FilePathAndName = FilePathAndName[FilePathAndName.find("/"):]
		FilePathAndName = FilePathAndName.replace(" ", "")

		LocalFileList.append(FilePathAndName)

	f = open(outputFileName, "w")
	for LocalFileName in LocalFileList:
		f.write("root://atlprf01.slac.stanford.edu:11094/"+LocalFileName+"\n")
	f.close()

def runGenerateFileListR2D2(version):
	R2D2_FileList = open("filelists/%s/filelist_derivation.txt" % (version))
	for line in R2D2_FileList:
		# if "DAOD_IDTRKVALID" not in line: continue

		line = line.split("\n")[0]
		line = line.split("/")[0]

		line_noscope = line.split(":")[1]

		print "Processing",line,"..."
		GenerateFileListR2D2(line, "SLAC-ATLAS-T3_GRIDFTP", "filelists/"+version+"/filelist_"+line_noscope+".txt")	




