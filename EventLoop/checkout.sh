# revert xAODTracking version, since the DAOD production use an old version
# This will make compilation very long ... but OK ...

# pkg checkout
git clone https://github.com/UCATLAS/xAODAnaHelpers.git
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasinst/Institutes/SLAC/AutoHists/trunk AutoHists
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasoff/Event/xAOD/xAODTracking/tags/xAODTracking-00-13-21 xAODTracking

# running scripts
python xAODAnaHelpers/scripts/checkoutASGtags.py 2.3.41 # just a temporary hack. xAH does not support 2.4.3 yet. 2.3.41 in xAH is empty, which is what we want
