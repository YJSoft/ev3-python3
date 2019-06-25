import ev3
import struct

def testSensor(my_ev3, s_no, s_type, s_mode):
    ops = b''.join([
        ev3.opInput_Device,
        ev3.READY_SI,
        ev3.LCX(0),          # LAYER
        ev3.LCX(s_no),       # NO
        ev3.LCX(s_type),     # TYPE
        ev3.LCX(s_mode),     # MODE
        ev3.LCX(1),          # VALUES
        ev3.GVX(0)           # VALUE1
    ])

    reply = my_ev3.send_direct_cmd(ops, global_mem=4)
    return struct.unpack('<f', reply[5:])[0]
