setupATLAS
asetup AtlasProduction,20.7.3.3,here
export G4RADIOACTIVEDATA=$G4NEUTRONHPDATA/../RadioactiveDecay

# for SLAC
export FRONTIER_SERVER="(serverurl=http://atlasfrontier-ai.cern.ch:8000/atlr)(serverurl=http://lcgft-atlas.gridpp.rl.ac.uk:3128/frontierATLAS)(serverurl=http://frontier-atlas.lcg.triumf.ca:3128/ATLAS_frontier)(serverurl=http://ccfrontier.in2p3.fr:23128/ccin2p3-AtlasFrontier)"
