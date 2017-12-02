#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import json
import os
import time
from pprint import pprint

import iso8601
import pandas as pd
from influxdb import InfluxDBClient

clickBaits = [
  
  "translate"
    ,"mapClick"
    ,"appIconClick"
    ,"clicked"

    # adding new measurements
    # new metrics only after 3/1/2017
    ,"wayfinding"
    
    ,"appRequest"
    ,"smsRequest"
    ,"voiceearch"
    ,"disability"
    ,"transit"
    ,"streetcarClick"
    ,"adCardClick"
]
captions = [
    "Translation Pressed"
    ,"Map Clicks"
    ,"Apps Pressed"
    ,"Smart Card Landing Pages Clicked"
    ,"Wayfinding"
    ,"App Request"
    ,"SMS Request"
    ,"Voice Search"
    ,"Disability"
    ,"Transit /StreetCar"
    ,"Streetcar"
    ,"AdCardClick"
]
graphs = ["./"+a+".png" for a in clickBaits ]

totalInteraction=0
 
counterDec=0
counterNov=0
counterOct=0
counterSept=0
counterAug=0
counterJuly=0
counterJune=0  
counterJan2017=0
counterFeb2017=0
counterMar2017=0
counterApr2017=0
counterMay=0
counterJune2017=0
counterJuly2017=0
counterAugust2017=0
counterSept2017=0
counterOct2017=0
counterNov2017=0

globalStats={}


          
URL=""
PORT=0
uname=""
password = ""
dbname=""

totalSelfieClicks=0
totalSms=0

kioskCount = {}
posterCount = {}
kioskPosterMap = {}
scKiosk={}
scKiosk2={}
appClickCount={}
selfieKiosks={}
smsKiosks={}
appNames={}
adCardCount={}

wayFindingKiosks={}
wayFTime={}

'''ad card releated info '''
adCardKioks={}

streetcarList=[]
posterClickList=[]
appIconList=[]
translateList=[]
mapclickList=[]
wayFindingList=[]

city="kc"


''' Kiosk mapping '''
kioskMap = {
"Union Station SB-North Face":   "Union Station",
"Union Station SB -North Face":  "Union Station",
"Union Station SB -South Face" : "Union Station",
"Power Light - 14th Main - SB West Face" : "P&L",
"Power Light - 14th Main - NB West Face" :"P&L",
"LIbrary - 9th Main - SB West Face":"Library",
"Power Light 14th Main - SB East Face" :"P&L",
"Financial District - 12th Grand":"Fidi",
"River Market 4th Delaware - SB East Face" : "River Market",
"River Market - 4th Delaware - SB West Face" : "River Market",
"Kauffman 16th Main - NB West Face" : "Kauffman",
"City Market - 17 E 5th St" :"City Market",
"Crossroads 19th Main - SB South Face":"Crossroads",
"Metro Center 12th Main - NB": "Metro Center",
"Crossroads 19th Main - NB West Face": "Crossroads",
"20thbaltimore":"20th&Baltimore",
"Crossroads 19th Main - NB East Face":"Crossroads",
"Library - 9th Main - NB East Face":"Library",
"Kauffman 16th Main -  SB East Face":"Kauffman",
"Kauffman 16th Main -  SB West Face":"Kauffman",
"Kauffman 16th Main - NB East Face":"Kauffman",
"No Other Pub - 1370 Grand":"No Other Pub",
"Johnny's Tavern - 13th Grand - North Face":"Jhonnys",
"Crown Center -2470 Grand - West Face":"Crown Center",
"Johnny's Tav - 13th Grand - South Face":"Jhonnys",
"Mannys - 201 SW Blvd.":"Mannys",
"LIbrary - 9th Main - SB East Face":"Library",
"Library  - 9th Main - NB West Face":"Library",
"River Market North - 3rd Grand":"River Market",
"Barney Allis -12th Wyandotte - North Face":"Barney",
"20thgrand":"20th&Grand",
"Crossroads - 19th Main - SB North Face":"Crossroads",
"Barney Allis -12th Wyandotte - South Face":"Barney",
"barneyallissouth":"Barney",
"Crown Center - 2470 Grand - East Face":"Crown",
"City Hall -12th Oak":"City Hall",
"barneysouth":"Barney",
"Convention Center - 301 W 13th":"Convention",
"Performing Arts Center":"PerformingArts",
"performingartscenter" : "PerformingArts",
"Oppenstein":"Oppenstein",
"Power Light 14th Main -NB East Face":"P&L",
"Zotac":"Zotac",
"Zotac2":"Zotac",
"bangalore KC":"Bangalore",
"bangalore":"Bangalore",
"4delawareeast":"River Market",
"Barney Allis - 12th Wyandotte - South Face":"Barney",
"dallas":"dallas",
}

