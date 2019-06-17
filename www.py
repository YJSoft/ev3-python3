import ev3, ev3_sound, ev3_vehicle
from flask import Flask
wwwapp = Flask(__name__)

my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host='00:16:53:4f:28:a6')
my_music = ev3_sound.Jukebox(ev3_obj=my_ev3)
my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.056,tread=0.028,ev3_obj=my_ev3)

@wwwapp.route("/")
def rootpage():
    return "EV3 WWW Gateway v0.1 by Robogram!"

@wwwapp.route("/moveSync/<type>/<port>/<speed>")
def cmd_move(type, port, speed):
    try:
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
    except Exception:
        return "Failure"
    return "Success"
    
if __name__ == '__main__':
    wwwapp.run(host='0.0.0.0', port=8088)
