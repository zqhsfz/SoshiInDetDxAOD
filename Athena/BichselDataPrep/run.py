import ROOT
from optparse import OptionParser
import os

ROOT.gSystem.Load("libBichselSimTool.so")

tool = ROOT.BichselSimTool()
tool.initialize()
db = tool.m_BichselData

def runOnePoint(iParticleType, index_BetaGammaLog10):
	# tool.Scan(iParticleType, index_BetaGammaLog10, 10, 10000000)
	tool.Scan(iParticleType, index_BetaGammaLog10, 5, 10000000)
	# tool.Scan(iParticleType, index_BetaGammaLog10, 1, 10000000)

def runBatch():
	for iParticleType in range(1, db.size()+1):
		for index_BetaGammaLog10 in range(db[iParticleType-1].Array_BetaGammaLog10.size()):
			cmd = "bsub -q atlas-t3 -W 2:00 python run.py -p %s -g %s" % (iParticleType, index_BetaGammaLog10)
			print cmd
			os.system(cmd)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-p", "--iParticleType", dest="iParticleType", help="Particle Type", type="int", default=-1)
	parser.add_option("-g", "--index_BetaGammaLog10", dest="index_BetaGammaLog10", help="index of beta-gamma log10", type="int", default=-1)
	parser.add_option("-b", "--batch", action="store_true", dest="batch", help="Whether do batch running", default=False)
	(options, args) = parser.parse_args()

	if options.batch:
		runBatch()
	else:
		runOnePoint(options.iParticleType, options.index_BetaGammaLog10)
