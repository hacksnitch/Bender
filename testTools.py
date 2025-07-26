from distance import checkDist	
from constants import _ORIGIN_

def  amiHome():
	""" Function doc """
	
	if checkDist() <= _ORIGIN_:	
		print "thing is home"
		return True
	else:
		print "thing is home"
		return False
