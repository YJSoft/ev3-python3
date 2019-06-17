from ev3 import EV3
from flask import Flask
wwwapp = Flask(__name__)

ev3 = EV3()

@wwwapp.route("/")
def rootpage():
    return "VoiceModule v0.1 by Robogram!"

@wwwapp.route("/moveSync/<type>/<port>/<speed>")
def cmd_move(type, port, speed):
    try:
        pass
    except Exception:
        return "Failure"
    return "Success"
    
if __name__ == '__main__':
    wwwapp.run(host='0.0.0.0', port=8088)
