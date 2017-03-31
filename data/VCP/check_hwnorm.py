"""check_hwnorm.py
   03-30-2017  ejf
   Check generated headwords using hwnorm1c.
   hwnorm1c.txt is copied from Github repository
   https://github.com/sanskrit-lexicon/hwnorm1/tree/master/ejf/hwnorm1c
"""
import re,sys,codecs
import hwnorm1

class HWnorma(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  (self.code,self.key2,self.key1alt,self.work,self.line1,self.line2)= line.split(':')
  # compute default key1
  self.key1 = re.sub(r'\(.*?\)','',self.key2)
  # there are other adjustments for a small (20+) entries
  self.key1 = re.sub(r'[ *]+','',self.key1)
  self.key1_hwnorm = None
  self.key1alt_hwnorm = None

def init_hwnorma(filein):
 with codecs.open(filein,"r","utf-8") as f:
  #print [x for x in f if len(x.split(':')) != 6]
  recs = [HWnorma(x) for x in f]
 print len(recs),"records read from",filein
 return recs

def main(recs):
 nkey1=0
 nkey1alt=0
 for rec in recs:
  rec.key1_hwnorm = hwnorm1.find(rec.key1)
  rec.key1alt_hwnorm = hwnorm1.find(rec.key1alt)
  if rec.key1_hwnorm != None:
   nkey1 = nkey1+1
  if rec.key1alt_hwnorm != None:
   nkey1alt = nkey1alt+1
 print nkey1,"key1 found"
 print nkey1alt,"key1alt found"

def write_recs(recs1,fileout):
 with codecs.open(fileout,"w","utf-8") as f:
  status_counter = {}
  for irec,rec in enumerate(recs):
   icase = irec+1
   if (rec.key1alt_hwnorm != None):
    ok1alt = 'OK'
   else:
    ok1alt = 'NF'
   if (rec.key1_hwnorm != None):
    ok1 = 'OK'
   else:
    ok1 = 'NF'
   status = "%s,%s" %(ok1,ok1alt)
   if status == "OK,OK":
    # check for cases where key1 = alt1 and both are found
    if rec.key1 == rec.key1alt:
     status = "OK=OK"
   if status not in status_counter:
    status_counter[status]=0
   status_counter[status] = status_counter[status] + 1
   out = "Case %04d: %s : %s\n" %(icase,status,rec.line)
   f.write(out)
 for status in status_counter:
  print status,status_counter[status]

def write_recs1(recs,fileout):
 """ include details of hwnorm matches
 """
 with codecs.open(fileout,"w","utf-8") as f:
  status_counter = {}
  for irec,rec in enumerate(recs):
   icase = irec+1
   if (rec.key1alt_hwnorm != None):
    ok1alt = 'OK'
    ndicts_key1alt = rec.key1alt_hwnorm.ndicts
   else:
    ok1alt = 'NF'
    ndicts_key1alt = 0
   if (rec.key1_hwnorm != None):
    ok1 = 'OK'
    ndicts_key1 = rec.key1_hwnorm.ndicts
   else:
    ok1 = 'NF'
    ndicts_key1 = 0
   status = "%s,%s" %(ok1,ok1alt)
   if status == "OK,OK":
    # check for cases where key1 = alt1 and both are found
    if rec.key1 == rec.key1alt:
     status = "OK=OK"
   if status not in status_counter:
    status_counter[status]=0
   status_counter[status] = status_counter[status] + 1
   out = "Case %04d: %s : %s\n" %(icase,status,rec.line)
   f.write(out)
   # key1 detail
   if (rec.key1_hwnorm != None):
    line = rec.key1_hwnorm.line
    data = re.sub(r'^.*?:','',line)  # remove norm spelling
    data = data.replace(';', ' ; ')
    out = " key1: %s found (%02d) %s\n" % (rec.key1,ndicts_key1,data)
   else:
    out = ' key1: %s NF\n' % rec.key1
   f.write(out)
   # alt detail
   if (rec.key1alt_hwnorm != None):
    line = rec.key1alt_hwnorm.line
    data = re.sub(r'^.*?:','',line)  # remove norm spelling
    data = data.replace(';', ' ; ')
    out = " alt1: %s found (%02d) %s\n" % (rec.key1alt,ndicts_key1alt,data)
   else:
    out = ' alt1: %s NF\n' % rec.key1alt 
   f.write(out)
   f.write('\n')
 for status in status_counter:
  print status,status_counter[status]

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 fileout1 = sys.argv[3]
 recs = init_hwnorma(filein)
 main(recs)
 write_recs(recs,fileout)
 write_recs1(recs,fileout1)

