# Written By: Thomas Richmond
# Email: Thomas.joakim@gmail.com
#
# This module is meant to decide how to set up the lights. It starts by deciding what lighting scheme to use - that is, 
# what lights are on, which are off, and what other associated logic. Once the lighting scheme has been decided, the
# lights can be set by passing the LightScheme structure returned by the decideLighting() function into the
# controlLights() function.
#
# In the event of an error, lights may flash. This has yet to be implemented.

# --------------------
# IMPORTS
# --------------------

#TAG = "pi-systems_lighting_lights-manager"

#from random import *
#import sys
#import gpio
#import time
#from collections import namedtuple
#import importlib
import importlib
subsys = importlib.import_module("pi-systems_subsystem-base")

#Try importing, gives error message if it fails
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
except ModuleNotFoundError:
    print("Running on non-pi machine")

class LightingSubsystem(subsys.Subsystem):
    def __init__(self, name=None, thread_id=None, address=None, pin=None, input_sig = 0):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms= 750)

        #variable definitions
        self.input_sig = input_sig
        self.output_pin = pin

        #Setting up the GPIO board
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.output_pin,GPIO.OUT, initial = GPIO.LOW)

    #Check input signal, if high, turn lights on, if low, turn lights off
    def loop(self):
        if self.input_sig == True:
            GPIO.output(self.output_pin, GPIO.HIGH)
        else:
            GPIO.output(self.output_pin, GPIO.LOW)

        



# LightScheme library is imported with importlib due 
# to some issues with how dash (-) characters interact 
# with the standard importing method (as used above)
#subsys = importlib.import_module('pi-systems_subsystem-base')
#
#
#class LightingSubsystem(subsys.Subsystem):
#
#    light_pins = (namedtuple("LightPins", ["overhead", "door_mars", "door_coln"]))(
#        # Random values
#        overhead=23,
#        door_mars=24,
#        door_colony=25
#    )
#
#    def __init__(self, name=None, thread_id=None):
#        super().__init__(name=name, thread_id=thread_id)
#
#        for pin in self.light_pins:
#            gpio.setup(pin, gpio.OUT)
#        
#        self._sensor_dict = None
#
#        
#    def loop(self):
#        if self._sensor_dict is None:
#            light_plan = generate_light_plan()
#            update_lights(light_plan)
#        time.sleep(2)   
#
#
#    def generate_light_plan(self) -> LightPlan:
#        light_plan = LightPlan()
#
#        #IMPLEMENT
#        if "somecondition":
#            light_plan[self.light_pins.overhead] = 1
#            light_plan[self.light_pins.door_mars] = 0
#            light_plan[self.light_pins.door_colony] = 0
#        "and so on..."
#        
#        return light_plan
#
#
#    def update_lights(light_plan):
#        if not isinstance(light_plan, LightPlan):
#            raise TypeError("ERROR: The parameter <light_plan> has type " + 
#                str(type(light_plan)) + " when it should be of type LightPlan!")
#        
#        with self:
#            for pin in self.light_pins:
#                GPIO.output(pin, light_plan[pin])
#
#
## The LightPlan dict object contains data about how to turn lights on and off.
## It is limited to keys defined in the _keys variable
#
## TODO Rework this whole class to take valid pins as a parameter. This will allow easier testing.
## This class doesn't work in its current state - make sure to update it.
#class LightPlan(dict):
#    
#    #LightPlan constructor
#    def __init__(self):
#        for key in LightPlan.__keys:
#            self[key] = 0
#            
#    #Modifies default dict element assignment to ensure the specified key is valid
#    def __setitem__(self, key, val):
#        if key not in LightPlan.__keys:
#            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
#        dict.__setitem__(self, key, val)
#    
#    def __getitem__(self, key):
#        if key not in LightPlan.__keys:
#            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
#        return dict.__getitem__(self, val)
#	
#    
#    #Returns the index associated with the key, or raises an error if the key is invalid
#    @staticmethod
#    def get_pin(self, key):
#        if key not in LightPlan.__keys:
#            raise KeyError("LightPlan key " + str(key) + " is unregistered, so it couldn't be used.")
#        return LightPlan.__keys[key]
#	
#    #Return the list of valid keys
#    @staticmethod
#    def get_keys():
#        return LightPlan.__keys
#