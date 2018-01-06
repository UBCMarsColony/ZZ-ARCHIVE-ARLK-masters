# Written By: Thomas Richmond
# Email: Thomas.joakim@gmail.com
#
# This module is meant to decide how to set up the lights. It starts by deciding what lighting scheme to use - that is, 
# what lights are on, which are off, and what other associated logic. Once the lighting scheme has been decided, the
# lights can be set by passing the LightScheme structure returned by the decideLighting() function into the
# controlLights() function.
#
# In the event of an error, lights may flash. This has yet to be implemented.

####################
# IMPORTS
####################

from random import *

try:
    import gpio
except:
    print("TODO: FIX ME")

# LightScheme library is imported with the __import__ method 
# due to some issues with how dash (-) characters interact 
# with the standard importing method used above
ls = __import__('lighting_light-control_light-scheme')


def generate_light_scheme():
    light_scheme = ls.LightScheme()
	
    # Temporary code to populate the lightscheme with some nonzero values
    try:
		for light_ID in light_scheme:
			light_scheme[light_ID] = randint(0,1)
    except KeyError:
        print("ERROR: Invalid key accessed.")
	
    #IMPLEMENT BELOW
    
    # PIR_data = get PIR sensor data
    # door_data = get door data
    
    # if PIR_data && door_data has not significantly changed
        # break

    # if PIR_data == person in room
    
    # if door_data = closed
        # Generate scheme for bright lights

    # elif door_data = open_colony
        # Generate scheme for dim lights

    # elif door_data = open_mars
        #Generate scheme for bright lights

    # else
        # if time_elapsed == 20 seconds
            # Generate scheme for lights off

    return light_scheme


def update_lights(light_scheme):
    if not isinstance(light_scheme, ls.LightScheme):
        raise TypeError("ERROR: The parameter <light_scheme> has type " + 
            str(type(light_scheme))[7 : len(str(type(light_scheme))) - 2] + 
            " when it should be of type LightScheme!")
		
    print(light_scheme)
#UNCOMMENT WHEN READY
    #for light_ID in light_scheme:
        #gpio.write(light_scheme.getGPIO(light_ID), light_scheme[light_ID])
	
    print("---")
    return 0