"""
python suggest.py inputword excludeddict

this gives the suggestions for possible headword based on these assumptions
1. The word starts with the first letter of input word
2. The output is sorted primarily on basis of the initmach i.e. maximum letters match on the left side. e.g. initmatch("Davala","DarA")==2 because two letters on the left side match.
3. The output is shown only for the least edit-distance. e.g. if the least possible edit-distance for a given inputword is 2, then only words whose edit-distance is 2 will be shown only.
"""
import levenshtein as lev
import hw1list as h
import sys
import re
import string
import datetime
import codecs
def timestamp():
	strtime = datetime.datetime.now()
	strtime = str(strtime)
	(date, time) = strtime.split(' ')
	return (date, time)
def initmatch(s1,s2):
	count = 0
	while len(s1) is not 0:
		if s1[0] == s2[0]:
			count += 1
			s1 = s1[1:]
			s2 = s2[1:]
		else:
			break
	return count
def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output
def suggesthw(hw1,inputword,excludeddict="None"):
	output = []
	typicalheadwords = [member for member in hw1 if (re.search('^'+inputword[0],member) and abs(len(inputword)-len(member))<2)]
	for headword in typicalheadwords:
		output.append( (headword,lev.levenshtein(inputword,headword),initmatch(inputword,headword)) )
	output = sorted(output,key=lambda x: x[2], reverse=True)
	output = sorted(output,key=lambda x: x[1])
	leasteditdistance = output[0][1]
	leastinitmatch = output[0][2]
	return [(hw,edit,init) for (hw,edit,init) in output if edit==leasteditdistance]

if __name__=="__main__":
	inputword = sys.argv[1]
	excludeddict = sys.argv[2]
	hw1 = h.hw1(excludeddict)
	hw1 = triming(hw1)
	print suggesthw(hw1,inputword,excludeddict)
	
