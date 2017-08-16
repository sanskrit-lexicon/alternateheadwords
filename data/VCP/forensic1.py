"""forensic1.py
   08-15-2017
   Compare two vcpahwX.txt files. Consider two such to be the same
   if the key2 fields and alt1 fields match.
   Read the files into HWnorma object sequences
"""
import sys,re
import check_hwnorm   # contains HWnorma object

def compare1(filein1,filein2):
 recs1=check_hwnorm.init_hwnorma(filein1)
 recs2=check_hwnorm.init_hwnorma(filein2)
 if len(recs1) != len(recs2):
  print "ERROR: %s and %s have different number of records"
  exit(1)
 ndiff = 0
 for idx,rec1 in enumerate(recs1):
  rec2 = recs2[idx]
  if (rec1.key2 != rec2.key2):
   ndiff = ndiff + 1
   print "DIfference in key2 at line #",idx+1
   print    '%s %s' %(filein1,rec1.line)
   print    '%s %s' %(filein2,rec2.line)
   continue
  if (rec1.key1alt != rec2.key1alt):
   ndiff = ndiff + 1
   print "DIfference in key1alt at line #",idx+1
   print    '%s %s' %(filein1,rec1.line)
   print    '%s %s' %(filein2,rec2.line)
 if ndiff == 0:
  print "SUCCESS: %s = %s with respect to key2 and key1alt" %(filein1,filein2)
 else:
  print "PROBLEM: %s differences in %s and %s" %(ndiff,filein1,filein2)
if __name__ == "__main__":
 filein1 = sys.argv[1]
 filein2= sys.argv[2]
 compare1(filein1,filein2)
