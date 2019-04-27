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

#  Define the pins used for the following inputs to the FSMs
pressure_butt = subsys_input.InputComponent(name='P', pin=10, subtype='Button')
depressure_butt = subsys_input.InputComponent(name='D', pin=9, subtype='Button')
lights_toggle = subsys_input.InputComponent(name='L', pin=8, subtype='Switch')
door_open_butt = subsys_input.InputComponent(name='O', pin=7, subtype='Button')
door_close_butt = subsys_input.InputComponent(name='C', pin=6, subtype='Button')
emergency_butt = subsys_input.InputComponent(name='E', pin=5, subtype='Button')

inputs.append(emergency_butt)
inputs.append(pressure_butt)
inputs.append(depressure_butt)
inputs.append(lights_toggle)
inputs.append(door_open_butt)
inputs.append(door_close_butt)

outputs = []

light_led = subsys_input.OutputComponent(name='Airlock Lights',
                                         pin=3,
                                         subtype='LED')
buzzer = subsys_input.OutputComponent(name='Emergency Buzzer',
                                      pin=4,
                                      subtype='Buzzer')

outputs.append(light_led)
outputs.append(buzzer)

#  Now create the interface where the buttons are pooled
try:
    interface = subsys_input.InterfaceSubsystem(name="Airlock-Colony",
                                                thread_id=12,
                                                inputs=inputs,
                                                outputs=outputs)
    interface.start()
except NameError:
    print("Interface not initialized. Ensure GPIO installed on device")

# Create an array to store all subsystems
subsystems = []

# Initiate PressureSubsystem
airlock_press_ss = pressure_ss.PressureSubsystem(name="Airlock Pressure",
                                                 thread_id=50)
subsystems.append(airlock_press_ss)
airlock_press_ss.start()

# Initiate the DoorSubsystem
airlock_door_ss = door_ss.DoorSubsystem(name="Airlock Door",
                                        thread_id=60)
subsystems.append(airlock_door_ss)
airlock_door_ss.start()

# Initiate the LightingSubsystem.
# Throws an exception while not running on RaspPi machine
try:
    airlock_light_ss = light_ss.LightingSubsystem(name="Airlock Lights",
                                                  thread_id=55)
    subsystems.append(airlock_light_ss)
    airlock_light_ss.start()

except NameError:
    print("GPIO not defined. Skipping...")
except ModuleNotFoundError:
    print("GPIO could not be found. Skipping...")

# FIX THIS 
try:
    airlock_sensor_ss = sensor_ss.SensorSubsystem(#name='Airlock Sensors',
                                              thread_id=100,
                                              address=10)
    subsystems.append(airlock_sensor_ss)                                      
    airlock_sensor_ss.start()
except TypeError:
    print("Unexpected name occured")

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
def loop_FSMs(subsystems,
              inputs):
    #pressure = sensor_ss.sensor_data[3]  # Replace the initialization of pressure
    pressure = 0

    while(True):
        # i and j are used for door logic
        # Change with sensor data as well
        i = 0
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

        # For now, manually set the button states.
        inputs[0].state = 0  # Emerg
        inputs[1].state = 0  # Pressurize
        inputs[2].state = 1  # Depressurize
        inputs[3].state = 0  # Lights
        inputs[4].state = 0  # Open
        inputs[5].state = 0  # Close
        print(inputs)

        # Check if user pressed E
        if inputs[0].state == 1:
            emergency = True
            fsm_pressure.detected_emerg_3(airlock_press_ss)
            fsm_door.detected_emerg_3(airlock_door_ss)

        # Check if user pressed P
        if inputs[1].state == 1:
            # if command is to pressurize, change states
            target_p = fsm_pressure.start_pressurize(t_range_p,
                                                     airlock_press_ss)
            # while not done pressurizing and no emergency...
            #inputs[0].state = 1
            #while (sensor_ss.sensor_data[3] < target_p) and emergency is False:
            while (pressure < target_p):
                if inputs[0].state == 0:
                    # ... we loop back into our current state
                    fsm_pressure.keep_pressurize(airlock_press_ss)
                    time.sleep(1)  # take this out
                    pressure = pressure + 1  # take this out
                    inputs[0].state = 1
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
        if inputs[2].state == 1:
            pressure = 10
            target_d = fsm_pressure.start_depressurize(t_range_d,
                                                       airlock_press_ss)
            #while (sensor_ss.sensor_data[3] < target_d) and emergency is False:
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

        #Check if user pressed O
        if inputs[4].state == 1:  # change to interface logic
            fsm_door.start_open(airlock_door_ss)
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
            fsm_door.start_close(airlock_door_ss)
            while(j is 0):
                if inputs[0].state == 0:
                    fsm_door.keep_closing(airlock_door_ss)
                    # j var represents when the door is in the processs of closing
                    j = 1
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

loop_FSMs(subsystems,
          inputs)

