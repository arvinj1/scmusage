#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import json
import os
import time
from pprint import pprint

import iso8601
import pandas as pd
from influxdb import InfluxDBClient

clickBaits = [
  
  "translate",
    "mapClick",
    "appIconClick"
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
]
captions = [
    "Translation Pressed"
    ,"App Clicks by Month"
    ,""
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
appClickCount={}
selfieKiosks={}
smsKiosks={}
appNames={}

wayFindingKiosks={}
wayFTime={}

streetcarList=[]
posterClickList=[]
appIconList=[]
translateList=[]
mapclickList=[]
wayFindingList=[]


''' Kiosk mapping '''
kioskMap = {
    "Union Station SB-North Face":"Union Station",
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
"Crown Center - 2470 Grand - East Face":"Crown",
"City Hall -12th Oak":"City Hall",
"barneysouth":"Barney",
"Convention Center - 301 W 13th":"Convention",
"Performing Arts Center":"PerformingArts",
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
    kioskName=kioskMap[kioskNameG]
    totalSms+=1
    if not kioskName in smsKiosks:
            smsKiosks[kioskName]=1
    else:
        smsKiosks[kioskName] += 1


def updateKioskSelfie (kioskNameG):
    global selfieKiosks
    global totalSelfieClicks

    kioskName=kioskMap[kioskNameG]

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


def updateAppClick(appNameMash,kioskName):
    global appClickCount
    global appNames

    appNameL = appNameMash.split("_")
    if len(appNameL) ==2 :
        appName=appNameL[1]
    else:
        appName=appNameL[0]

   
    if not kioskName in appClickCount:
        appClickCount[kioskName]=1
    else:
        appClickCount[kioskName] += 1

   
    if not appName in appNames:
        appNames[appName]=1
    else:
        appNames[appName] += 1    

def updateTransit(click):
    print(click)

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
                            


  
def getSMSRequests():
    print ("GEtting Selfies")
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;
    query="select * FROM smsRequest WHERE city='kc'"
    filename="sms.json"
    result=client.query(query)
    with open (filename,'w') as f:
        json.dump(result.raw,f)

    print ("Calling the items ")
    items = result.items()
    print (items)

    print ("Calling the keys ")
    keys = result.keys()
    print (keys)

def getSMSRequestsFromFile():
    print ("Getting sms clicks from file")
    with open ("./sms.json","r") as f:
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
                    
                    updateKioskSMS(click[3])        
    
def connect (currentMonthOnly):
   
    client=InfluxDBClient(URL,PORT,uname,password,dbname)
    if (client == None):
        print ("Error connecting to URL");
        return;

    today= (time.strftime("%m"))
    lastMonth=int(today)-1
    year = time.strftime("%Y")
    strformat='0{0}'.format(lastMonth)[-2:]
    startDay=year+"-"+strformat+"-01"
    strformat='0{0}'.format(today)[-2:]
    endDay=year+"-"+strformat+"-01"    

    for click in clickBaits:
        print ("Executing ",click)
        if currentMonthOnly == True:
            query="select * from " + click + " where time > '" +startDay + "' and time < '" + endDay + "'"
            print (query)
            filename=click+"_currentMonth.json"
        else:
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
        global counterApr2017
        counterApr2017=0
        global counterMay2017
        counterMay2017=0

           
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
        print (sortedKiosk[x][0])

    pie_chart.x_labels=xaxis
    pie_chart.add("Selfies",yaxis)
        
    print("*"*60)
    print("Total selfies taken is ", total)    
    pie_chart.render_to_png ("selfies.png")       

def printSMSRequests():
    import pygal
    import operator
        
    print ("SMS of Selfies Clicked")
    sortedKiosk=sorted( smsKiosks.items(),key=operator.itemgetter(1))
    sortedKiosk.reverse()

    import time
## dd/mm/yyyy format
    today= (time.strftime("%d/%m/%Y"))

    print (len(sortedKiosk))
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

    pie_chart.x_labels=xaxis
    pie_chart.add("SMS",yaxis)
    print("*"*60)
    print("Total SMS taken is ", total)    
    pie_chart.render_to_png ("sms.png")                    
    
def currentMonthReport ():
    totalInt=0
    import time
## dd/mm/yyyy format
    today= (time.strftime("%m"))
    lastMonth=int(today)-1
    year = time.strftime("%Y")
    strformat='0{0}'.format(lastMonth)[-2:]
    strformat=year+"-"+strformat

    import operator
    import pygal
    import calendar
         
    for clickBait in clickBaits:
        filename=clickBait + "_currentMonth.json"
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
                            else:   
                                totalInt+=1    

                            if any ("2017-06" in str(c) for c in click):
                                continue

                            if clickBait == "clicked":
                                updateIndividualCount(click[3],click[5])

                            if clickBait == "streetcarClick" :
                                updateKioskStreetCar(click[3])    

                            if clickBait == "appIconClick":    
                                updateAppClick(click[1],click[4])   

                            if clickBait == "transit":  
                                print ("updating transit as streetcar")
                                updateKioskStreetCar(click[3])    

                            keys = counterManager.keys()
                            for key in keys:
                                if any (key in str(c) for c in click):
                                    counterManager.get(key,incNoop) ()
                                    break;   

        if clickBait == "appIconClick":
            print ("Top Icons Clicked")
            sortedKiosk=sorted( appNames.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            print (len(sortedKiosk))
            pie_chart = pygal.Pie()
            pie_chart.title = "CurrentMonth Top 5 AppIcon Clicks"
            for x in range(5):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("appicontopcurrent.svg")     
            
            
        if clickBait == "TTT":
            print ("WayFinding Clicks")
            sortedKiosk=sorted( wayFindingKiosks.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            pie_chart = pygal.Pie()
            pie_chart.title = "CurrentMonth Top 5 Wayfinding Kiosks"
            for x in range(len(wayFindingKiosks.items())):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("wayfindingtopcurrent.svg")  

            sortedKiosk=sorted( wayFTime.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            pie_chart = pygal.Pie()
            pie_chart.title = "CurrentMonth Top 5 Wayfinding Time"
            for x in range(5):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("wayfindingTimetopcurrent.svg")  

          
            
            
        if clickBait == "streetcarClick" or clickBait =="transit":
            print ("Kiosk based StreetCar Clicks")
            sortedKiosk=sorted( scKiosk.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            pie_chart = pygal.Pie()
            pie_chart.title = "CurrentMonth Top 5 StreetCar Clicks"
            for x in range(len(sortedKiosk)):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("streetcartopcurrent.svg")  
            
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
            pie_chart.title = "Current Month All Kiosk Clicks"
            for x in range(len(sortedKiosk)):
                pie_chart.add(sortedKiosk[x][0],sortedKiosk[x][1])

            pie_chart.render_to_file ("topkioskcurrent.svg")      
        
          
            pie_chart = pygal.Pie()
            pie_chart.title = "Current Month TopPoster Clicks"
            for x in range(len(sortedPoster)):
                pie_chart.add(sortedPoster[x][0],sortedPoster[x][1])

            pie_chart.render_to_file ("toppostercurrent.svg")    

    print ("Total Monthly Interaction=",totalInt)                                     

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


def formatOutput (report=True,selfieOnly=False):
  
    if selfieOnly == True:
        printSelfieCharts()
        return

    totalInteraction=0
    for clickBait in clickBaits:
        if clickBait != "streetcarClick":
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
                            else:
                                global totalInteraction            
                                totalInteraction+=1             
                              

                            if clickBait == "clicked":
                                updateIndividualCount(click[3],click[5])

                            if clickBait == "streetcarClick":
                                updateKioskStreetCar(click[3])   
                             
                            if clickBait == "transit":  
                                #print ("updating transit as streetcar")
                                updateKioskStreetCar(click[3])    

                            if clickBait == "appIconClick":    
                                updateAppClick(click[1],click[4])   

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

                            if "2017-05" in click or "bangalore" or "Bangalore" in click:
                                pass;
                                        
                                
                        
        print ("*" * 40 )   
        print ("Stats for ", clickBait )                      
        print ("Clicks is=",len(clicks), "offsetted=",offset,counterMay2017+ counterApr2017+counterMar2017+counterFeb2017+counterJan2017+counterDec+counterNov+counterOct+counterSept+counterAug+counterJuly+counterJune)  
        print ("*" * 40  )   
        print ("Total Clicks in Apr 2017 ", counterMay2017)
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

        bar_chart.add(clickBait,[counterJune,counterJuly,counterAug,counterSept,counterOct,counterNov,counterDec,counterJan2017,counterFeb2017, counterMar2017, counterApr2017,counterMay2017])
       

        filename=clickBait+".svg"
        sfilename=clickBait+".png"
        bar_chart.x_labels=["June","July","August","Sept","Oct","Nov","Dec","Jan017","Feb2017","Mar2017","April 2017","May2017"]
        bar_chart.render_to_png(sfilename)


        import operator

        xaxis=[]
        yaxis=[]
        pie_chart = pygal.Bar(print_values=True, print_values_position='top')
         
        if clickBait == "appIconClick":
            print ("Top Icons Clicked")
            sortedKiosk=sorted( appNames.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            print (len(sortedKiosk))
            
            pie_chart.title = "Top 5 AppIcon Clicks"
            
            for x in range(5):
                 xaxis.append(sortedKiosk[x][0])
                 yaxis.append(sortedKiosk[x][1])
                 
            pie_chart.x_labels=xaxis
            pie_chart.add(clickBait,yaxis)

            pie_chart.render_to_png ("appicontop.png")     
            
            

            
        if clickBait == "streetcarClick" or clickBait =="transit":
            print ("Kiosk based StreetCar Clicks")
            sortedKiosk=sorted( scKiosk.items(),key=operator.itemgetter(1))
            sortedKiosk.reverse()

            pie_chart.title = "Top 5 StreetCar Clicks By Location"
            for x in range(5):
                 xaxis.append(sortedKiosk[x][0])
                 yaxis.append(sortedKiosk[x][1])

            pie_chart.x_labels=xaxis
            pie_chart.add(clickBait,yaxis)
            pie_chart.render_to_png ("streetcartop.png")  
            
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
            for x in range(5):
                 xaxis.append(sortedKiosk[x][0])
                 yaxis.append(sortedKiosk[x][1])

            pie_chart.x_labels=xaxis
            pie_chart.add(clickBait,yaxis)
            pie_chart.render_to_png ("topkiosk.png")      
          
            xaxis=[]
            yaxis=[]
            pie_chart = pygal.Bar(print_values=True, print_values_position='top')
            pie_chart.title = "Top 5 Poster Clicks"
            for x in range(5):
                 xaxis.append(sortedPoster[x][0])
                 yaxis.append(sortedPoster[x][1])

            pie_chart.x_labels=xaxis
            pie_chart.add(clickBait,yaxis)

            pie_chart.render_to_png ("topposter.png") 
    
   
    
    
    xaxis=[]
    yaxis=[]
    pie_chart = pygal.Bar(print_values=True, print_values_position='top')
    xaxis=["StreetCar","Wayfinding","Multilanguage"]
    yaxis=[totalStreetCar,totalWayfinding,totalMulti]
    pie_chart.title = "Core Apps Interactions till date"
    pie_chart.x_labels=xaxis
    pie_chart.add(clickBait,yaxis)  
    pie_chart.render_to_png ("coreapps.png") 

    print("Total Interactions="+str(totalInteraction))
    print ("Total StreetCar", totalStreetCar)
    print("Total Wayfinding", totalWayfinding)
    print("Total Multi", totalMulti)        
    
        



def run(arg):
    if arg == "full":
        loadConfig()
        connect(False)
        formatOutput()

    if arg == "output":
        formatOutput();

    if arg == "report":
        fullReport()     

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
        printSelfieCharts() 

        getSMSRequestsFromFile()
        printSMSRequests()

    if arg == "current":
        loadConfig()
        connect(True)
        currentMonthReport()    
       
    
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
