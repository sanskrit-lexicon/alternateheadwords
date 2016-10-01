# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 30 September 2016
Expected output:
	To find out the alternate headwords from VCP (and later on from various dictionaries)
Input:
	data/vcp/vcphw0.txt
Output:
	data/vcp/vcpahw.txt (VCP additional Headwords)
Usage:
	python ahw.py inputfile outputfile
	e.g.
	python ahw.py ../data/vcp/vcphw0.txt ../data/vcp/vcpahw0.txt ../data/vcpahw1.txt
"""
import sys, re
import codecs
import datetime
import suggest as s
import hw1list as h
import levenshtein as l
# Function to remove trailinig whitespaces from a list
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output
def knownsolutions(inputlist,headword):
	for (input, output) in inputlist:
		headword = re.sub(input,output,headword)
	return headword
class dataholder:
	global hw1, fout, inputlist
	'Class to hold the data while manipulation'
	def __init__(self, singleline):
		self.len = len(re.split('[,:]',singleline))
		self.parts = re.split('[,:]',singleline)
		# Initialize all entries. Will fill as and when needed.
		self.pagenum, self.pageside, self.hw, self.startline, self.endline, self.newhw1, self.newhw2, self.pre, self.mid, self.post, self.decodetype, self.matchcode, self.midlen = '','','','','','','','','','',2,0,0
		if self.len == 5 and '(' in singleline:
			[self.pagenum, self.pageside, self.hw, self.startline, self.endline] = re.split('[,:]',singleline)
			if '(' in self.hw:
				self.decodetype = 1 # Parenthesis at last
				self.strippedhw = re.sub('[^a-zA-Z()|]','',self.hw)
				trip = re.split('[(]([^)]*)[)]',self.strippedhw)
				self.pre = trip[0].strip()
				self.mid = trip[1].strip()
				self.post = trip[2].strip()
				self.midlen = len(self.mid)
				self.newhw1 = self.pre[:-self.midlen]+self.mid+self.post
				self.newhw2 = self.pre+self.mid+self.post[:-self.midlen]
				knownhw = knownsolutions(inputlist,self.hw)
				if self.post == '' and self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('1:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')
				elif self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('1:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')
				elif len(self.pre) == 1 and len(self.mid) == 1: # u(U)rdda,a(A)hituRqika
					print '5:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('5:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')
				elif not knownhw == self.hw: # upadfzada(d)
					self.newhw1 = knownhw
					print '6:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('6:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')
				elif self.newhw2 in hw1:
					print '2:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('2:'+self.hw+':'+self.newhw2+':'+self.newhw1+'\n')
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) < l.levenshtein(self.post[:self.midlen],self.mid):
					print '3:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('3:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) > l.levenshtein(self.post[:self.midlen],self.mid):
					print '4:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('4:'+self.hw+':'+self.newhw2+':'+self.newhw1+'\n')
				else:
					fout.write('0:'+self.hw+':'+self.newhw1+':'+self.newhw2+'\n')

if __name__=="__main__":
	#print '#Step0'
	#print '    Preparing list of headwords from sanhw1.txt'
	excludeddict = 'VCP'
	hw1 = h.hw1(excludeddict)
	hw1 = triming(hw1)
	inputlist = [(r'da[(]d[)]$','d'),(r'rA[(]mA[)]m$','mAm'),(r'[(]da[)]d$','d'),]
	#print '#Step1'
	#print '    Analysing', sys.argv[1], 'and writing potential entries to', sys.argv[2]
	fin0 = codecs.open(sys.argv[1],'r','utf-8')
	data0 = fin0.readlines()
	data0 = triming(data0)
	fin0.close()
	fout0 = codecs.open(sys.argv[2],'w','utf-8')
	fout = codecs.open(sys.argv[3],'w','utf-8')
	counterfirsttype = 0
	for datum0 in data0:
		dat = dataholder(datum0)
		if not dat.hw == '':
			fout0.write(dat.pagenum+','+dat.pageside+':'+dat.hw+':'+dat.startline+','+dat.endline+'\n')
			if dat.decodetype == 1:
				counterfirsttype += 1
	fout0.close()

