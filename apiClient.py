#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import os
import pandas as pd
from influxdb import InfluxDBClient
import time
import iso8601
import json
from pprint import pprint

clickBaits = [
    "streetcarClick",
    "translate",
    "mapClick",
    "appIconClick",
    "clicked"
]
 
counterDec=0
counterNov=0
counterOct=0
counterSept=0
counterAug=0
counterJuly=0
counterJune=0  
counterJan2017=0
          
URL=""
PORT=0
uname=""
password = ""
dbname=""


def incJan ():
    global counterJan2017
    counterJan2017 =counterJan2017+1

def incDec ():
    global counterDec
    counterDec=counterDec+1
def incNov ():
    global counterNov
    counterNov=counterNov+1
def incOct ():
    global counterOct
    counterOct=counterOct+1
def incSept ():
    global counterSept
    counterSept=counterSept+1
def incAug ():
    global counterAug
    counterAug=counterAug+1
def incJul ():
    global counterJuly
    counterJuly=counterJuly+1
def incJun ():
    global counterJune
    counterJune=counterJune+1

def incNoop ():
    print (":Empty funcion")    
        
counterManager = {
    "2017-01" : incJan,
    "2016-12" : incDec,
    "2016-11" : incNov,
    "2016-10" : incOct, 
    "2016-09" : incSept,
    "2016-08" : incAug,
    "2016-07" : incJul, 
    "2016-06" : incJun 
};          

def loadConfig ():
    global URL,PORT,uname,password,dbname
    with open ("./config.json", 'r') as configFile:
        data=json.load(configFile)
        URL = data['mongodb']['host']
        PORT = data['mongodb']['port']
        uname = data['creds']['name']
        password=data['creds']['pwd']
        dbname = data['mongodb']['db']

  
    
def connect (qtype):
   
    
    client=InfluxDBClient(URL,PORT,uname,password,store)
    if (client == None):
        print ("Error connecting to URL");
        return;

    for click in clickBaits:
        print ("Executing ",click)
        query="select * from " + click
        filename=click+".json"
        result=client.query(query)
        
        with open (filename,'w') as f:
            json.dump(result.raw,f)
        
        print ("Calling the items ")
        items = result.items()
        print (items)

        print ("Calling the keys ")
        keys = result.keys()
        print (keys)
        
        
       
def clearCounters ():
        global counterDec
        counterDec=0
        global counterNov
        counterNov=0
        global counterOct
        counterOct=0
        global counterSept
        counterSept=0
        global counterAug
        counterAug=0
        global counterJuly
        counterJuly=0
        global counterJune
        counterJune=0  
        global counterJan2017 
        counterJan2017=0
           
           
    
def formatOutput ():
    
    for clickBait in clickBaits:
        clearCounters()

        # 2017 has started
        olditer=1
        
        filename=clickBait + ".json"
        print ("Parsing  ", clickBait)
        with open (filename,"r") as jsonfile:
            data=json.load(jsonfile)
            keys=data.keys()
            for key in keys:
                
                value=data[key]
            
                lent=list(value[0])
                
                for lentee in lent:
                    if lentee == "values":
                       
                        clicks= (data[key][0][lentee])
                        offset = 0
                        for click in clicks:
                            if "Bangalore" in click or "bangalore" in click:
                                offset = offset +1
                                #print (click)

                            keys = counterManager.keys()
                            for key in keys:
                                if any (key in str(c) for c in click):
                                    counterManager.get(key,incNoop) ()
                                    break;   
                        
        print ("*" * 40 )   
        print ("Stats for ", clickBait )                      
        print ("Clicks is=",len(clicks), "offsetted=",offset,
        counterJan2017+counterDec+counterNov+counterOct+counterSept+counterAug+counterJuly+counterJune)  
        print ("*" * 40  )                      
        print ("Total Clicks in Jan 2017 ", counterJan2017) 
        print ("Total Clicks in Dec ", counterDec) 
        print ("Total Clicks in Nov ", counterNov) 
        print ("Total Clicks in Oct ", counterOct)      
        print ("Total Clicks in September ", counterSept) 
        print ("Total Clicks in August ", counterAug) 
        print ("Total Clicks in July ", counterJuly) 
        print ("Total Clicks in June ", counterJune)   

 


def run(arg):
    if arg == "full":
        loadConfig()
        connect(True)
        formatOutput()

    if arg == "output":
        formatOutput()

    if arg == "connect":
        connect(True)
    if arg == "configTest":
        loadConfig()   
       
        
    

def main(args):
    if len(args) == 0:
        print ("No args passed");
        run("output")

        
    else:
        print ("Arguments passed");
        for arg in args:
            run(arg)
            
    
if __name__ == '__main__':
    import sys;
    main(sys.argv[1:])
   
