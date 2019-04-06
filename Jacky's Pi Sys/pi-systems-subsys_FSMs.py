# FSMs
# Pressure - Working
# Lights - Not working yet
# Door - Working
from statemachine import StateMachine, State
import time
from enum import Enum
from abc import ABC, abstractmethod
import threading
from threading import Lock
import struct
import struct
import importlib
subsys_input = importlib.import_module('pi-systems_input-subsystem')
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")
pressure_ss = importlib.import_module('pi-systems_pressure-manager')
subsys_base = importlib.import_module('pi-systems_subsystem-base')

# Define the pins used for the following inputs to the FSMs
# ### pressure_butt   -   Button to start pressurize procedure
# ### depressure_butt -   Button to start depressurizing
# ### lights_toggle   -   Button to turn on/off lights
# ### door_open_butt  -   Button to open door
# ### door_close_butt -   Button to close door
pressure_butt = 10
depressure_butt = 9
lights_toggle = 8
door_open_butt = 7
door_close_butt = 6

# Now we will instantiate the FSM subsystems
# Subsystems needed: Pressure, Lighting, and Door

subsystems = []
press_sys = pressure_ss.PressureSubsystem(name="pressure", thread_id=50)

print(press_sys.name)
print(type(press_sys))
subsystems.append(press_sys)
subsys_base.Subsystem.start(press_sys)
print(subsystems)  # subsystem has been added to pool and is running


class PressureFSM(StateMachine):

    #   State Definitions
    idle = State("idle", initial=True)
    pressurize = State("pressurize")
    depressurize = State("depressurize")
    done = State("done")
    Emergency = State("Emergency")

    #   Next State Transitions
    keep_idling = idle.to(idle)
    start_pressurize = idle.to(pressurize)
    keep_pressurize = pressurize.to(pressurize)
    done_pressurize = pressurize.to(idle)
    start_depressurize = idle.to(depressurize)
    keep_depressurize = depressurize.to(depressurize)
    done_depressurize = depressurize.to(idle)
    detected_emerg_1 = pressurize.to(Emergency)
    detected_emerg_2 = depressurize.to(Emergency)
    detected_emerg_3 = idle.to(Emergency)
    emerg_unresolved = Emergency.to(Emergency)

    # Methods for the states actions
    #   executed when the state transition (defined above) is triggered
    def on_keep_idling(self):
        print("I AM IDLING")

    def on_start_pressurize(self, range):
        print("START PRESSURIZING")
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_pressurize(self):
        print("I AM PRESSURIZING")

    def on_done_pressurize(self):
        print("I AM DONE PRESSURIZING")

    def on_start_depressurize(self, range):
        print("START DEPRESSURIZING")
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_depressurize(self):
        print("I AM DEPRESSURIZING")

    def on_done_depressurize(self):
        print("I AM DONE DEPRESSURIZING")

    def on_detected_emerg_1(self):
        print("EMERGENCY DETECTED")

    def on_detected_emerg_2(self):
        print("EMERGENCY DETECTED")

    def on_emerg_unresolved(self):
        print("EMERGENCY UNRESOLVED")


# Create FSM for Doors
class DoorFSM(StateMachine):
    #   State Definitions
    idle = State("Idle", initial=True)
    door_open = State("Open")
    door_close = State("Close")
    keep_idling = State("Continuing to idle")
    done = State("completed door process")
    Emergency = State("Emergency")

    #   State Transitions
    keep_idling = idle.to(idle)
    start_open = idle.to(door_open)
    keep_opening = door_open.to(door_open)
    done_open = door_open.to(idle)
    start_close = idle.to(door_close)
    keep_closing = door_close.to(door_close)
    done_close = door_close.to(idle)
    # emergency states
    detected_emerg_1 = door_open.to(Emergency)
    detected_emerg_2 = door_close.to(Emergency)
    detected_emerg_3 = idle.to(Emergency)
    emerg_unresolved = Emergency.to(Emergency)

    # Methods for the states
    #   executed when the state transition (defined above) is triggered
    def on_keep_idling(self):
        print("I AM IDLING")

    def on_start_open(self):
        print("I AM STARTING TO OPEN")

    def on_start_close(self):
        print("I AM STARTING TO CLOSE")

    def on_done_open(self):
        print("I AM DONE OPENING")

    def on_done_close(self):
        print("I AM DONE CLOSING")

    def on_keep_opening(self):
        print("I AM OPENING")

    def on_keep_closing(self):
        print("I AM CLOSING")

    def on_detected_emerg_1(self):
        print("EMERGENCY DETECTED")

    def on_detected_emerg_2(self):
        print("EMERGENCY DETECTED")

    def on_detected_emerg_3(self):
        print("EMERGENCY DETECTED")

    def on_emerg_unresolved(self):
        print("EMERGENCY UNRESOLVED")


