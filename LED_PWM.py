#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


class LED_PWM:

    # setup the GPIO pins for use
    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)

    # specify which ports are being used for what
    red   = GPIO.PWM(21, 100)      # red LED at 1000 Hz
    green = GPIO.PWM(20, 100)      # green LED at 1000 Hz
    blue  = GPIO.PWM(16, 100)      # blue LED at 1000 Hz

    # begin the PWM
    red.start(0)
    green.start(0)
    blue.start(0)

    # set the initial intensity values
    rInten = 0
    gInten = 0
    bInten = 0

    #set the status of the LED. It is initally off. 
    LED_status = False

    def __init__(self):
        return

    # flask API functions
    def turnLED_ON(self):
        self.red.ChangeDutyCycle(self.rInten)
        self.green.ChangeDutyCycle(self.gInten)
        self.blue.ChangeDutyCycle(self.bInten)
        self.LED_status = True
        return "LED on"

    def turnLED_OFF(self):
        self.red.ChangeDutyCycle(0)
        self.green.ChangeDutyCycle(0)
        self.blue.ChangeDutyCycle(0)
        self.LED_status = False
        return "LED off"

    def changeIntensity(self, color, intensity):

        if (self.LED_status):
            if(color == "red"):         # red
                self.rInten = intensity
            elif(color == "green"):     # green
                self.gInten = intensity
            elif(color == "blue"):      # blue
                self.bInten = intensity
            else:
                print("Invalid Color choice")

            self.red.ChangeDutyCycle(self.rInten)
            self.green.ChangeDutyCycle(self.gInten)
            self.blue.ChangeDutyCycle(self.bInten)

            return("Successfully set " + color + "\'s intensity to " + str(intensity))

        else:
            return("LED is off")
        
    def info(self):
        LED_Info = {
            "red" : self.rInten,
            "green" : self.gInten,
            "blue" : self.bInten,
            "status" : int(self.LED_status)
            }
        return LED_Info
            

if __name__ == "__main__":

    #test this class
    obj = LED_PWM()

    obj.turnLED_ON()

    for x in range(0, 100):
        obj.changeIntensity("red", x)
        time.sleep(0.125)
        obj.changeIntensity("green", x)
        time.sleep(0.125)
        obj.changeIntensity("blue", x)
        time.sleep(0.125)

    obj.turnLED_OFF()

    obj.info()
