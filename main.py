__author__ = 'mirvin'
from time import sleep
from queryv1 import QueryForTests
import drive
import queryv1
import logging
import re
import drive
import RPi.GPIO as GPIO 
import os 
import sys
import distance
import ussInit
import testTools
import constants
from constants import _INSTANCE_,_RESTENDPOINT_,_POLLTIME_,_AUTOTEST_,_ORIGIN_
#from constants import *
from testTools import amiHome


######################
# Begin Main Section  #
#####################




#Get the car & sensors GPIO ready for action
drive.initCar("startup")
ussInit.initUltraSensor()

#Car location status variables.  home <= 5 cm.

currentLoc = 13.0


currentLoc=distance.checkDist()
currentLoc = drive.goHome(constants._ORIGIN_,currentLoc)
	
while 1:
	currentTestHash = QueryForTests(constants._INSTANCE_ + '/' + constants._RESTENDPOINT_)
	print "sleeping"
	sleep(_POLLTIME_)
		
	if currentTestHash['Status'] == 'NOTEST':
		print "NOTESTS - Checking for home in the interim"
		drive.goHome(_ORIGIN_,currentLoc)
	else:
		if _AUTOTEST_ == True:
			cleanedDescription = queryv1.cleanString(currentTestHash['Desc'])
			x = re.search('(^-G) (\w+)', cleanedDescription)
			if (x != None):
				if x.group(1) == '-G':
					ghRepo = x.group(2)  # extract the repo name from second argument
					print "Getting from GH repo"
					print "Copying script to local folder"
			else:
				queryv1.outputScriptToFile(cleanedDescription)
				print "TESTING AFTER OUTPUT TO FILE",currentLoc,_ORIGIN_
				if (currentLoc > _ORIGIN_): 
					currentLoc = drive.goHome(_ORIGIN_,currentLoc)
					
				queryv1.execTest("script1.py")
				passFail = constants._FAILED_
				if (amiHome() == True): 
					passFail = constants._PASSED_
				queryv1.updateTest(_INSTANCE_ + '/' + _RESTENDPOINT_,currentTestHash['ID'],passFail)	
				queryv1.updateConversation(_INSTANCE_ + '/' + _RESTENDPOINT_,currentTestHash['Number'],passFail)
		else:
			print "Cannot autoTest since autoTest=False"
	try:
		print "Preparing to sleep"
		sleep(_POLLTIME_)
	except KeyboardInterrupt:
		print "interrupted man"
		drive.initCar("shutdown")
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

	
	
			
