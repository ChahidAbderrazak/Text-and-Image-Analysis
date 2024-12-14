#/bin/bash
clear
filename=dev/requirements_dev.txt
#### -----------------------   GET/RECTIFY THE PACKAGES  -------------------------------
pipreqs src/ --force --mode  no-pin  --savepath temp.txt
#  remove deplicate l;ines
awk '!seen[$0]++' temp.txt > $filename 
rm temp.txt

#### -----------------------   SHOW THE PACKAGES  -------------------------------
clear
echo && echo " The python packages are :" && echo 
cat $filename
echo && echo "INFO: Successfully saved requirements file in $filename"

