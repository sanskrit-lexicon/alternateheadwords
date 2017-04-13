""" extract_detail.py
  04-13-2017 ejf
  Usage:
  python extract_detail.py test.txt temp_test_hwnorm_detail.txt
"""
import codecs,re,sys
import subprocess

def prepare(filein,fileout):
 # slurp lines into filein
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 # remove initial part of each line
 newlines=[]
 for line in lines:
  newline = re.sub(r'^Case [0-9]+:.*?: *','',line)
  newlines.append(newline)
 # write altered lines
 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line+'\n')
 print len(lines),"records read from",filein
 print len(lines),"converted records written to",fileout

def detail(filein,fileout1):
 fileout = "temp_prep_test_hwnorm.txt" # not of interest
 cmd = "python check_hwnorm.py %s %s %s"%(filein,fileout,fileout1)
 args = cmd.split()
 subprocess.call(args)

if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 # convert input (test.txt) to format of vcpahw1.txt
 # and write to a temporary file
 filetemp = "temp_prep_%s" %filein
 prepare(filein,filetemp)
 # Use check_hwnorm.py to get output
 detail(filetemp,fileout)
