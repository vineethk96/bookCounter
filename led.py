#!flask/bin/python3
#!/usr/bin/env python3

import logging
import socket
import sys
import LED_PWM
from time import sleep

from zeroconf import ServiceInfo, Zeroconf


#********** F L A S K **********
from flask import Flask, jsonify, request

app = Flask(__name__)

LED_obj = LED_PWM.LED_PWM()

@app.route('/LED/on', methods=['POST'])
def LED_ON():
    return LED_obj.turnLED_ON()

@app.route('/LED/off', methods=['POST'])
def LED_OFF():
    return LED_obj.turnLED_OFF()

@app.route('/LED', methods=['POST'])
def LED():
    LEDDict = request.get_json()
    color = LEDDict["color"]
    intensity = LEDDict["intensity"]
    
    return LED_obj.changeIntensity(color, intensity)

@app.route('/LED/info', methods=['GET'])
def LED_INFO():
    return str(LED_obj.info())

#*******************************

if __name__ == '__main__':

#******************** Z E R O C O N F ********************

    # ping google to grab my IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 80))
    IP = s.getsockname()[0]    

    desc = {'path': ''}

    info = ServiceInfo("_http._tcp.local.",
                       "Team7LED_Rpi._http._tcp.local.",
                       socket.inet_aton(IP), 5000, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)

    # testing to look for zeroconf connection
    try:
        while True:
            sleep(0.1)
            
            #********** F L A S K **********
            app.run(host = IP, debug=True)

            
            #*******************************
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()



