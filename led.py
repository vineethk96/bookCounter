#!flask/bin/python3
#!/usr/bin/env python3

import logging
import socket
import sys
import LED_PWM
from time import sleep

from zeroconf import ServiceInfo, Zeroconf


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 80))
    IP = s.getsockname()[0]
    print(IP)
    

    desc = {'path': '/I<3Mo/'}

    info = ServiceInfo("_http._tcp.local.",
                       "Team7LED_Rpi._http._tcp.local.",
                       socket.inet_aton(IP), 80, 0, 0,
                       desc, "ash-2.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()


#******* F L A S K ****************

'''
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
'''
