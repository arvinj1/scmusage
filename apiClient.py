#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import json
import os
import time
import datetime
from pprint import pprint

import iso8601
import pandas as pd
from influxdb import InfluxDBClient

COL_KIOSK_ID=3
COL_KIOSK_NAME=4
COL_POSTER_NAME=7

tempClickCount=0
KIOSK_COUNT=10

showAll=False

exludeKiosks=[]

kioskMapFile="kiosks.csv"

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
captions = {
   "translate": "Translation Pressed"
    ,"appIconClick":"Apps Pressed"
    ,"clicked":"Smart Card Landing Pages Clicked"
    ,"wayfinding":"Wayfinding"
    ,"appRequest":"App Request"
    ,"smsRequest":"SMS Request"
    ,"voicesearch":"Voice Search"
    ,"disability":"Disability"
    ,"transit":"Transit /StreetCar"
    ,"streetcarClick":"Streetcar"
    ,"adCardClick":"AdCardClick"
}
graphs = ["./"+a+".svg" for a in clickBaits ]

totalInteraction=0
 
# support for range click count
counterCustom=0
counterCurrent=0

globalStats={}
city="kc"
fordate=None
rangeInDays=1
rangeInWeeks=0
customRange=False
textModeOutput=False

          
URL=""
PORT=0
uname=""
password = ""
dbname=""

dbs={}

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

kioskWrongData= [
    "Kcatademo","BlueLine","TRAILS","Bangalore","demo","duke1","nanov2","nanov1","duke22057"
]

ConfigFile="./config.json"

# core APPS
totalStreetCar=0
totalStreetCar2=0
totalWayfinding=0
totalMulti=0

def customClickCount():
    global counterCustom
    counterCustom+=1

def genCounter():
    global counterCurrent
    counterCurrent+=1

def clearCounter():
    global counterCurrent
    counterCurrent=0

def incNoop ():
    print (":Empty funcion")  

def updateKioskSMS(kioskName):
    global smsKiosks
    global totalSms

    totalSms+=1
    if not kioskName in smsKiosks:
            smsKiosks[kioskName]=1
    else:
        smsKiosks[kioskName] += 1

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
    global adCardCount
    location = click[COL_KIOSK_ID]
    adName = click[5]

    global adCardKioks
    
    if not location in adCardKioks:
        adCardKioks[location]=1
    else:
        adCardKioks[location]+=1

    global adClicks
    adClicks+=1   

    if not adName in adCardCount:
        adCardCount[adName]=1
    else:
        adCardCount[adName]+=1

def updateWayfindingKiosks (click):
    global wayFindingKiosks  
    global wayFTime 
    global totalWayfinding
    totalWayfinding+=1

    timeOftouch=click[0]
    location=click[3]

    if not location in wayFindingKiosks:
        wayFindingKiosks[location]=1
    else:
       wayFindingKiosks[location]+=1 

    if not timeOftouch in wayFTime:
        wayFTime[timeOftouch]=1
    else:
        wayFTime[timeOftouch]+=1     
            
def updateIndividualCount(kioskNameMash,posterName):
    global tempClickCount
    global kioskCount
    global posterCount
    global kioskPosterMap

    if kioskNameMash is None:
        print("none kiosk")
        return

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
    
    tempClickCount += 1     
        
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
    
def getSelfieFromFile():
    with open ("./selfie.json","r") as f:
         data=json.load(f)

    keys=data.keys()
    for key in keys:  
        if key != 'series':
            continue

        value=data[key]
        lent=list(value[0])
        for lentee in lent:
            if lentee == "values":
                clicks= (data[key][0][lentee])
                
                for click in clicks:
                    if "Bangalore" in click or "bangalore" in click:
                        #print ("There is banglore kciosk selfie")
                        pass
                    else:    
                        updateKioskSelfie(click[5])    

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

def getSMSRequestsFromFile():
    #print ("Getting sms clicks from file")
    with open ("./sms.json","r") as f:
         data=json.load(f)

    keys=data.keys()
    for key in keys:     
        if key != 'series':
            continue
           
        value=data[key]
        lent=list(value[0])
        for lentee in lent:
            if lentee == "values":
                clicks= (data[key][0][lentee])
                for click in clicks:
                    if "Bangalore" in click or "bangalore" in click:
                        pass
                    else:
                        updateKioskSMS(click[4])        
    
