
vcphw0.txt is from Cologne.
vcpahw0.txt is almost the same as temp_vcpahw0.txt, constructed by grep:
grep '(' vcphw0.txt > temp_vcpahw0.txt
The temp_vcpahw0.txt has two additional entries:
4276,b:paSa(za--sa):321600,321604
4276,b:paSa(za--sa):321607,321608


python check_hwnorm.py vcpahw2.txt vcpahw1_hwnorm.txt vcpahw1_hwnorm_detail.txt 


4 cases where 
 (a) key1 is non-standard:  always UrdDva
1388,a:UrdDa(rdDva)kaca:102807,102808 key1 = UrdDvakaca
1388,a:UrdDa(rdDva)kaRWa:102809,102810 key1 = UrdDvakaRWa
1388,b:UrdDa(rdDva)karmman:102811,102814 key1 = UrdDvakarmman
1391,b:UrdDa(rdDva)mAna:103062,103075 key1 = UrdDvamAna
 (b) and the 'normal' key1 is not found in any dictionary,
    e.g. UrdDakaca is not found, etc.

See readme1.md for further work on VCP alternate headwords.
