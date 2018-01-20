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
import importlib

try:
    import gpio
except:
    print("TODO: FIX ME")

# LightScheme library is imported with importlib due 
# to some issues with how dash (-) characters interact 
# with the standard importing method (as used above)
ls = importlib.import_module('lighting_light-control_light-plan')


def generate_light_plan():
    light_plan = ls.LightPlan()
	
    # Temporary code to populate light_plan with some nonzero values
    try:
        for light_key in light_plan:
            light_plan[light_key] = randint(0,1)
    except KeyError as ke:
        print(ke)
	
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

    return light_plan


def update_lights(light_plan):
    if not isinstance(light_plan, ls.LightPlan):
        raise TypeError("ERROR: The parameter <light_plan> has type " + 
            str(type(light_plan))[7 : len(str(type(light_plan))) - 2] + 
            " when it should be of type LightPlan!")
		
    print(light_plan)
    
#UNCOMMENT WHEN READY
    #for light_ID in light_plan:
        #gpio.write(light_plan.getGPIO(light_ID), light_plan[light_ID])
	
    print("---")
    return 0