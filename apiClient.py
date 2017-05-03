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
    "appIconClick"
    ,"clicked"
]
 
counterDec=0
counterNov=0
counterOct=0
counterSept=0
counterAug=0
counterJuly=0
counterJune=0  
counterJan2017=0
counterFeb2017=0
counterMarch=0

          
URL=""
PORT=0
uname=""
password = ""
dbname=""
totalSelfieClicks=0

kioskCount = {}
posterCount = {}
kioskPosterMap = {}
scKiosk={}
appClickCount={}
selfieKiosks={}
appNames={}

streetcarList=[]
posterClickList=[]
appIconList=[]
translateList=[]
mapclickList=[]



def incJan ():
    global counterJan2017
    counterJan2017 =counterJan2017+1

def incFeb ():
    global counterFeb2017
    counterFeb2017 =counterFeb2017+1    

def incMar ():
    global counterMar2017
    counterMar2017 =counterMar2017+1

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

def updateKioskSelfie (kioskName):
    global selfieKiosks
    global totalSelfieClicks

    totalSelfieClicks=totalSelfieClicks+1
    if not kioskName in selfieKiosks:
        selfieKiosks[kioskName]=1
    else:
        selfieKiosks[kioskName] += 1

def updateKioskStreetCar(kioskName):
    global scKiosk

    if not kioskName in scKiosk:
            scKiosk[kioskName]=1
    else:
        scKiosk[kioskName] += 1

def updateAppClick(appName,kioskName):
    global appClickCount
    global appNames

    print("Updating App ", appName, " For ", kioskName)

    if not kioskName in appClickCount:
        appClickCount[kioskName]=1
    else:
        appClickCount[kioskName] += 1

   
    if not appName in appNames:
        appNames[appName]=1
    else:
        appNames[appName] += 1    


         


            

def updateIndividualCount(kioskName,posterName):
    global kioskCount
    global posterCount
    global kioskPosterMap

    if not kioskName in kioskCount:
        kioskCount[kioskName]=1
    else:
        kioskCount[kioskName] += 1

    if not posterName in posterCount:
        posterCount[posterName]=1
    else:
        posterCount[posterName] += 1

    newname = str(kioskName)+"#"+str(posterName)    
    if not newname in kioskPosterMap:
        kioskPosterMap[newname]=1
    else:
        kioskPosterMap[newname] += 1    
    
            

    

        
counterManager = {
    "2017-03" : incMar,
    "2017-02" : incFeb,
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

def getSelfieClicks():
    print ("GEtting Selfies")
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;
    query="select * FROM appIconClick WHERE appName='selfie' AND city='kc'"
    filename="selfie.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)

    print ("Calling the items ")
    items = result.items()
    print (items)

    print ("Calling the keys ")
    keys = result.keys()
    print (keys)

def getSelfieFromFile():
    print ("Getting selfie clicks from file")
    with open ("./selfie.json","r") as f:
         data=json.load(f)

    keys=data.keys()
    for key in keys:        
        value=data[key]
        lent=list(value[0])
        for lentee in lent:
            if lentee == "values":
                clicks= (data[key][0][lentee])
                print("Clicks:",clicks) 
                for click in clicks:
                    if "Bangalore" in click or "bangalore" in click:
                        print ("There is banglore kciosk selfie")
                    updateKioskSelfie(click[4])    
                            


  
    
    
def connect (qtype):
   
    
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
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
        global counterFeb2017 
        counterFeb2017=0
        global counterMar2017 
        counterMar2017=0

           
def printSelfieCharts():
    import pygal
    import operator
        
    print ("Selfie Clicked")
    sortedKiosk=sorted( selfieKiosks.items(),key=operator.itemgetter(1))
    sortedKiosk.reverse()

    import time
## dd/mm/yyyy format
    today= (time.strftime("%d/%m/%Y"))

    print (len(sortedKiosk))
    pie_chart = pygal.HorizontalBar()

    pie_chart.title = "Kiosks With Selfies Total["+str(totalSelfieClicks)+"]  "+str(today)
    total = 0
    for x in range(len(sortedKiosk)):
        pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])
        print(sortedKiosk[x][0],":",sortedKiosk[x][1])
        total += sortedKiosk[x][1]

    print("*"*60)
    print("Total selfies taken is ", total)    
    pie_chart.render_to_file ("selfies.svg")                
    
def currentMonthReport ():
    import time
## dd/mm/yyyy format
    today= (time.strftime("%m"))
    lastMonth=int(today)-1
    for click in clickBaits:
        
        
