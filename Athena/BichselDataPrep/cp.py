import os

sourceDirs = ["1step", "5steps", "10steps"]
targetDir = "/u/gl/zengq/nfs/PixelClusterAnalysis/Soshi2/SoshiInDetDxAOD/Athena/DigiRecon/InnerDetector/InDetDigitization/PixelDigitization/share"

for iParticleType in range(1, 7):
	for sourceDir in sourceDirs:

		if sourceDir == "1step":
			targetFileName = "Bichsel_%s.dat" % (iParticleType)
		else:
			targetFileName = "Bichsel_%s_%s.dat" % (iParticleType, sourceDir)

		cmd = "cp %s/newBichsel_%s.dat %s/%s" % (sourceDir, iParticleType, targetDir, targetFileName)
		print cmd
		os.system(cmd)