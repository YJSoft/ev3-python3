#-*- coding: utf-8 -*-

import struct
import time
import bluetooth
import pexpect
import subprocess
import sys
import socket

class Bluetoothctl:
    def __init__(self):
        out = subprocess.check_output("sudo rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", echo = False, encoding='utf-8')
        self.get_output("pairable on",1)
        self.get_output("agent NoInputNoOutput",1)
        self.get_output("default-agent",1)
        self.get_output("scan on")

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)
        return self.child.before.split("\r\n")

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            print("Try to pair with ",mac_address)
            out = self.get_output("pair " + mac_address, 10)
            print(out)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Request PIN code", pexpect.EOF])
            if res == 1:
                print("PIN should be 1234 in order to connect..")
                out = self.get_output("1234", 4)
            else:
                return False

            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            if res == 1:
                print("Pairing is done!")
                return True
            else:
                print("Pairing failed...")
                return False

    def autoconnect(self):
        print("Connecting to nearby EV3...")
        retry_cnt = 0
        while True:
            found = 0
            num = 0
            nearby_devices=bluetooth.discover_devices(duration=15)
            for i in nearby_devices:
                print(i)
                if bluetooth.lookup_name(i) == 'MyEV3':
                    self.addr = nearby_devices[num]
                    found = 1
                else:
                    if nearby_devices[num][0:8] == '00:16:53' and found==0:
                        self.addr = nearby_devices[num]
                        found = 1
                num += 1

            if found == 1:
                print('You have selected', bluetooth.lookup_name(self.addr))
                try:
                    self.pair(self.addr)
                    print('Connect Success')
                    break
                    
                except bluetooth.btcommon.BluetoothError as err:
                    print('Not Connect')
                    pass
            else:
                retry_cnt = retry_cnt + 1
                print("EV3 not found. retrying... (",retry_cnt,"/ 10 )")
                if retry_cnt > 10:
                    self.addr = None
                    self._sock = None
                    self.error = "CannotFindEV3"
                    return
                else:
                    time.sleep(5)
        return self.addr
