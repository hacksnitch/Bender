'''
from enum import Enum     # for enum34, or the stdlib version
# from aenum import Enum  # for the aenum version

#direction = Enum('', 'ant bee cat dog')

GPIO.setup(GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(11,0)
GPIO.output(12,1)

GPIO.output(12,0)
GPIO.output(12,1)
GPIO.output(12,0)
GPIO.output(11,1)
GPIO.output(11,0)
'''


		'''
		try:
			sleep(5)
			ctr += 1
		except KeyboardInterrupt:
			print "You have selected the friggin control C"
			
			try:
				sys.exit(0)
			except SystemExit:
				os._exit(0)
			'''