# core APPS
totalStreetCar=0
totalStreetCar2=0
totalWayfinding=0
totalMulti=0

def incJan ():
    global counterJan2017
    counterJan2017 =counterJan2017+1

def incFeb ():
    global counterFeb2017
    counterFeb2017 =counterFeb2017+1    

def incMar ():
    global counterMar2017
    counterMar2017 =counterMar2017+1

def incApr ():
    global counterApr2017
    counterApr2017 =counterApr2017+1    

def incMay17 ():
    global counterMay2017
    counterMay2017 =counterMay2017+1      

def incJune17 ():
    global counterJune2017
    counterJune2017 =counterJune2017+1     

def incJuly17 ():
    global counterJuly2017
    counterJuly2017 =counterJuly2017+1          

def incAug17 ():
    global counterAugust2017
    counterAugust2017 =counterAugust2017+1    

def incSep17 ():
    global counterSept2017
    counterSept2017 =counterSept2017+1    

def incOct17 ():
    global counterOct2017
    counterOct2017=counterOct2017+1                  
      
def incNov17 ():
    global counterNov2017
    counterNov2017=counterNov2017+1                  
      


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

def updateKioskSMS(kioskNameG):
    global smsKiosks
    global totalSms
    try:
        kioskName=kioskMap[kioskNameG]

    except KeyError:
        print ("no kiosks in selfiekiosk ",kioskNameG)
        return

    totalSms+=1
    if not kioskName in smsKiosks:
            smsKiosks[kioskName]=1
    else:
        smsKiosks[kioskName] += 1


def updateKioskSelfie (kioskNameG):
    global selfieKiosks
    global totalSelfieClicks

    try:
        kioskName=kioskMap[kioskNameG]
    except KeyError:
        print ("unknonw kiosk name.",kioskNameG,"...returning")
        return

    totalSelfieClicks=totalSelfieClicks+1
    if not kioskName in selfieKiosks:
        selfieKiosks[kioskName]=1
    else:
        selfieKiosks[kioskName] += 1

def updateKioskStreetCar(kioskName):
    global scKiosk
    global totalStreetCar
    totalStreetCar+=1
    if not kioskName in scKiosk:
            scKiosk[kioskName]=1
    else:
        scKiosk[kioskName] += 1

def updateKioskTransitStreetCar(kioskName):
    global scKiosk2
    global totalStreetCar2
    totalStreetCar2+=1
    if not kioskName in scKiosk2:
            scKiosk2[kioskName]=1
    else:
        scKiosk2[kioskName] += 1
            


def updateAppClick(appNameMash,kioskName):
    global appClickCount
    global appNames

    appNameL = appNameMash.split("_")
    if len(appNameL) ==2 :
        appName=appNameL[1]
    else:
        appName=appNameL[0]

    if appName == "kcvisitorinfo":
        return    

   
    if not kioskName in appClickCount:
        appClickCount[kioskName]=1
    else:
        appClickCount[kioskName] += 1

   
    if not appName in appNames:
        appNames[appName]=1
    else:
        appNames[appName] += 1    

def updateTransit(click):
    #Sprint(click)
    pass

adMistakes=0
adClicks=0

def updateAdCount(click):
    global adMistakes
    global kioskMap
    location = click[4]
    try:
        kioskName=kioskMap[location]
    except KeyError:
        #print ("Could not find ",location)
        adMistakes+=1
        return    

    if kioskName == "":
        adMistakes+=1
        return

    global adCardKioks
    
    if not kioskName in adCardKioks:
        adCardKioks[kioskName]=1
    else:
        adCardKioks[kioskName]+=1

    global adClicks
    adClicks+=1   
            


def updateWayfindingKiosks (click):
    global wayFindingKiosks  
    global wayFTime 
    global totalWayfinding
    totalWayfinding+=1

    timeOftouch=click[0]
    location=click[3]

    
    #return

    if not location in wayFindingKiosks:
        wayFindingKiosks[location]=1
    else:
       wayFindingKiosks[location]+=1 

    if not timeOftouch in wayFTime:
        wayFTime[timeOftouch]=1
    else:
        wayFTime[timeOftouch]+=1     
            

