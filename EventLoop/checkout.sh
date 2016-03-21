# revert xAODTracking version, since the DAOD production use an old version
# This will make compilation very long ... but OK ...

# pkg checkout
git clone https://github.com/UCATLAS/xAODAnaHelpers.git
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasinst/Institutes/SLAC/AutoHists/trunk AutoHists
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasoff/Event/xAOD/xAODTracking/tags/xAODTracking-00-13-21 xAODTracking
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasoff/PhysicsAnalysis/D3PDTools/EventLoop/tags/EventLoop-00-01-37 EventLoop
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasoff/Control/xAODRootAccess/tags/xAODRootAccess-00-01-41 xAODRootAccess

# running scripts
python xAODAnaHelpers/scripts/checkoutASGtags.py 2.3.41 # just a temporary hack. xAH does not support 2.4.3 yet. 2.3.41 in xAH is empty, which is what we want

# for SLAC user:
# commnet out the option setting on "sharedLSF" in xAODAnaHelpers/scripts/xAH_run.py
