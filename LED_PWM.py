#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


class LED_PWM:

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
        
    red   = GPIO.PWM(21, 100)      # red LED at 1000 Hz
    green = GPIO.PWM(20, 100)      # green LED at 1000 Hz
    blue  = GPIO.PWM(16, 100)      # blue LED at 1000 Hz

    red.start(0)
    green.start(0)
    blue.start(0)

    def __init__(self):
        return
    
    def setIntensity(self, color, dutyCycle):

        if(color == 1):     # red
            self.red.ChangeDutyCycle(dutyCycle)
            self.green.ChangeDutyCycle(0)
            self.blue.ChangeDutyCycle(0)
            print("red LED ON")
        elif(color == 2):   # green
            self.red.ChangeDutyCycle(0)
            self.green.ChangeDutyCycle(dutyCycle)
            self.blue.ChangeDutyCycle(0)
            print("Green LED ON")
        elif(color == 3):   # blue
            self.red.ChangeDutyCycle(0)
            self.green.ChangeDutyCycle(0)
            self.blue.ChangeDutyCycle(dutyCycle)
            print("Blue LED ON")
        else:
            print("Invalid Color choice")
            

if __name__ == "__main__":
    print("This is LED_PWM.py")

    #test this class
    obj = LED_PWM()

    for x in range(0, 100):
        obj.setIntensity(1, x)
        time.sleep(0.125)
        print("red: " + str(x))

    for y in range(0, 100):
        obj.setIntensity(2, y)
        time.sleep(0.125)
        print("green: " + str(y))


    for z in range(0, 100):
        obj.setIntensity(3, z)
        time.sleep(0.125)
        print("blue: " + str(z))

    