def updateIndividualCount(kioskNameMash,posterName):
    global kioskCount
    global posterCount
    global kioskPosterMap

    kioskNameList=kioskNameMash.split("_")
    if len(kioskNameList) ==2:
        kioskName=kioskNameList[1]
    else:
        kioskName=kioskNameList[0]
        
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
    "2017-11" : incNov17,
    "2017-10" : incOct17,
    "2017-09" : incSep17,
    "2017-08" : incAug17,
    "2017-07" : incJuly17,
    "2017-06" : incJune17,
    "2017-05" : incMay17,
    "2017-04" : incApr,
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
     
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;
    query="select * FROM appIconClick WHERE appName='selfie' AND city='kc'"
    filename="selfie.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)

    
    items = result.items()
    keys = result.keys()
    
def getSelfieFromFile():
    with open ("./selfie.json","r") as f:
         data=json.load(f)

    keys=data.keys()
    for key in keys:        
        value=data[key]
        lent=list(value[0])
        for lentee in lent:
            if lentee == "values":
                clicks= (data[key][0][lentee])
                #print("Clicks:",clicks) 
                for click in clicks:
                    if "Bangalore" in click or "bangalore" in click:
                        print ("There is banglore kciosk selfie")
                    updateKioskSelfie(click[4])    
                            


  
def getSMSRequests():
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;
    query="select * FROM smsRequest WHERE city='kc'"
    filename="sms.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)

    #print ("Calling the items ")
    items = result.items()
    #print (items)

    #print ("Calling the keys ")
    keys = result.keys()
    #print (keys)

def getSMSRequestsFromFile():
    #print ("Getting sms clicks from file")
    with open ("./sms.json","r") as f:
         data=json.load(f)

    keys=data.keys()
    for key in keys:        
        value=data[key]
        lent=list(value[0])
        for lentee in lent:
            if lentee == "values":
                clicks= (data[key][0][lentee])
                #print("Clicks:",clicks) 
                for click in clicks:
                    if "Bangalore" in click or "bangalore" in click:
                        #print ("There is banglore kciosk selfie")
                        pass
                    else:
                        updateKioskSMS(click[3])        
    
def connect (currentMonth):
   
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;

    today= int(time.strftime("%m"))
    if int(time.strftime("%d")) > 15:
        today=today+1
        #print ("Added today to", today)
    else:
        pass
        #print (int(time.strftime("%d"))," is the date no addings")  

    lastMonth=int(today)-1

    year = time.strftime("%Y")
    strformat='0{0}'.format(lastMonth)[-2:]
    startDay=year+"-"+strformat+"-01"
    strformat='0{0}'.format(today)[-2:]
    endDay=year+"-"+strformat+"-01"    

    print (startDay,"to " , endDay)
    

    for click in clickBaits:
        
        if currentMonth == True:
            query="select * from " + click + " where time > '" +startDay + "' and time < '" + endDay + "'"
            filename=click+"_currentMonth.json"
        else:
            query="select * from " + click
            filename=click+".json"
        
        
        result=client.query(query)
        
        with open (filename,'w') as f:
            json.dump(result.raw,f)
        
        items = result.items()
        keys = result.keys()
        
        
       
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
        global counterApr2017
        counterApr2017=0
        global counterMay2017
        counterMay2017=0

        global counterJune2017
        counterJune2017=0

        global counterJuly2017
        counterJuly2017=0

        global counterAugust2017
        counterAugust2017=0

        global counterSept2017
        counterSept2017=0

        global counterOct2017
        counterOct2017=0

        global counterNov2017
        counterNov2017=0

           
def printSelfieCharts(textOnly=False):
    if not textOnly:
        import pygal
        
    import operator
        
    #print ("Selfie Clicked")
    sortedKiosk=sorted( selfieKiosks.items(),key=operator.itemgetter(1))
    sortedKiosk.reverse()

    import time
## dd/mm/yyyy format
    today= (time.strftime("%d/%m/%Y"))
    if not textOnly:
        pie_chart = pygal.Bar(print_values=True, print_values_position='top')
        pie_chart.title = "Kiosks With Selfies Total["+str(totalSelfieClicks)+"]  "+str(today)

    total = 0
    xaxis=[]
    yaxis=[]
    for x in range(len(sortedKiosk)):
        if x < 10:
            xaxis.append(sortedKiosk[x][0])
            yaxis.append(sortedKiosk[x][1])
                 
        total += sortedKiosk[x][1]
        print (sortedKiosk[x][0], sortedKiosk[x][1])

    if not textOnly:
        pie_chart.x_labels=xaxis
        pie_chart.add("Selfies",yaxis)
        
    print("*"*60)
    print("Total selfies taken is ", total)    
    #pie_chart.render_to_png ("selfies.png")       

