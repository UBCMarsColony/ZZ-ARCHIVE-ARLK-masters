#initialization
TAG = "pi-main_primary"

import sys
import importlib
import time
import RPi.GPIO as gpio
    
print("STARTING SYSTEM")

# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the pool
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

sensor_ss = importlib.import_module('pi-systems_sensor-reader')
input_ss = importlib.import_module('pi-systems_input-manager')
light_ss = importlib.import_module('pi-systems_lighting_lights-manager')
valve_ss = importlib.import_module('pi-systems_valve-manager')

print("SYSTEM READY\n-------------\n-------------\n\n")


# MAIN SYSTEM FUNCTIONS
# Based on the Arduino setup

def begin(config_data_dict):
    
    #Set GPIO mode to Broadcom SOC Channel
    gpio.setmode(gpio.bcm)
    
    #Initialize various systems
    
    global sensors
    sensors = sensor_ss.SensorSubsystem(gpio, "Sensors_Subsystem", 3)
    sensor.start()
    
    global lights
    lights = light_ss.LightingSubsystem(gpio, "Lights_Subsystem", 4)
    lights.start() 
    
    global input
    input = input_ss.InputManager(gpio, "Input_Subsystem", 5)
    input.start()
    
    global valves
    valves = valve_ss.ValveManager(gpio, "Valve_Subsystem", 6)
    valves.start()
    
    try:
        loop(config_data_dict)
    except KeyboardInterrupt:
        cmd_input = cmd_input("Shut down colony? (y/n)\n")
        if cmd_input == "y" or cmd_input == "Y":
            ss_pool.stop_all()
            exit(0)
        else:
            print("Airlock shutdown cancelled")

        
def loop(config_data):
    # TODO find a nicer way to do this
    global sensors
    global lights
    global input
    global valves
    
    while True:
        data = sensors.get_data()
        next_button = input.check_buttons()
        
        if next_button == 16:
            #This is placeholder code
            valves.request_new_state(valve_ss.ValveManager.std_state["close"])
            pass
        
        lights.input_data(data)
        
        time.sleep(config_data["loop_delay"])
        
"""
INIT
----


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