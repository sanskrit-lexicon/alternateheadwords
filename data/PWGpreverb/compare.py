"""compare.py
   Oct 10, 2016
   Compare preverb1a.txt and Dhaval's PWG/PWGehw3.txt
"""
import sys, re
import codecs

class Preverb(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.L,self.hw,self.pfx,self.pfxhw,self.linenum) = line.split(':')

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

class PWGehw3(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n
  (self.hw,self.pfx,self.pfxhw,self.linenum,self.code) = line.split('@')

class Merge(object):
 def __init__(self,linenum):
  self.linenum = linenum
  self.preverb = None
  self.pwgehw3 = None
 def update(self,rec):
  if isinstance(rec,Preverb):
   self.preverb = rec
  else:
   self.pwgehw3 = rec


def fmerge(rec):
 lnum = int(rec.linenum)
 if isinstance(rec,Preverb):
  icode = 1
 else:
  icode = 2
 return (lnum*10) + icode

def merge(preverbrecs,pwgehw3recs):
 """ Assume both are sorted by the 'linenum' field, which is an int
 """
 recs = [] # list of Merge records
 recs1 = preverbrecs
 recs2 = pwgehw3recs
 recsboth = recs1 + recs2
 recsboth.sort(key=fmerge)
 print len(recsboth)
 lnum0=None
 for recboth in recsboth:
  lnum = int(recboth.linenum)
  if lnum != lnum0:
   rec = Merge(lnum)
   recs.append(rec)
   lnum0 = lnum
  rec.update(recboth)
 print len(recs),"merged records"
 return recs

def init_pwgehw3(filein):
 #f = codecs.open(filein,encoding='utf-8',mode='r')
 # filein is ascii file (pwhw2.txt)
 # read it as Ascii so slp_cmp string.translate works
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(PWGehw3(line,n))
 f.close()
 return recs

def writemerge(allrecs,fileout,filein,filein1):
 f = codecs.open(fileout,"w")
 n = 0
 nsame = 0
 ndiff = 0
 n1only = 0
 n2only = 0
 for allrec in allrecs:
  n = n + 1
  rec1 = allrec.preverb
  rec2 = allrec.pwgehw3
  if rec1 and rec2:
   lnum = rec1.linenum
   if rec1.pfxhw == rec2.pfxhw:
    nsame = nsame + 1
    compcode = 'SAME'
    out = rec1.line + ' ##EQ ' + rec2.line 
   else:
    ndiff = ndiff + 1
    out = rec1.line + ' ##NEQ ' + rec2.line 
  elif rec1:
   out = rec1.line + ' ##NA ' 
   n1only = n1only + 1
  else:
   out = 'NA## ' + rec2.line
   n2only = n2only + 1
  f.write(out+'\n')
 f.close()
 print n,"records written to",fileout
 print nsame,"prefixed headwords in both, spellings the same"
 print ndiff,"prefixed headwords in both, spellings different"
 print n1only,"prefixed headwords only in",filein
 print n2only,"prefixed headwords only in",filein1

if __name__=="__main__":
 filein = sys.argv[1] # preverb1a.txt
 filein1 = sys.argv[2] # PWGehw3.txt
 fileout = sys.argv[3] # compare.txt
 preverbrecs = init_preverbs(filein)
 print len(preverbrecs),"records from",filein

 pwgehw3recs = init_pwgehw3(filein1)
 print len(pwgehw3recs),"records from",filein1
 allrecs = merge(preverbrecs,pwgehw3recs)
 writemerge(allrecs,fileout,filein,filein1)
