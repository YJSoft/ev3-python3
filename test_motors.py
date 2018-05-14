#! /usr/bin/python3

import ev3

import ev3_vehicle

import time


def read_mac_address():
    # read MAC ADDRESS from file (in gitignore)
    f=open("MAC_ADDRESS","r")
    mac=f.read().strip()
    f.close()
    if len(mac)!=2*6+5:
        raise Exception("file MAC_ADDRESS has wrong format")


mac_address=read_mac_address()

e=ev3.EV3(protocol=ev3.BLUETOOTH, host=mac_address)

e.verbosity=1

ops=b''.join([ev3.opSound,ev3.TONE,ev3.LCX(1),ev3.LCX(440),ev3.LCX(1000),])

e.send_direct_cmd(ops)

# v=ev3_vehicle.TwoWheelVehicle(e)

v=ev3_vehicle.TwoWheelVehicle(0.02,0.02,ev3_obj=e)

v.move(10,0)

time.sleep(2)

v.stop()



