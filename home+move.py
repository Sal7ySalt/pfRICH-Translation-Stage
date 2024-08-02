import serial
import time
from binascii import unhexlify

def main():

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

    print("Move")

    #Set Velocity; MGMSG_MOT_SET_VELPARAMS
    Velocity = "1304"
    MinVelocity = 0 #mm/s
    Acceleration = 0.5 #mm/s²
    MaxVelocity = 0.5 #mm/s

    MinVelocityDU = round(Device_Unit_Vel * MinVelocity)
    AccelerationDU = round(Device_Unit_Acc * Acceleration)
    MaxVelocityDU = round(Device_Unit_Vel * MaxVelocity)

    ser.write(unhexlify(Velocity + "0E00" + DestinationI + Source + ChanIdent) + MinVelocityDU.to_bytes(4, byteorder="little") + AccelerationDU.to_bytes(4, byteorder="little") + MaxVelocityDU.to_bytes(4, byteorder="little"))

    AbsDistance = 20 #mm
    AbsDistanceDU = round(Device_Unit_SF * AbsDistance)

    #Move Stage; MGMSG_MOT_MOVE_ABSOLUTE
    Move = "5304"
    ser.write(unhexlify(Move + "0600" + DestinationI + Source + ChanIdent) + AbsDistanceDU.to_bytes(4, byteorder="little"))

    print("Starting to leep")
    time.sleep(10)
    print("Finished Sleeping")

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
    main()

