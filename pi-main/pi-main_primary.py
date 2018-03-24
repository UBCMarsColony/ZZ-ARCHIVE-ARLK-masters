#initialization
TAG = "pi-main_primary"

import sys
import importlib
import time
import RPi.GPIO as gpio
    
print("STARTING SYSTEM")

#Data Reader
sys.path.insert(0, '../pi-comms')
log = importlib.import_module("pi-comms_log")

sys.path.insert(0, '../pi-comms/pi-comms_data-reader')
data_reader = importlib.import_module('pi-comms_data-reader-v2')

#Lighting
sys.path.insert(0, '../pi-systems/')

ss_pool = importlib.import_module('pi-systems_subsystem-pool')

light_ss = importlib.import_module('pi-systems_lighting_lights-manager')
valve_ss = importlib.import_module('pi-systems_valve-manager')

_current_state = None
print("SYSTEM READY\n-------------\n-------------\n\n")


# MAIN SYSTEM FUNCTIONS
# Based on the Arduino setup

def begin(config_data_dict):
    log.print_config(config_data_dict["log_level"])
    
    #Set GPIO mode to Broadcom SOC Channel
    gpio.setmode(gpio.bcm)
    
    #Initialize various systems
    light_thread = light_ss.LightingThread(gpio, "LightThread", 3)
    light_thread.start() 
    
    try:
        loop(config_data_dict)
    except KeyboardInterrupt:
        print("Shutting down colony...")
        ss_pool.stopAll()
        exit(0)

        
def loop(config_data):
    while True:
        data = data_reader.update_sensor_data()
        #door_state = (door_col, door_mars)
        
        #Check data safety
        
        # Process user input
            #Handle user input
        
        
        
        time.sleep(config_data["loop_delay"])

"""
NORMAL PROCESS
--------------
Get sensors, doors
    Check safety, handle issues

Check user input    
    Handle any input

Update:
    Lights
    UI

    
OPEN DOOR
---------
Get sensors, doors
    Check safety

Check user input

Run door, valves, pressure

Update:
    Lights
    UI

EMERGENCY
--------
Lights Full
Update UI wth warning

Close doors

Run valve, pressure
    Safety checks always
    
"""