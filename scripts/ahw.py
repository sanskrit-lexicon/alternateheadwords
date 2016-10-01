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
class dataholder:
	global hw1
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
				trip = re.split('[(]([^)]*)[)]',self.hw)
				self.pre = trip[0]
				self.mid = trip[1]
				self.post = trip[2]
				self.midlen = len(self.mid)
				self.newhw1 = self.pre[:-self.midlen]+self.mid+self.post
				self.newhw2 = self.pre+self.mid+self.post[:-self.midlen]
				if self.post == '' and self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
				elif self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
				elif self.newhw2 in hw1:
					print '2:'+self.hw+':'+self.newhw2+':'+self.newhw1
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) < l.levenshtein(self.post[:self.midlen],self.mid):
					print '3:'+self.hw+':'+self.newhw1+':'+self.newhw2
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) > l.levenshtein(self.post[:self.midlen],self.mid):
					print '4:'+self.hw+':'+self.newhw2+':'+self.newhw1
				else:
					print '0:'+self.hw+':'+self.newhw1+':'+self.newhw2

if __name__=="__main__":
	#print '#Step0'
	#print '    Preparing list of headwords from sanhw1.txt'
	excludeddict = 'VCP'
	hw1 = h.hw1(excludeddict)
	hw1 = triming(hw1)
	#print '#Step1'
	#print '    Analysing', sys.argv[1], 'and writing potential entries to', sys.argv[2]
	fin0 = codecs.open(sys.argv[1],'r','utf-8')
	data0 = fin0.readlines()
	data0 = triming(data0)
	fin0.close()
	fout0 = codecs.open(sys.argv[2],'w','utf-8')
	counterfirsttype = 0
	for datum0 in data0:
		dat = dataholder(datum0)
		if not dat.hw == '':
			fout0.write(dat.pagenum+','+dat.pageside+':'+dat.hw+':'+dat.startline+','+dat.endline+'\n')
			if dat.decodetype == 1:
				counterfirsttype += 1
	#print counterfirsttype, 'entries have parenthesis at end'
	fout0.close()

	"""
	print '#Step2'
	print '    Analysing', sys.argv[2], 'and writing suggested output to', sys.argv[3]
	fin1 = codecs.open(sys.argv[2],'r','utf-8')
	data1 = fin1.readlines()
	data1 = triming(data1)
	fin1.close()
	fout1 = codecs.open(sys.argv[3],'w','utf-8')
	for datum1 in data1:
		dat1 = dataholder(datum1)
		print dat1.matchcode, dat1.hw, dat1.newhw
	"""