def connect (currentMonth,customDate=False,forDate=None):
    #to support new influxdb 1.5
    client=InfluxDBClient(host=URL, port=PORT, username=uname, password=password, ssl=True, verify_ssl=True)
    if (client == None):
        print ("Error connecting to URL");
        exit;

    global dbs
    dbs = client.get_list_database()

    # pity no error code here
    client.switch_database(city)

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


    for click in clickBaits:
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

            query="select * from " + click + " where city='"+city+"' and time >= '" +startDay + "' and time < '" + endDay + "'"
            filename=click+"_daily.json"
        elif currentMonth == True:
            query="select * from " + click + " where city='"+city+"' and time >= '" +startDay + "' and time < '" + endDay + "'"
            filename=click+"_currentMonth.json"
        else:
            query="select * from " + click
            filename=click+".json"
        
        result=client.query(query)
        
        with open (filename,'w') as f:
            json.dump(result.raw,f)
        
        items = result.items()
        keys = result.keys()
        
       

           
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
        if showAll or x < KIOSK_COUNT:
            xaxis.append(sortedKiosk[x][0])
            yaxis.append(sortedKiosk[x][1])
                 
        total += sortedKiosk[x][1]
        print (sortedKiosk[x][0], sortedKiosk[x][1])

    if not textOnly:
        pie_chart.x_labels=xaxis
        pie_chart.add("Selfies",yaxis)
        
    print("*"*60)
    print("Total selfies taken is ", total)  
    if not textOnly:  
        pie_chart.render_to_file ("selfies.svg")       


def printTodayCharts(textOnly=False):
    if not textOnly:
        import pygal
        
    import operator    
    import time
