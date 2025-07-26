import RPi.GPIO as GPIO
from constants import _TRIG_,_ECHO_


def initUltraSensor():
	try:
		GPIO.setup(_TRIG_,GPIO.OUT)
		GPIO.setup(_ECHO_,GPIO.IN)
		print "Setup UltraSensor suceesfully"
	except:
		print "Error attempting to set up Ultrasound devices"
		exit 

