#! /usr/bin/python3

import ev3
import ev3_commands

import time

mac_address = ev3_commands.read_mac_address()

print("mac = "+mac_address)

e=ev3_commands.EV3Command(protocol=ev3.BLUETOOTH, host=mac_address)

# e.verbosity=1

# test beep

# play some tones
e.play_tone(256,0.1,1)
time.sleep(0.2)
e.play_tone(320,0.1,1)
time.sleep(0.2)
e.play_tone(384,0.1,1)
time.sleep(0.2)
e.play_tone(512,0.1,1)
time.sleep(0.2)

# time.sleep(2)

# test motors

pos=e.get_wheel_position()
print("wheel position = "+str(pos))
(a,b)=e.get_gyro_data()
print("a="+str(a)+", b="+str(b))

e.drive_with_turn(10,200)
time.sleep(2)
e.drive_with_turn(30,200)
time.sleep(1)
pos=e.get_wheel_position()
print("wheel position = "+str(pos))
e.stop(False)
(a,b)=e.get_gyro_data()
print("a="+str(a)+", b="+str(b))
pos=e.get_wheel_position()
print("wheel position = "+str(pos))
time.sleep(2)
e.drive_with_turn(-70,200)
time.sleep(1)
e.stop(True)
pos=e.get_wheel_position()
print("wheel position = "+str(pos))
time.sleep(0.5)


for i in range(300):
    b=e.get_gyro_rate()
    print("b="+str(b)+", type="+str(type(b)))
    time.sleep(0.2)


