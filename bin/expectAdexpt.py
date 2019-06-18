#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
''' ad pop file '''
import time
import datetime
import csv,  sys
import json
from collections import defaultdict

from fpdf import FPDF

class hits:
    def __init__(self,hittime,value):
        self.hittime=hittime
        self.value=int(value)
    def __str__(self):
        return ("<%s--%s>" % (self.hittime, self.value))



countMap={}
startDate = datetime.datetime(2019,3,1)

kioskhitmap = defaultdict(list)
expectedmap = defaultdict(list)
adjustedHitMap = defaultdict(list)
    

def createExpectedHitsInSecs(name,h,c):
    global countMap
    from dateutil import parser
    t = parser.parse(h)
    dayssince=t.replace(tzinfo=None) - startDate.replace(tzinfo=None)
    ev=720*dayssince.days# 720 every day
    delta=0
    dev = ev + delta # total times it was shown
    a=0
    try:
        a=countMap[name]
        b=a+c
        countMap[name]=b
        print("Setting ",name," with c= ",b)
    except KeyError as k:
        print("No ",name, " in countmap with c=",c)
        countMap[name]=c

    return dev, a+c

    

def massage(name, hitlist):
    global adjustedHitMap
    global expectedmap

    for hit in hitlist:
        ev,todate=createExpectedHitsInSecs(name,hit.hittime,hit.value/10000)
       # print (name,hit.hittime, "Actual Impressions :", todate, " Expected Impressions=",ev, "delta=",(ev-todate))
        hit=hits(hit.hittime, todate)
        adjustedHitMap[name].append(hit)
        hit2=hits(hit.hittime, ev)
        expectedmap[name].append(hit2)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('scm_logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'SCM POP Report', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def reportKiosk(name):
    import pygal
    linech=pygal.Line(x_label_rotation=20)
    # get the times
    times=[]
    ahits=[]
    evs=[]
    hits=adjustedHitMap[name]
    exps=expectedmap[name]
    for hit in hits:
        times.append(hit.hittime)
        ahits.append(hit.value)
    for exp in exps:
        evs.append(exp.value)

    linech.x_labels = times
    linech.add("Hits",ahits)
    linech.add("Expected",evs)
    filename="./"+name+".txt"
    imagefile="./"+name+".png"
    
    linech.render_to_png(imagefile) 

    with open (filename,'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(zip(times,ahits,evs))

    import pandas as pd
    import pdfkit as pdfk

    html_file = "./" + name + '.html'
    pdf_file = "./" + name + '.pdf'    

    df = pd.read_csv(filename, sep=',')
    df.to_html(html_file)
    pdfk.from_file(html_file, pdf_file)
    
    with open ("tots.csv",'w') as f2:
        writer = csv.writer(f2,delimiter='\t')
        writer.writerows(zip(countMap.keys(),countMap.values()))

def reportHeader(pdffile):
    pass
        
def reportGen():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Sprint Saves Ad", align="C")
    reportHeader(pdf)

    for hit in adjustedHitMap:
        # generate report for each kiosk
        reportKiosk(hit)
        
    pdf.output("pop.pdf")
    

def createHeaderFile():
    import pdfkit as pdfk
    import datetime
    message="""<html>
                <body><img='scm_logo.png'><center><H1>SCM Proof of Play Documentation</h1>
                <h2> Customer: Sprint </h2>
                <h2> Ad:    Sprint Saves 1000 </h2>
                <h3> Date:""" + datetime.datetime.today().strftime('%Y-%m-%d') + """ </h3>
                </center></body></html>
            """
    with open ("header.html","wt") as f:
        f.write(message)

    pdfk.from_file("header.html", "A.pdf")   

def massageData():
    for khit in kioskhitmap:
        massage(khit, kioskhitmap[khit])


#if you are not using utf-8 files, remove the next line
#check if you pass the input file and output file
if len(sys.argv ) ==2 and  sys.argv[1] is not None :
    filename = sys.argv[1]
    totes=0

                    
    with open (filename,"r") as csvfile:
        reader=csv.reader(csvfile)
        for l in reader:
            if 'Sprint Save $1000' in l[5]:
                totes = totes + 1
                hit = hits(l[0],l[6])
                
                kioskhitmap[l[3]].append(hit)
                #print("Found sprint",l[3])
            else:
                pass
                #print("No sprint")
        
    #print(totes) 
    massageData()
    reportGen()
else:
    createHeaderFile()