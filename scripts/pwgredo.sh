python embedded.py PWG 3
cp ../data/PWG/PWGehw3.txt ../data/PWGpreverb/PWGehw3.txt
cd ../data/PWGpreverb
python compare.py preverb1a.txt PWGehw3.txt compare.txt
python compare1.py compare.txt compare1.txt
