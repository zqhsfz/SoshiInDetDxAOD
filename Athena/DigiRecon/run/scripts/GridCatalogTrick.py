import os

# add calibration files to catalog: 
print 'adding calibration files to catalog:' 
os.system('coolHist_insertFileToCatalog.py '+'NNCalibFinal_NNTrained_20160513_LGTide_JZ6W.root') 
print 'file ready:' 
import commands 
stat, out = commands.getstatusoutput('cat PoolFileCatalog.xml') 
print out 
