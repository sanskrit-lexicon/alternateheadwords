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
# Function to store regexes which require no change e.g. 'tva'
def nochange(joinedword):
	global nochangelist
	for regex in nochangelist:
		#print joinedword
		if re.search(regex,joinedword):
			return True
			break
	else:
		return None

def overlap(head,sub):
	for i in range(2,len(head)):
		if not '(' in head:
			if sub.startswith(head[-i:]): # nizkuz@kuzita
				return head+sub[i:]
				break
			elif sub.startswith(head[:i]): # aNkayati@aNkita
				return sub
				break
	else:
		return head+sub
def upasargaremoval(head,sub):
	global upasarga
	output = []
	for upa in upasarga:
		if head.startswith(upa):
			head1 = head.lstrip(upa)
			upa1 = upa
			output.append(upa1+overlap(head1,sub))
	return output

if __name__=="__main__":
	dictname = sys.argv[1]
	reHeadword = r'^<P>\(?\[?\{@(.*?)@}'
	reEmbedded = r'\{\%([^%]*)\%\}'
	knownsolutionlist = [('[aA]Ikf$','Ikf'),('antat$','at'),('[aAi]it([aA])$','it\g<1>'),('a([Aei])$','\g<1>'),('[ai]in$','in'),('[ai]I$','I'),('aI([yn])a$','I\g<1>a'),('aik([aA])$','ik\g<1>'),("[.,|']",''),('aa([mMs])$','a\g<1>'),('aIBU$','IBU'),('aAs$','As'),('aAt$','At'),('aiya$','iya'),('aAvant$','Avant'),('ae([Rn])a$','e\g<1>a'),('aAya$','Aya'),('^a([hl])am','a\g<1>am'),('man([^aAiIuUfFxXeEoO])','ma\g<1>'),('tite$','te'),('s\(z\)ka$','zka'),('aAlu$','Alu'),('^agniA','agnyA'),('^asant([KPCWTcwtkpSzs])','asat\g<1>'),('^asant([^KPCWTcwtkpSzs])','asad\g<1>'),('^aDas([KPWTwtkps])','aDaH\g<1>'),('^aDas([JBGQDjbgqd])','aDo\g<1>'),('^aDasS','aDaSS'),('^aDas([cC])','aDaS\g<1>'),('^tria','trya'),('^dvia','dvya'),('^vyoman([^v])','vyoma\g<1>'),('akf$','Ikf'),('vanvarI$','varI'),('a[(]n[)]([^aAiIuUfFxXeEoO])','a\g<1>'),('a[(]n[)]([aAiIuUfFxXeEoO])','\g<1>')]
	nochangelist = [('tva$'),('tA$'),('avant$')]
	upasarga = ['ava','ati','aDi','vy','vyA']

	"""
	print "#Step 1. Writing embedded headwords with their corresponding line in ehw0.txt"
	fin = codecs.open('../data/'+dictname+'/'+dictname+'.txt','r','utf-8')
	fout = codecs.open('../data/'+dictname+'/'+dictname+'ehw0.txt','w','utf-8')
	headword = ''
	embeddedtag = ''
	dictstart = False
	dictend = False
	counter = 0
	
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
			if len(matchembed) > 0 and not re.match('^[A-Z]',headword):
				for embeddedtag in matchembed:
					emb = re.split(r'[ ;]',embeddedtag)
					for memb in emb:
						if not re.search(r'^[^a-zA-Z0-9]*$',memb):
							print headword.encode('utf-8'), memb.encode('utf-8')
							fout.write(';'+line+'\n')
							fout.write(headword+'@'+memb+'@'+unicode(counter)+'\n')
	fin.close()
	fout.close()

	print "#Step 2. Writing embedded headwords in SLP1 in ehw1.txt"
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
			line = line.replace(u'|','')
			line = line.replace(u"'","")
			line = line.replace(u'-','')
			line = line.replace('.','')
			line = line.replace(u'¤','')
			fout1.write(line+'@'+linenum+'\n')
	fin1.close()
	fout1.close()
	"""
	
	print '#Step 3. Writing suggestions for bracket resolutions in ehw2.txt'
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
			head = re.split(' \(',head)[0]
			if head+sub in hw:
				hwmatch += 1
				fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@1\n')
			elif len(sub) >= len(head) and sub.startswith(head[:-1]) and sub in hw: #asuKa@asuKAvaha
				hwmatch += 1
				fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@1\n')
			elif len(sub) >= len(head) and sub.startswith(head[:-1]): #asuKa@asuKAvaha
				hwmatch += 1
				fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@4\n')
			else:
				trialsolution = knownsolutions(head+sub)
				overlapsolution = overlap(head,sub)
				upasargasolution = upasargaremoval(head,sub)
				if (not trialsolution == head+sub) and (trialsolution in hw):
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+trialsolution+'@'+linenum+'@2\n')
				elif (not overlapsolution == head+sub) and (overlapsolution in hw): # nizkuz@kuzita
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+overlapsolution+'@'+linenum+'@2\n')
				elif (not head+sub in upasargasolution) and len(upasargasolution)>0: # vyAkulayati@kulita
					for mem in upasargasolution:
						if mem in hw:
							hwmatch += 1
							fout2.write(head+'@'+sub+'@'+mem+'@'+linenum+'@2\n')
				elif not trialsolution == head+sub:
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+trialsolution+'@'+linenum+'@3\n')
				elif nochange(head+sub): #aSakta@tva@aSaktatva
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@5\n')
				elif not overlapsolution == head+sub:
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+overlapsolution+'@'+linenum+'@7\n')
				elif l.levenshtein(head,sub) < 2 and sub in hw: # banDya@vanDya
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@1\n')
				elif l.levenshtein(head,sub) < 2: # banDya@vanDya
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@6\n')
				else:
					fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@0\n')
			
	print hwmatch, 'subheadwords matched.'
	fin2.close()
	fout2.close()
