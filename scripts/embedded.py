# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 06 October 2016
Expected output:
	To find out the embedded headwords from STC (and later on from various dictionaries). See sanskrit-lexicon/alternateheadwords issue 5
Input:
	data/STC/stc.txt
Output:
	data/STC/STCehw0.txt (STC embedded Headwords)
	data/STC/STCehw1.txt (STC headwords with suggestions)
Usage:
	python ahw.py dictname
	e.g.
	e.g. python ahw.py STC
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

reHeadword = r'^<P>\(?\[?\{@(.*?)@}'
reEmbedded = r'[{][%](.*?)[%][}]'

if __name__=="__main__":
	dictname = sys.argv[1]
	fin = codecs.open('../data/'+dictname+'/'+dictname+'.txt','r','utf-8')
	fout = codecs.open('../data/'+dictname+'/'+dictname+'ehw.txt','w','utf-8')
	headword = ''
	embeddedtag = ''
	dictstart = False
	dictend = False
	for line in fin:
		line = line.strip()
		if '[Page1-1]' in line:
			dictstart = True
		if 'ADDITIONS ET CORRECTIONS' in line:
			dictend = True
		if dictstart and not dictend:
			matchheadword = re.match(reHeadword,line)
			if matchheadword:
				headword = matchheadword.group(1)
			matchembed = re.search(reEmbedded,line)
			if matchembed:
				embeddedtag = matchembed.group(1)
				print headword.encode('utf-8'), embeddedtag.encode('utf-8')
				fout.write(headword+':'+embeddedtag+'\n')
	fin.close()
	