## dd/mm/yyyy format
    today= (time.strftime("%d/%m/%Y"))
    if not textOnly:
        pie_chart = pygal.Bar(print_values=True, print_values_position='top')
        pie_chart.title = "Kiosks With Selfies Total["+str(totalSelfieClicks)+"]  "+str(today)

    localbaits=["clicked"]
    for click in clickBaits:
        print (40*"-")
        print (click)
        print (40*"-")
        filename=click+"_daily.json"
        with open (filename,"r") as jsonfile:
            data=json.load(jsonfile)
            keys=data.keys()
            for key in keys:   
                value=data[key]
                lent=list(value[0])
                for lentee in lent:
                    if lentee == "values":
                        clicks= (data[key][0][lentee])
                        for click in clicks:
                            try:
                                print(click)
                            except IndexError:
                                print ("SomethingOff"+str(len(click)))
                                print(str(click[0])+","+str(click[3]))


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
    pie_chart.render_to_file ("sms.svg")                    
    

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


    
def formatOutput (currentMonth=False,selfieOnly=False,textOnly=False, customDate=False):
  
    strformat=""
    if selfieOnly == True:
        printSelfieCharts()
        return

    global totalInteraction
    totalInteraction=0
       
    i=0    
    for clickBait in clickBaits:
        clearCounter()    

        olditer=1
        if customDate == True:
            filename=clickBait+"_daily.json"
        elif currentMonth == True:
            filename=clickBait + "_currentMonth.json"
        else:        
            filename=clickBait + ".json"
        
        try:
            with open (filename,"r") as jsonfile:
                data=json.load(jsonfile)
                keys=data.keys()
            
                for key in keys:
                    if key != 'series':
                        continue

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
                                # dirty test data        
                                if any (c.lower() in str(clickpart).lower() for clickpart in click for c in kioskWrongData):
                                    offset = offset +1
                                    continue
                            
                                totalInteraction = totalInteraction + 1          

                                if clickBait == "clicked":
                                    
                                    colposterid = COL_POSTER_NAME
                                    kiosknamecol= COL_KIOSK_NAME
                                    if city == "louisville":
                                        colposterid = 8
                                        kiosknamecol = 6
                                    else: #(city == "kc" or city == "umkc" or city=="lr" or city=='scs') :
                                        colposterid = 7
                                        kiosknamecol = 5

                                    updateIndividualCount(click[kiosknamecol],click[colposterid])

                                if clickBait == "streetcarClick":
                                    updateKioskStreetCar(click[3])   
                                if clickBait == "transit":  
                                    #print ("updating transit as streetcar")
                                    updateKioskTransitStreetCar(click[4])    

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
                                
                                global globalStats 
                                if globalStats.get(clickBait) != None:
                                    globalStats[clickBait]=globalStats[clickBait]+1
                                else:
                                    globalStats[clickBait]=1    

                                if customRange == True:
                                    customClickCount()   
                                else:
                                    genCounter()

            print (40*"-")  
            caption="Data"
            try:
                caption=captions[clickBait]
            except:
                caption=clickBait 

            if customRange == True:
                print (caption,counterCustom)
            else:
                print (caption,counterCurrent)
            i=i+1
            
            if customRange == True:
                print (caption,counterCustom)
                globalStats[clickBait]=counterCustom
            else:    
                globalStats[clickBait]=counterCurrent
    
            import pygal
            import calendar
            import operator

            xaxis=[]
            yaxis=[]
            pie_chart = pygal.Bar(print_values=True, print_values_position='top')

            if clickBait == "adCardClick":
                print ("Top ad locations")
                sortedKiosk=sorted( adCardKioks.items(),key=operator.itemgetter(1))
                sortedKiosk.reverse()
            
                if showAll:
                    ren=len(sortedKiosk)
                else:
                    ren=KIOSK_COUNT

                for x in range(ren):
                    try:
                        print (sortedKiosk[x][0],sortedKiosk[x][1] )
                        if textOnly == False:
                            xaxis.append(sortedKiosk[x][0])
                            yaxis.append(sortedKiosk[x][1])
                    except Exception:
                        pass        
            
                if textOnly == False:   
                    pie_chart.x_labels=xaxis
                    pie_chart.add(clickBait,yaxis)
                    pie_chart.render_to_png ("adTopKiosks.png") 
                else:
                    print ("--------------")    

                print ("Top Ads")  
                sortedKiosk=sorted( adCardCount.items(),key=operator.itemgetter(1))
                sortedKiosk.reverse()
            
                for x in range(len(sortedKiosk)):
                    try:
                        print (sortedKiosk[x][0],sortedKiosk[x][1] )
                        if textOnly == False:
                            xaxis.append(sortedKiosk[x][0])
                            yaxis.append(sortedKiosk[x][1])
                    except Exception:
                        pass        
            
                if textOnly == False:   
                    pie_chart.x_labels=xaxis
                    pie_chart.add(clickBait,yaxis)
                    pie_chart.render_to_png ("topAd.png") 
                else:
                    print ("--------------")      
                        

            if clickBait == "appIconClick":
                print ("Top Icons Clicked")
                sortedKiosk=sorted( appNames.items(),key=operator.itemgetter(1))
                sortedKiosk.reverse()
            
                pie_chart.title = "Top 5 AppIcon Clicks"
                if len(sortedKiosk) < KIOSK_COUNT:
                    a=len(sortedKiosk)
                else:
                    if showAll:
                        a=len(sortedKiosk)
                    else:
                        a=KIOSK_COUNT
                
                for x in range(a):
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
                pie_chart.title = "Top Kiosk Clicks By Location"
                print ("Top Kiosk Clicks By Location")
                if len(sortedKiosk) < KIOSK_COUNT:
                    a=len(sortedKiosk)
                else:
                    if not showAll:
                        a=KIOSK_COUNT
                    else:
                        a=len(sortedKiosk)
                        

                for x in range(a):
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
                print (25*'-')
                if len(sortedKiosk) < 5:
                    a=len(sortedKiosk)
                else:
                    a=5
                a=5     
                for x in range(a):
                    print (sortedPoster[x][0],":",sortedPoster[x][1])
                    xaxis.append(sortedPoster[x][0])
                    yaxis.append(sortedPoster[x][1])

                if textOnly == False:
                    pie_chart.x_labels=xaxis
                    pie_chart.add(clickBait,yaxis)

                    pie_chart.render_to_png ("topposter.png") 
    
        except FileNotFoundError as fe:
            #print("skipping",filename)
            continue
    
    xaxis=[]
    yaxis=[]
    pie_chart = pygal.Pie(print_values=True)
    #pie_chart = pygal.Bar(print_values=True, print_values_position='top')
    pie_chart.title = "Core Apps Interactions till date"
    
    if textOnly == False:
        for name,data in globalStats.items():
            pie_chart.add(name,int(data))
            
        pie_chart.render_to_png('./coreapps.png') 
    
    sortedKiosk=dsum(scKiosk,scKiosk2)
    sortedKiosk=sorted(sortedKiosk.items(), key=operator.itemgetter(1))
    sortedKiosk.reverse()

    if len(sortedKiosk) < KIOSK_COUNT:
        a=len(sortedKiosk)
    else:
        if not showAll:
            a=KIOSK_COUNT
        else:
            a=len(sortedKiosk)
    print ("Top SC interactions")
    for x in range(a):
        print (sortedKiosk[x][0],":",sortedKiosk[x][1])
        
    print("Total Interactions="+str(totalInteraction))
    print("Total ClickCount="+str(tempClickCount))
    print ("Total StreetCar", totalStreetCar+totalStreetCar2)
    print("Total Wayfinding", totalWayfinding)
    print("Total Multi", totalMulti)   

    #pDatrint("Total mistakes", adMistakes)   
    print("Total ad clicks", adClicks)    

    print("Global Stats")
    for name,data in globalStats.items():
        print(name,"=",data)
            
    
        



