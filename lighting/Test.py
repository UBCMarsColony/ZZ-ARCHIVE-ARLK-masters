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
import time

#Some constant
ON = 1
OFF = 0

# The LightScheme dict object contains data about how to turn lights on and off.
# It is limited to keys defined in the scheme_keys variable
class LightScheme(dict):
	
	#ALL VALID LIGHT SCHEME KEYS MUST BE INCLUDED IN THE ARRAY BELOW
	_scheme_keys = ["OVERHEAD_1", "OVERHEAD_2", "DOOR_COLN1", "DOOR_MARS1"]
	
	def __init__(self, val_type = int):
		for key in LightScheme._scheme_keys:
			self[key] = val_type()
		
	#Only sets the item if it is a valid LightScheme item
	def __setitem__(self, key, val):
		if key not in LightScheme._scheme_keys:
			raise KeyError
		dict.__setitem__(self, key, val)

		
counter = 0
def generateLightScheme():
	lightScheme = LightScheme()
	
	lightScheme["OVERHEAD_1"] = ON
	#PIR_data = get PIR sensor data
	#door_data = get door data
	
	#if PIR_data == person in room
		
		#if door_data = closed
			#Generate scheme for bright lights
		
		#elif door_data = open_colony
			#Generate scheme for dim lights
	
		#elif door_data = open_mars	
			#Generate scheme for bright lights
	
	#else
		#if time_elapsed == 20 seconds
			#Generate scheme for lights off
		
	return lightScheme
	
def controlLights(light_scheme = LightScheme):
	print(light_scheme)
	return 0

counter = 0
while counter < 100:
	try:
		nextScheme = generateLightScheme()
	except KeyError:
		print("Error in task - Invalid LightScheme key reference")
	else:
		controlLights(nextScheme)
	counter += 1
	
	time.sleep(0.1)

os.system("PAUSE")
