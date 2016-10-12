echo "preverb1..."
python preverb1.py ../../../Cologne_localcopy/pw/pwtxt/pw.txt ../../../Cologne_localcopy/pw/pwxml/xml/pwhw2.txt  preverb1.txt > preverb1_log.txt
echo "preverb1a..."
python preverb1a.py preverb1.txt preverb1a.txt > preverb1a_log.txt
echo "preverb1b..."
python preverb1b.py preverb1a.txt verb_step0a.txt preverb1b_mw.txt preverb1b_notmw.txt
cp ../PW/PWehw3.txt PWehw3.txt
echo "compare Preverb with ehw3.txt"
python compare.py preverb1a.txt PWehw3.txt compare.txt
