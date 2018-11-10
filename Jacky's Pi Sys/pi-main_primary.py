import sys
import importlib
import time

# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the subsystem pool for use
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

# Import all subsystem files so we can create new instances of each one.
sensor_ss = importlib.import_module('pi-systems_sensor-reader')
input_ss = importlib.import_module('pi-systems_input-manager')
# light_ss = importlib.import_module('pi-systems_lighting_lights-manager')
# valve_ss = importlib.import_module('pi-systems_valve-manager')
door_ss = importlib.import_module('pi-systems_door-subsystem')

"""
Purpose: Performs initial system setup and begins airlock loop cycle. Handles any breakouts within the loop cycle.
Parameter: runtime_params - The Namespace returned by the argument parser in init.py
"""
def begin(runtime_params):
    print("\n\n---INITIALIZING AIRLOCK SYSTEMS---")
    
    # Start initializing the vital airlock systems
    subsystems = []
    
    subsystems.append(sensor_ss.SensorSubsystem(name="airlock1_sensors", thread_id=0xDE7EC7, address=0x0A))
    subsystems.append(door_ss.DoorSubsystem(name="airlock1_door_col", thread_id=0xD00121, address=0))
    subsystems.append(door_ss.DoorSubsystem(name="airlock1_door_mars", thread_id=0xD00122, address="FILL ME IN"))
    subsystems.append(input_ss.InputSubsystem(name="airlock1_input_mars", thread_id=0xE, address="FILL ME IN"))
    # input = input_ss.InputSubsystem("input", 5)
    # input.start()
    
    # valves = valve_ss.PressureSubsystem("valves", 6)
    # valves.start()
    
    # lights = light_ss.LightingSubsystem("lights", 4)
    # lights.start() 
    
    print("---AIRLOCK SYSTEMS INITIALIZED---\n")

    print("---STARTING SUBSYSTEMS---")
    for subsystem in subsystems:
        try:
            subsystem.start()
        except Exception as e:
            print("WARNING: Subsystem could not start as due to an unexpected exception:\n\t", e)
    
    print("\n---ALL SUBSYSTEMS STARTED---")

    print("\n---AIRLOCK SETUP COMPLETE.---\n")

    print("\n---STARTING LOOPER SEQUENCE---\n")
    print("Command input enabled.")
    while True:
        try:
            loop(runtime_params)
        except KeyboardInterrupt:
            cmd_input = input("Shut down colony? (y/n)\n")
            if cmd_input == "y" or cmd_input == "Y":
                ss_pool.stop_all()
                exit(0)
                break
            else:
                print("Airlock shutdown cancelled")
        
def loop(runtime_params):
    nextinput = input()

    subsystems = ss_pool.get_all()

    # DOOR LOGIC
    if nextinput == "o" or nextinput == "O":
        print("Requesting door open")
        subsystems["airlock1_doors"].request_door_state(subsystems["airlock1_doors"].Procedure.OpenDoor)
    elif nextinput == "c" or nextinput == "C":
        print("Requesting door close")
        subsystems["airlock1_doors"].request_door_state(subsystems["airlock1_doors"].Procedure.CloseDoor)
    
    # SUBSYSTEMS INFO
    elif nextinput == "i" or nextinput == "I":
        print("Current subsystem pool data:\n---------\n")
        print(repr(ss_pool.get_all()))
    
    # CLI INFO
    elif nextinput == '?':
        print("----- H E L P -----\n\to: Request door open\n\tc: Request door close" +
            "\n\ti: Print contents of the subsystem pool\n\t?: Help window (this text)" + 
            "\n-------------------")
    else:
        print("Command not recognized")



    ######
    # TODO find a nicer way to do this
    # subsystems = ss_pool.get_all()
    # data = subsystems["sensors"].get_data()
    # next_button = subsystems["input"].check_buttons()
    
    # if next_button == 16:
    #     #This is placeholder code
    #     subsystems["valves"].request_new_state(valve_ss.PressureSubsystem.std_state["close"])
    #     pass
    
    # subsystems["lights"].input_data(data)
    # #input.update_UI()
    
    # time.sleep(runtime_params.loop_delay)

        
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