import sys
import importlib
import time
import RPi.GPIO as gpio

# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the subsystem pool for use
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

# Import all subsystems for use
sensor_ss = importlib.import_module('pi-systems_sensor-reader')
input_ss = importlib.import_module('pi-systems_input-manager')
light_ss = importlib.import_module('pi-systems_lighting_lights-manager')
valve_ss = importlib.import_module('pi-systems_valve-manager')


"""
Purpose: Performs initial system setup and begins airlock loop cycle. Handles any breakouts within the loop cycle.
Parameter: runtime_params - The Namespace returned by the argument parser in init.py
"""
def begin(runtime_params):
    print("Performing systems initialization...\n")
    
    # Set GPIO mode to Broadcom SOC Channel (Mars Colony Default)
    gpio.setmode(gpio.bcm)
    
    # Start initializing the vital airlock systems
    
    # TODO Need to rework this. Remove global calls, make it reference the subsystem pool instead,
    # as all the systems will already be stored there.
    print("Initializing Sensors...\n") 
    global sensors                     
    sensors = sensor_ss.SensorSubsystem(gpio, "Sensors_Subsystem", 3)
    sensor.start()
    print("Sensors Initialized!\n")
    
    print("Initializing UI...\n")
    global input
    input = input_ss.InputManager(gpio, "Input_Subsystem", 5)
    input.start()
    
    print("Initializing Valves...\n")
    global valves
    valves = valve_ss.ValveManager(gpio, "Valve_Subsystem", 6)
    valves.start()
    
    print("Initializing Lights...\n")
    global lights
    lights = light_ss.LightingSubsystem(gpio, "Lights_Subsystem", 4)
    lights.start() 
    
    print("Beginning Main Loop Sequence...\n")
    try:
        loop(runtime_params)
    except KeyboardInterrupt:
        cmd_input = cmd_input("Shut down colony? (y/n)\n")
        if cmd_input == "y" or cmd_input == "Y":
            ss_pool.stop_all()
            exit(0)
        else:
            print("Airlock shutdown cancelled")

        
def loop(runtime_params):
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
        #input.update_UI()
        
        time.sleep(runtime_params.loop_delay)
        
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