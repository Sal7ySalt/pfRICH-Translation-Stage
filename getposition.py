import serial
import time
from binascii import unhexlify
from setup import setup


def getposition():

    setup()

    #Get Position; MGMSG_MOT_REQ_USTATUSUPDATE
    Status = "9004"
    ser.write(unhexlify(Status + Channel + "00" + Destination + Source))
    
    Rx = ser.read(20)
    
    Position = Rx[8:12]
    
    PositionDU = int.from_bytes(Position, "little")
    print("Position:", PositionDU, "Device Units" )
    PositionRU = PositionDU / 34304
    print("Position:", PositionRU, "mm")


if __name__ == "__main__":
  getposition()
