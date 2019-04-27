# Written by Noah Caleanu for Mars Colony's Airlock Project.
#
# See pi-systems-defn-FSMs for FSM classes
# Each subsystem has its own FSM.

import time
from enum import Enum
from abc import ABC, abstractmethod
import threading
from threading import Lock
import struct
import importlib
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
except ModuleNotFoundError:
    print("Running on non-pi machine")

# Import the subsystems & relevant modules
subsys_input = importlib.import_module('pi-systems_input-subsystem')
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")
pressure_ss = importlib.import_module('pi-systems_pressure-manager')
light_ss = importlib.import_module('pi-systems_lights-manager')
door_ss = importlib.import_module('pi-systems_door-subsystem')
comms = importlib.import_module('pi-systems_communications')
subsys_base = importlib.import_module('pi-systems_subsystem-base')
sensor_ss = importlib.import_module('pi-systems_sensor-reader')
FSM = importlib.import_module('pi-systems-defn-FSMs')

inputs = []

#  Define the pins used for the following butt/switch
#  inputs to the FSM interface
pressure_butt = subsys_input.InputComponent(name='P', pin=10, subtype='Button')  # CHECK PIN NUMs
depressure_butt = subsys_input.InputComponent(name='D', pin=9, subtype='Button')  # screw u pep8
lights_toggle = subsys_input.InputComponent(name='L', pin=8, subtype='Switch')
door_open_butt = subsys_input.InputComponent(name='O', pin=7, subtype='Button')
door_close_butt = subsys_input.InputComponent(name='C', pin=6, subtype='Button')
emergency_butt = subsys_input.InputComponent(name='E', pin=5, subtype='Button')

# Add to inputs list
inputs.append(emergency_butt)
inputs.append(pressure_butt)
inputs.append(depressure_butt)
inputs.append(lights_toggle)
inputs.append(door_open_butt)
inputs.append(door_close_butt) 

outputs = []

light_led = subsys_input.OutputComponent(name='Airlock Lights',
                                         pin=3,         # CHECK PIN NUM.
                                         subtype='LED')  # initial state OFF
buzzer = subsys_input.OutputComponent(name='Emergency Buzzer',
                                      pin=4,            # CHECK PIN NUM.
                                      subtype='Buzzer')  # initial state OFF

outputs.append(light_led)
outputs.append(buzzer)

#  Now create the interface where the buttons are pooled
try:
    interface = subsys_input.InterfaceSubsystem(name="Airlock-Colony",
                                                thread_id=12,   # CHECK PIN NUM.
                                                inputs=inputs,
                                                outputs=outputs)
    interface.start()
except NameError:
    print("Interface not initialized. Ensure GPIO installed on this device")

# Create an array to store all subsystems
subsystems = []

# Initiate PressureSubsystem
airlock_press_ss = pressure_ss.PressureSubsystem(name="Airlock Pressure",
                                                 thread_id=50) 
subsystems.append(airlock_press_ss)
airlock_press_ss.start()

# Initiate the DoorSubsystem
airlock_door_ss = door_ss.DoorSubsystem(name="Airlock Door",
                                        thread_id=51)
subsystems.append(airlock_door_ss)
airlock_door_ss.start()

# Initiate the LightingSubsystem.
# Throws an exception while not running on RaspPi machine
try:
    airlock_light_ss = light_ss.LightingSubsystem(name="Airlock Lights",
                                                  thread_id=52)
    subsystems.append(airlock_light_ss)
    airlock_light_ss.start()

except NameError:
    print("GPIO not defined. Skipping...")
except ModuleNotFoundError:
    print("GPIO could not be found. Skipping...")

# FIX THIS 
# Why is there a name error?? hopefully GPIO
try:
    airlock_sensor_ss = sensor_ss.SensorSubsystem(#name='Airlock Sensors',
                                              thread_id=53,
                                              address=10)  # check address
    subsystems.append(airlock_sensor_ss)                                  
    airlock_sensor_ss.start()
except TypeError:
    print("Unexpected name occured.  Ensure GPIO is installed on this device")

