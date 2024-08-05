import serial
import time
from binascii import unhexlify
from setup.py import setup

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
    
    #Get Position; MGMSG_MOT_REQ_USTATUSUPDATE
    Status = "9004"
    ser.write(unhexlify(Status + Channel + "00" + Destination + Source))
    
    Rx = ser.read(20)
    
    Position = Rx[8:12]
    
    PositionDU = int.from_bytes(Position, "little")
    print("Position:", PositionDU, "Device Units" )
    PositionRU = PositionDU / 34304
    print("Position:", PositionRU, "mm")
    
    #Disable Stage; MGMSG_MOD_SET_CHANENABLESTATE
    Enable = "1002"
    State = "02"
    ser.write(unhexlify(Enable + Channel + State + Destination + Source))
    
    
    ser.close()


if __name__ == "__main__":
    home()
    
