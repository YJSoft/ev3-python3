import ev3, ev3_sound, ev3_vehicle
from task import STATE_STOPPED
import traceback, struct
from time import time
from flask import Flask
wwwapp = Flask(__name__)

my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host='00:16:53:4f:28:a6')
my_music = ev3_sound.Jukebox(ev3_obj=my_ev3)
my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.056,tread=0.028,ev3_obj=my_ev3)

curLED = "N/A"
lastUltra = 0
curUltra = -1
curDirection = {"port_ad":"N/A", "port_bc":"N/A"}
curSpeed = {"port_ad":0, "port_bc":0}
curSong = None

def ultra(port):
    global lastUltra
    global curUltra
    if time() - lastUltra < 0.5:
        return curUltra
    ops = b''.join([
        ev3.opInput_Device,
        ev3.READY_SI,
        ev3.LCX(0),          # LAYER
        ev3.LCX(port),          # NO
        ev3.LCX(30),         # TYPE - EV3-IR
        ev3.LCX(0),          # MODE - Proximity
        ev3.LCX(1),          # VALUES
        ev3.GVX(0)           # VALUE1
    ])
    reply = my_ev3.send_direct_cmd(ops, global_mem=4)
    lastUltra = time()
    curUltra = struct.unpack('<f', reply[5:])[0]
    return curUltra

def led(color):
    global curLED
    if curLED != color:
        ops = b''.join([
            ev3.opUI_Write,
            ev3.LED,
            ev3.__dict__["LED_" + color]
        ])
        my_ev3.send_direct_cmd(ops)
        curLED = color

@wwwapp.route("/")
def rootpage():
    return "EV3 WWW Gateway v0.1 by Robogram!"

@wwwapp.route("/moveSync/<type>/<port>/<speed>")
def cmd_move(type, port, speed):
    global curDirection
    global curSpeed
    
    # if direction and speed are same, skip command send
    if curDirection[port] == type and curSpeed[port] == speed:
        return "Success-cached"
    try:
        # save last direction and speed
        curDirection[port] = type
        curSpeed[port] = speed
        
        speed = int(speed)
        my_vehicle.port_left = ev3.PORT_A
        my_vehicle.port_right = ev3.PORT_D
        if port == "port_bc":
            my_vehicle.port_left = ev3.PORT_B
            my_vehicle.port_right = ev3.PORT_C
        
        if type == "forward":
            my_vehicle.move(speed, 0)
        elif type == "backward":
            my_vehicle.move(speed * -1, 0)
        elif type == "left":
            my_vehicle.move(speed, 200)
        elif type == "right":
            my_vehicle.move(speed, -200)
        else:
            pass
    except:
        return "Failure<xmp>" + traceback.format_exc() + "</xmp>", 500
    return "Success"

@wwwapp.route("/sensor/<type>/<port>")
def cmd_sensor(type, port):
    try:
        port = int(port) - 1
        assert port >= 0 and port < 4, "Port number out of range"
        assert type == "ultra", "Not supported yet"
        
        return str(ultra(port))
    except:
        return "Failure<xmp>" + traceback.format_exc() + "</xmp>", 500
    return "Success"

@wwwapp.route("/led/<color>")
def cmd_led(color):
    try:
        assert "LED_" + color in ev3.__dict__, "Invalid color id"
        led(color)
    except:
        return "Failure<xmp>" + traceback.format_exc() + "</xmp>", 500
    return "Success"

@wwwapp.route("/tone/<hz>/<time>/<vol>")
def cmd_tone(hz, time, vol):
    try:
        my_music.volume = int(vol)
        try:
            parsed_hz = int(hz)
        except ValueError:
            parsed_hz = hz
        my_music.play_tone(parsed_hz, float(time) / 1000)
    except:
        return "Failure<xmp>" + traceback.format_exc() + "</xmp>", 500
    return "Success"

@wwwapp.route("/song/<name>/<vol>")
def cmd_song(name, vol):
    global curSong
    try:
        if curSong is not None and curSong.state !== STATE_STOPPED:
            curSong.stop()
        my_music.volume = int(vol)
        curSong = my_music.song(ev3_sound.__dict__[name])
        curSong.start()
    except:
        return "Failure<xmp>" + traceback.format_exc() + "</xmp>", 500
    return "Success"
    
if __name__ == '__main__':
    wwwapp.run(host='0.0.0.0', port=8088)