#  Create an instance of the FSMs
fsm_pressure = FSM.PressureFSM()
fsm_lights = FSM.LightFSM()
fsm_door = FSM.DoorFSM()

# IN PROCESS OF: REPLACING THE MOCK DATA WITH THE SENSOR DATA
# _________________________________________________________________________
# Make some mock data
# _________________________________________________________________________
# Pressure Mock data
# Fill an array of size 100 to 0, 1, 2, 3, ..., 100
# to simulate the pressurizing process
mock_press_data = [None]*100
for i in range(100):
    mock_press_data[i] = i
t_range_p = [5, 10]
t_range_d = [2, 5]


# Improved code with the button interface incorporated and FSM for subsys.
# Do i need to put outputs here if subsys already in
def loop_FSMs(subsystems,
              inputs):
    #pressure = sensor_ss.sensor_data[3]  # Replace the initialization of pressure  # CHANGE TO THIS
    #O2 = sensor_ss.sensor_data[0]  # Use for HEX display
    #CO2= sensor_ss.sensor_data[4]
    #HUM= sensor_ss.sensor_data[1]  
    pressure = 0

    while(True):
        # i and j are used for door logic
        # Change to sensor data as well
        i = 0   # Col_Airlock_door = sensor_ss.sensor_data[3]
        j = 0

        # Read the button states
        # Assume buttons are always pressed by user one at a time.
        # With the exception of emergency, which may be pressed at any random time.
        # logic: 0 if not pressed, 1 if pressed.
        try:
            emergency_status = emergency_butt.read()
            start_pressurize = pressure_butt.read()
            start_depressurize = depressure_butt.read()
            switch_position = lights_toggle.read()
            door_open = door_open_butt.read()
            door_close = door_close_butt.read()
        except NameError:
            print("Skipping button reading...Module GPIO not found")

        # For now, manually set the GPIO button states.
        inputs[0].state = 0  # emergency_status
        inputs[1].state = 0  # start_pressurize
        inputs[2].state = 0  # start_depressurize
        inputs[3].state = 0  # switch_position
        inputs[4].state = 0  # door_open
        inputs[5].state = 0  # door_close

        print("E button: ", inputs[0].state,
              "P button: ", inputs[1].state,
              "D button: ", inputs[2].state,
              "L switch: ", inputs[3].state,
              "O button: ", inputs[4].state,
              "C button: ", inputs[5].state)

        # Check if user pressed E
        # Check if emergency happens while all FSMs idling
        if inputs[0].state == 1:
            emergency = True  # theres really no point in this besides an easier way to display Emergencies to user
            fsm_pressure.detected_emerg_3(airlock_press_ss)
            fsm_door.detected_emerg_3(airlock_door_ss)

        # Check if user pressed P
        # CHANGE THIS TO READ SENSOR DATA NOT MOCK DATA
        if inputs[1].state == 1:
            # if command is to pressurize, change states
            try:
                target_p = fsm_pressure.start_pressurize(t_range_p,
                                                         airlock_press_ss)
            except:
                print("Exit, cannot pressurize.  Possibly in emergency state.")
                break
            # while not done pressurizing and no emergency...
            #inputs[0].state = 1
            #while (sensor_ss.sensor_data[3] < target_p) and emergency is False:
            while (pressure < target_p):
                if inputs[0].state == 0:
                    # ... we loop back into our current state
                    fsm_pressure.keep_pressurize(airlock_press_ss)
                    time.sleep(1)  # take this out after sensor
                    pressure = pressure + 1  # take this out after sensor
                    #sensor_ss.__update_sensor_data()
                    print("PRESSURIZING...")
                else:
                    if(fsm_pressure.current_state == fsm_pressure.Emergency):
                        fsm_pressure.emerg_unresolved(airlock_press_ss)
                    else:
                        fsm_pressure.detected_emerg_1(airlock_press_ss)

            fsm_pressure.done_pressurize(airlock_press_ss)
        else:
            if(fsm_pressure.current_state == fsm_pressure.Emergency):
                fsm_pressure.emerg_unresolved(airlock_press_ss)
            else:
                fsm_pressure.keep_idling(airlock_press_ss)

        # Check if user pressed D
        # CHANGE THIS TO READ SENSOR DATA NOT MOCK DATA
        if inputs[2].state == 1:
            pressure = 10
            try:
                target_d = fsm_pressure.start_depressurize(t_range_d,
                                                           airlock_press_ss)
            except:
                print("Exit, cannot depressurize.  Possibly in emergency state.")
                break
            #while (sensor_ss.sensor_data[3] < target_d) and emergency is False:  # CHANGE TO THIS (GPIO)
            while(pressure > target_d):
                if inputs[0].state == 0:
                    fsm_pressure.keep_depressurize(airlock_press_ss)
                    time.sleep(1)           # Take this out
                    pressure = pressure - 1 # Take this out
                    print("DEPRESSURIZING")
                else:
                    if(fsm_pressure.current_state == fsm_pressure.Emergency):
                        fsm_pressure.emerg_unresolved(airlock_press_ss)
                    else:
                        fsm_pressure.detected_emerg_2(airlock_press_ss)    
                # sensor_ss.__update_sensor_data()
            fsm_pressure.done_depressurize(airlock_press_ss)
        else:
            if(fsm_pressure.current_state == fsm_pressure.Emergency):
                fsm_pressure.emerg_unresolved(airlock_press_ss)
            else:
                fsm_pressure.keep_idling(airlock_press_ss)

        print("I am in idle again? ",
              fsm_pressure.current_state == fsm_pressure.idle)

        # Check if user pressed L
        if inputs[3].state == 0:    
            # we want the lights off and theyre on
            if(fsm_lights.current_state.name == "ON"):
                try:
                    fsm_lights.turn_off(airlock_light_ss)
                except NameError:
                    print("Subsys doesnt exist")
            # else the light switch is ON
            else:
                print("Lights already off")
        else:
            if(fsm_lights.current_state.name == "OFF"):
                try:
                    fsm_lights.turn_on(airlock_light_ss)
                except NameError:
                    print("Subsys doesnt exist")
            else:
                print("Lights already on")
        print("we idling? ", fsm_door.current_state == fsm_door.idle)

        #Check if user pressed O button
        # CHANGE THIS TO READ SENSOR DATA NOT MOCK DATA
        if inputs[4].state == 1:  
            try:
                fsm_door.start_open(airlock_door_ss)
            except:
                print("Exit, cannot move door.  Possibly in emergency state.")
                break

            while i is 0:
                if inputs[0].state == 0:
                    fsm_door.keep_opening(airlock_door_ss)
                    # i var represents when the door is in the process of opening
                    i = 1
                    if(i is 1):
                        fsm_door.done_open(airlock_door_ss)
                else:
                    fsm_door.detected_emerg_1(airlock_door_ss)
        else:
            if(fsm_door.current_state == fsm_door.Emergency):
                fsm_door.emerg_unresolved(airlock_door_ss)
            else:
                # no code red so keep idling
                fsm_door.keep_idling(airlock_door_ss)

        # Check if user pressed C
        if inputs[5].state == 1:  # change to interface logic
            try:
                fsm_door.start_close(airlock_door_ss)
            except:
                print("Exit, cannot move door.  Possibly in emergency state.")
                break
            while(j is 0):
                if inputs[0].state == 0:
                    fsm_door.keep_closing(airlock_door_ss)
                    # j var represents when the door is in the processs of closing
                    j = 0
                    if(j is 1):
                        fsm_door.done_close(airlock_door_ss)
                else:
                    if(fsm_door.current_state == fsm_door.Emergency):
                        fsm_door.emerg_unresolved(airlock_door_ss)
                    else:
                        fsm_door.detected_emerg_2(airlock_door_ss)
        else:
            if(fsm_door.current_state == fsm_door.Emergency):
                fsm_door.emerg_unresolved(airlock_door_ss)
            else:
                fsm_door.keep_idling(airlock_door_ss)
        print("Current Pressure State: ", fsm_pressure.current_state.name)
        print("Current Door State: ", fsm_door.current_state.name)
        print("Current Light State: ", fsm_lights.current_state.name, "\n")

loop_FSMs(subsystems,
          inputs)