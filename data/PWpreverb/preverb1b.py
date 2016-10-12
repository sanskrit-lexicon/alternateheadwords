"""preverb1b.py
   Oct 10, 2016
   Compare preverb1a.txt with MW prefixed verbs
"""
import sys, re
import codecs

class Preverb(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.L,self.hw,self.pfx,self.pfxhw,self.linenum) = line.split(':')
  self.mwflag = False # filled in later
  self.mwhw = None  # either self.hw, or MW spelling of self.hw

 def Mtest(self,test,mwd):
  if test in mwd:
   self.mwflag=True
   self.mwhw = test
   return True
  # Do some nasal changes
  if 'Mp' in test:
   test1 = test.replace('Mp','mp')
   if test1 in mwd:
    self.mwflag=True
    self.mwhw = test1
    return True
  if 'Nk' in test:
   test1 = test.replace('Nk','Mk')
   if test1 in mwd:
    self.mwflag=True
    self.mwhw = test1
    return True
  if 'Ng' in test:
   test1 = test.replace('Ng','Mg')
   if test1 in mwd:
    self.mwflag=True
    self.mwhw = test1
    return True
  if re.search('Y[jJcC]',test):
   test1 = re.sub(r'Y([jJcC])',r'M\1',test)
   if test1 in mwd:
    self.mwflag=True
    self.mwhw = test1
    return True
  if 'nt' in test:
   # santar <-> saMtF
   test1 = test.replace('nt','Mt')
   if test1 in mwd:
    self.mwflag=True
    self.mwhw = test1
    return True
  return False
  
 def matchmw(self,mwd):
  dbg=True
  if self.pfxhw in mwd:
   self.mwflag=True
   self.mwhw = self.pfxhw
   return
  if re.search(r'ar',self.hw):
   # this works for 'kar'-'kf' type examples, 
   hw1 = re.sub(r'ar','f',self.hw)
   test = re.sub(self.hw,hw1,self.pfxhw)
   if self.Mtest(test,mwd):
    return
   # some roots in PWG ending in 'ar' correspond to roots in MW ending in F
   hw1 = re.sub(r'ar','F',self.hw)
   test = re.sub(self.hw,hw1,self.pfxhw)
   if self.Mtest(test,mwd):
    return

  if (self.hw == 'har') and (self.pfx.endswith('d')):
   # special sandhi d+h ->D
   test = re.sub('Dar$','Df',self.pfxhw)
   if self.Mtest(test,mwd):
    return
  if self.hw == 'kalp':
   hw1='kxp'
   test = re.sub(self.hw,hw1,self.pfxhw)
   if self.Mtest(test,mwd):
    return
  if self.hw.endswith('A'):
   # change that A to E for MW spelling
   test = re.sub('A$','E',self.pfxhw)
   if self.Mtest(test,mwd):
    return
   # some (e.g. hve (others?) are spelled with 'e' in MW
   test = re.sub('A$','e',self.pfxhw)
   if self.Mtest(test,mwd):
    return
   # some (e.g. so(?)) are spelled with 'o' in MW
   test = re.sub('A$','o',self.pfxhw)
   if self.Mtest(test,mwd):
    return
  dtemp = {
   'jramB':'jfmB',
   'cUrRay':'cUrR',
   'graB':'grah',
   'caraRy':'caraRya',
   'cihnay':'cihnaya',
   'guRay':'guR',
   'gaRay':'gaR',
   'gopAy':'gopAya',
   'DUnay':'DUnaya',
   'DUpay':'DUpaya',
   'nyUNKay':'nyUNKaya',
   'pAlay':'pAl',
   'pASay':'pASaya',
   'manasy':'manasya',
   'mantray':'mantr',
   'mfgay':'mfg',
   'mokzay':'mokz',
   'arTay':'arT',
   'kaTay':'kaT',
   'KaRqay':'KaRq',
   'yantray':'yantr',
   'rUkzay':'rUkz',
   'yucC':'yuC',
   'rUpay':'rUp',
   'lakzay':'lakz',
   'liNgay':'liNg',
   'varRay':'varR',
   'vAjay':'vAjaya',
   'vAsay':'vAs',
   'viGnay':'viGnaya',
   'vfzAy':'vfzAya',
   'vraRay':'vraR',
   'Sabday':'Sabd',
   'SIlay':'SIl',
   'Sravasy':'Sravasya',
   'SlakzRay':'SlakzRaya',
   'Slokay':'Slokaya',
   'saMDay':'saMDaya',
   'sapary':'saparya',
   'saBAjay':'saBAj',
   'sAntvay':'sAntv',
   'sUcay':'sUc',
   'sUtray':'sUtr',
   'aYcay':'aYc',
   'daSasy':'daSasya',
   'miSray':'miSr',
   'mUtray':'mUtraya',
   'mudray':'mudraya',
   'asUy':'asUya',
   'kIrtay':'kIrt',
  }
  if self.hw in dtemp:
   test = self.pfxhw.replace(self.hw,dtemp[self.hw])
   if self.Mtest(test,mwd):
    return

  self.mwflag=False
  self.mwhw = None

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

class MWvlex(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.hw,self.L,self.H,self.verbcode,self.key2,self.unknown) = line.split(':')


def init_mwvlex(filein):
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(MWvlex(line,n))
 f.close()
 d = {}
 for rec in recs:
  hw = rec.hw
  if hw not in d:
   d[hw]= [] 
  d[hw].append(rec)
 return d

def write_preverbs(recs,fileout,flag):
 """ recs is array of Preverb objects
 """
 fout = codecs.open(fileout,'w')
 recs1 = [rec for rec in recs if rec.mwflag == flag]
 n = 0
 nmwsame = 0
 nmwdiff = 0
 for rec in recs1:
  L = rec.L # headword record number
  hw = rec.hw  # the headword
  pfx = rec.pfx # the preverb prefixes
  pfxhw = rec.pfxhw
  mwhw = rec.mwhw
  linenum = rec.linenum
  if flag:
   if mwhw == pfxhw:
    x = 'MWSAME'
    nmwsame = nmwsame+1
   else:
    x = 'MWDIFF'
    nmwdiff = nmwdiff + 1
   out = "%s:%s:%s:%s:%s:%s:%s" %(L,hw,pfx,pfxhw,mwhw,linenum,x)
  else:
   out = "%s:%s:%s:%s:%s" %(L,hw,pfx,pfxhw,linenum)
  fout.write(out + '\n')
  n = n + 1
 fout.close()
 print n,"records written to",fileout
 if flag:
  print nmwsame,"of these have same MW spelling and implied PWG spelling"
  print nmwdiff,"of these have different MW spelling and implied PWG spelling"

if __name__=="__main__":
 filein = sys.argv[1] # preverb1a.txt
 filein1 = sys.argv[2] # verb-step0a.txt
 fileout1 = sys.argv[3] # preverb1b_mw.txt.txt
 fileout2 = sys.argv[4] #  preverb1b_notmw.txt.txt
 preverbrecs = init_preverbs(filein)
 print len(preverbrecs),"records from",filein
 mwvlexd = init_mwvlex(filein1)
 print len(mwvlexd.keys()),"distinct headwords read from",filein1
 
 for rec in preverbrecs:
  rec.matchmw(mwvlexd)

 write_preverbs(preverbrecs,fileout1,True)
 write_preverbs(preverbrecs,fileout2,False)

