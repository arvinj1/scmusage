#!/usr/bin/python

import serial,time
from enum import Enum

global ser

class ColorModes(Enum):
    Auto1=1
    Rainbow1=2
    Auto2=3
    Rainbow2=4
    Manual=5
    Blink=6




def setup():
    print("In Setup")
    ser=serial.Serial(0)
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #ser.timeout = None          #block read
    ser.timeout = 1            #non-block read
    #ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2     #timeout for write

    try: 
        ser.open()
    except Exception:
        print ("error open serial port: ")
        exit()

def protocol(theMode,r=0,g=0,b=0,delay=0,repeat=0):
    print("Protocol to ", theMode,r,g,b,delay,repeat)
    startBit=3
    mode=109
    endBit=3

    if theMode < 5: # auto mode just command
        print("")
        length=2
        decarray=[startBit,length,mode,theMode,endBit]
    elif theMode == 5:
        print("")
        length=5
        decarray=[startBit,length,mode,theMode,r,g,b,endBit]
    else:
        length=7 
        decarray=[startBit,length,mode,theMode,r,g,b,delay,repeat,endBit]
      
    hexarray=[hex(c) for c in decarray]
    strcmd=bytes(decarray).hex()
    print(strcmd)

    exit()

    send(strcmd)
    time.sleep(0.5)
    numLines=0
    while True:
        response=ser.readline()
        print("read data:" + response)
        numLines=numLines+1

        if (numLines > 3):
            break
        


def send(theString):
    if ser.isOpen():
        ser.write(theString)
    else:
        print("The serial port is not open")        

def close():
    try:
        ser.close()
    except Exception:
        print("Error closing serial bus")    
            

if __name__ == "__main__":
    import sys;
    import argparse
    parser=argparse.ArgumentParser()

    print("Welcome to SCM Lightbox controler")
    #setup()

    ''' options are -a 1-4 
                    -m r,g,b values in integer
                    -c r,g,b,delay,repeat in integer '''

    parser.add_argument('-a',
                        "--auto",
                        dest="auto",
                        action="store",type=int)           

    parser.add_argument('-s',
                        "--static",
                        dest="static",
                        nargs="+",type=int)           

    parser.add_argument('-b',
                        "--blinking",
                        dest="blinking",
                        nargs="+",type=int)     
    
    args=parser.parse_args() 
    if args.auto:
        print("Auto mode",args.auto)
        setup()
        protocol(args.auto)

    if args.static:
        print("static mode",args.static)
        print(args.static[1])
        setup()
        protocol(5,r=args.static[0],g=args.static[1],b=args.static[2])

    if args.blinking:
        print("blinking mode",args.blinking)
        setup()
        protocol(5,r=args.blinking[0],g=args.blinking[1],b=args.blinking[2],delay=args.blinking[3],repeat=args.blinking[4])

    print ("Entered"  )  
    
