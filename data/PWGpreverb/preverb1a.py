"""preverb1a.py
   Oct 10, 2016
   Join verb and prefix for preverbs of pwg
   Modified to use nR sandhi
"""
import sys, re
import codecs
from scharfsandhi import ScharfSandhi
from sandhi_nR import sandhi_nR

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
    elif root in ['sad','sac','saYj']:
     ans = pfx + 'z' + root[1:]
    elif root in ['svar','svap','svan','sru','sraMs','syad']:
     ans = pfx + root # ?
    elif root in ['sah']:
     if pfx.endswith('prati'):
      ans = pfx + root
     else:
      ans = pfx + 'z' + root[1:]
    elif root.startswith(('sa','sA')):
     # example 'sar','sarp', etc in PWG (= 'sf','sfp',etc in MW)
     ans = pfx + root # ?
    else: # any other root starting with 's'
     ans = pfx + 'z' + root[1:]
   elif pfx.endswith('nis'):
    # examples: nissar = niHsar -> mw niHsf
    ans = pfx[0:-1] + 'H' + root
  #======================
  elif pfx.endswith('nis') and root.startswith('kzi'):
   # examples niHzki, niHkzip (acc. to MW spelling)
   ans = pfx[0:-1] + 'H' + root
  elif pfx.endswith('nis') and (root in ['waNk']):
   ans = pfx[0:-1]+'z' + root
  elif pfx.endswith('nis') and (root in ['SAs','Siz','SI','Suc','Sri','Svas','zWiv']):
   ans = pfx[0:-1] + 'H' + root
  elif pfx.endswith('pra') and (root in ['an','in']):
   # examples pra+an -> prAR  (mw shows prAn as alternate)
   if root == 'an':
    ans = pfx[0:-1]+'AR'
   elif root == 'in':
    ans = pfx[0:-1]+'eR'
  if ans == None:
   ans = super(PreverbSandhi,self).sandhi(s)

  if self.nR_sandhi_filter(pfx,root):
   # apply nR_sandhi
   ans = sandhi_nR(ans)

   
  if dbg:
   old = super(PreverbSandhi,self).sandhi(s)
   if ans != old: 
    print "DBG: %s. PreverbSandhi=>%s, ScharfSandhi=>%s" %(s, ans,old)
  return ans

 def nR_sandhi_filter(self,pfx,root):
  """ Returns True if nR_sandhi SHOULD be applied
      Returns False if nR_sandhi SHOULD  NOT be applied
  """
  # do_apply:  When nR_sandhi applied, the 'R' form is found in MW
  # Note that there may be other adjustments, as the root spelling is
  # as provided in PWG
  do_apply = [
   "aBipra-nakz", 
   "pari-nad", 
   "pra-nad", 
   "aBipra-nad", 
   "nis-nam", 
   "pari-nam", 
   "vipari-nam", 
   "pra-nam", 
   "aBipra-nam", 
   "pari-naS", 
   "pra-naS", 
   "atipra-naS", 
   "vipra-naS", 
   "pari-naS", 
   "pra-naS", 
   "paryA-nah", 
   "pari-nah", 
   "pra-nikz", 
   "nis-nij", 
   "pra-nij", 
   "paryA-nI", 
   "nis-nI", 
   "vinis-nI", 
   "parA-nI", 
   "pratiparA-nI", 
   "upasaMparA-nI", 
   "pari-nI", 
   "anupari-nI", 
   "pra-nI", 
   "atipra-nI", 
   "aBipra-nI", 
   "paripra-nI", 
   "vipra-nI", 
   "pra-nu", 
   "aBipra-nu", 
   "nis-nud", 
   "aBinis-nud", 
   "parA-nud", 
   "pari-nud", 
   "pra-nud", 
   "atipra-nud", 
   "anupra-nud", 
   "pari-nad", 
   "nis-nam", 
   "pari-nam", 
   "pra-nam", 
   "pari-nah", 
   "nis-nij", 
   "pra-nij", 
   "pari-nI", 
   "pra-nI", 
   "pra-nu", 
   "aBinis-nud", 
   "pra-nud", 
   "ni-snA", 
   "pari-nam", 
   "vipari-nam", 
   "pari-nI", 
   "atipra-nI",
   "saMpra-nad", 
   "saMpra-nam", 
   "saMpra-naS", 
   "saMpra-nI", 
   "saMpra-nud", 

  ]
  dont_apply = [
   "parini-as", 
   "paryanu-iz", 
   "prani-kar", 
   "prani-kunT", 
   "prani-Kad", 
   "prani-KAd", 
   "parinis-ji", 
   "pravinis-DU", 
   "pari-nakz", 
   "pra-nakz", 
   "prod-nad", 
   "vipra-nad", 
   "pari-nand", 
   "prod-nam", 
   "pari-nart", # confirmed MW, parinft
   "pra-nart", # confirmed MW , pranft
   "saMpra-nart", # implied by pra-nart
   "pra-nard",  # confirmed MW
   "pravi-naS", 
   "paryava-nah", 
   "prAva-nah", 
   "nirA-nah", 
   "pra-nah", 
   "prAva-nij", 
   "parinis-nij", 
   "pari-nid", 
   "pra-nid", 
   "paryanu-nI", 
   "antar-nI", 
   "prod-nI", 
   "vipari-nI", 
   "pari-nu", 
   "paryava-nud", 
   "pra-pinv", 
   "prani-piz", 
   "paryanu-banD", 
   "prani-Bid", 
   "prani-BU", 
   "prod-maT", 
   "prod-mad", 
   "parinis-mA", 
   "prod-mIl", 
   "pari-mnA", 
   "parinis-ci", 
   "pra-nart", 
   "nis-naS", 
   "pravi-naS", 
   "pari-nid", 
   "parinis-mA", 
   "paryanu-yuj", 
   "parinis-luW", 
   "parinis-vap", 
   "parini-vart", 
   "parinis-vA", 
   "parinis-vid", 
   "parini-SnaT", 
   "parini-sad", 
   "parini-sev", 
   "parini-sTA", 
   "parinis-sTA", 
   "aBi-snA", 
   "prati-snA", 
   "vi-snA", 
   "aBi-snih", 
   "parinis-han", 
   "pari-hnu"
  ]
  test = pfx + '-' + root
  if test in do_apply:
   return True
  if test in dont_apply:
   return False
  # anything not in one of the list: assume not to apply nR_sandhi
  return False

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
