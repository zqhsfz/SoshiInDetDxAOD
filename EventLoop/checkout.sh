# pkg checkout
git clone https://github.com/UCATLAS/xAODAnaHelpers.git
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasinst/Institutes/SLAC/AutoHists/trunk AutoHists
svn co $SVNOFF/PhysicsAnalysis/MuonID/MuonSelectorTools/tags/MuonSelectorTools-00-05-32 MuonSelectorTools

# running scripts
python xAODAnaHelpers/scripts/checkoutASGtags.py 2.4.11
