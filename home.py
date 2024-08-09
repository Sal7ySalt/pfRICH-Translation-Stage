import serial
import time
from binascii import unhexlify
from setup import setup
from getposition import getposition

def home():

    setup()
    
    #Home Stage; MGMSG_MOT_MOVE_HOME
    Home = "4304"
    print("Homing")
    ser.write(unhexlify(Home + Channel + "00" + Destination + Source))
    
    #Confirm stage homed before advancing; MGMSG_MOT_MOVE_HOMED
    Rx = ''
    Homed = unhexlify("4404")
    while Rx != Homed:
        Rx = ser.read(2)
    print('Stage Homed')
    ser.flushInput()
    ser.flushOutput()
    
    getposition()
    
    #Disable Stage; MGMSG_MOD_SET_CHANENABLESTATE
    Enable = "1002"
    State = "02"
    ser.write(unhexlify(Enable + Channel + State + Destination + Source))
    
    
    ser.close()


if __name__ == "__main__":
    home()
    
