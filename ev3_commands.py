#! /usr/bin/python3

import ev3 
import struct

def read_mac_address():
    # read MAC ADDRESS from file (in gitignore)
    f=open("MAC_ADDRESS","r")
    mac=f.read().strip()
    f.close()
    if len(mac)!=2*6+5:
        raise Exception("file MAC_ADDRESS has wrong format")
    return mac

class EV3Command(ev3.EV3):
    # __init__ is used from base class EV3
    """
    EV3Command implements some commands of the EV3
    """

    def beep(self) -> None:
        """Produce a beep with 440 hz at volume 20 for 1 second."""
        self.play_tone(440,1000,20)

    def play_tone(self,frequency:int ,duration: float,vol=50) -> None:
        """Play a tone with the specified frequency, duration in seconds,
        and volume.
        """
        milli_seconds = int(duration*1000)
        # TODO: check possible frequency range
        # TODO: check if input is valid, convert to int if necessary
        ops=b''.join([ev3.opSound,ev3.TONE,ev3.LCX(vol),ev3.LCX(frequency),
                      ev3.LCX(milli_seconds),])
        self.send_direct_cmd(ops)

    def drive_with_turn(self,speed: int, turn: int):
        """
        Start unlimited movement of the vehicle

        Arguments:
        speed: speed in percent [-100 - 100]
          > 0: forward
          < 0: backward
        turn: type of turn [-200 - 200]
          -200: circle right on place
          -100: turn right with unmoved right wheel
           0  : straight
           100: turn left with unmoved left wheel
           200: circle left on place
        """
        assert self._sync_mode != ev3.SYNC, \
                'no unlimited operations allowed in sync_mode SYNC'
        assert isinstance(speed, int), \
                'speed needs to be an integer value'
        assert -100 <= speed and speed <= 100, \
                "speed needs to be in range [-100 - 100]"
        assert isinstance(turn, int), \
                'turn needs to be an integer value'
        assert -200 <= turn and turn <= 200, \
                'turn needs to be in range [-200 - 200]'
        ports = ev3.PORT_A+ev3.PORT_D
        ops = b''.join([
            ev3.opOutput_Step_Sync,
            ev3.LCX(0),              # LAYER
            ev3.LCX(ports),          # NOS
            ev3.LCX(speed),
            ev3.LCX(turn),
            ev3.LCX(0),              # STEPS
            ev3.LCX(0),              # BRAKE
            ev3.opOutput_Start,
            ev3.LCX(0),              # LAYER
            ev3.LCX(ports)           # NOS
        ])
        self.send_direct_cmd(ops)


    def stop(self, brake: bool=False) -> None:
        """
        Stop movement of the vehicle

        Arguments:
        brake: flag if activating brake
        """
        assert isinstance(brake, bool), "brake needs to be a boolean value"
        if brake:
            brake_int = 1
        else:
            brake_int = 0
        ports = ev3.PORT_A+ev3.PORT_D
        ops = b''.join([
            ev3.opOutput_Stop,
            ev3.LCX(0),                                  # LAYER
            ev3.LCX(ports), # NOS
            ev3.LCX(brake_int)                           # BRAKE
        ])
        self.send_direct_cmd(ops)

    def drive_motor(self,speed:int,port:str) -> None :
        # TODO
        pass

    def reset_wheel_position(self) -> None :
        # TODO
        pass

    def get_wheel_position(self) -> int:
        # TODO: eman{e reading as float
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_RAW,
            ev3.LCX(0),                         # LAYER
            ev3.port_motor_input(ev3.PORT_A),   # NO
            ev3.LCX(7),                         # TYPE - EV3-Large-Motor
            ev3.LCX(1),                         # MODE - Degree
            ev3.LCX(1),                         # VALUES
            ev3.GVX(0),                         # VALUE1
            ev3.opInput_Device,
            ev3.READY_RAW,
            ev3.LCX(0),                         # LAYER
            ev3.port_motor_input(ev3.PORT_B),   # NO
            ev3.LCX(7),                         # TYPE - EV3-Large-Motor
            ev3.LCX(0),                         # MODE - Degree
            ev3.LCX(1),                         # VALUES
            ev3.GVX(4)                          # VALUE1
        ])
        reply = self.send_direct_cmd(ops, global_mem=8)
        pos = struct.unpack('<ii', reply[5:])
        # pos has length 2
        return pos[0]

    def get_gyro_rate(self):
         ops = b''.join([
             ev3.opInput_Device,
             ev3.READY_RAW,
             ev3.LCX(0),                # LAYER
             ev3.LCX(1),       # NO ( port 2)
             ev3.LCX(32),      # TYPE - GYRO
             ev3.LCX(1),       # MODE - Gyro-Rate
             ev3.LCX(1),       # VALUES
             ev3.GVX(0),       # VALUE1
         ])
         reply = self.send_direct_cmd(ops, global_mem=4)
         pos = struct.unpack('<i',reply[5:])
         return pos[0]
        

    def get_gyro_data(self):
         ops = b''.join([
             ev3.opInput_Device,
             ev3.READY_RAW,
             ev3.LCX(0),                # LAYER
             ev3.LCX(3),       # NO ( port 4)
             ev3.LCX(32),      # TYPE - GYRO
             ev3.LCX(1),       # MODE - Gyro-Rate
             ev3.LCX(1),       # VALUES
             ev3.GVX(0),       # VALUE1
             ev3.opInput_Device,
             ev3.READY_RAW,
             ev3.LCX(0),       # LAYER
             ev3.LCX(3),       # NO ( port 4)
             ev3.LCX(32),      # TYPE - GYRO
             ev3.LCX(4),       # MODE - Gyro-Calibration
             ev3.LCX(1),       # VALUES
             ev3.GVX(4)        # VALUE1
         ])
         reply = self.send_direct_cmd(ops, global_mem=8)
#          print(reply)
         pos = struct.unpack('<ii', reply[5:])
         # pos has length 2
         return (pos[0],pos[1])

    def get_distance(self):
        # TODO
        return


