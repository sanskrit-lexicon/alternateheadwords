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
	python embedded.py dictname
	e.g.
	e.g. python embedded.py STC
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
def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]
def commsubstring(head,sub):
	lcs = longest_common_substring(head,sub)
	if (lcs) > 2:
		headparts = head.split(lcs)
		subparts = sub.split(lcs)
		if len(subparts[0]) > 0 and len(subparts[1]) > 0:
			return sub
		elif len(subparts[0]) >= len(headparts[0]):
			return sub
		elif len(headparts[0]) > len(subparts[0]) and len(headparts[1]) <= len(subparts[1]):
			return headparts[0]+lcs+subparts[1]
		else:
			return headparts[0]+lcs+subparts[1]
class dataholder:
	'Class to hold the data from ehw2.txt file'
	def __init__(self, singleline):
		[self.head,self.sub,self.solution,self.line,self.code] = re.split('[@]',singleline)

def headwordembedwordregex(dict):
	if dict in ['STC']:
		reHeadword = r'^<P>\(?\[?\{@(.*?)@}'
		reEmbedded = r'\{\%([^%]*)\%\}'
	elif dict in ['PWG']:
		reHeadword = r'^<H1>000{(.*?)}1'
		reEmbedded = r'^-<P>- +{#(.*?)[ ,#]'
	elif dict in ['PW']:
		reHeadword = r'^<H1>...{(.*?)}1'
		reEmbedded = r'^<\+> \#\{(.*?)[ ,}]'
	elif dict in ['AE']:
		reHeadword = r'^<><P>{[@]([a-zA-Z]*)[,]'
		reEmbedded = r'{[@]-([a-z]+)[,]*[@]}'
	return [reHeadword,reEmbedded]
	
def dictstartendreturn(dict):
	if dict in ['STC']:
		startstring = '[Page1-1]'
		endstring = 'ADDITIONS ET CORRECTIONS'
	elif dict in ['PWG']:
		startstring = '<H>{#a#}'
		endstring = '<H1>000{hArikeyI}1{hArikeyI}'
	elif dict in ['PW']:
		startstring = 'Line ignored'
		endstring = 'PW135785'
	elif dict in ['AE']:
		startstring = '<><H>{@A.@}'
		endstring = '[Page502]'
	return [startstring,endstring]
	