def printSMSRequests():
    import pygal
    import operator
        
    print ("SMS of Selfies Clicked")
    sortedKiosk=sorted( smsKiosks.items(),key=operator.itemgetter(1))
    sortedKiosk.reverse()

    import time
## dd/mm/yyyy format
    today= (time.strftime("%d/%m/%Y"))

    pie_chart = pygal.Bar(print_values=True, print_values_position='top')

    pie_chart.title = "Kiosks With SMS Total["+str(totalSms)+"]  "+str(today)
    total = 0
    xaxis=[]
    yaxis=[]
    for x in range(len(sortedKiosk)):
        if x < 5:
            xaxis.append(sortedKiosk[x][0])
            yaxis.append(sortedKiosk[x][1])
                 
        total += sortedKiosk[x][1]
        print (sortedKiosk[x][0], sortedKiosk[x][1])

    pie_chart.x_labels=xaxis
    pie_chart.add("SMS",yaxis)
    print("*"*60)
    print("Total SMS taken is ", total)    
    #pie_chart.render_to_png ("sms.png")                    
    

from IPython.display import display, HTML

def report_block_template(report_type, graph_url, caption='Per Month'):
    print ("Graph url passed is", graph_url)
    if report_type == 'interactive':
        graph_block = '<iframe style="border: none;" src="{graph_url}.embed" width="100%" height="600px"></iframe>'
    elif report_type == 'static':
        graph_block = (
                '<img style="height: 400px;" src="{graph_url}.png">'
            )

    report_block = ('' +
        graph_block + 
        '{caption}' + # Optional caption to include below the graph
        '<br>'      + # Line break
        '<img src="{graph_url} />'
        '<br>' + 
        '<hr>') # horizontal line                       

    return report_block.format(graph_url=graph_url, caption="Clicks Per Month")


def fullReport():
    width = 768
    height = 1024
    template = (''
        '<img style="width: {width}; height: {height}" src="{image}">' 
        '{caption}'                              # Optional caption to include below the graph
        '<br>'
        '<hr>'
    '')
    report_html = ''
    for image in graphs:
        _ = template
        _ = _.format(image=image, caption='', width=width, height=height)
        report_html += _

    interactive_report = ''
    static_report = ''

    for graph_url in graphs:
        _static_block = report_block_template('static', graph_url, caption='')
        static_report += _static_block
       

    #import pyfpdf
    from fpdf import FPDF, HTMLMixin
    class MyFPDF (FPDF,HTMLMixin):
        pass
        
    pdf = MyFPDF()

    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Courier', '', 12)
    print(static_report)
    pdf.write_html(static_report)
    pdf.output("report.pdf",'F')


def dsum (*dicts):
    from collections import defaultdict
    ret=defaultdict(int)
    for d in dicts:
        for k,v in d.items():
            ret[k] += v
    return dict(ret)        

