"""updateByLine.py  Begun Apr 10, 2014
 This program is intended to be rather general.
 The 'changein' file consists of a sequence of line pairs:
 nn old old-text
 nn new new-text
 nn is the line number (starting at 1) in the input vcp file.
 'old' and 'new' are fixed.
 old-text should be identical to the text of line nn in input vcp file.
 new-text is the replacement for line nn, written to the output vcp file.
 'changein' file should be utf-8 encoded.
 Nov 6, 2014. comment lines begin with semicolon
 
"""
#

import re,sys
import codecs
class Change(object):
 def __init__(self,n,oldline,newline):
  self.n = n
  m = re.search(r'^([0-9]+) old (.*)$',oldline)
  m1 = re.search(r'^([0-9]+) new (.*)$',newline)
  if (not m) or (not m1):
   print 'Change error(1) @ line %s:' % n
   out= 'oldline=%s' % oldline
   print out.encode('utf-8')
   out= 'newline=%s' % newline
   print out.encode('utf-8')
   exit(1)
  nold = m.group(1)
  m = re.search(r'^([0-9]+) old (.*)$',oldline)
  oldtext = m.group(2)
  nnew = m1.group(1)
  newtext = m1.group(2)
  if nold != nnew:
   print 'Change error(2) @ line %s:' % n
   print 'nold(%s) != nnew(%s)' % (nold,nnew)
   out= 'oldline=%s' % oldline
   print out.encode('utf-8')
   out= 'newline=%s' % newline
   print out.encode('utf-8')
   exit(1)   
  if (not m) or (not m1):
   print 'Change error(2) @ line %s:' % n
   out= 'oldline=%s' % oldline
   print out.encode('utf-8')
   out= 'newline=%s' % newline
   print out.encode('utf-8')
   exit(1)
  self.lnumstr = nold # same as nnew
  self.oldtext = oldtext
  self.newtext = newtext

def init_changein(changein ):
 changes = [] # ret
 f = codecs.open(changein,encoding='utf-8',mode='r')
 n = 0
 sep='XXXX'
 for line in f:
  line = line.rstrip()
  if line.startswith(';'): # Nov 6, 2014, comment line
   continue
  n = n + 1
  if (n % 2) == 1:
   oldline = line
  else:
   newline = line
   chgrec = Change(n-1,oldline,newline)
   changes.append(chgrec)
 f.close()
 if (n % 2) != 0:
  print "ERROR init_changein: Expected EVEN number of lines in",changein
  exit(1)
 return changes
def update(filein,changein,fileout):
 # determine change structure from changein file
 changes = init_changein(changein)
 # initialize input records
 f = codecs.open(filein,encoding='utf-8',mode='r')
 recs = [line.rstrip('\n\r') for line in f]
 f.close()
 # process change records
 for change in changes:
  lnum = int(change.lnumstr)
  irec = lnum - 1 # since lnum assumed to start at 1
  oldrec = recs[irec]
  if oldrec != change.oldtext:
   print "CHANGE ERROR: Old mismatch line %s of %s" %(change.n,changein)
   print "Change record lnum =",lnum
   out = "Change old text:\n%s" % change.oldtext
   print out.encode('utf-8')
   out = "Change old input:\n%s" % oldrec
   print out.encode('utf-8')
   out = "line from %s:" % filein
   print out.encode('utf-8')
   exit(1)
  recs[irec] = change.newtext
 # write all records to fileout
 fout = codecs.open(fileout,'w','utf-8')
 for rec in recs:
  fout.write("%s\n" % rec)
 fout.close()
 # write summary of changes performed
 print "%s change records processed from %s" % (len(changes),changein)
 print "%s records read from %s and written to %s" %(len(recs),filein,fileout)
 
if __name__=="__main__":
 filein = sys.argv[1]
 changein = sys.argv[2]
 fileout = sys.argv[3]
 update(filein,changein,fileout)

