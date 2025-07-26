__author__ = 'mirvin'
import time
import distance

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print "Error with importing RPI.GPIO.  Try sudo man"

def GetCode(descIn):
    print "I have the code"
    
'''
# Left right forward back stop
def go(direction):
    print "driving  " + direction
'''

def PostMessage():
    print "Post conversation"

def AddScriptToQueue():
    print "Add to quey"

def Check4Dupes():
    print "Add to quey"
	
	
def initCar(mode):
	if mode == "startup":
		#Init the GPIO pins
		GPIO.setmode(GPIO.BOARD)
			
		#Select headers to output to wheels
		GPIO.setup(11,GPIO.OUT) #Reverse
		GPIO.setup(12,GPIO.OUT) #Forward
		GPIO.setup(13,GPIO.OUT) #Left
		GPIO.setup(15,GPIO.OUT) #Right
	elif mode == "shutdown":
		try:
			GPIO.cleanup()
			print "Successful GPIO cleanup"
		except:
			print "problem with trying to cleanup GPIOs."
		
# These di	
def go(direction,interval):
	if direction == "reverse":
		GPIO.output(11,GPIO.HIGH)
		time.sleep(interval)
		GPIO.output(11,GPIO.LOW)
	elif direction == "forward":
		GPIO.output(12,GPIO.HIGH)
		time.sleep(interval)
		GPIO.output(12,GPIO.LOW)
	elif direction == "left":
		GPIO.output(13,GPIO.HIGH)
		time.sleep(interval)
		GPIO.output(13,GPIO.LOW)
	elif direction == "right":
		GPIO.output(15,GPIO.HIGH)
		time.sleep(interval)
		GPIO.output(15,GPIO.LOW)
	elif direction == "stop":
		GPIO.output([11,12,13,15],GPIO.LOW)
		
#Back that thang up		
def goHome(home,current):
	while (current > home):
		ptr = GPIO.PWM(11,4)
		ptr.start(35)
		time.sleep(1)
		ptr.stop()
		current = distance.checkDist()
		print current," cm away and shrinking trying to get home"
	return current
	

