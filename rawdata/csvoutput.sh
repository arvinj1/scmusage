#!/bin/bash
#'''
#this one will create ALL the csv output for all the dates 

offsets=(31 28 31 30 31 30 31 31 30 31 30 31)
startdate=2018-06-01
enddate=2018-12-01
offset=86400*30

currentDateTs=$(date -j -f "%Y-%m-%d" $startdate "+%s")
endDateTs=$(date -j -f "%Y-%m-%d" $enddate "+%s")
offset=86400
declare -a dirs=('kc' 'lr' 'louisville' 'umkc' 'kci' 'kcata')

while [ "$currentDateTs" -le "$endDateTs" ]
do
  date=$(date -j -f "%s" $currentDateTs "+%Y-%m-%d")
  echo $date
  mold=$(date -j -f "%s" $currentDateTs "+%m")
  month=${mold#0}
  prev=$((month-1))
  offie=${offsets[$prev]}
  offTs=$((offie*offset))
  currentDateTs=$(($currentDateTs+$offTs))
  for dir in ${dirs[@]}
  do
	python3 ../simpleclient.py -m days -f ../config.json -d $date -c $dir -r $offie 
	done
done




