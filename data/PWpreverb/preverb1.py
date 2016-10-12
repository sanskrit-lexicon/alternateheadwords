# -*- coding: utf-8 -*-
"""preverb1.py
   Oct 6, 2016
   Filter pwg.txt for preverbs
   Identifed as line starting with -<P>- {#...#}
   e.g., under nI, -<P>- {#ati#}
   
"""
import sys, re
import codecs

class Hwrec(object):
 def __init__(self,line,n):
  line = line.rstrip('\r\n')
  self.line = line # the text
  self.n = n # integer line number within file (starting at 1)
  (self.pageref,self.hwslp,self.linenum12) = re.split(r':',line)
  # next required for use in slp_cmp
  (self.linenum1,self.linenum2) = re.split('[,]',self.linenum12)
  self.lnum1 = int(self.linenum1)
  self.lnum2 = int(self.linenum2)
  self.pfxes = []

def init_hwrecs(filein):
 #f = codecs.open(filein,encoding='utf-8',mode='r')
 # filein is ascii file (pwhw2.txt)
 # read it as Ascii so slp_cmp string.translate works
 f = codecs.open(filein,mode='r') 
 recs = [] 
 n = 0 # count of lines in file
 for line in f:
  n = n + 1
  recs.append(Hwrec(line,n))
 f.close()
 return recs

def adjust_pfx(p):
 # remove comma and following.  
 # Several hunder instances. The material after ',' appears to be 
 # usage instances
 q = re.sub(r',.*$','',p) 
 q = re.sub(r'\(.*$','',q) 
 q = re.sub(r'[=].*$','',q) 
 q = q.strip() # remove whitespace
 #q1 = re.sub(r'[^A-Za-z]','?',q)
 #assert q == q1,"adjust_pfx: unknown letters: %s"%p
 q1 = re.sub(r'[^A-Za-z]','',q)
 return q1

def preverb1(hwrecs,vrecs):
 recs=[]
 for hwrec in hwrecs:
  idx1 = hwrec.lnum1-1
  idx2 = hwrec.lnum2-1
  pfxes=[]
  for idx in xrange(idx1,idx2+1):
   line = vrecs[idx]
   #m = re.search(r'^-<P>- +{#(.*?)#}',line) # PWG
   m = re.search(r'^<\+> \#\{(.*?)[ ,}]',line) # PW
   if not m:
    continue
   pfx = m.group(1)
   pfxes.append((pfx,idx+1))
  if len(pfxes)>0:
   hwrec.pfxes = pfxes
   recs.append(hwrec)
 return recs

def write_preverbs(recs,fileout):
 """ recs is array of Hwrec objects
 """
 fout = codecs.open(fileout,'w','utf-8')
 n = 0
 nadj=0
 for hwrec in recs:
  L = hwrec.n # headword record number
  key1 = hwrec.hwslp  # the headword
  pfxes = hwrec.pfxes # the preverb prefixes
  for (pfx0,linenum) in pfxes:
   #print key1, pfx0.encode('utf-8')
   pfx = adjust_pfx(pfx0)    
   out = "%s:%s:%s:%s" %(L,key1,pfx,linenum)
   fout.write(out + '\n')
   n = n + 1
   if pfx != pfx0:
    nadj = nadj+1
    outadj = "ADJUST %03d: %s:%s:%s:%s => %s" %(nadj,L,key1,linenum,pfx0,pfx)
    print outadj.encode('utf-8')
 fout.close()
 print n,"records written to",fileout

if __name__=="__main__":
 filein = sys.argv[1] # xxx.txt  (xxx is dictcode, lower-case)
 filein1 = sys.argv[2] # xxxhw2.txt
 fileout = sys.argv[3] #
 hwrecs = init_hwrecs(filein1)
 print len(hwrecs),"records from",filein1
 vrecs = []
 with codecs.open(filein,'r','utf-8') as f:
  vrecs=[line.rstrip('\r\n') for line in f]
 print len(vrecs),"records read from",filein
 recs = preverb1(hwrecs,vrecs)
 print len(recs),"filtered"
 # output
 write_preverbs(recs,fileout)
