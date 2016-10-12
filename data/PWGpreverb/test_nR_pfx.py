"""test_nR_pfx.py
   Reads the prefixes from preverb1a, and notes any that are mis-spelled
   when nR sandhi is taken into account.
   python test_nR_pfx.py preverb1a.txt test_nR_pfx.txt
"""
import sys,codecs
from sandhi_nR import sandhi_nR

class Preverb(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.L,self.hw,self.pfx,self.pfxhw,self.linenum) = line.split(':')
  self.mwflag = False # filled in later
  self.mwhw = None  # either self.hw, or MW spelling of self.hw

def init_preverbs(filein):
 #f = codecs.open(filein,encoding='utf-8',mode='r')
 # filein is ascii file (pwhw2.txt)
 # read it as Ascii so slp_cmp string.translate works
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(Preverb(line,n))
 f.close()
 return recs

if __name__=="__main__":
 filein = sys.argv[1] # preverb1a.txt
 fileout = sys.argv[2] # 
 preverbrecs = init_preverbs(filein)
 print len(preverbrecs),"records from",filein
 fout = codecs.open(fileout,"w")
 nout = 0
 cases = {}
 for preverbrec in preverbrecs:
  pfx = preverbrec.pfx
  pfx_adj = sandhi_nR(pfx)
  if pfx != pfx_adj:
   nout = nout + 1
   out = '%s ## %s ADJ= %s' %(preverbrec.line,pfx,pfx_adj)
   fout.write(out + '\n')
   if pfx not in cases:
    cases[pfx]=0
   cases[pfx] = cases[pfx]+1
 fout.close()
 print nout,"cases written to",fileout
 keys = cases.keys()
 keys.sort()
 for pfx in keys:
  print pfx,cases[pfx],sandhi_nR(pfx)
