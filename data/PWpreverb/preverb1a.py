"""preverb1a.py
   Oct 10, 2016
   Join verb and prefix for preverbs of pwg
"""
import sys, re
import codecs
from scharfsandhi import ScharfSandhi

class PreverbSandhi(ScharfSandhi):
 def sandhi(self,s):
  dbg=True
  ans=None
  parts = s.split(self.Padbound) # '-' for Compound sandhi
  (pfx,root) = parts # error if more than 2 parts
  if root.startswith('s'):
   if pfx.endswith('antar'):
    pfx1 = pfx[0:-1]+'H' # replace r with 'H'
    ans = pfx1 + root
   elif pfx.endswith('i') and (root in ['star','spar']): # MW stf
    # star (MW stf) is apparently different 
    pass  # so use 'defualt' sandhi
   elif root == 'smar':
    # smar = MW smf
    pass # so use 'default' sandhi
   elif pfx.endswith(('i','u')):
    if root.startswith('sT'):
     ans = pfx + 'zW' + root[2:]
    elif root.startswith('st'):
     ans = pfx + 'zw' + root[2:]
    elif root.startswith(('sa','sA')):
     # example 'sar','sarp', etc in PWG (= 'sf','sfp',etc in MW)
     ans = pfx + root # ?
    else: # any other root starting with 's'
     ans = pfx + 'z' + root[1:]
   elif pfx.endswith('nis'):
    # examples: nissar = niHsar -> mw niHsf
    ans = pfx[0:-1] + 'H' + root
  if ans == None:
   ans = super(PreverbSandhi,self).sandhi(s)
  if dbg:
   old = super(PreverbSandhi,self).sandhi(s)
   if ans != old: 
    print "DBG: %s. PreverbSandhi=>%s, ScharfSandhi=>%s" %(s, ans,old)
  return ans

class Preverb(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.L,self.hw,self.pfx,self.linenum) = line.split(':')
  self.pfxhw = None # computed later
 def join(self,sandhi):
  # assume compound sandhi (C)
  s = self.pfx + '-' + self.hw
  self.pfxhw = sandhi.sandhi(s)

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

def write_preverbs(recs,fileout):
 """ recs is array of Preverb objects
 """
 fout = codecs.open(fileout,'w')
 n = 0
 nadj=0
 for rec in recs:
  L = rec.L # headword record number
  hw = rec.hw  # the headword
  pfx = rec.pfx # the preverb prefixes
  pfxhw = rec.pfxhw
  linenum = rec.linenum
  out = "%s:%s:%s:%s:%s" %(L,hw,pfx,pfxhw,linenum)
  fout.write(out + '\n')
  n = n + 1
  dumb_pfxhw = pfx + hw
  if dumb_pfxhw != pfxhw:
   nadj = nadj+1
   outadj = "ADJUST %03d: %s:%s:%s:%s  (dumb=%s)" %(nadj,L,hw,pfx,pfxhw,dumb_pfxhw)
   try:
    #print outadj.encode('utf-8')
    pass
   except :
    print "ERROR PRINTING for line=",n,rec.line
 fout.close()
 print n,"records written to",fileout
 print nadj,"prefixed verbs required sandhi adjustments"
if __name__=="__main__":
 filein = sys.argv[1] # preverb1.txt
 fileout = sys.argv[2] # preverb1a.txt
 preverbrecs = init_preverbs(filein)
 print len(preverbrecs),"records from",filein
 #sandhi = ScharfSandhi()
 sandhi = PreverbSandhi()
 err = sandhi.simple_sandhioptions('C')
 for rec in preverbrecs:
  rec.join(sandhi)

 # output
 write_preverbs(preverbrecs,fileout)