if __name__=="__main__":
	dictname = sys.argv[1]
	startpoint = '1'
	colognedir = '../../Cologne_localcopy/'+dictname
	if len(sys.argv) > 2:
		startpoint = sys.argv[2]
	[reHeadword, reEmbedded] = headwordembedwordregex(dictname)
	hw = set(h.hw1())

	upasargacombinations = ['ati','atinis','atipra','ativi','ativyA','atisam','atyati','atyaBi','atyA','atyud','atyupa','aDi','aDini','aDinis','aDivi','aDyava','aDyA','aDyupa','anu','anuni','anunis','anuparA','anupari','anuparyA','anupra','anuprati','anuvi','anuvyava','anuvyA','anusam','anusampra','anUd','anvapa','anvava','anvA','apa','apani','apanis','apaparA','apaparyA','apapra','apavyA','apA','apAti','api','apipari','apod','apyati','aBi','aBini','aBinis','aBiparA','aBipari','aBiparyA','aBipra','aBivi','aBivyA','aBisamA','aBisam','aByati','aByaDi','aByanu','aByapa','aByava','aByA','aByudA','aByud','aByupa','aByupA','aByupAva','ava','avani','avA','A','utpra','udava','udA','ud','udvi','unni','upa','upani','upanis','upanyA','upapari','upaparyA','upapra','upavi','upavyA','upasaṁni','upasamA','upasam','upA','upAti','upAva','upodA','upod','upopa','duHsam','duranu','durava','durA','durud','durupa','durni','duzpari','duzpra','dus','ni','nipra','nirati','niraDi','niranu','nirapa','niraBi','niraBi','nirava','nirupA','nirvi','nivyA','nizpra','nisu','nis','nyA','parA','pari','parini','parinis','paripra','parivi','parivyA','parisam','paryaDi','paryanu','paryava','paryA','paryud','paryupa','pra','praNi','prati','pratini','pratinis','pratiparA','pratipari','pratipra','prativi','prativyA','pratisam','pratyaDi','pratyanu','pratyapa','pratyapi','pratyaBi','pratyava','pratyA','pratyudA','pratyud','pratyupa','pratyupA','pravi','pravyA','prasam','prA','prADi','prod','vi','vini','vinis','viparA','vipari','viparyA','vipra','viprati','visam','vyati','vyanu','vyanvA','vyapa','vyapA','vyaBi','vyava','vyA','vyud','vyupa','saṁvi','saṁvyava','saṁvyA','sanni','samati','samaDi','samanu','samanuvi','samanvA','samapa','samapi','samaBi','samaBivyA','samaBisam','samaBisampra','samaByava','samaByA','samaByud','samava','samava','samavA','samA','samudA','samud','samupa','samupA','sam','samparA','sampari','sampra','samprati','samprA','samprod','sampari','su','supari','suvi','susamA','svanu','svaBi','svaByA','saMpra','samupani','saṁvi','saṁvyava','saṁvyA','sanni','samati','samaDi','samanu','samanuvi','samanvA','samapa','samapi','samaBi','samaBivyA','samaBisaM','samaBisaMpra','samaByava','samaByA','samaByud','samava','samava','samavA','samA','samudA','samud','samupa','samupA','saM','saMparA','saMpari','saMpra','saMprati','saMprA','saMprod','saMpari','saMni','nirA','prani','pratyAsam','sapra','praRyA','pariRi','saMpratyA','saMnis','aBiprati','avasam','nyava','anusamA','anuvyud','Ani','praRi','saMvi','avanis','pratyaByanu','Avi','anUpa','vyatisam','pratisamA','prAva','aBisaMpra','aBiprati','upaparA','samaByati','paryupA','pratinyA','saMpravi','upaprati','upasaMparA','upasaMni','vyApa','pratiparyA','aDisam','atini','pratyaBini','aBisaMni','atyanu','anuvinis','atyava','nirupa','aByudava','anvaBi','aDipra','nizwavan','aDyud','avapra','pratyati','saMvyava','apyA','pratiparyA','anusamaBivyA','aDyud','samupasam','vyatyanu','apisam','aByupani','prABi','anvati','antarupAti','aBipratyava','anUdA','aBipratyA','samaByupa','samopa','prativipari','aBivyud','parisamA','samaBinis']
	# specific to PWG (maybe later can be extended to other dicts too.)
	upasargacombinations += ['antar','punar','saha','acCa','sama','acCA','ku','aram','astam','aByastam','paScAt','prapalA','vipalA','saMpalA','pali','upapali','vipali','pla','palA']
	knownsolutionlist = [('[aA]Ikf$','Ikf'),('antat$','at'),('[aAi]it([aA])$','it\g<1>'),('a([Aei])$','\g<1>'),('[aiA]in$','in'),('[ai]I$','I'),('aI([yn])a$','I\g<1>a'),('[aAI]ik([aA])$','ik\g<1>'),("[.,|']",''),('aa([mMs])$','a\g<1>'),('aIBU$','IBU'),('aAs$','As'),('aAt$','At'),('aiya$','iya'),('aAvant$','Avant'),('ae([Rn])a$','e\g<1>a'),('aAya$','Aya'),('^a([hl])am','a\g<1>am'),('man([^aAiIuUfFxXeEoO])','ma\g<1>'),('tite$','te'),('s\(z\)ka$','zka'),('aAlu$','Alu'),('^agniA','agnyA'),('^asant([KPCWTcwtkpSzs])','asat\g<1>'),('^asant([^KPCWTcwtkpSzs])','asad\g<1>'),('^aDas([KPWTwtkps])','aDaH\g<1>'),('^aDas([JBGQDjbgqd])','aDo\g<1>'),('^aDasS','aDaSS'),('^aDas([cC])','aDaS\g<1>'),('^tria','trya'),('^dvia','dvya'),('^vyoman([^v])','vyoma\g<1>'),('[aAIi]kf$','Ikf'),('vanvarI$','varI'),('a[(]n[)]([^aAiIuUfFxXeEoO])','a\g<1>'),('a[(]n[)]([aAiIuUfFxXeEoO])','\g<1>'),('^ap([JBGQDjbgqd])','ab\g<1>'),('janjAta$','jAta'),('aAvatI$','AvatI'),('u\(v\)I$','vI'),('vantvat$','vat'),('aIkf','Ikf'),('tl','ll'),('DAhita$','hita'),('aant$','at'),('iI$','I')]
	nochangelist = [('tva$'),('tA$'),('avant$'),('vat$')]
	upasarga = ['pra','prati','praty','api','parA','apa','pari','pary','anu','anv','ava','vi','vyati','vyA','vy','saM','sam','su','sv','ati','nir','ni','ud','ut','aDi','aDy','dur','duH','aBi','aBy','vyati','aprati','vipra']
	upasargasandhi = [('[iI]([aAuUfFxeEoO])','y\g<1>'),('[uU]([aAiIfFxeEoO])','v\g<1>'),('[aA][aA]','A'),('[iI][iI]','I'),('[uU][uU]','U'),('nis([aAiIuUfFxeEoO])','nir\g<1>'),('(pr[aAiIuUfFxXeEoOhyvrkKgGNpPbBmM]*)n','\g<1>R'),('[aA][iI]','e'),('[aA][uU]','o'),('[aA][fF]','ar'),('[aA][x]','al'),('[aA][eE]','E'),('[aA][oO]','O'),('([iu])s([WTwtSzs])','\g<1>H\g<2>'),('([iu])s([kKpP])','\g<1>z\g<2>'),('([iu])H([KPCWTcwtkpSzs][^Szs])','\g<1>s\g<2>'),('([iu])s([hyvrlJBGQDjbgqd])','\g<1>r\g<2>'),('prE','pre'),('sam([^aAiIuUfFxeEoO])','saM\g<1>'),('([uUo])[dt]([KPCWTcwtkpSzs])','\g<1>t\g<2>'),('([Uuo])[td]([cC])','\g<1>c\g<2>'),('([Uuo])[td]([jJ])','\g<1>j\g<2>'),('([Uuo])[td]([qQ])','\g<1>q\g<2>'),('tn','nn'),('[td]m','nm'),('[td]l','ll'),('^antar([KPWTwtkpSzs])','antaH\g<1>'),('^antar([cC])','antaS\g<1>'),('\(\?\)',''),('^Avisas$','Aviras'),('^prAdusas$','prAduras'),('^dus([^KPWTwtkpSzsCc])','dur\g<1>'),('^dus([^cCSzs])','duH\g<1>'),('^dus([cCS])','duS\g<1>'),('kraRd','krand'),('s([cCjJ])','S\g<1>'),('([aAiIuUfFeEoOeE])C','\g<1>cC'),('zt','zw'),('zT','zW'),('zd','zq'),('zD','zQ'),('zn','zR'),('puras([hyvrlJBGQDjbgqd])','puro\g<1>'),('tiras([hyvrlJBGQDjbgqd])','tiro\g<1>'),('[JjCc]([JBGQDjbgqd])','j\g<1>'),('[pPbB]([JBGQDjbgqd])','b\g<1>'),('[kKgG]([JBGQDjbgqd])','g\g<1>'),('[wWqQ]([JBGQDjbgqd])','q\g<1>'),('[tTdD]([JBGQDjbgqd])','d\g<1>'),]
	#upasargasandhi += [('kraRd','krand'),]
	
	if not startpoint in ['2','3','4','5']:
		print "#Step 1. Writing embedded headwords with their corresponding line in ehw0.txt"
		fin = codecs.open(colognedir+'/'+dictname+'txt/'+dictname+'.txt','r','utf-8')
		fout = codecs.open('../data/'+dictname+'/'+dictname+'ehw0.txt','w','utf-8')
		headword = ''
		embeddedtag = ''
		dictstart = False
		dictend = False
		[startstring,endstring] = dictstartendreturn(dictname)
		counter = 0
		
		for line in fin:
			counter += 1
			line = line.strip()
			if startstring in line:
				dictstart = True
			if endstring in line:
				dictend = True
			if dictstart and not dictend:
				matchheadword = re.match(reHeadword,line)
				if matchheadword:
					headword = matchheadword.group(1)
				matchembed = re.findall(reEmbedded,line)
				if len(matchembed) > 0 and not (re.match('^[A-Z]+$',headword) and dictname in ['STC']):
					for embeddedtag in matchembed:
						emb = re.split(r'[ ;,]',embeddedtag)
						for memb in emb:
							if not re.search(r'^[^a-zA-Z0-9]*$',memb):
								print headword.encode('utf-8'), memb.encode('utf-8')
								fout.write(';'+line+'\n')
								fout.write(headword+'@'+memb+'@'+unicode(counter)+'\n')
		fin.close()
		fout.close()

	if not startpoint in ['3','4','5']:
		print "#Step 2. Writing embedded headwords in SLP1 in ehw1.txt"
		fin1 = codecs.open('../data/'+dictname+'/'+dictname+'ehw0.txt','r','utf-8')
		fout1 = codecs.open('../data/'+dictname+'/'+dictname+'ehw1.txt','w','utf-8')
		for line in fin1:
			if line.startswith(';'):
				fout1.write(line)
			else:
				line = line.strip()
				if dictname in ['STC']:
					line = line.lower()
					line = t.transcoder_processString(line,'as','slp1')
				[head,sub,linenum] = line.split('@')
				line = head+'@'+sub
				line = line.strip('1234567890')
				line = line.replace(u'ç','S')
				line = line.replace(u'°','')
				line = line.replace(u',','')
				line = line.replace(u'|','')
				line = line.replace(u"'","")
				line = line.replace(u'-','')
				line = line.replace('.','')
				line = line.replace(u'¤','')
				line = line.replace(u'*','')
				fout1.write(line+'@'+linenum+'\n')
		fin1.close()
		fout1.close()
	
	if not startpoint in ['4','5']:
		print '#Step 3. Writing suggestions for bracket resolutions in ehw2.txt'
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
				if dictname in ['AE']:
					fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@0\n')
				elif str(sub) in upasargacombinations and str(dictname) in ['PWG','PW']: # PWG,PW has mostly upasarga+verb kind of stuff.
					hwmatch += 1
					fout2.write(head+'@'+sub+'@'+sub+head+'@'+linenum+'@9\n')
				elif head+sub in hw:
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
					lcs = longest_common_substring(head,sub)
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
								break
						else:
							fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@0\n')
					elif len(lcs) > 2 and commsubstring(head,sub) in hw:
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+commsubstring(head,sub)+'@'+linenum+'@2\n')
					elif len(lcs) > 2:
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+commsubstring(head,sub)+'@'+linenum+'@8\n')
					elif not trialsolution == head+sub:
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+trialsolution+'@'+linenum+'@3\n')
					elif nochange(head+sub): #aSakta@tva@aSaktatva
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@5\n')
					elif l.levenshtein(head,sub) < 2 and sub in hw: # banDya@vanDya
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@1\n')
					elif len(re.findall('([aAiIuUfFxXeEoO])',head)) <= 1 and sub in ['ti','te']: # tan@tenuH - Ignoring verbs (only one vowel identifies verbs mostly)
						hwmatch += 1
						fout2.write(head+'@'+sub+'@'+sub+'@'+linenum+'@99\n')
					elif str(dictname) in ['PWG']: # PWG has strong prediliction towards joining sub+head.
						fout2.write(head+'@'+sub+'@'+sub+head+'@'+linenum+'@10\n')
					else:
						fout2.write(head+'@'+sub+'@'+head+sub+'@'+linenum+'@0\n')
				
		print hwmatch, 'subheadwords matched.'
		fin2.close()
		fout2.close()

	if not startpoint in ['5','6']:
		print '#Step 4. Storing sandhi resolved data in ehw3.txt.'
		fin3 = codecs.open('../data/'+dictname+'/'+dictname+'ehw2.txt','r','utf-8')
		fout3 = codecs.open('../data/'+dictname+'/'+dictname+'ehw3.txt','w','utf-8')
		codelist = ['0','1','2','3','4','5','8','9','10','99']
		data = fin3.readlines()
		fin3.close()
		for line in data:
			line = line.strip()
			dat = dataholder(line)
			for (a,b) in upasargasandhi:
				if not(re.match('pra[nR]',dat.sub)):
					dat.solution = re.sub(a,b,dat.solution)
				if dat.solution in hw:
					dat.code = '1'
			fout3.write(dat.head+'@'+dat.sub+'@'+dat.solution+'@'+dat.line+'@'+dat.code+'\n')
		fout3.close()

	if not startpoint in ['6']:
		print '#Step 5. Analysis of codes.'
		fin4 = codecs.open('../data/'+dictname+'/'+dictname+'ehw3.txt','r','utf-8')
		codelist = ['0','1','2','3','4','5','8','9','10','99']
		data = fin4.readlines()
		fin4.close()
		for member in codelist:
			counter = 0
			for line in data:
				line = line.strip()
				dat = dataholder(line)
				if dat.code == member:
					counter += 1
			print 'Total', counter, 'entries with code', member
			
		
