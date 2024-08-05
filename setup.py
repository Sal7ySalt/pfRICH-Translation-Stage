import serial
import time
from binascii import unhexlify

def setup():

    #open serial port
    #For Linux
    # use 'dmesg | grep tty' to find serial port
    # eventually need to change permissions for /dev/tty*
    # uncomment the following lines
    ser=serial.Serial('/dev/ttyUSB0', baudrate=115200,bytesize=8,
                      parity=serial.PARITY_NONE,
                      stopbits=1,xonxoff=0,
                      rtscts=0,
                      timeout=1)  

    Channel = "01" #Channel is always 1 for a K Cube/T Cube
    ChanIdent = "0100" #Channel Ident if not in Header
    Destination = "50" #Destination; 50 for T Cube/K Cube, USB controllers
    DestinationI = "D0" #Logic Or Destination; D0 for T Cube/K Cube, USB controllers
    Source = "01" #Source
    Device_Unit_SF = 34304.96 #pg 34 of protocal PDF (as of Issue 23)
    Device_Unit_Vel = 772981.3692
    Device_Unit_Acc = 263.8443072


    print(ser.is_open)
    ser.flushInput()
    ser.flushOutput()

    command = bytearray([0x23, 0x02, 0x00, 0x00, 0x50, 0x01])  # MGMSG_MOD_IDENTIFY
    ser.write(command)
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)
    print("test1")

    ser.write(bytearray([0x10, 0x02, 0x01, 0x01, 0x50, 0x01]))  # MGMSG_MOD_SET_CHANENABLESTATE
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)
    print("test2")
