
##Identify preverbs in PWG
Oct 2016


```
python preverb1.py ../../orig/pwg.txt ../pwghw2.txt  preverb1.txt > preverb1_log.txt
The log file contains adjustments to the prefix text.

8644 prefixes found under 1209 headwords.
```
Filter method for prefix:

Lines of pwg.txt starting with regexp: `-<P>- +{#(.*?)#}`

Output of preverb1.txt has lines with 3 colon delimited fields:
* L = PWG L-number 
* hw = headword
* pfx = the prefix.

## Joining prefix and headword
This has to be done with sandhi.
For sandhi, using python code from [ScharfSandhi](https://github.com/funderburkjim/ScharfSandhi).

```
python preverb1a.py preverb1.txt preverb1a.txt > preverb1a_log.txt
```

This uses [scharfsandhi module](https://github.com/funderburkjim/ScharfSandhi/blob/master/pythonv4/scharfsandhi.py).
ScharfSandhi is subclassed to PreverbSandhi, with different results for
 some combinations of prefix and root, notably when the root spelling starts
 with 's'.  See PreverbSandhi.join() method for the precise details.

## Compare to MW roots

```
python preverb1b.py preverb1a.txt verb_step0a.txt preverb1b_mw.txt preverb1b_notmw.txt
```

The MW prefixed verbs are gathered from 
[verb_step0a.txt](https://github.com/funderburkjim/MWvlex/blob/master/step0/verb-prep4.out).
The prefixed verbs are those classified as 'K' or 'P', but this fact is
not used by preverb1b.py. 

sample record of verb-prep4.out
```
atibfh:3111:<H1>:K:<key2>ati-<root>bfh<hom>1</hom></root></key2>:
```

Various alterations are tried in order to match PWG prefixed root with
MW prefixed root.  

Currently, there are:
* 8644 preverb records, per preverb1a.txt
* 6379 records in preverb1b_mw.txt
  * 5052 of these matches involve no spelling adjustments (marked as MWSAME)
  * 1327 of these matches DO involve a spelling adjustment (marked as MWDIFF)
* 2265 records in preverb1b_notmw.txt  - The implied PWG preverb spelling,
  even with current adjustments, is not found in verb-step0a.out.
  These can be viewed as the prefixed verb forms from PWG that are not present
  in MW.

## potential errors to investigate
kar:is:iskar

There is no prefix 'is'

7250:saMjYita:aBisaMjYita:aBisaMjYitasaMjYita
 saMjYita not a verb

## compare
A similar analysis of prefixed verb headwords was done by Dhaval in the
PWG directory.

The main output is in PWGehw3.txt.

This program does a comparison of PWGehw3.txt and preverb1a.txt.

```
python compare.py preverb1a.txt ../PWG/PWGehw3.txt compare.txt
```

For some reason, there are a different number of records in the two:
* PWGehw3.txt 7090
* preverb1a.txt 8644

In compare.txt, records from the two systems are merged. There
are 8644 merged records. The merging is done on the basis of the
line number of pwg.txt at which the prefix is noticed.

Each record is marked with an additional bit of metadata:

* 8644 records written to compare.txt
* 6249 prefixed headwords in both, spellings the same
* 841 prefixed headwords in both, spellings different
* 1554 prefixed headwords only in preverb1a.txt
* 0 prefixed headwords only in PWGehw3.txt

## nR sandhi on prefixes

```
python test_nR_pfx.py preverb1a.txt test_nR_pfx.txt
```
$ python test_nR_pfx.py preverb1a.txt test_nR_pfx.txt
8644 records from preverb1a.txt
29 cases written to test_nR_pfx.txt
parini 6 pariRi (24)
parinis 11 pariRis (0)
paryanu 4 paryaRu (0)
prani 7 praRi (24)
pravinis 1 praviRis (0)

The numbers in parens are counts of the nR sandhi form that occur as
prefixes in preverb1a.txt.
