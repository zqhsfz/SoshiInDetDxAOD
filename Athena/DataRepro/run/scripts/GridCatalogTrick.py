import os

# add calibration files to catalog: 
print 'adding calibration files to catalog:' 
os.system('coolHist_insertFileToCatalog.py '+'NNCalibBichselFinal.root') 
print 'file ready:' 
import commands 
stat, out = commands.getstatusoutput('cat PoolFileCatalog.xml') 
print out 