class LightFSM(StateMachine):
    # State Defintions.  Lights either on or off
    on = State("ON")
    off = State("OFF", initial=True)

    # Define the state transitions
    turn_off = on.to(off)
    turn_on = off.to(on)

    def on_turn_off(self):
        print("Turn the lights off")

    def on_turn_on(self):
        print("Turn the lights on")

fsm_pressure = PressureFSM()
fsm_lights = LightFSM()
fsm_door = DoorFSM()

# Fill an array of size 100 to 0, 1, 2, 3, ..., 100
mock_press_data = [None]*100
for i in range(100):
    mock_press_data[i] = i
# Specify range of target pressures to pressurize/depressurize to
t_range_p = [5, 10]
t_range_d = [2, 5]

# Fill an array of size 10
mock_door_data = [None]*10
for i in range(10):
    mock_door_data[i] = 0
mock_door_data[5] = 1
mock_door_data[9] = 1


# Create loop to run all FSMs
def loop_FSMs():
    emergency = False
    pressure = 0  # Pressure variable

    while(emergency is False):
        # i and j are used for door logic
        i = 0
        j = 0

        # will have to replace this input logic with the code
        # from thomas' interface code
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
        if(command == 'e' or command == "E"):  # change to interface logic
            emergency = True
            print(fsm_pressure.current_state)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # COMMAND TO PRESSURIZE AND DEPRESSURIZE THE AIRLOCK
        # inputs: start_pressurize and start_depressurize only work
        #         if emergency is not True
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if(command == 'p' or command == 'P' and emergency is False):
            # if command is to pressurize, change states
            target_p = fsm_pressure.start_pressurize(t_range_p)
            # while not done pressurizing and no emergency...
            while (pressure < target_p) and emergency is False: # WHERE DOES IT GO TO WHEN EMERG TRUE?
                # ... we loop back into our current state
                fsm_pressure.keep_pressurize()
                time.sleep(1)
                pressure = pressure + 1
            # When we are done pressurizing, go back to idle
            fsm_pressure.done_pressurize()
        else:
            if(emergency is True):
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    fsm_pressure.emerg_unresolved()
                fsm_pressure.detected_emerg_3()
            else:
                fsm_pressure.keep_idling()
        print("I am in idle again? ",
              fsm_pressure.current_state == fsm_pressure.idle)

        if(command == 'd' or command == 'D' and emergency is False):  # change to interface logic
            target_d = fsm_pressure.start_depressurize(t_range_d)
            while(pressure > target_d) and emergency is False:
                fsm_pressure.keep_depressurize()
                time.sleep(1)
                pressure = pressure - 1
            fsm_pressure.done_depressurize()
        else:
            if(emergency is True):
                # If an emergency has already been detected while pressurizing
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    # we stay in emergency unresovled
                    fsm_pressure.emerg_unresolved()
                # Else we are depressurizing when the emergency happens
                else:
                    fsm_pressure.detected_emerg_2()
            else:
                fsm_pressure.keep_idling()
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
            fsm_door.start_open()
            while (i is 0 and emergency is False):
                fsm_door.keep_opening()
                # i var represents when the door is in the process of opening
                i = 1
                if(i is 1):
                    fsm_door.done_open()
        elif (emergency is True):
            # if theres an emerg we gotta handle it unfortunately
            fsm_door.detected_emerg_3()
        else:
            # no code red so keep idling
            fsm_door.keep_idling()

        if(command == 'c' or command == 'C') and emergency is False:  # change to interface logic
            fsm_door.start_close()
            while(j is 0):
                fsm_door.keep_closing()
                # j var represents when the door is in the processs of closing
                j = 1
                if(j is 1):
                    fsm_door.done_close()
        elif (emergency is True):
            if(fsm_door.current_state == fsm_door.Emergency):
                fsm_door.emerg_unresolved()
            else:
                fsm_door.detected_emerg_2()
        else:
            fsm_door.keep_idling()
    # Emergency is True WEEEOOO WEEEOO WEEOOO!!!
    # we must put the FSMs in their respective emergency states
    print(fsm_pressure.current_state)
    print(fsm_door.current_state)
    # go to the loop again

