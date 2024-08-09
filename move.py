import serial
import time
from binascii import unhexlify
from setup import setup
from getposition import getposition

def move():

    setup()
    
    #Set Velocity; MGMSG_MOT_SET_VELPARAMS
    Velocity = "1304"
    MinVelocity = 0 #mm/s
    Acceleration = 1 #mm/s²
    MaxVelocity = 1.5 #mm/s
    
    MinVelocityDU = round(Device_Unit_Vel * MinVelocity)
    AccelerationDU = round(Device_Unit_Acc * Acceleration)
    MaxVelocityDU = round(Device_Unit_Vel * MaxVelocity)
    
    ser.write(unhexlify(Velocity + "0E00" + DestinationI + Source + ChanIdent) + MinVelocityDU.to_bytes(4, byteorder="little") + AccelerationDU.to_bytes(4, byteorder="little") + MaxVelocityDU.to_bytes(4, byteorder="little"))
    
    AbsDistance = 20 #mm
    AbsDistanceDU = round(Device_Unit_SF * AbsDistance)
    
    #Move Stage; MGMSG_MOT_MOVE_ABSOLUTE
    Move = "5304"
    print("Moving Stage")
    ser.write(unhexlify(Move + "0600" + DestinationI + Source + ChanIdent) + AbsDistanceDU.to_bytes(4, byteorder="little"))
    
    #Confirm stage moved before advancing; MGMSG_MOT_MOVE_COMPLETED
    Rx = ''
    Completed = unhexlify("6404")
    while Rx != Completed:
        Rx = ser.read(2)
    print('Finished Moving')
    ser.flushInput()
    ser.flushOutput()
    
    getposition()
    
    #Disable Stage; MGMSG_MOD_SET_CHANENABLESTATE
    Enable = "1002"
    State = "02"
    ser.write(unhexlify(Enable + Channel + State + Destination + Source))
    
    
    ser.close()


if __name__ == "__main__":
    move()