def formatOutput (currentMonth=False,selfieOnly=False,textOnly=False):
  
    strformat=""
    if selfieOnly == True:
        printSelfieCharts()
        return

    global totalInteraction
    totalInteraction=0

    
       
    i=0    
    for clickBait in clickBaits:
        if clickBait != "streetcarClick":
            clearCounters()
        clearCounters()    

        # 2017 has started
        olditer=1
        if currentMonth == True:
            filename=clickBait + "_currentMonth.json"
        else:        
            filename=clickBait + ".json"

        
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
                            if currentMonth == True:
                                if any(strformat in str(clickpart) for clickpart in click) == False:
                                    print ("Not of this month",strformat)
                                    continue
                                    
                            if "Bangalore" in click or "bangalore" in click:
                                offset = offset +1
                            else: 
                                       
                                totalInteraction = totalInteraction + 1           
                              

                            if clickBait == "clicked":
                                updateIndividualCount(click[3],click[5])

                            if clickBait == "streetcarClick":
                                updateKioskStreetCar(click[3])   
                             
                            if clickBait == "transit":  
                                #print ("updating transit as streetcar")
                                updateKioskTransitStreetCar(click[3])    

                            if clickBait == "appIconClick":    
                                updateAppClick(click[1],click[4])   

                              
                            if clickBait == "adCardClick":
                                updateAdCount(click)    

                            if clickBait == "wayfinding":    
                                updateWayfindingKiosks(click)

                            if clickBait == "mapClick":
                                updateWayfindingKiosks(click)    

                            if clickBait== "translate":
                                global totalMulti
                                totalMulti=totalMulti +1   
                                
                              
                            keys = counterManager.keys()
                            for key in keys:
                                if any (key in str(c) for c in click):
                                    counterManager.get(key,incNoop) ()
                                    break;  

                            if "bangalore" or "Bangalore" in click:
                                pass;
                                        
                                
        print (40*"-")                        
        print (captions[i]," : ", counterNov2017)
        i=i+1
        #print(captions[])
        globalStats[clickBait]=counterNov2017
        
        if currentMonth==False:
            print ("Total Clicks in Nov 2017 ", counterNov2017)
            print ("Total Clicks in Sept 2017 ", counterSept2017)
            print ("Total Clicks in August 2017 ", counterAugust2017)
            print ("Total Clicks in July 2017 ", counterJuly2017)
            print ("Total Clicks in June 2017 ", counterJune2017)
            print ("Total Clicks in May 2017 ", counterMay2017)
            print ("Total Clicks in Apr 2017 ", counterApr2017)
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

        bar_chart=pygal.Bar(print_values=True, print_values_position='top')
        if clickBait == "clicked":
            bar_chart.title="Total Monthly Smart Card interactions by month"
        else:
             bar_chart.title="Total Monthly interactions by month"   
        if clickBait=="transit":
           pass

        bar_chart.add(clickBait,[counterJune,counterJuly,counterAug,counterSept,counterOct,counterNov,counterDec,counterJan2017,counterFeb2017, counterMar2017, counterApr2017,counterMay2017,counterJune2017, counterJuly2017,counterAugust2017])
       

        filename=clickBait+".svg"
        sfilename=clickBait+".png"
        bar_chart.x_labels=["June","July","August","Sept","Oct","Nov","Dec","Jan017","Feb2017","Mar2017","April 2017","May2017","June'17","July'17","Aug 17"]
        if textOnly == False:
            bar_chart.render_to_png(sfilename)


        import operator

        xaxis=[]
        yaxis=[]
        pie_chart = pygal.Bar(print_values=True, print_values_position='top')

        if clickBait == "adCardClick":
            print ("Top ad locations")
            sortedKiosk=sorted( adCardKioks.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()
            print (len(sortedKiosk))
            for x in range(len(sortedKiosk)):
                print (sortedKiosk[x][0],sortedKiosk[x][1] )
                if textOnly == False:
                    xaxis.append(sortedKiosk[x][0])
                    yaxis.append(sortedKiosk[x][1])
            
            if textOnly == False:   
                pie_chart.x_labels=xaxis
                pie_chart.add(clickBait,yaxis)
                pie_chart.render_to_png ("adTopKiosks.png") 
            else:
                print ("--------------")    
                        

        if clickBait == "appIconClick":
            print ("Top Icons Clicked")
            sortedKiosk=sorted( appNames.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()
            
            pie_chart.title = "Top 5 AppIcon Clicks"
            
            for x in range(len(sortedKiosk)):
                print (sortedKiosk[x][0],":",sortedKiosk[x][1])
                if textOnly == False:
                    xaxis.append(sortedKiosk[x][0])
                    yaxis.append(sortedKiosk[x][1])
            if textOnly == False:     
                pie_chart.x_labels=xaxis
                pie_chart.add(clickBait,yaxis)

                pie_chart.render_to_png ("appicontop.png")     
            
        

            
        if clickBait == "streetcarClick" or clickBait =="transit":
            pass
          #  print ("Kiosk based StreetCar Clicks")
            #sortedKiosk=sorted( scKiosk.items(),key=operator.itemgetter(1))
           # sortedKiosk=dsum(scKiosk,scKiosk2)
           # sortedKiosk=sorted(sortedKiosk.items(), key=operator.itemgetter(1))
            #sortedKiosk.reverse()

         #   pie_chart.title = "Top 5 StreetCar Clicks By Location"
         #   for x in range(len(sortedKiosk)):
         #       print (sortedKiosk[x][0],":",sortedKiosk[x][1])
         #       xaxis.append(sortedKiosk[x][0])
         #       yaxis.append(sortedKiosk[x][1])
         #   if textOnly == False:
         #       pie_chart.x_labels=xaxis
         #       pie_chart.add(clickBait,yaxis)
         #       pie_chart.render_to_png ("streetcartop.png")  
            
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
            xaxis=[]
            yaxis=[]
            pie_chart.title = "Top 5 Kiosk Clicks By Location"
            print ("Top 5 Kiosk Clicks By Location")
            for x in range(len(sortedKiosk)):
                 print (sortedKiosk[x][0],":",sortedKiosk[x][1])
                 xaxis.append(sortedKiosk[x][0])
                 yaxis.append(sortedKiosk[x][1])
            if textOnly == False:
                pie_chart.x_labels=xaxis
                pie_chart.add(clickBait,yaxis)
                pie_chart.render_to_png ("topkiosk.png")      
          
            xaxis=[]
            yaxis=[]
            pie_chart = pygal.Bar(print_values=True, print_values_position='top')
            pie_chart.title = "Top 5 Poster Clicks"
            print ("Top 5 Poster Clicks ")
            for x in range(10):
                print (sortedPoster[x][0],":",sortedPoster[x][1])
                xaxis.append(sortedPoster[x][0])
                yaxis.append(sortedPoster[x][1])

            if textOnly == False:
                pie_chart.x_labels=xaxis
                pie_chart.add(clickBait,yaxis)

                pie_chart.render_to_png ("topposter.png") 
    
   
    
    
    xaxis=[]
    yaxis=[]
    pie_chart = pygal.Bar(print_values=True, print_values_position='top')
    xaxis=["StreetCar","Wayfinding","Multilanguage"]
    yaxis=[totalStreetCar,totalWayfinding,totalMulti]
    pie_chart.title = "Core Apps Interactions till date"
    print ("Core Apps Interactions")
    if textOnly == False:
        pie_chart.x_labels=xaxis
        pie_chart.add(clickBait,yaxis)  
        pie_chart.render_to_png ("coreapps.png") 

    
    sortedKiosk=dsum(scKiosk,scKiosk2)
    sortedKiosk=sorted(sortedKiosk.items(), key=operator.itemgetter(1))
    sortedKiosk.reverse()

    for x in range(5):
        print (sortedKiosk[x][0],":",sortedKiosk[x][1])
        
    print("Total Interactions="+str(totalInteraction))
    print ("Total StreetCar", totalStreetCar+totalStreetCar2)
    print("Total Wayfinding", totalWayfinding)
    print("Total Multi", totalMulti)   

    print("Total mistakes", adMistakes)   
    print("Total ad clicks", adClicks)        
    
        



def run(arg):
    global clickBaits
    if arg == "full":
        loadConfig()
        connect(False)
        formatOutput(textOnly=True)

    if arg == "output":
        formatOutput();

    if arg == "report":
        fullReport()     
    
    if arg == "sc":
        clickBaits=["streetcarClick","transit"]
        loadConfig()
        connect(False)
        formatOutput(textOnly=True)

    if arg == "clicked":
        
        clickBaits=["clicked"]
        loadConfig()
        connect(False)
        formatOutput()    

    if arg == "adonly":
       
        clickBaits=["adCardClick"]
        formatOutput()

    if arg == "currentMonthAd":
       
        clickBaits=["adCardClick"]
        formatOutput(currentMonth=True,textOnly=True)

    if arg == "adFull":
        
        clickBaits=["adCardClick"]
        loadConfig()
        connect(False)
        formatOutput()

    if arg == "connect":
        connect(False)

    if arg == "configTest":
        loadConfig()   

    if arg == "selfieClick":  
        loadConfig()
        getSelfieClicks()
        getSelfieFromFile()  
        printSelfieCharts()

        getSMSRequests()
        getSMSRequestsFromFile()
        printSMSRequests()

    if arg == "loadSelfieData":
        getSelfieFromFile()   
        printSelfieCharts(textOnly=True) 

        getSMSRequestsFromFile()
        printSMSRequests()

    if arg == "current":
        loadConfig()
        connect(currentMonth=True)
        formatOutput(currentMonth=True,textOnly=True)

    if arg == "currentMonthFromData":
        loadCurrentFromData()
        
            
       
    
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
                        dest=city,
                        action="store")                    
    args=parser.parse_args()                    
        
    if args.mode:
        print ("Arguments passed");
        run(args.mode)
    else:
        run ("output")   