def formatOutput (report=True,selfieOnly=False):
  
    if selfieOnly == True:
        printSelfieCharts()
        return

    
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
                        # offset are any data not to be considered
                        offset = 0
                        for click in clicks:
                            if "Bangalore" in click or "bangalore" in click:
                                offset = offset +1
                              

                            if clickBait == "clicked":
                                updateIndividualCount(click[3],click[5])

                            if clickBait == "streetcarClick":
                                updateKioskStreetCar(click[3])    

                            if clickBait == "appIconClick":
                                
                                updateAppClick(click[1],click[4])   
                              
                            keys = counterManager.keys()
                            for key in keys:
                                if any (key in str(c) for c in click):
                                    counterManager.get(key,incNoop) ()
                                    break;   
                        
        print ("*" * 40 )   
        print ("Stats for ", clickBait )                      
        print ("Clicks is=",len(clicks), "offsetted=",offset,
        counterMar2017+counterFeb2017+counterJan2017+counterDec+counterNov+counterOct+counterSept+counterAug+counterJuly+counterJune)  
        print ("*" * 40  )   
        print ("Total Clicks in Mar 2017 ", counterMar2017)
        print ("Total Clicks in Feb 2017 ", counterFeb2017)                   
        print ("Total Clicks in Jan 2017 ", counterJan2017) 
        print ("Total Clicks in Dec ", counterDec) 
        print ("Total Clicks in Nov ", counterNov) 
        print ("Total Clicks in Oct ", counterOct)      
        print ("Total Clicks in September ", counterSept) 
        print ("Total Clicks in August ", counterAug) 
        print ("Total Clicks in July ", counterJuly) 
        print ("Total Clicks in June ", counterJune)   

        

        import pygal
        import calendar

        bar_chart=pygal.Bar()
        bar_chart.add(clickBait,[counterJune,counterJuly,counterAug,counterSept,counterOct,counterNov,counterDec,counterJan2017,counterFeb2017,counterMar2017])
        filename=clickBait+".svg"
        bar_chart.x_labels=["June","July","August","Sept","Oct","Nov","Dec","Jan017","Feb2017","Mar2017"]
        bar_chart.render_to_file(filename)

        import operator
         
        if clickBait == "appIconClick":
            print ("Top Icons Clicked")
            sortedKiosk=sorted( appNames.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            print (len(sortedKiosk))
            pie_chart = pygal.Pie()
            pie_chart.title = "Top 5 AppIcon Clicks"
            for x in range(5):
                 pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("appicontop.svg")     
            
            

            
        if clickBait == "streetcarClick":
            print ("Kiosk based StreetCar Clicks")
            sortedKiosk=sorted( scKiosk.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            pie_chart = pygal.Pie()
            pie_chart.title = "Top 5 StreetCar Clicks"
            for x in range(5):
                 pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("streetcartop.svg")  
            
        if clickBait == "clicked":
            print ("The individual stats")
            

            global kioskCount
            global posterCount
            global kioskPosterMap

            sortedKiosk=sorted(kioskCount.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            sortedPoster=sorted(posterCount.items(),key=operator.itemgetter(1))
            sortedPoster.reverse()
        
            sortedKioskPosterMap=sorted(kioskPosterMap.items(),key=operator.itemgetter(1))
            sortedKioskPosterMap.reverse()
        
            # top 5 
            pie_chart = pygal.Pie()
            pie_chart.title = "Top 5 Kiosk Clicks"
            for x in range(5):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("topkiosk.svg")      
        
          
            pie_chart = pygal.Pie()
            pie_chart.title = "Top 5 Poster Clicks"
            for x in range(5):
                 pie_chart.add(sortedPoster[x][0],sortedPoster[x][1])

            pie_chart.render_to_file ("topposter.svg") 
       
         

 


def run(arg):
    if arg == "full":
        loadConfig()
        connect(True)
        formatOutput()

    if arg == "output":
        formatOutput();

    if arg == "report":
        formatOutput(report=True);    

    if arg == "connect":
        connect(True)
    if arg == "configTest":
        loadConfig()   

    if arg == "selfieClick":  
        loadConfig()
        getSelfieClicks()
        getSelfieFromFile()  
        printSelfieCharts()

    if arg == "loadSelfieData":
        getSelfieFromFile()   
        printSelfieCharts() 
       
    
if __name__ == '__main__':
    import sys;
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('-m',
                        "--mode",
                        dest="mode",
                        action="store")
    args=parser.parse_args()                    
        
    if args.mode:
        print ("Arguments passed");
        run(args.mode)
    else:
        run ("output")   
   
   
