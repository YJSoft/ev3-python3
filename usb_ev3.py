from os import system
import ev3
from ev3 import BLUETOOTH
from ev3 import USB
from ev3_sound import Jukebox as music
from ev3_vehicle import TwoWheelVehicle as car
from time import sleep
from flask import Flask
import traceback
from autopair import Bluetoothctl
from sys import exit
import struct

PORT_A                    = 1
PORT_B                    = 2
PORT_C                    = 4
PORT_D                    = 8
PORTS_ALL                 = 15
FORWARD                   = 20
BACKWARD                  = -20
TURN                      = 8

wwwapp = Flask(__name__)
bt = Bluetoothctl()
#addr = bt.autoconnect()
addr = None

def setPort(port,both):
    if both:
        if port == 0:
            hw_ctl.port_left = PORT_A
            hw_ctl.port_right = PORT_D
        else:
            hw_ctl.port_left = PORT_B
            hw_ctl.port_right = PORT_C
    else:
        hw_ctl._port_left = 0
        hw_ctl.port_right = port

@wwwapp.route("/")
def rootpage():
    return "EV3 WWW Gateway v0.3 by Robogram"

# TODO : Convert legacy function to new one
@wwwapp.route("/led/<color>")
def cmd_led(color):
    try:
        my_ev3.ev3_led(color)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success-Legacy"

# TODO : Convert legacy function to new one
@wwwapp.route("/tone/<hz>/<time>/<vol>")
def cmd_tone(hz, time, vol):
    try:
        my_ev3.tone(vol, hz, time)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success-Legacy"

@wwwapp.route("/move/<port>/<speed>")
def cmd_move(port, speed, direction):
    try:
        port = int(port)
        speed = int(speed)
        direction = int(direction)
        setPort(port,False)
        hw_ctl.move(speed,0)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/moveSync/<port>/<speed>/<direction>")
def cmd_moveSync(port, speed, direction):
    try:
        port = int(port)
        speed = int(speed)
        direction = int(direction)
        if port < 0 or port > 1:
            port = 0
        setPort(port,True)
        hw_ctl.move(speed,direction)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/forward/<port>/<speed>")
def cmd_forward(port,speed):
    try:
        port = int(port)
        speed = int(speed)
        if speed < 0:
            speed *= -1
        if port < 0 or port > 1:
            port = 0
        setPort(port,True)
        hw_ctl.move(speed,0)
        #ev3.tone(1,262,500)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/forward/<speed>")
def cmd_forward_ad(speed):
    return cmd_forward(0, speed)

@wwwapp.route("/backward/<port>/<speed>")
def cmd_backward(port, speed):
    try:
        port = int(port)
        speed = int(speed)
        if speed > 0:
            speed *= -1
        if port < 0 or port > 1:
            port = 0
        setPort(port,True)
        hw_ctl.move(speed,0)
        #ev3.tone(1,294,500)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/backward/<speed>")
def cmd_backward_ad(speed):
    return cmd_backward(0, speed)

@wwwapp.route("/stop")
def cmd_stop():
    try:
        hw_ctl.port_left = PORT_A
        hw_ctl.port_right = PORT_D
        hw_ctl.stop(True)
        hw_ctl.port_left = PORT_B
        hw_ctl.port_right = PORT_C
        hw_ctl.stop(True)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/stop/<port>")
def cmd_stop_with_port(port):
    try:
        port = int(port)
        setPort(port,0)
        hw_ctl.stop(True)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/left/<port>/<speed>")
def cmd_left(port, speed):
    try:
        port = int(port)
        speed = int(speed)
        if speed < 0:
            speed *= -1
        if port < 0 or port > 1:
            port = 0
        setPort(port,True)
        hw_ctl.move(speed,-200)
        #ev3.tone(1,330,500)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/left/<speed>")
def cmd_left_ad(speed):
    return cmd_left(0, speed)

@wwwapp.route("/right/<port>/<speed>")
def cmd_right(port, speed):
    try:
        port = int(port)
        speed = int(speed)
        if speed < 0:
            speed *= -1
        if port < 0 or port > 1:
            port = 0
        setPort(port,True)
        hw_ctl.move(speed,200)
        #ev3.tone(1,349,500)
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500
    return "Success"

@wwwapp.route("/right/<speed>")
def cmd_right_ad(speed):
    return cmd_right(0, speed)

@wwwapp.route("/touch/<port>")
def cmd_get_touch(port):
    try:
        port = int(port)
        if port > 4 or port < 1:
            port = 1
        port -= 1
        ops_read = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.LCX(port),  # NO
            ev3.LCX(16), # TYPE - EV3-Touch
            ev3.LCX(0),  # MODE - Touch
            ev3.LCX(1),  # VALUES
            ev3.GVX(0),  # VALUE1
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.LCX(port),  # NO
            ev3.LCX(16), # TYPE - EV3-Touch
            ev3.LCX(1),  # MODE - Bump
            ev3.LCX(1),  # VALUES
            ev3.GVX(4)   # VALUE1
        ])
        reply = my_ev3.send_direct_cmd(ops_read, global_mem=8)
        (touched, bumps) = struct.unpack('<ff', reply[5:])

        if touched == 1:
            return "Success-True", 200
        else:
            return "Success-False", 200
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500

@wwwapp.route("/ultra/<port>")
def get_ultra(port):
    try:
        port = int(port)
        if port > 4 or port < 1:
            port = 1
        port -= 1
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.LCX(port),  # NO
            ev3.LCX(30), # TYPE - EV3-Ultrasonic
            ev3.LCX(0),  # MODE - Cm
            ev3.LCX(1),  # VALUES
            ev3.GVX(0)   # VALUE1
        ])
        reply = my_ev3.send_direct_cmd(ops, global_mem=4)
        return str(struct.unpack('<f', reply[5:])[0])
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500

@wwwapp.route("/color/<port>")
def get_color(port):
    try:
        port = int(port)
        if port > 4 or port < 1:
            port = 1
        port -= 1
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.LCX(port),  # NO
            ev3.LCX(29), # TYPE - EV3-Color
            ev3.LCX(2),  # MODE -Color
            ev3.LCX(1),  # VALUES
            ev3.GVX(0)   # VALUE1
        ])
        reply = my_ev3.send_direct_cmd(ops, global_mem=4)
        return str(struct.unpack('<f', reply[5:])[0])
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500

@wwwapp.route("/light/<port>")
def get_light(port):
    try:
        port = int(port)
        if port > 4 or port < 1:
            port = 1
        port -= 1
        ops = b''.join([
            ev3.opInput_Device,
            ev3.READY_SI,
            ev3.LCX(0),  # LAYER
            ev3.LCX(port),  # NO
            ev3.LCX(29), # TYPE - EV3-Color
            ev3.LCX(0),  # MODE -
            ev3.LCX(1),  # VALUES
            ev3.GVX(0)   # VALUE1
        ])
        reply = my_ev3.send_direct_cmd(ops, global_mem=4)
        return str(struct.unpack('<f', reply[5:])[0])
    except Exception as e:
        return "Failure<pre>" + traceback.format_exc() + "</pre>", 500


if __name__ == '__main__':
    if addr == None:
        print("EV3 BT Failed! Trying USB...")
        try:
            my_ev3 = ev3.EV3(protocol=ev3.USB)
        except Exception:
            exit("EV3 Not Detected! Cannot continue...")
    else:
        my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host=addr)
    sw_ctl = music(ev3_obj=my_ev3)
    hw_ctl = car(ev3_obj=my_ev3,radius_wheel=0.056,tread=0.024)
    wwwapp.run(host='0.0.0.0', port=8088)