def run(arg):
    global clickBaits
    global city
    #print ("Doing for city="+city)
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
        formatOutput(currentMonth=True,textOnly=False)

    if arg == "clicked":
        
        clickBaits=["clicked"]
        loadConfig()
        connect(False)
        formatOutput(currentMonth=True,textOnly=False)    

    if arg == "adonly":
        clickBaits=["adCardClick"]
        loadConfig()
        connect(False)
        
        formatOutput(textOnly=True)

    if arg == "currentMonthAd":
       
        clickBaits=["adCardClick"]
        formatOutput(currentMonth=True,textOnly=False)

    if arg == "adFull":
        
        clickBaits=["adCardClick"]
        loadConfig()
        connect(False)
        formatOutput()

    if arg == "connect":
        loadConfig()
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

    if arg == "today":
        loadConfig()
        connect(currentMonth=False,customDate=True,forDate=fordate)
        formatOutput(currentMonth=False,customDate=True,textOnly=True)

    if arg == "adCustom":
        clickBaits=["adCardClick"]
        loadConfig()
        connect(currentMonth=False,customDate=True,forDate=fordate)
        formatOutput(currentMonth=False,customDate=True,textOnly=True)

    if arg == "days":
        loadConfig()
        connect(currentMonth=False,customDate=True,forDate=fordate)
        formatOutput(currentMonth=False,customDate=True,textOnly=True)
            

    if arg == "currentFromFile":
        formatOutput(currentMonth=True, textOnly=True)
        
            

    if arg == "uptime":
        clickBaits=["ageOfAdpost","ageOfSmartPost"]
        loadConfig()
        connect(currentMonth=True)
        formatOutput(currentMonth=True)


    
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
                        dest="range",
                        action="store", type=int)      
    parser.add_argument("-f",
                        "--configFile",
                        dest="cfg",
                        action="store") 

    parser.add_argument("-a",
                        "--all",
                        dest="kcomb",
                        action="store_true") 

    parser.add_argument("-b",
                        "--dblist",
                        dest="dblist",
                        action="store_true") 

    parser.add_argument("-x",
                        "--excludeKioskLists",
                        dest="xlist",
                        action="store")                     


                    
    args=parser.parse_args()   
    
    if args.kcomb:
        showAll=True             
    if args.city:
        city=args.city   
    if args.date:
        fordate=args.date  
    else:
        fordate=None 

    if args.range:
        rangeInDays=args.range  
        customRange=True
    if args.cfg:
        ConfigFile=args.cfg 

    if args.mode:
        run(args.mode)

    if args.xlist:
        with open(args.xlist) as f:
            exludeKiosks = f.read().splitlines()

    if args.dblist:
        print("Getting dblist")
        loadConfig()
        client=InfluxDBClient(host=URL, port=PORT, username=uname, password=password, ssl=True, verify_ssl=True)
        if (client == None):
            print ("Error connecting to URL");
            exit;

        dblist=[]
        dblist = client.get_list_database()
        print (dblist)
