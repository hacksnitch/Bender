__author__ = 'mirvin'

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)



GPIO.output(11,GPIO.HIGH)

time.sleep(3)

GPIO.output(11,GPIO.LOW)



GPIO.output(12,GPIO.HIGH)

time.sleep(4)

GPIO.output(12,GPIO.LOW)



