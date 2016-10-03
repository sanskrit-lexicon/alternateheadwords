# alternateheadwords
Prepare list of alternate headwords for all Cologne dictionaries

# Usage
sh redo.sh

# Input
This program uses DICTNAMEhw0.txt (e.g. skdhw0.txt) file from Cologne.

# Output
`ahw` here stands for alternateheadwords.

1. DICTNAMEahw0.txt (skdahw0.txt) - Only the lines of hw0.txt which have a bracket `( )`. Typical line is `2,144:kube(ve)raH:71062,71072`.
2. DICTNAMEahw1.txt (skdahw1.txt) - ahw0.txt with suggestions for alternate headwords. Typical line is `3:kube(ve)raH:kuveraH:kubeveH`. Here the first entry is correction code. Second entry is the given headword. Third entry is the most preferred solution. Fourth entry is less prefferred solution.
3. DICTNAMEahw2.txt (skdahw2.txt) - same as ahw1.txt, but the suggested alternate headwords which have abnormal bigrams are trigrams are reverted to code '0' of correction.

# How to analyse results.
1. Copy skdahw2.txt file manually to skdahw3.txt. (Because redo.sh generates ahw2.txt, corrections made thereto have the risk of regeneration programatically.)
2. Read skdahw3.txt line by line.
3. Each line is in the format `correctioncode:givenheadword:preferredheadword:scrap` e.g. `3:kube(ve)raH:kuveraH:kubeveH`
4. See the second entry and third member e.g. kube(ve)raH and kuveraH respectively.
5. If it is found OK, that additional headword may be incorporated. (The modality has to be decided by Jim)
6. If it is not found OK, correct the third member, and change the code to '99' - to depict that it is manually corrected.
7. Lines with '0' code need the closest examination. These are places where there was no computational suggestion possible whatsoever.

# Correction codes
When the machine gives some suggestion as to the correct alternate headword intended by resolving brackets, it gives a code to the entry.
By looking at the code, it is possible to find out the logic which resolved this bracket.
The following explanation gives a somewhat nearby explanation to this issue.

`0` - Machine couldn't identify any solution. Mostly problematic cases.

`1` - When the bracket string is superimposed on left side, the resulting word is already in sanhw1.txt (known headwords). e.g. 1:DvA(DmA)kza:DmAkza:DvADmA

`2` - When the bracket string is superimposed on right side, the resulting headword is already in sanhw1.txt (known headwords). e.g. 2:Buvanako(Sa)za:BuvanakoSa:BuvanaSaza

`3` - Edit distance for left side bracket opening is less than right side bracket opening. e.g. 3:muSa(za)likA:muzalikA:muSazakA

`4` - Edit distance for right side bracket opening is less than left side bracket opening. e.g. 4:lA(ba)vakaH:lAbakaH:bavakaH

`5` - String to the left of bracket is only one letter. Such case has strong prediliction towards left side bracket opening. e.g. 5:a(A)nEpuRa:AnEpuRa:aAEpuRa

`6` - The solution is in the list of known hand coded patterns. e.g. 6:Bakza(kzya)patrA:BakzyapatrA:BakzakzyaA. (Here kza and kzya pair is hand-coded in variable inputlist of ahw.py program).

`7` - Orthographically similar solution can be reached by opening bracket on left side. e.g. 'b' and 'v'. in 7:va(ba)halaH:bahalaH:vabalaH (Here the orthographically similar pairs are noted in variable similarlist of ahw.py program)

`8` - Orthographically similar solution can be reached by opening bracket on right side e.g. 'b' and 'v' in 8:Sa(ba)valaH:SabalaH:bavalaH. (Noted in similarlist)

`9` - Left side is lesser in length than replacement string. This prefers opening bracket on right side. e.g. 9:u(du)qumbara:udumbara:duqumbara

`10`- Right side is lesser in length than replacement string. This prefers opening bracket on left side. e.g. 10:pawwa(tta)na:pattana:pawwatta

`11` - Bracket is in the last, and can be constructed by adding a vowel to the last letter of headword. e.g. 11:puroqAS(Sa):puroqASa:puroqASSa

`12` - Edit distance is the same, but left opening has consonant matching. e.g. 12:ma(mi)hira:mihira:mamira

`13` - Edit distance is the same, but right opening has consonant matching. 

