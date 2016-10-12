"""compare.py
   Oct 11, 2016
   Make minor force-matches in compare.txt
"""
import sys, re
import codecs

#15071:kar:ni:nikar:31624 ##EQ kar@ni@nikar@31624@9
class Input(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line # the text
  (self.L,self.hw,self.pfx,self.pfxhw,self.linenum,self.matchstatus,self.hw1,self.pfx1,self.pfxhw1,self.linenum1,self.code1) = re.split('[:@ ]',line)

if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 fin = codecs.open(filein,'r','utf-8')
 fout = codecs.open(fileout,'w','utf-8')
 for line in fin:
  dat = Input(line)
  if dat.matchstatus == "##NEQ" and not re.sub('sa[NYRnM]','saM',dat.pfxhw) == dat.pfxhw1:
   fout.write(line)
 fin.close()
 fout.close()

