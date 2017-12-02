# Written By: Thomas Richmond
# Email: Thomas.joakim@gmail.com
#
# This module is meant to decide how to set up the lights. It starts by deciding what lighting scheme to use - that is, 
# what lights are on, which are off, and what other associated logic. Once the lighting scheme has been decided, the
# lights can be set by passing the LightScheme structure returned by the decideLighting() function into the
# controlLights() function.
#
# In the event of an error, lights may flash. This has yet to be implemented.


# Some constant
ON = 1
OFF = 0

#LightScheme library
ls = __import__('lighting_light-control_light-scheme')

#GPIO Library
try:
	import RPi.GPIO as GPIO
	print("Success")
except ImportError:
	print("ERROR: RPi.GPIO library could not be imported. Program may not work as expected.")
except RuntimeError:
	print("ERROR: RPi.GPIO library encountered an error while importing. Make sure you have superuser privileges")

def generate_light_scheme():
	light_scheme = ls.LightScheme()
	
	try:
		light_scheme["OVERHEAD_1"] = ON
	except KeyError:
		print("ERROR: Invalid key accessed.")

    # PIR_data = get PIR sensor data
    # door_data = get door data

    # if PIR_data == person in room

    # if door_data = closed
    # Generate scheme for bright lights

    # elif door_data = open_colony
    # Generate scheme for dim lights

    # elif door_data = open_mars
    # Generate scheme for bright lights

    # else
    # if time_elapsed == 20 seconds
    # Generate scheme for lights off

	return light_scheme


def control_lights(light_scheme=ls.LightScheme):
    print(light_scheme)
    #GPIO.output(25, GPIO.HIGH)

    return 0