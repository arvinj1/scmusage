#!/usr/bin/python

import serial,time
from enum import Enum

ser=None
munge=False
keepFlashing=False
oldVoltage=False

class ColorModes(Enum):
    Auto1=1
    Rainbow1=2
    Auto2=3
    Rainbow2=4
    Manual=5
    Blink=6



def setup(dev='/dev/ttyS1'):
    global ser
    print("In Setup",dev)
    ser=serial.Serial()
    ser.port=dev
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
        if ser.is_open == False:
            ser.open()
    except Exception as ex:
        print ("error open serial port: ")
        print(ex)
        #exit()

def demoProtocol2():
    global ser
    if ser.is_open == False:
        print("Serial port is not open")
        return

    packet=bytearray()
    packet.append(0x2)
    packet.append(0x7)
    packet.append(0x6d)
    packet.append(0x3)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0xFF)
    ''' blinking '''
    packet.append(0x20)
    packet.append(0x02)
    packet.append(0x3)

    ser.write(packet)

def reset():
    print('reset')
    global ser
    if ser.is_open == False:
        print("Serial port is not open")
        return

    packet=bytearray()
    packet.append(0x2)
    packet.append(0x5)
    packet.append(0x6d)
    packet.append(0x2)
    packet.append(0xFF)
    packet.append(0xFF)
    packet.append(0xFF)
    packet.append(0x3)

    ser.write(packet)
   
def demoProtocol(turnOn):
    print('demoProtocol')
    global ser
    if ser.is_open == False:
        print("Serial port is not open")
        return

    packet=bytearray()
    packet2=bytearray()
    packet.append(0x2)
    packet.append(0x5)
    packet.append(0x6d)
    packet.append(0x2)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0xFF)
    packet.append(0x3)
    
    packet2.append(0x2)
    packet2.append(0x5)
    packet2.append(0x6d)
    packet2.append(0x2)
    packet2.append(0xFF)
    packet2.append(0xFF)
    packet2.append(0xFF)
    packet2.append(0x3)

    if turnOn:
        loop=1
        while loop < 31:
                ser.write(packet)
                time.sleep(0.5)
                ser.write(packet2)
                time.sleep(0.5)
                loop=loop+1

        ser.write(packet2)
    else:
        ser.write(packet2) 
    
    
def protocol(theMode,r=0,g=0,b=0,delay=0,repeat=0):
    print("Protocol to ", theMode,r,g,b,delay,repeat)
    startBit=2
    mode=109
    endBit=3

    if theMode < 5: # auto mode just command
        print("")
        length=2
        decarray=[startBit,length,mode,theMode,endBit]
    elif theMode == 5:
        print("")
        length=5
        decrray=[startBit,length,mode,theMode,r,g,b,endBit]
    else:
        length=7 
        decarray=[startBit,length,mode,theMode,r,g,b,delay,repeat,endBit]
     
    decarray=[2,5,109,2,2,0,0,255,3] 
    hexarray=[hex(c) for c in decarray]
    strcmd=bytes(decarray).hex()

    sendBytes(r,g,b)
    time.sleep(0.5)
    numLines=0
    while True:
        response=ser.readline()
        s=response.decode()
        print(type(s),"...",s)

        numLines=numLines+1

        if (numLines > 3):
            break
        

def sendBytes(r=0,g=55,b=55):
    global ser
    packet=bytearray()
    packet.append(0x2)
    packet.append(0x5)
    packet.append(0x6d)
    if oldVoltage:
        packet.append(0x5)
    else:
        packet.append(0x2)
    if munge == False:
        print("non munge mode")   
        packet.append(0x00)
        packet.append(0xFF)
        packet.append(0xFF)
    else:
        print("munge mode")   
        print ("Sending ", r, ",", g,',',b)
        packet.append(r)
        packet.append(g)
        packet.append(b)
    packet.append(0x3)
    print(packet)
    if ser.is_open:
        ser.write(packet)
    else:
        print("The serial port is not open")        
    
def send(theString):
    global ser
    if ser.is_open:
        ser.write(theString.encode())
    else:
        print("The serial port is not open")        

def close():
    global ser
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
                    -c r,g,b,delay,repeat in integer
                    -d dev 
		    -x munge to true'''

    parser.add_argument('-a',
                        "--auto",
                        dest="auto",
                        action="store",type=int)           
    parser.add_argument('-x',
                        "--munge",
                        dest="munge",
                        action="store_true")           
   
    parser.add_argument('-d',
                        "--dev",
                        dest="dev",
                        action="store")           
                    

    parser.add_argument('-s',
                        "--static",
                        dest="static",
                        nargs="+",type=int)           

    parser.add_argument('-b',
                        "--blinking",
                        dest="blinking",
                        nargs="+",type=int)     

    parser.add_argument('-v',
                        "--voltage",
                        dest="voltage",
			action="store",type=int)

    parser.add_argument('-l',
                        "--lbon",
                        dest="lbon",
			action="store",type=int)
                        
    
    parser.add_argument('-o',
                        "--lboff",
                        dest="lboff",
			action="store",type=int)
    args=parser.parse_args() 

    if args.voltage:
        oldVoltage = (args.voltage == 5)
    if args.lbon == 1:
        setup()
        demoProtocol(True)

    if args.lboff == 1:
        setup()
        reset()
       
    if args.munge:
        munge=args.munge
        print(munge,"==munge")
    
    if args.dev:
        dev=args.dev
        setup(dev)
    else:
        setup()
    if args.auto:
        print("Auto mode",args.auto)
        protocol(args.auto)

    if args.static:
        print("static mode",args.static)
        print(args.static[1])
        protocol(5,r=args.static[0],g=args.static[1],b=args.static[2])

    if args.blinking:
        print("blinking mode",args.blinking)
        protocol(5,r=args.blinking[0],g=args.blinking[1],b=args.blinking[2],delay=args.blinking[3],repeat=args.blinking[4])

    print ("Entered"  )  
    
