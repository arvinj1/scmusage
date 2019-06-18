#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
''' csv file outputs '''

import csv, json, sys
#if you are not using utf-8 files, remove the next line
#check if you pass the input file and output file
if sys.argv[1] is not None and sys.argv[2] is not None:
    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]
    inputFile = open(fileInput) #open json file
    outputFile = open(fileOutput, 'w') #load csv file
    data = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    output = csv.writer(outputFile) #create a csv.write
    value = data['series'][0]
    output.writerow(value['columns'])  # header row
    for row in value['values']:
        output.writerow(row) 
    
    outputFile.close()
