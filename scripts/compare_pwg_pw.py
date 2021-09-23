# -*- coding: utf-8 -*-
"""
Author:
	Dr. Dhaval Patel, 22 September 2021
Expected output:
	Compare the suggested upasarge+verb combinations
	between PWG and PW dictionaries.
	If exact matches are found, they are most probably correct.
	Create a list of upasarga+verb combinations
	which are unique to PWG and PW.
Input:
	data/PW/PWehw3.txt and data/PWG/PWGehw3.txt
Output:
	data/PW/PW_unique_ehw.txt
	data/PWG/PWG_unique_ehw.txt
Usage:
	python compare_pwg_pw.py
"""
from __future__ import print_function
import codecs
import os

def find_unique(PWGehw3file, PWehw3file, PWGuniquefile, PWuniquefile):
	pwg = codecs.open(PWGehw3file, 'r', 'utf-8')
	pwgcomb = set()
	pwglist = []
	for lin in pwg:
		lin = lin.strip()
		[hw, upasarga, comb, linenum, code] = lin.split('@')
		pwglist.append((hw, upasarga, comb, linenum, code))
		pwgcomb.add(comb)
	pwg.close()
	pw = codecs.open(PWehw3file, 'r', 'utf-8')
	pwcomb = []
	pwlist = []
	for lin in pw:
		lin = lin.strip()
		[hw, upasarga, comb, linenum, code] = lin.split('@')
		pwlist.append((hw, upasarga, comb, linenum, code))
		pwcomb.append(comb)
	
	print("PRESENT IN PWG AND ABSENT IN PW.")
	pwguniq = codecs.open(PWGuniquefile, 'w', 'utf-8')
	for (hw, upasarga, comb, linenum, code) in pwglist:
		if comb not in pwcomb:
			if code != '1':
				lin = hw + '@' + upasarga + '@' + comb + '@' + linenum + '@' + code
				pwguniq.write(lin + '\n')
	pwguniq.close()
	print("PRESENT IN PW AND ABSENT IN PWG.")
	pwuniq = codecs.open(PWuniquefile, 'w', 'utf-8')
	for (hw, upasarga, comb, linenum, code) in pwlist:
		if comb not in pwgcomb:
			if code != '1':
				lin = hw + '@' + upasarga + '@' + comb + '@' + linenum + '@' + code
				pwuniq.write(lin + '\n')
	pwuniq.close()


if __name__ == "__main__":
	PWGehw3file = os.path.join('..', 'data', 'PWG', 'PWGehw3.txt')
	PWehw3file = os.path.join('..', 'data', 'PW', 'PWehw3.txt')
	PWGuniquefile = os.path.join('..', 'data', 'PWG', 'PWG_unique_ehw.txt')
	PWuniquefile = os.path.join('..', 'data', 'PW', 'PW_unique_ehw.txt')
	find_unique(PWGehw3file, PWehw3file, PWGuniquefile, PWuniquefile)
