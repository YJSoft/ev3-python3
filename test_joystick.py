#! /usr/bin/python3

import ev3
import ev3_commands

import time

from sfml import sf

mac_address = ev3_commands.read_mac_address()

print("mac = "+mac_address)

e=ev3_commands.EV3Command(protocol=ev3.BLUETOOTH, host=mac_address)

e.verbosity=0

# the joystick
j = sf.Joystick

# test beep

# play some tones
e.play_tone(256,0.3,1)
time.sleep(0.4)

#time.sleep(2)

# test motors

pos=e.get_wheel_position()
print("wheel position = "+str(pos))


while True:
    j.update()
    v = j.get_axis_position(0, 0)
    v = int(v)
    print('%d' % v)
    e.drive_with_turn(v,200)
    time.sleep(0.05)

#e.drive_with_turn(-100,200)
#time.sleep(1)
#e.drive_with_turn(100,200)
#time.sleep(1)
#e.drive_with_turn(-100,200)
#time.sleep(1)
#e.drive_with_turn(0,200)
#time.sleep(1)






