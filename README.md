# alternateheadwords
Prepare list of alternate headwords for all Cologne dictionaries

# Usage
sh redo.sh

# Input
This program uses DICTNAMEhw0.txt (e.g. skdhw0.txt) file from Cologne.

# Output
ahw here stands for alternateheadwords.
1. DICTNAMEahw0.txt (skdahw0.txt) - Only the lines of hw0.txt which have a bracket `( )`. Typical line is `2,144:kube(ve)raH:71062,71072`. 
2. DICTNAMEahw1.txt (skdahw1.txt) - ahw0.txt with suggestions for alternate headwords. Typical line is `3:kube(ve)raH:kuveraH:kubeveH`. Here the first entry is correction code (yet to be documented). Second entry is the given headword. Third entry is the most preferred solution. Fourth entry is less prefferred solution.
3. DICTNAMEahw2.txt (skdahw2.txt) - same as ahw1.txt, but the suggested alternate headwords which have abnormal bigrams are trigrams are reverted to code '0' of correction.

# How to analyse results.
0. Copy skdahw2.txt file manually to skdahw3.txt. (Because redo.sh generates ahw2.txt, corrections made thereto have the risk of regeneration programatically.)
1. Read skdahw3.txt line by line.
2. Each line is in the format `correctioncode:givenheadword:preferredheadword:scrap` e.g. `3:kube(ve)raH:kuveraH:kubeveH`
3. See the second entry and third member e.g. kube(ve)raH and kuveraH respectively.
4. If it is found OK, that additional headword may be incorporated. (The modality has to be decided by Jim)
5. If it is not found OK, correct the third member, and change the code to '99' - to depict that it is manually corrected.
6. Lines with '0' code need the closest examination. These are places where there was no computational suggestion possible whatsoever.


