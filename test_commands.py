#! /usr/bin/python3

import ev3_commands

import time

mac_address = ev3_commands.read_mac_adress()

e=ev3_commands.EV3Command(protocol=ev3.BLUETOOTH, host=mac_address)

e.verbosity=1

# test beep
e.beep()
time.sleep(2)

# play some tones
e.play_tone(256,0.3,1)
time.sleep(0.1)
e.play_tone(320,0.3,1)
time.sleep(0.1)
e.play_tone(384,0.3,1)
time.sleep(0.1)
e.play_tone(256,0.6,20)
time.sleep(0.2)

time.sleep(2)

# test motors

e.drive_with_turn(10,200)
time.sleep(2)
e.drive_with_turn(30,200)
time.sleep(1)
e.stop(False)

