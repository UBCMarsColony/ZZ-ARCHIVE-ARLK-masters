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

TAG = "pi-systems_lighting_lights-manager"

from random import *
import sys
import time
import importlib
    
# LightScheme library is imported with importlib due 
# to some issues with how dash (-) characters interact 
# with the standard importing method (as used above)
subsys = importlib.import_module('pi-systems_subsystem-base')

sys.path.insert(0,"../pi-comms")
log = importlib.import_module("pi-comms_log")

sys.path.insert(0, '../lighting')
lp = importlib.import_module('lighting_light-control_light-plan')

sys.path.insert(0, '../pi-comms/pi-comms_data-reader')
data_mgr = importlib.import_module('pi-comms_data-reader-v2')

try:
    import RPi.GPIO as GPIO
except ImportError or ImportWarning or ModuleNotFoundError:
    log.w(TAG, "TODO: FIX ME - GPIO import")

#DELETE ME LATER
GPIO.setmode(gpio.bcm)
GPIO.setup(lp.get_pin("OVERHEAD_1"), GPIO.OUT)
GPIO.setup(lp.get_pin("OVERHEAD_2"), GPIO.OUT)
GPIO.setup(lp.get_pin("DOOR_MARS1"), GPIO.OUT)
GPIO.setup(lp.get_pin("DOOR_COLN1"), GPIO.OUT)

class LightingThread(subsys.Subsystem):
    def __init__(self, name, threadID = None):
        super().__init__(name, threadID)

    def thread_task(self):
        while self.is_running:
            light_plan = generate_light_plan()
            update_lights(light_plan)
            time.sleep(2)
        

def generate_light_plan():
    light_plan = lp.LightPlan()
    
    # IMPLEMENT BELOW
    pir_data = data_mgr.get_sensor_data("Motion Detector")
    # door_data = get door data
    door_colony = 0
    door_mars = 0
    
     if pir_data: #or GPIO.input(gas):
        light_plan["OVERHEAD_1"] = 1
        light_plan["OVERHEAD_2"] = 1

    elif door_colony and not door_mars:
        light_plan["OVERHEAD_1"] = 1
        light_plan["OVERHEAD_2"] = 1
        light_plan["DOOR_COLN1"] = 1

    elif door_mars and not door_colony:
        light_plan["OVERHEAD_1"] = 1
        light_plan["OVERHEAD_2"] = 1
        light_plan["DOOR_MARS1"] = 1

    #elif GPIO.input(lights):
        #lights_on = GPIO.wait_for_edge(pir, GPIO_RISING, timeout=30000)
    
    return light_plan


def update_lights(light_plan):
    if not isinstance(light_plan, lp.LightPlan):
        raise TypeError("ERROR: The parameter <light_plan> has type " + 
            str(type(light_plan))[7 : len(str(type(light_plan))) - 2] + 
            " when it should be of type LightPlan!")
    log.d(TAG, str(light_plan))
    
    for key in lp.get_keys():
        GPIO.output(lp.get_pin(key), light_plan[key])
        
    return 0
