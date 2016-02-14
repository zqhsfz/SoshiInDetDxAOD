# pkg checkout
git clone https://github.com/UCATLAS/xAODAnaHelpers.git
svn co svn+ssh://qzeng@svn.cern.ch/reps/atlasinst/Institutes/SLAC/AutoHists/trunk AutoHists

# running scripts
# rcSetup use 2.4.3 to be compatible with 20.7
# However, we still use 2.3.39 for xAH, which should not matter for now 
# data,rel20.1 - 2.3.39
# mc,rel20.7 - 2.4.3
python xAODAnaHelpers/scripts/checkoutASGtags.py 2.3.39
