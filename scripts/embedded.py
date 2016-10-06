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
	data/STC/STCehw1.txt (STC headwords in SLP1)
	data/STC/STCehw2.txt (STC headwords in SLP1, with suggestions)
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
#import listngrams as n
import transcoder as t
# Function to remove trailinig whitespaces from a list
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output

# Function to find patterns in the headword and subheadwordtag to enable its joining.
def knownsolutions(joinedword):
	global knownsolutionlist
	result = joinedword
	for (regex,replaceregex) in knownsolutionlist:
		result = re.sub(regex,replaceregex,result)
	return result

if __name__=="__main__":
	dictname = sys.argv[1]
	reHeadword = r'^<P>\(?\[?\{@(.*?)@}'
	reEmbedded = r'\{\%([^%]*)\%\}'
	knownsolutionlist = [('aIkf$','Ikf'),('antat$','at'),('[aAi]ita$','ita'),('a([Ae])$','\g<1>'),('ain$','in'),('aI$','I'),('aI([yn])a$','I\g<1>a'),('aik([aA])$','ik\g<1>')]
	"""
	fin = codecs.open('../data/'+dictname+'/'+dictname+'.txt','r','utf-8')
	fout = codecs.open('../data/'+dictname+'/'+dictname+'ehw0.txt','w','utf-8')
	headword = ''
	embeddedtag = ''
	dictstart = False
	dictend = False
	counter = 0
	print re.findall(reEmbedded,"<P>{%°kalpana1-%} f. assignation d'une part (d'he4ri|tage); {%°prakalpana1-%}")
	
	for line in fin:
		counter += 1
		line = line.strip()
		if '[Page1-1]' in line:
			dictstart = True
		if 'ADDITIONS ET CORRECTIONS' in line:
			dictend = True
		if dictstart and not dictend:
			matchheadword = re.match(reHeadword,line)
			if matchheadword:
				headword = matchheadword.group(1)
			matchembed = re.findall(reEmbedded,line)
			if len(matchembed) > 0:
				for embeddedtag in matchembed:
					emb = re.split(r'[ ;]',embeddedtag)
					for memb in emb:
						if not re.search(r'^[^a-zA-Z0-9]*$',memb):
							print headword.encode('utf-8'), memb.encode('utf-8')
							fout.write(';'+line+'\n')
							fout.write(headword+'@'+memb+'@'+unicode(counter)+'\n')
	fin.close()
	fout.close()

	fin1 = codecs.open('../data/'+dictname+'/'+dictname+'ehw0.txt','r','utf-8')
	fout1 = codecs.open('../data/'+dictname+'/'+dictname+'ehw1.txt','w','utf-8')
	for line in fin1:
		if line.startswith(';'):
			fout1.write(line)
		else:
			line = line.strip()
			line = line.lower()
			line = t.transcoder_processString(line,'as','slp1')
			[head,sub,linenum] = line.split('@')
			line = head+'@'+sub
			line = line.strip('1234567890')
			line = line.replace(u'ç','S')
			line = line.replace(u'°','')
			line = line.replace(u'-','')
			line = line.replace('.','')
			fout1.write(line+'@'+linenum+'\n')
	fin1.close()
	fout1.close()
	"""
	
	hw = set(h.hw1())
	fin2 = codecs.open('../data/'+dictname+'/'+dictname+'ehw1.txt','r','utf-8')
	fout2 = codecs.open('../data/'+dictname+'/'+dictname+'ehw2.txt','w','utf-8')
	hwmatch = 0
	for line in fin2:
		if line.startswith(';'):
			pass
		else:
			line = line.strip()
			[head,sub,linenum] = line.split('@')			
			if head+sub in hw:
				hwmatch += 1
				fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@1\n')
			else:
				trialsolution = knownsolutions(head+sub)
				if (not trialsolution == head+sub) and (trialsolution in hw):
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+trialsolution+'@'+linenum+'@2\n')
				elif not trialsolution == head+sub:
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+trialsolution+'@'+linenum+'@3\n')
				else:
					fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@0\n')
			
	print hwmatch, 'subheadwords found in sanhw1.'
	fin2.close()
	fout2.close()
