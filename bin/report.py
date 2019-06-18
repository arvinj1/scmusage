#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import json
import os
import pygal
import pandas as pd

svgs=['coreapps.png'
        #'adTopKiosks.svg',
        'appicontop.png',
        'topkiosk.png',
        'topposter.png'
        ]

descs=[
    'Overall Interactions',
    #'Top Ad Kiosks',
    'Top Icons',
    'Top Kiosks',
    'Top Posters'
]        

def genReport(fileName):
    ''' generating report '''
    from reportlab.graphics import renderPDF, renderPM
    from reportlab.platypus import SimpleDocTemplate, Paragraph,Image
    from reportlab.lib.styles import getSampleStyleSheet
    from svglib.svglib import svg2rlg
    import cairosvg

    doc = SimpleDocTemplate(fileName)
    story = [] 
    i=0   
    styles = getSampleStyleSheet()
    for img in svgs:
        text = descs[i]
        i = i+1
        para = Paragraph(text, style=styles["Normal"])        
        story.append(para)
        drawing=Image(img)
        story.append(drawing)

    doc.build(story)    


def reportToday(filename):
    df = pd.read_json(filename, orient='columns')
    df.head()


if __name__ == "__main__":
    print ("Report Generator")
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('-f',
                        "--filename",
                        dest="filename",
                        action="store")
    parser.add_argument("-t",
                        "--today",
                        dest="today",
                        action="store_true")     

    args=parser.parse_args() 
    if args.filename:
        genReport(args.filename)
    if args.today:
        reportToday("./clicked_daily.json")                       

