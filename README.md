# scmapi
apiinterface to scm

only python3 compatible no plans to support python 2

To run the content
echo "Getting the data "
python3 ../bin/apiClient.py  -m adpop2 -d "2019-06-01" -r -61 -f ../bin/config.json 

echo " Converting it to csv"

python3 ../bin/csvopt.py ./ageOfAdpost_2019-04-01-2019-06-01.json adKC04012019-06012019.csv

echo " Filering out Army "
grep "Army" ./adKC04012019-06012019.csv > armyKC04-05.csv