loop_FSMs()



# -------------------------------------------------------------------------------------------------
# TESTING THE FSMs INDIVIDUALLY
# -------------------------------------------------------------------------------------------------
# The FSMs,their states and respective transitions have been defined
# Create loop for PressureFSM to test if it is working as expected
# PressureFSM ---> THIS HAS BEEN TESTED AND WORKS!!!
'''
# Create instance of the Pressure FSM
fsm_pressure = PressureFSM()
# Fill an array of size 100 to 0, 1, 2, 3, ..., 100
mock_press_data = [None]*100
for i in range(100):
    mock_press_data[i] = i
# Specify range of target pressures to pressurize/depressurize to
t_range_p = [70, 75]
t_range_d = [30, 35]


def pressure_loop():
    # Will replace this with the pressure reading from the sensors
    pressure = 0
    emergency = False

    while(emergency is False):
        # Begin the process of collecting an input and going through states

        start_p = input("Enter P to pressurize (press 0 to skip): ")

        if(start_p == 'p' or start_p == 'P'):
            # if command is to pressurize, change states
            target_p = fsm_pressure.start_pressurize(t_range_p)
            # while not done pressurizing...
            while(pressure < target_p):
                # ... we loop back into our current state
                fsm_pressure.keep_pressurize()
                pressure = pressure + 1
            # When we are done pressurizing, go back to idle
            fsm_pressure.done_pressurize()
        else:
            fsm_pressure.keep_idling()
        print("I am in idle again? ", fsm_pressure.current_state ==
        fsm_pressure.idle)
        # Goes here when break executed
        start_d = input("Enter D to pressurize (press 0 to exit): ")
        if(start_d == 'd' or start_d == 'D'):
            target_d = fsm_pressure.start_depressurize(t_range_d)
            # fsm_pressure.start_depressurize()
            while(pressure > target_d):
                fsm_pressure.keep_depressurize()
                pressure = pressure - 1
            fsm_pressure.done_depressurize()
        else:
            fsm_pressure.keep_idling
        print("I am in idle again? ", fsm_pressure.current_state ==
        fsm_pressure.idle)
# Emergency is True WEEEOOO WEEEOO WEEOOO!!!
# we must handle accordingly

pressure_loop()
'''

# Now create the FSM for the lights and test
# LightFSM ----> THIS HAS BEEN TESTED AND WORKS
'''
fsm_lights = LightFSM()


def light_loop():
    while(True):
        print("Lights are on? ", fsm_lights.current_state == fsm_lights.on)
        print("Lights are off? ", fsm_lights.current_state == fsm_lights.off)
        user_input = input("Press (1) to turn light on and (0) to turn off: ")
        if (user_input == '1'):
            fsm_lights.turn_on()
        elif(user_input == '0'):
            fsm_lights.turn_off()
    # If there is an emergency, we want to keep
    # sensors enabled so we can monitor it

light_loop()
'''
'''
fsm_door = DoorFSM()
# Fill an array of size 10
mock_door_data = [None]*10
for i in range(10):
    mock_door_data[i] = 0
mock_door_data[5] = 1
mock_door_data[9] = 1


def door_loop():
    emergency = False
    while(emergency is False):
        i = 0
        j = 0
        print("we idling? ", fsm_door.current_state == fsm_door.idle)
        user_input = input("Press (o) to open door on and (c) to close door: ")
        if (user_input == 'o' or user_input == 'O'):
            fsm_door.start_open()
            while (i is 0):
                fsm_door.keep_opening()
                i = 1
                if(i is 1):
                    fsm_door.done_open()
        else:
            fsm_door.keep_idling()
        if(user_input == 'c' or user_input == 'C'):
            fsm_door.start_close()
            while(j is 0):
                fsm_door.keep_closing()
                j = 1
                if(j is 1):
                    fsm_door.done_close()
        else:
            fsm_door.keep_idling()

    # If there is an emergency, we want to keep
    # sensors enabled so we can monitor it

door_loop()
'''
