#! /usr/bin/python3

import ev3
import ev3_commands

import time

mac_address = ev3_commands.read_mac_address()


e=ev3_commands.EV3Command(protocol=ev3.BLUETOOTH, host=mac_address)

a=0
#Parameter a gibt Anzahl von Hin- und Herfahren an

listedt=[]
listew1=[]
listew2=[]
datenpunkte=16
startzeit=time.time()
#Das Hin-und Herfahren

e.drive_with_turn(100,200)
time.sleep(0.2)
while a<16:
    (w1,w2) = e.get_wheel_position()
    t=time.time()
    dt=t-startzeit
    print(dt)
    listedt.append(dt)
    print("w1=%4d, w2=%4d" %(w1,w2))
    listew1.append(w1)
    listew2.append(w2)
    time.sleep(0.01)
    a=a+1
    #e.drive_with_turn(-100,200)
    #time.sleep(1)
    #(w1,w2) = e.get_wheel_position()
    #print("w1=%4d, w2=%4d" %(w1,w2))
    #print("w1=%4d, w2=%4d" %(w1,w2))
print(listedt)
print(listew1)
print(listew2)
    
e.stop()
file = open("ergebnisse_wheelposition.txt","w")



x=0
while x<datenpunkte:
    #auf Textdatei wird die gesamte Liste listea angezeigt
    text=str(listedt[x])+" "+ str(listew1[x])+" "+str(listew2[x])
    file.write(text)
    file.write("\n")
    x=x+1

file.close()

#Messreihe Motor
