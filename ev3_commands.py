#! /usr/bin/python3

import ev3 # includes lots of other stuff


class EV3Command(ev3.EV3):
    # __init__ is used from base class EV3
    """
    EV3Command implements some commands of the EV3
    """

    def beep(self):
        """Produce a beep with 440 hz at volume 20 for 1 second."""
        self.play_tone(440,1000,20)
        return

    def play_tone(self,frequency,duration,vol=50):
        """Play a tone with the specified frequency, duration in seconds,
        and volume.
        """
        milli_seconds = int(duration*1000)
        # TODO: check possible frequency range
        # TODO: check input for ranges
        ops=b''.join([ev3.opSound,ev3.TONE,ev3.LCX(vol),ev3.LCX(frequency),
                      ev3.LCX(milli_seconds),])
        self.send_direct_cmd(ops)
        return

