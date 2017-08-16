##  Further analysis of alternate headwords

This file documents further work by @funderburkjim on the alternate
headwords for VCP. 

Before proceeding with the analysis, we need to review the files

### Origin of the files

* vcpahw0.txt Lines extracted from vcphw0.txt which have parentheses.
  `0067,b:agredizizu(zU):2465,2472`   0067,b is the page,col. 2465,2472
  are the lines of the digitization comprising this headword.
* vcpahw1.txt  contains suggestions for alternates
  `7:agredizizu(zU):agredizizU:agredizizuzU:2465:2472`
   'agredizizU' is the suggested alternate
   '7' is a method or reason code by which the suggestion was constructed
   'agredizizuzU' is a *working* intermediate
* vcpahw2.txt  is a revision of vcpahw1.txt
  `with abnormal bigrams and trigrams removed`
* Files vcpahw0.txt and vcpahw1.txt are constructed from vcphw0.txt
  * within the scripts directory, `python ahw.py VCP`
  * The original construction done as part of bash script 'redo.sh'
* File vcpahw2.txt is constructed from vcpahw1.txt:
  * within the scripts directory, `python ahw1.py VCP`
  * The original construction done as part of bash script 'redo.sh'
* File vcpahw3.txt is originally a copy of vcpahw2.txt. It has been 
  subjected to some manual editing.
* File vcpahw4.txt :  Not sure of origin. Best guess: a manual revision
  of vcpahw3.txt, possibly by @funderburkjim.
* See the [readme.md](https://github.com/sanskrit-lexicon/alternateheadwords)
  for Dhaval's discussion, and in particular a description of the 
  correction codes (first field)

### comparison of the records of vcpahw1-4
For the purpose of introducing alternate headwords into the list of
headwords for vcp, the most important field of the vcpahwX.txt files 
is the 'suggested' alternate headword (third field).
A small program, forensic1.py, does this comparison for two files.
It was invoked  for vcpahw1.txt v. vcpahw2.txt,
vcpahw2.txt v. vcpahw3.txt and vcpahw3.txt v. vcpahw4.txt.
```
python forensic1.py vcpahw1.txt vcpahw2.txt  
  no difference in alternate headwords between these two.
```

```
python forensic1.py vcpahw2.txt vcpahw3.txt  > vcpahw2_3_diff.txt
  58 differences, the details in vcpahw2_3_diff.txt.
```
From the documentation mentioned above, vcpahw3 is a 'manual' adjustment
of vcpahw2.
[This comment](https://github.com/sanskrit-lexicon/alternateheadwords/issues/11#issuecomment-252474042) by Dhaval says that this manual process was carried
out for the first 300 or so of the 1740 records.

```
 python forensic1.py vcpahw3.txt vcpahw4.txt  > vcpahw3_4_diff.txt
#  14 differences, the details in vcpahw3_4_diff.txt.
```

### Correction code = 0
Dhaval states somewhere that cases with a correction code of '0' should be
viewed with suspicion.  There are 
* 126 such cases in vcpahw2
*  89 such cases in vcpahw2
*  77 such cases in vcpahw4

### hwnorm analysis of alternates
Several months ago, I did a further analysis of the alternates from
vcpahw2.  This analysis used the hwnorm1c normalized headword data from
all dictionaries.  The idea was to check whether  both key1 and key1alt 
from vcpahw2 are found in other dictionaries.

```
python check_hwnorm.py vcpahw2.txt vcpahw2_hwnorm.txt vcpahw2_hwnorm_detail.txt
```
The first output prints a status code for the presence of key1 and key1alt
in the hwnorm1c file. Representative possibilities:
```
Case 0001: OK,OK : 1:aMsa(se)BAra:aMseBAra:aMsasera:169:170
  Both aMsaBAra (key1) and aMseBAra (key2) are found.  This is a confirmation
  of aMseBAra.
  1069/1740 cases

Case 0005: OK,NF : 7:agnizvA(sva)tta:agnisvatta:agnizvAsva:2003:2015
  agnizvAtta (key1) is found, but agnisvatta (key1alt is not found).  This
  indicates suspicion of agnisvatta. Note: agnisvAtta IS found in mw.
   So the `(sva)`  is probably a typo.
  637/1740 case

Case 0224: NF,NF : 3:UrdDa(rdDva)kaca:rdDvakaca:UrdDardDva:102807:102808
  This indicates that UrdDakaca (key1) is not found, nor is `rdDvakaca` .
  Note1 : There are only 4 of these cases.
Case 0225: NF,NF : 3:UrdDa(rdDva)kaRWa:rdDvakaRWa:UrdDardDva:102809:102810
Case 0226: NF,NF : 3:UrdDa(rdDva)karmman:rdDvakarmman:UrdDardDvaan:102811:102814
Case 0228: NF,NF : 3:UrdDa(rdDva)mAna:rdDvamAna:UrdDardDva:103062:103075
  Note2 : Current lookup in VCP does not find `UrdDakaca` -- Was there a 
    subsequent correction here?

Case 0055: OK=OK : 0:abBra(Bra):abBra:abBraBra:18104:18107
  abBra is found,  but the oddity is that both key1 and key1alt are the same.
  This suggests an error situation somewhere
  30/1740 cases of this sort.

```

### vcpahw2_hwnorm_ok1.txt
File [vcpahw2_hwnorm_ok1.txt](https://github.com/sanskrit-lexicon/alternateheadwords/blob/master/data/vcp/vcpahw2_hwnorm_ok1.txt) contains the safest (most certain) cases:
  `OK,OK  and correction code!=0`
There are 1066 such cases (out of 1740).   Here we know that 
* the alternate spelling is found in some dictionary (OK,OK) 
* the alternate spelling differs from the primary spelling
* A known algorithmic step generated the alternate spelling (code !=0).

These cases can be considered ready to install as alternate spellings.


### vcpahw2_hwnorm_todo1.txt
More work needs to be done on the remaining cases 692 cases, which
are saved in [vcpahw2_hwnorm_todo1.txt](https://github.com/sanskrit-lexicon/alternateheadwords/blob/master/data/vcp/vcpahw2_hwnorm_todo1.txt)
There are  692 remaining cases.
The extraction of these cases from vcpahw2_hwnorm.txt is saved in
vcpahw2_hwnorm_todo1.txt.

Note 1:  Some of these cases may have been resolved by the manual work
done in files vcpahw3 and vcpahw4.  Tying down this prior work might
be a good first step in the analysis of the todo cases.

Note 2: In a [comment](https://github.com/sanskrit-lexicon/alternateheadwords/issues/11#issuecomment-252474003) to #11, Dhaval points out a print error.
 This will help with case 0298 in the ...todo1.txt file:
```
Case 0298: OK=OK : 0:kizkinDyA(nDyA)Dipa:kizkinDyADipa:kizkinDyAnDyA:153424:153425
```

Note 3: #17 provides a UI for correction a selection of 211 cases.
   All of these are cases where the suggested alternate is not found in
   any dictionary (thus these are a subset of the ...todo1.txt list).
   I'm not sure why all of the 637 ',NF' cases are not included in this
   selection of 212.

