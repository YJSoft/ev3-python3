#! /usr/bin/python3

import ev3
import ev3_commands

import time

mac_address = ev3_commands.read_mac_address()


e=ev3_commands.EV3Command(protocol=ev3.BLUETOOTH, host=mac_address)


# test beep

# play some tones
e.play_tone(256,0.3,1)
time.sleep(0.4)
e.reset_gyro_angle()
startzeit=time.time()
i=0
datenpunkte=50
listea=[]
listeb=[]
listec=[]
while i<datenpunkte:
    # code
    (a,b) = e.get_gyro_angle_rate()
    listea.append(a)
    listeb.append(b)
    t=time.time()
    deltat=t-startzeit
    listec.append(deltat)
    print("a="+str(a)+", b="+str(b)+", deltat="+str(deltat))
    time.sleep(0.05)
    i = i+1
    
print(listea)
print(listeb)    
print(listec)


file = open("ergebnisse.txt","w")

x=0

while x<datenpunkte:
    #auf Textdatei wird die gesamte Liste listea angezeigt
    text=str(listea[x])+" "+ str(listeb[x])+" "+str(listec[x])
    file.write(text)
    file.write("\n")
    x=x+1

file.close()