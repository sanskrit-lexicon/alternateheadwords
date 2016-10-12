# coding: utf-8
""" hwnorm1c.py  
   Feb 25, 2016. Initially, based on hwnorm1_v1c.py used by display
   http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/hwnorm/hwnorm1.php
   However, now considered independent.
   Jan 27, 2015
   Feb 22, 2016
   Revised hwnorm1_v1b.py so that 
   records with the same normalized spelling are put on 
   the same line of output.
"""
import re
def init(filename):
    with open(filename,'r') as f:
        ans = {}
        for x in f:
         x = x.rstrip('\r\n')
         (normkey,key,dictstr) = re.split(r':',x)
         if normkey not in ans:
          ans[normkey]=[]
         ans[normkey].append("%s:%s" %(key,dictstr))
    return ans

slp1_cmp1_helper_data = {
 'k':'N','K':'N','g':'N','G':'N','N':'N',
 'c':'Y','C':'Y','j':'Y','J':'Y','Y':'Y',
 'w':'R','W':'R','q':'R','Q':'R','R':'R',
 't':'n','T':'n','d':'n','D':'n','n':'n',
 'p':'m','P':'m','b':'m','B':'m','m':'m'
}
def slp_cmp1_helper1(m):
 #n = m.group(1) # always M
 c = m.group(2)
 nasal = slp1_cmp1_helper_data[c]
 return (nasal+c)
def normalize_key(a):
 #1. normalize so that M is used rather than homorganic nasal
 a = re.sub(r'(M)([kKgGNcCjJYwWqQRtTdDnpPbBm])',slp_cmp1_helper1,a)
 #2. normalize so that 'rxx' is 'rx' (similarly, fxx is fx)
 a = re.sub(r'([rf])(.)\2',r'\1\2',a)
 #3. ending 'aM' is 'a' (Apte)
 a = re.sub(r'aM$','a',a)
 #4. ending 'aH' is 'a' (Apte)
 a = re.sub(r'aH$','a',a)
 #4a. ending 'uH' is 'u' (Apte)
 a = re.sub(r'uH$','u',a)
 #4b. ending 'iH' is 'i' (Apte)
 a = re.sub(r'iH$','i',a)
 #5. 'ttr' is 'tr' (pattra v. patra)
 a = re.sub(r'ttr','tr',a)
 #6. ending 'ant' is 'at'
 a = re.sub(r'ant$','at',a)
 #7. 'cC' is 'C'
 a = re.sub(r'cC','C',a)
 return a

def query(sanhwd_norm):
 while True:
    keyin = raw_input('Enter hw (empty to quit): ')
    if keyin == '':
        print "bye"
        break
    normkey = normalize_key(keyin)
    if normkey not in sanhwd_norm:
        print "No match for normalized key ",normkey
    else:
        for rec in sanhwd_norm[normkey]:
            print "     ",rec

class Normkey(object):
 def __init__(self,normkey):
  self.normkey = normkey
  self.lines = []

def main():
 import sys
 filein = sys.argv[1]
 fileout = sys.argv[2]
 f = open(filein,'r')
 fout = open(fileout,'w')
 n = 0
 dnorm={}
 recsout=[]
 for line in f:
  n = n + 1
  line = line.rstrip('\r\n')
  if line.startswith(':'):
   continue # skip ':AP90
  (key,dictstr) = re.split(r':',line)
  normkey = normalize_key(key)
  if normkey in dnorm:
   rec = dnorm[normkey]
  else:
   rec = Normkey(normkey)
   recsout.append(rec)
   dnorm[normkey]=rec
  rec.lines.append(line)
 # Loop through recsout, generating output
 for rec in recsout:
  outline = ';'.join(rec.lines)
  out = '%s:%s' %(rec.normkey,outline)
  fout.write("%s\n" % out)
 #
 f.close()
 fout.close()
 print n,"lines read from",filein
 print len(recsout),"lines written to",fileout
 dups = [r for r in recsout if len(r.lines)>1]
 print len(dups),"duplicates found"

if __name__=="__main__":
 main()
