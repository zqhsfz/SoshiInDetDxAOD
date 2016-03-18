import ROOT
from run import db
from optparse import OptionParser
import os

_dataFolder = "5steps/"

def ProcessOneROOT(iParticleType, index_BetaGammaLog10, outputStream_ColELog10, outputStream_Boundary, saveFile=False):
	filename =  _dataFolder+"/Bichsel_%s_%s.root" % (iParticleType, index_BetaGammaLog10)
	print "processing",filename

	f = ROOT.TFile(filename)
	t = f.Get("tree")

	currentDB = db[iParticleType-1]

	UpperBoundIntX = ROOT.TMath.Power(10., currentDB.Array_BetaGammaLog10_UpperBoundIntXLog10[index_BetaGammaLog10])

	def GetHistogram(branchname, nbins):
		low = int(t.GetMinimum(branchname))-1
		up  = int(t.GetMaximum(branchname))+1

		h = ROOT.TH1D("hist_"+branchname, "hist_"+branchname, nbins, low, up)
		t.Draw("%s >> %s" % (branchname, h.GetName()))
		h.SetDirectory(0)

		if branchname == "ColELog10":
			h.Scale(UpperBoundIntX/h.Integral(0, h.GetNbinsX()+1))
		else:
			h.Scale(1./h.Integral(0, h.GetNbinsX()+1))

		cdf = h.GetCumulative()
		cdf.SetDirectory(0)

		return (h, cdf)

	pdf_ColELog10, cdf_ColELog10 = GetHistogram("ColELog10", 100)
	pdf_Boundary, cdf_Boundary = GetHistogram("Boundary", 100)

	def ConvertCDFtoDAT(cdf, outputStream, doLogy):
		if outputStream is None:
			return

		startRecord = False
		for ibin in range(1, cdf.GetNbinsX()+1):
			if (startRecord) or (cdf.GetBinContent(ibin) > 0):
				startRecord = True

			if startRecord:
				BetaGammaLog10 = currentDB.Array_BetaGammaLog10[index_BetaGammaLog10]
				ColELog10 = cdf.GetBinLowEdge(ibin+1)    # the upper edge of current bin. This is consistent with how we build the CDF. Also, it matters which point we choose, since it is in log scale and will affect final energy distribution significantly
				if doLogy:
					y = ROOT.TMath.Log10(cdf.GetBinContent(ibin))
				else:
					y = cdf.GetBinContent(ibin)

				outputStream.write("%.10e %.10e %.10e\n" % (BetaGammaLog10, ColELog10, y))

	ConvertCDFtoDAT(cdf_ColELog10, outputStream_ColELog10, True)      
	ConvertCDFtoDAT(cdf_Boundary, outputStream_Boundary, False)      # for boundary, the X is in linear scale, not log-scale

	if saveFile:
		cdf_ColELog10.SaveAs("CDF_ColELog10.root")
		cdf_Boundary.SaveAs("CDF_Boundary.root")

def ProcessOneParticleType(iParticleType):
	currentDB = db[iParticleType-1]

	outputStream_ColELog10 = open("newBichsel_%s.dat" % (iParticleType), "w")
	outputStream_Boundary = open("Boundary_%s.dat" % (iParticleType), "w")

	for index_BetaGammaLog10 in range(currentDB.Array_BetaGammaLog10.size()):
		# ProcessOneROOT(iParticleType, index_BetaGammaLog10, outputStream_ColELog10, outputStream_Boundary)
		ProcessOneROOT(iParticleType, index_BetaGammaLog10, outputStream_ColELog10, None)

	outputStream_ColELog10.close()
	outputStream_Boundary.close()

def GenerateDataFiles():
	parser = OptionParser()
	parser.add_option("-p", "--iParticleType", dest="iParticleType", help="Particle Type", type="int", default=-1)
	parser.add_option("-b", "--batch", action="store_true", dest="batch", help="Whether do batch running", default=False)
	(options, args) = parser.parse_args()

	if options.batch:
		for iParticleType in range(1, 7):
			cmd = "bsub -q atlas-t3 -W 2:00 python buildTable.py -p %s" % (iParticleType)
			os.system(cmd)
	else:
		ProcessOneParticleType(options.iParticleType)

if __name__ == "__main__":
	# ProcessOneROOT(3, 18, None, None, True)

	GenerateDataFiles()









