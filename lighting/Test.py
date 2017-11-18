# Written By: Thomas Richmond
# Email: Thomas.joakim@gmail.com
#
# This program is meant to decide how to set up the lights. It starts by deciding what lighting scheme to use - that is, 
# what lights are on, which are off, and what other associated logic. Once the lighting scheme has been decided, the
# lights can be set by passing the LightScheme structure returned by the decideLighting() fuction into the controlLights()
# function.
#
# In the event of an error, lights may flash. This has yet to be implemented.

import os

class LightScheme(dict):
	
	#ALL VALID LIGHT SCHEME KEYS MUST BE INCLUDED IN THE ARRAY BELOW
	scheme_keys = ["L1", "L2", "L3", "L4"]
	
	def __init__(self, val_type = int):
		for key in LightScheme.scheme_keys:
			self[key] = val_type()
		
	#Only sets the item if it is a valid LightScheme item
	def __setitem__(self, key, val):
		if key not in LightScheme.scheme_keys:
			raise KeyError
		dict.__setitem__(self, key, val)
 
def generateLightingScheme():
	lighting_scheme = LightScheme()
	
	# Check if the passed in errorCode.
		# If the errorCode supports a valid error, return error to flash the lights 3 times.
		
	# Get PIR sensor data
		#If somebody is in range of the PIR sensor, return lights on scheme.

	#If nobody is detected, check the time since somebody was last seen.
		#If it is greater than the time limit, return lights off scheme.
		
	return lighting_scheme
	
def controlLights(light_scheme = LightScheme):
	print(light_scheme)
	return 1
	
print(controlLights(generateLightingScheme()))
	
os.system("PAUSE")
