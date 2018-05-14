#! /usr/bin/python3

import ev3 # includes lots of other stuff


class ev3_commands(ev3.EV3):
	# init should be copied from base class EV3

	def beep(self):
		""" produce a beep with 440 hz at volume 20 for 1 second"""
		ops=b''.join([ev3.opSound,ev3.TONE,ev3.LCX(20),ev3.LCX(440),ev3.LCX(1000),])
		self.send_direct_cmd(ops)

		return
	
