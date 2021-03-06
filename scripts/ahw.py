# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 30 September 2016
Expected output:
	To find out the alternate headwords from VCP (and later on from various dictionaries)
Input:
	data/vcp/vcphw0.txt
Output:
	data/vcp/vcpahw0.txt (VCP additional Headwords)
	data/vcp/vcpahw1.txt (VCP headwords with suggestions)
Usage:
	python ahw.py dictname
	e.g.
	e.g. python ahw.py VCP
"""
import sys, re
import codecs
import datetime
import suggest as s
import hw1list as h
import levenshtein as l
import listngrams as n
# Function to remove trailinig whitespaces from a list
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output
# Hard coded list of known solutions
def knownsolutions(inputlist,headword):
	for (input, output) in inputlist:
		headword = re.sub(input,output,headword)
	return headword
# Levenshtein distance is same, but there is a group of similar orthography which helps us give it more priority. e.g. aRa(na)ka
def similarorthography(headword):
	global similarlist
	for (input, output) in similarlist:
		headword = re.sub(input,output,headword)
	return headword

class dataholder:
	global hw1, inputlist, dictname
	'Class to hold the data while manipulation'
	def __init__(self, singleline,fout):
		self.len = len(re.split('[,:-]',singleline))
		self.parts = re.split('[,:-]',singleline)
		singleline = singleline.replace(u'¤','')
		# Initialize all entries. Will fill as and when needed.
		self.pagenum, self.pageside, self.hw, self.startline, self.endline, self.newhw1, self.newhw2, self.pre, self.mid, self.post, self.decodetype, self.matchcode, self.midlen = '','','','','','','','','','',2,0,0
		if self.len == 5 and '(' in singleline:
			[self.pagenum, self.pageside, self.hw, self.startline, self.endline] = re.split('[,:-]',singleline)
			if '(' in self.hw and ')' in self.hw: # ')' in self.hw added because of entry in SKD - 1-105:arda yAtanAgatiyAcanezu . (gatO:16328,16331
				self.strippedhw = re.sub('[^a-zA-Z()| ]','',self.hw)
				trip = re.split('[(]([^)]*)[)]',self.strippedhw)
				self.pre = trip[0].strip()
				self.mid = trip[1].strip()
				self.post = trip[2].strip()
				self.midlen = len(self.mid)
				self.newhw1 = self.pre[:-self.midlen]+self.mid+self.post
				self.newhw2 = self.pre+self.mid+self.post[self.midlen:]
				if not dictname in ['mwe','ae','bor']:
					knownhw = knownsolutions(inputlist,self.hw)
				else:
					knownhw = []
				if self.midlen > 1 and (self.pre[-self.midlen:] == self.mid or self.mid == self.post[:self.midlen]): # asU(kza)kzaRa - These are mainly some errors in print / typo. Needs examination.
					fout.write('0:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif self.post == '' and self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('1:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif self.newhw1 in hw1 and l.levenshtein1(self.hw, self.newhw1, 1):
					print '1:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('1:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif len(self.pre) == 1 and len(self.mid) == 1: # u(U)rdda,a(A)hituRqika
					print '5:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('5:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif not knownhw == self.hw: # upadfzada(d)
					self.newhw1 = knownhw
					print '6:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('6:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif self.newhw2 in hw1:
					print '2:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('2:'+self.hw+':'+self.newhw2+':'+self.newhw1+':'+self.startline+':'+self.endline+'\n')
				elif similarorthography(self.pre[-self.midlen:]) == similarorthography(self.mid):
					print '7:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('7:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif similarorthography(self.post[:self.midlen]) == similarorthography(self.mid):
					print '8:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('8:'+self.hw+':'+self.newhw2+':'+self.newhw1+':'+self.startline+':'+self.endline+'\n')
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) < l.levenshtein(self.post[:self.midlen],self.mid):
					print '3:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('3:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif l.levenshtein(self.pre[-self.midlen:],self.mid) > l.levenshtein(self.post[:self.midlen],self.mid):
					print '4:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('4:'+self.hw+':'+self.newhw2+':'+self.newhw1+':'+self.startline+':'+self.endline+'\n')
				elif self.midlen <= len(self.pre) and self.pre[-len(self.mid)] == self.mid[0] and self.mid[0] in 'kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshl|': # ma(mi)hira. Consonant matching has higher priority than vowel matching.
					print '12:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('12:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif len(self.mid)==2 and self.pre[-1] == self.mid[0] and self.post=='' and re.search('[aAiIuU]',self.mid[1]): # vIruD(DA)
					self.newhw1 = self.pre[:-1]+self.mid
					print '11:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('11:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				elif len(self.pre) < len(self.mid): # u(du)qumbara. There is no enough space on left.
					print '9:'+self.hw+':'+self.newhw2+':'+self.newhw1
					fout.write('9:'+self.hw+':'+self.newhw2+':'+self.newhw1+':'+self.startline+':'+self.endline+'\n')
				elif len(self.post)>0 and len(self.post) < len(self.pre): #pawwa(tta)na. There is no enough space on right.
					print '10:'+self.hw+':'+self.newhw1+':'+self.newhw2
					fout.write('10:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
				else:
					fout.write('0:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.startline+':'+self.endline+'\n')
		
	

if __name__=="__main__":
	dictionary = sys.argv[1]
	dictname = dictionary.lower()
	print '#Step0'
	print '    Preparing list of headwords from sanhw1.txt'
	hw1 = h.hw1(dictionary)
	hw1 = triming(hw1)
	inputlist = [(r'da[(]d[)]$','d'),(r'rA[(]mA[)]m$','mAm'),(r'[(]da[)]d$','d'),(r'man[(]mA[)]$','mA'),(r'c[(]cA[)]$','cA'),(r'z[(]zA[)]$','zA'),(r'c[(]cA[)]$','cA'),(r'duH[(]du[)]','du'),(r'niH[(]ni[)]','ni'),(r'kza[(]kzya[)]','kzya'),(r'[(]zwa[)]sta','zwa'),(r'ttva[(]tva[)]','tva'),(r'rDa[(]rdDa[)]','rdDa'),(r'rda[(]rdDa[)]','rdDa'),(r'[(]tra[)]ttra','tra'),(r'ttra[(]tra[)]','tra'),(r'[(]ttra[)]tra','ttra'),(r'bBra[(]Bra[)]','Bra'),(r'bBri[(]Bri[)]','Bri'),(r'bBraM[(]BraM[)]','BraM'),(r'bBro[(]Bro[)]','Bro')]
	similarlist = [(r'[NYRnmM]','m'),(r'[rl]','l'),(r'[bv]','v'),(r'[Szs]','s'),(r'[Uu]','u'),(r'[iI]','i'),(r'[aA]','a')]
	#print '#Step1'
	#print '    Analysing', sys.argv[1], 'and writing potential entries to', sys.argv[2]
	fin0 = codecs.open('../data/'+dictname+'/'+dictname+'hw0.txt','r','utf-8')
	data0 = fin0.readlines()
	data0 = triming(data0)
	fin0.close()
	fout0 = codecs.open('../data/'+dictname+'/'+dictname+'ahw0.txt','w','utf-8')
	fout1 = codecs.open('../data/'+dictname+'/'+dictname+'ahw1.txt','w','utf-8')
	counterfirsttype = 0
	for datum0 in data0:
		dat = dataholder(datum0,fout1)
		if not dat.hw == '':
			fout0.write(dat.pagenum+','+dat.pageside+':'+dat.hw+':'+dat.startline+','+dat.endline+'\n')
	fout0.close()
