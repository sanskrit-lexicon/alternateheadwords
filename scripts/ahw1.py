# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 3 October 2016
Expected output:
	To find out the alternate headwords from VCP (and later on from various dictionaries)
	Second step after ahw.py
Input:
	data/vcp/vcpahw1.txt (VCP headwords with suggestions)
Output:
	data/vcp/vcpahw2.txt (VCP headwords with suggestions, with abnormal bigrams and trigrams removed)
Usage:
	python ahw1.py dictname
	e.g.
	e.g. python ahw.py VCP
"""
import sys, re
import codecs
import datetime
import hw1list as h
import listngrams as n
# Function to remove trailinig whitespaces from a list
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output

class secondtime:
	global bigrams, trigrams
	'Class to identify abberrant suggestions which need manual examination'
	def __init__(self,singleline,fout):
		#singleline = singleline.replace(' ','')
		[self.code,self.hw,self.newhw1,self.newhw2,self.stratline,self.endline] = re.split('[:]',singleline)
		wordbigram = set(n.ngrams(self.newhw1,2))
		wordtrigram = set(n.ngrams(self.newhw1,3))
		# Reconverting the codes which were found to have abnormal bigrams or trigrams to '0'.
		if not wordbigram.issubset(bigrams):
			print 'bigram\t', singleline, wordbigram.difference(bigrams)
			fout.write('0:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.stratline+':'+self.endline+'\n')
		elif not wordtrigram.issubset(trigrams):
			print 'trigram\t', singleline, wordtrigram.difference(trigrams)
			fout.write('0:'+self.hw+':'+self.newhw1+':'+self.newhw2+':'+self.stratline+':'+self.endline+'\n')
		else:
			fout.write(singleline+'\n')
		
	

if __name__=="__main__":
	dictionary = sys.argv[1]
	dictname = dictionary.lower()

	fin1 = codecs.open('../data/'+dictname+'/'+dictname+'ahw1.txt','r','utf-8')
	data1 = fin1.readlines()
	data1 = triming(data1)
	fin1.close()
	
	hw = n.hw
	bigrams = n.getngrams(hw,2)
	bigrams = set(bigrams)
	trigrams = n.getngrams(hw,3)
	trigrams = set(trigrams)
	print "Created bigrams and trigrams"
	print "Finding abnormal bigrams and trigrams"
	fout2 = codecs.open('../data/'+dictname+'/'+dictname+'ahw2.txt','w','utf-8')
	for datum1 in data1:
		dat2 = secondtime(datum1,fout2)
	fout2.close()
