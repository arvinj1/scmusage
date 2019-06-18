#!/bin/bash

declare -a dirs=('rawdata/early2018') 
for dir in ${dirs[@]}
do
	files=`ls $dir/*.json`
	for file in ${files[@]}
	do
		echo $file
		NAME=`echo $file | cut -d '.' -f1`	
		EXT=`echo $file | cut -d '.' -f1`	
		NEWNAME=$NAME.csv
		echo $NEWNAME is filename
		python3 csvopt.py $file $NEWNAME
	done
done
