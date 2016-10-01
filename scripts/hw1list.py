# -*- coding: utf-8 -*-
import sys, re
import codecs
import string
from string import maketrans
import datetime

def sanhw1(excludeddict="None"):
	fin = codecs.open('../../CORRECTIONS/sanhw1/sanhw1.txt','r','utf-8');
	lines = fin.readlines()
	output = []
	for line in lines:
		line = line.strip()
		split = line.split(':')
		word = split[0]
		dicts = split[1].split(',')
		if not excludeddict in dicts:
			output.append((split[0],dicts)) # Added a tuple of (word,dicts)
	return output
def hw1(excludeddict="None"):
	headwithdicts = sanhw1(excludeddict)
	output = []
	for (word,dicts) in headwithdicts:
		output.append(word)
	return output
