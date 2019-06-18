#!/bin/bash
today=$(date +%F)
echo $today
bold=$(tput bold)
normal=$(tput sgr0)
ul=$(tput sgr1)


#declare -a dirs=($(find . -type d))
declare -a dirs=('kc' 'lr' 'louisville' 'umkc' 'kci' 'kcata' 'jc')
for dir in ${dirs[@]}
do
	cd $dir
	echo `pwd`
	./report.sh a
	cd ..
done

report="SCM Usage Report"
reportName="report_${today}.txt"
echo $reportName
echo $report > $reportName
for dir in ${dirs[@]}
do
	cd $dir
	echo Report for $dir >> ../$reportName
	echo "--------------------------------"
	cat ./datausage.txt >> ../$reportName
	cat ./selfies.txt >> ../$reportName
	#cat ./uptime.txt >> ../$reportName
	cd ..
done
echo "------" >> $reportName

