cp ../CORRECTIONS/sanhw2/sanhw2.txt data/sanhw2.txt
cd scripts
dictlist=(PD VCP SKD AP AP90)
for value in "${dictlist[@]}"
do
	echo 
	mkdir ../data/${value}
	echo "Started analysing ${value} dictionary."
	cp ../../Cologne_localcopy/${value}/${value}xml/xml/${value}hw0.txt ../data/${value}/${value}hw0.txt
	python ahw.py ${value}
	python ahw1.py ${value}
done
echo
