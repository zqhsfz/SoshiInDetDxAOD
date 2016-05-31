import ROOT
import sys

#################################################################################
# adapted from https://root.cern.ch/root/html/tutorials/io/copyFiles.C.html
#################################################################################

# assume you are at the directory you want to copy to (i.e. destination)
# dir.cd() is like you "activate" this dir. It is important when you are doing some manipulation across directories, since all objects are under some certain directory
def CopyDir(source):
	# source.ls()
	
	savdir = ROOT.gDirectory
	adir = savdir.mkdir(source.GetName())
	adir.cd()

	keyList = source.GetListOfKeys()
	for iKey in range(keyList.GetEntries()):
		key = keyList.At(iKey)

		classname = key.GetClassName()
		cl = ROOT.gROOT.GetClass(classname)

		if(not cl): continue

		if(cl.InheritsFrom(ROOT.TDirectory.Class())):
			soure.cd(key.GetName())
			subdir = ROOT.gDirectory
			adir.cd()
			CopyDir(subdir)
			adir.cd()
		elif(cl.InheritsFrom(ROOT.TTree.Class())):
			T = source.Get(key.GetName())
			adir.cd()
			newT = T.CloneTree(-1, "fast")
			newT.Write()
		else:
			source.cd()
			obj = key.ReadObj()
			adir.cd()
			obj.Write()
			del obj

	adir.SaveSelf(True)
	savdir.cd()

def mergeCalibration(pathOLD, pathBICHSEL, outputNAME):
	print "Merging %s and %s to %s ..." % (pathOLD, pathBICHSEL, outputNAME)

	# the list that you want to write into new calibration file eventually
	# Order matters here!
	dirList = [
	            "NumberParticles_NoTrack",
	            "ImpactPoints1P_NoTrack",
	            "ImpactPoints2P_NoTrack",
	            "ImpactPoints3P_NoTrack",
	            "ImpactPointErrorsX1_NoTrack",
	            "ImpactPointErrorsX2_NoTrack",
	            "ImpactPointErrorsX3_NoTrack",
	            "ImpactPointErrorsY1_NoTrack",
	            "ImpactPointErrorsY2_NoTrack",
	            "ImpactPointErrorsY3_NoTrack",

	            "NumberParticles",
	            "ImpactPoints1P",
	            "ImpactPoints2P",
	            "ImpactPoints3P",
	            "ImpactPointErrorsX1",
	            "ImpactPointErrorsX2",
	            "ImpactPointErrorsX3",
	            "ImpactPointErrorsY1",
	            "ImpactPointErrorsY2",
	            "ImpactPointErrorsY3",
	          ]

	# f_old = ROOT.TFile("NNCalibFiles/OFLCOND-MC15c-SDR-05/cond09_mc.000036.gen.COND._0002.pool.root")
	# f_bichsel = ROOT.TFile("NNClusteringCalibration_RunII/NNCalibBichsel.root")

	f_old = ROOT.TFile(pathOLD)
	f_bichsel = ROOT.TFile(pathBICHSEL)

	# first check if all dirList exists in f_old
	keyList_old = f_old.GetListOfKeys()
	dirList_old = [keyList_old.At(index).GetName() for index in range(keyList_old.GetEntries())]
	_isContained = (set(dirList) & set(dirList_old) == set(dirList))
	print "Check if dirList is contained in old file:", _isContained
	if not _isContained:
		print "ERROR! Quitting ..."
		print "dirList:",dirList
		print "dirList_old:",dirList_old
		sys.exit(0)

	# next check the dirList in f_bichsel that should overwrite the old files
	keyList_bichsel = f_bichsel.GetListOfKeys()
	dirList_bichsel = [keyList_bichsel.At(index).GetName() for index in range(keyList_bichsel.GetEntries())]

	# create new file
	f_new = ROOT.TFile(outputNAME, "RECREATE")

	print "Merging files to %s ..." % (outputNAME)

	for keyName in dirList:
		print "Processing dir:",keyName,"..."

		f_new.cd()

		if keyName in dirList_bichsel:
			print "\tTake content from bichsel file"
			source = f_bichsel.Get(keyName)
			CopyDir(source)
		else:	
			print "\tTake content from old file"
			source = f_old.Get(keyName)
			CopyDir(source)

	f_new.Close()

if __name__ == "__main__":
	# There are two IOVs in this tag, one for run 1 and one for run 2. We only overwrite the run 2 one
	mergeCalibration("NNCalibFiles/OFLCOND-MC15c-SDR-05/cond09_mc.000087.gen.COND._0004.pool.root", "NNClusteringCalibration_RunII/NNCalibBichsel_NNTrained_20160513_LGTide_JZ6W.root", "NNCalibFinal_NNTrained_20160513_LGTide_JZ6W.root")

