import RPi.GPIO as GPIO
import time
from constants import _TRIG_,_ECHO_





def checkDist():
	
	GPIO.output(_TRIG_, False)
	print "Initializing sensor"
	time.sleep(1)

	#Take a reading by transmitting sound wave
	GPIO.output(_TRIG_, True)
	time.sleep(0.00001)

	#Shut off tranmitting ofsound wave
	GPIO.output(_TRIG_, False)

	#Get t0, the time of echo starts listening
	while GPIO.input(_ECHO_)==0:
		pulse_start = time.time()

	while GPIO.input(_ECHO_)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)
	distanceI = round(distance *0.393701,2)
	print "Distance:",distance,"cm ",distanceI,"inches"
	if  distanceI > 12:
		print round(distanceI/12,1)," feet"
	#GPIO.cleanup()
	return distance	
	
#Before leaving, set back to BOARD so wheels will work
#GPIO.setmode(GPIO.BOARD)

#Dont want to clean up yet
#GPIO.cleanup()
