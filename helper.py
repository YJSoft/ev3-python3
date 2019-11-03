import ev3, ev3_sound, ev3_vehicle
from task import STATE_STOPPED
import traceback, struct
from time import time

my_ev3 = ev3.EV3(protocol=ev3.BLUETOOTH, host='00:16:53:4f:28:a6')
my_vehicle = ev3_vehicle.TwoWheelVehicle(radius_wheel=0.056,tread=0.028,ev3_obj=my_ev3)