# Old code for loop_FSMs(subsystems)
# Uses correct FSM and subsytem logic
# but button interface is NOT incorporated
'''
# Create loop to run all FSMs
def loop_FSMs(subsystems):
    # Force start loop with False
    emergency = False
    pressure = 0  # Pressure variable.  Will be sensor data
    #emergency_status = emergency_butt.read()

    #while(emergency_status == 0)
    while(emergency is False):
        # i and j are used for door logic
        i = 0
        j = 0

        # Get button States
        # Assume buttons are always pressed by user one at a time
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

        # These print statements will change to button interfaces on the switch box.
        print("Command list:\n p: pressurize\n d: depressurize\n o: open door")
        print(" c: close door\n 0: turn on/off\n e: simulate an emergency")
        command = input("Enter command: ")
        #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # COMMAND TO SIMULATE AN EMERGENCY
        # this is a button on the interface that will lock the airlock
        # once the emergency has been resolved:
        #       (1) first, the the power is cut
        #       (2) then, the system turns back on
        #       (3) FSM goes back to initial states
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # say user pushes the EMERG button.  Set the Loop variable 
        # if(emergency_status == 1)
        if(command == 'e' or command == "E"):  # change to interface logic
            emergency = True

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # COMMAND TO PRESSURIZE AND DEPRESSURIZE THE AIRLOCK
        # inputs: start_pressurize and start_depressurize only work
        #         if emergency is not True
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if(command == 'p' or command == 'P' and emergency is False):
            # if command is to pressurize, change states
            target_p = fsm_pressure.start_pressurize(t_range_p,
                                                     airlock_press_ss)
            # while not done pressurizing and no emergency...
            while (pressure < target_p) and emergency is False:  # WHERE DOES IT GO TO WHEN EMERG TRUE?
                # ... we loop back into our current state
                fsm_pressure.keep_pressurize(airlock_press_ss)
                time.sleep(1)
                pressure = pressure + 1
                print("PRESSURIZING...")
            fsm_pressure.done_pressurize(airlock_press_ss)
        else:
            if(emergency is True):
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    fsm_pressure.emerg_unresolved(airlock_press_ss)
                fsm_pressure.detected_emerg_3(airlock_press_ss)
            else:
                fsm_pressure.keep_idling(airlock_press_ss)
        print("I am in idle again? ",
              fsm_pressure.current_state == fsm_pressure.idle)

        if(command == 'd' or command == 'D' and emergency is False):
            target_d = fsm_pressure.start_depressurize(t_range_d,
                                                       airlock_press_ss)
            while(pressure > target_d) and emergency is False:
                fsm_pressure.keep_depressurize(airlock_press_ss)
                time.sleep(1)
                pressure = pressure - 1
            fsm_pressure.done_depressurize(airlock_press_ss)
        else:
            if(emergency is True):
                # If an emergency has already been detected while pressurizing
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    # we stay in emergency unresovled
                    fsm_pressure.emerg_unresolved(airlock_press_ss)
                # Else we are depressurizing when the emergency happens
                else:
                    fsm_pressure.detected_emerg_2(airlock_press_ss)
            else:
                fsm_pressure.keep_idling(airlock_press_ss)
        print("I am in idle again? ",
              fsm_pressure.current_state == fsm_pressure.idle)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # LIGHT COMMANDS:
        # input: 0 (toggles lights on, off, on, off, ...)
        # NOTE the light FSM does not have an emergency state
        # This is bc lights will not be effected by emergencies
        # Possible implementation: keep them lights on during emergencies???
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if(command == '0'):  # change to interface logic
            if(fsm_lights.current_state.name == "ON"):
                fsm_lights.turn_off()
            else:
                fsm_lights.turn_on()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # DOOR COMMANDS
        # inputs: open door, close door.  Self-explanatory commands
        # emergency detection sends FSM to emerg. state until
        # the emergency has been resolved.  Essentially locks the
        # FSM so doors cannot be changed
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        print("we idling? ", fsm_door.current_state == fsm_door.idle)

        if (command == 'o' or command == 'O') and emergency is False:  # change to interface logic
            fsm_door.start_open(airlock_door_ss)
            door_state = airlock_door_ss.loop()
            print(door_state)
            while (i is 0 and emergency is False):
                fsm_door.keep_opening(airlock_door_ss)
                # i var represents when the door is in the process of opening
                i = 1
                if(i is 1):
                    fsm_door.done_open(airlock_door_ss)
        elif (emergency is True):
            # if theres an emerg we gotta handle it
            fsm_door.detected_emerg_3(airlock_door_ss)
        else:
            # no code red so keep idling
            fsm_door.keep_idling(airlock_door_ss)

        if(command == 'c' or command == 'C') and emergency is False:  # change to interface logic
            fsm_door.start_close(airlock_door_ss)
            while(j is 0):
                fsm_door.keep_closing(airlock_door_ss)
                # j var represents when the door is in the processs of closing
                j = 1
                if(j is 1):
                    fsm_door.done_close(airlock_door_ss)
        elif (emergency is True):
            if(fsm_door.current_state == fsm_door.Emergency):
                fsm_door.emerg_unresolved(airlock_door_ss)
            else:
                fsm_door.detected_emerg_2(airlock_door_ss)
        else:
            fsm_door.keep_idling(airlock_door_ss)

loop_FSMs(subsystems)

'''


