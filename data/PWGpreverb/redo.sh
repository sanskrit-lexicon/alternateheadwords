echo "preverb1..."
python preverb1.py ../../orig/pwg.txt ../pwghw2.txt  preverb1.txt > preverb1_log.txt
echo "preverb1a..."
python preverb1a.py preverb1.txt preverb1a.txt > preverb1a_log.txt
echo "preverb1b..."
python preverb1b.py preverb1a.txt verb_step0a.txt preverb1b_mw.txt preverb1b_notmw.txt
