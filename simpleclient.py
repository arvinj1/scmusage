#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
# only downloads json files and converts to cvs


import json
import os
import time
import datetime
from pprint import pprint

import iso8601
import pandas as pd
from influxdb import InfluxDBClient


clickBaits = [
  "translate"
    ,"appIconClick"
    ,"clicked"

    # adding new measurements
    # new metrics only after 3/1/2017
    ,"wayfinding"
    ,"appRequest"
    ,"smsRequest"
    ,"voicesearch"
    ,"disability"
    ,"transit"
    ,"streetcarClick"
    ,"adCardClick"
]
          
URL=""
PORT=0
uname=""
password = ""
dbname=""

rangeInDays=30
ConfigFile="./config.json"
city="kc"
        
def loadConfig ():
    global URL,PORT,uname,password,dbname
    with open (ConfigFile, 'r') as configFile:
        data=json.load(configFile)
        URL = data['mongodb']['host']
        PORT = data['mongodb']['port']
        uname = data['creds']['name']
        password=data['creds']['pwd']
        dbname = data['mongodb']['db']

def getSelfieClicks():
     
    client=InfluxDBClient(host=URL, port=PORT, username=uname, password=password, ssl=True, verify_ssl=True)
    if (client == None):
        print ("Error connecting to URL");
        exit;

    global dbs
    dbs = client.get_list_database()

    # pity no error code here
    client.switch_database(city)
    
    query="select * FROM appIconClick WHERE appName='selfie' AND city='"+city+"'"
    filename="selfie.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)
    
    items = result.items()
    keys = result.keys()
    

def getSMSRequests():
    client=InfluxDBClient(host=URL, port=PORT, username=uname, password=password, ssl=True, verify_ssl=True)
    if (client == None):
        print ("Error connecting to URL");
        exit;

    global dbs
    dbs = client.get_list_database()
    # pity no error code here
    client.switch_database(city)

    query="select * FROM smsRequest WHERE city='" + city +"'"
    filename="sms.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)

    items = result.items()
    keys = result.keys()


def getQueryRange(currentMonth,customDate=False,forDate=None):
    ''' returns startDay and endDay '''
    today= int(time.strftime("%m"))
    if int(time.strftime("%d")) > 15:
        today=today+1
    else:
        pass

    year = time.strftime("%Y")
    endyear=year
    lastMonth=int(today)-1
    
    if lastMonth == 0:
        lastMonth=12
        yearint=int(year)-1
        year='0{0}'.format(yearint)[-4:]
    
    strformat='0{0}'.format(lastMonth)[-2:]
    startDay=year+"-"+strformat+"-01"
    strformat='0{0}'.format(today)[-2:]
    endDay=endyear+"-"+strformat+"-01"    

    if customDate == True:
        if forDate is None:
            d = datetime.datetime.today()
        else:
            d=datetime.datetime.strptime(forDate,"%Y-%m-%d")  
            ''' account for utc offset in etc '''
            
        startDay=d.strftime("%Y-%m-%d")
        tomorrow=d+datetime.timedelta(days=rangeInDays)
        endDay=tomorrow.strftime("%Y-%m-%d")
            
        ''' to account for negative range '''
        if startDay > endDay:
            temp=startDay
            startDay=endDay
            endDay=temp
    else:
        pass

    return startDay,endDay

    
    
        
def connect (currentMonth,customDate=False,forDate=None):
    startDay,endDay=getQueryRange(currentMonth,customDate,forDate)
    print (startDay," to ", endDay)

    #to support new influxdb 1.5
    client=InfluxDBClient(host=URL, port=PORT, username=uname, password=password, ssl=True, verify_ssl=True)
    if (client == None):
        print ("Error connecting to URL");
        exit;

    global dbs
    dbs = client.get_list_database()

    # pity no error code here
    client.switch_database(city)

    for click in clickBaits:
        if customDate == True:
            query="select * from " + click + " where city='"+city+"' and time >= '" +startDay + "' and time < '" + endDay + "'"
            filename=city+"_"+click+"_"+startDay+"_"+endDay+".json"
        
        elif currentMonth == True:
            query="select * from " + click + " where city='"+city+"' and time >= '" +startDay + "' and time < '" + endDay + "'"
            filename=city+"_"+click+"_currentMonth.json"
        
        else:
            query="select * from " + click
            filename=city+"_"+click+".json"
        
        print("Query is ",query,"")
        print("Filename is ", filename)
        result=client.query(query)
        
        with open (filename,'w') as f:
            json.dump(result.raw,f)
        

def run(arg):
    global clickBaits
    global city

    if arg == "current":
        loadConfig()
        connect(currentMonth=True)
    
    if arg == "today":
        loadConfig()
        connect(currentMonth=False,customDate=True,forDate=fordate)
        
    if arg == "days":
        loadConfig()
        connect(currentMonth=False,customDate=True,forDate=fordate)
            

    
if __name__ == '__main__':
    import sys;
    import argparse
    parser=argparse.ArgumentParser()
    
    parser.add_argument('-m',
                        "--mode",
                        dest="mode",
                        action="store")
    parser.add_argument("-c",
                        "--city",
                        dest="city",
                        action="store") 
    
    parser.add_argument("-d",
                        "--date",
                        dest="date",
                        action="store")

    parser.add_argument("-r",
                        "--rangeInDays",
                        dest="rangeInDays",
                        action="store",
                        type=int)       

    parser.add_argument("-f",
                        "--configFile",
                        dest="cfg",
                        action="store") 

    
    

                    
    args=parser.parse_args()   
    
    if args.city:
        city=args.city   
    if args.date:
        fordate=args.date  
    else:
        fordate=None 

    if args.rangeInDays:
        rangeInDays=args.rangeInDays  
        customRange=True
    
    if args.cfg:
        ConfigFile=args.cfg 

    if args.mode:
        run(args.mode)

    