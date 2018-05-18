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

tolerance = 7
tolerance2 = 12
anzahlgrenze = 30

k=-0.7

# pos=e.get_wheel_position()
# print("wheel position = "+str(pos))
anzahl=0
anzahl2=0

e.drive_with_turn(100,200)
time.sleep(0.6)
e.drive_with_turn(-100,200)
time.sleep(0.6)
e.drive_with_turn(10,200)
e.play_tone(512,0.1,1)
time.sleep(0.5)


while True:
    j.update()
    v = j.get_axis_position(0, 0)
    #v = int(v)
    rate=e.get_gyro_rate()
    v += k*rate
    v=int(v)
    if v>100:
        v=100
    if v<-100:
        v=-100
    if -5 <= v and v <= 5:
        v=0
    milli_seconds=int(time.time()*1000)%(60*1000)
    print('v=%4d, rate=%4d ms=%5d' % (v,rate,milli_seconds) )
    if v==0:
        e.drive_with_turn(0,200)
        e.stop(False)
    else:
            
        e.drive_with_turn(v,200)
    time.sleep(0.01)
    
    if -tolerance<=rate and rate<=tolerance:
        anzahl=anzahl+1
    else:
        anzahl=0
    if rate > tolerance2 or rate < -tolerance2:
        anzahl2=anzahl2+1
    
    if anzahl==anzahlgrenze and anzahl2>=10:
        print('Du hast es geschafft! Das Pendel steht still.')
        e.play_tone(256,0.3,1)
        anzahl2=0
        
        
        
#e.drive_with_turn(-100,200)
#time.sleep(1)
#e.drive_with_turn(100,200)
#time.sleep(1)
#e.drive_with_turn(-100,200)
#time.sleep(1)
#e.drive_with_turn(0,200)
#time.sleep(1)


    








