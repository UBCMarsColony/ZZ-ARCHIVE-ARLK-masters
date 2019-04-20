# Written by Noah Caleanu for Mars Colony's Airlock Project.
#
# The following code imports subsystems and defines the FSM classes
# that control the various subsystems.  Each subsystem has its own FSM.

from statemachine import StateMachine, State
import time
from enum import Enum
from abc import ABC, abstractmethod
import threading
from threading import Lock
import struct
import struct
import importlib

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")
except ModuleNotFoundError:
    print("Running on non-pi machine")

# Define the pins used for the following inputs to the FSMs
# ### pressure_butt   -   Button to start pressurize procedure
# ### depressure_butt -   Button to start depressurizing
# ### lights_toggle   -   Button to turn on/off lights
# ### door_open_butt  -   Button to open door
# ### door_close_butt -   Button to close door
# ### emergency_butt -    Button to trigger an emergency state. Cuts power 2 Pi
pressure_butt = 10
depressure_butt = 9
lights_toggle = 8
door_open_butt = 7
door_close_butt = 6
emergency_butt = 5

# Import the subsystems & relevant modules
subsys_input = importlib.import_module('pi-systems_input-subsystem')
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")
pressure_ss = importlib.import_module('pi-systems_pressure-manager')
light_ss = importlib.import_module('pi-systems_lights-manager')
door_ss = importlib.import_module('pi-systems_door-subsystem')
subsys_base = importlib.import_module('pi-systems_subsystem-base')

# Create an array to store all subsystems
subsystems = []

# Initiate PressureSubsystem
airlock_press_ss = pressure_ss.PressureSubsystem(name="Airlock Pressure",
                                                 thread_id=50)
subsystems.append(airlock_press_ss)
airlock_press_ss.start()

# Initiate the DoorSubsystem
airlock_door_ss = door_ss.DoorSubsystem(name="Airlock Door", thread_id=60)
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

# _________________________________________________________________________
# DEFINE THE FSM CLASSES:
# i.   PressureFSM
# ii.  DoorFSM
# iii. LightFSM
# _________________________________________________________________________


# i. Create a pressure FSM that controls TargetState and Priority of
#    the Pressure subsystem
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
    # executed when the state transition (defined above) is triggered
    def on_keep_idling(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        self.airlock_press_ss.priority = 'low'

    def on_start_pressurize(self, range, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize'
        self.airlock_press_ss.priority = 'low'
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_pressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize'
        self.airlock_press_ss.priority = 'low'

    def on_done_pressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        self.airlock_press_ss.priority = 'low'

    def on_start_depressurize(self, range, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Depressurize'
        self.airlock_press_ss.priority = 'low'
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_depressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Depressurize'
        self.airlock_press_ss.priority = 'low'

    def on_done_depressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = "Idle"
        self.airlock_press_ss.priority = 'low'

    def on_detected_emerg_1(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        self.airlock_press_ss.priority = 'high'

    def on_detected_emerg_2(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        self.airlock_press_ss.priority = 'high'

    def on_emerg_unresolved(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        self.airlock_press_ss.priority = 'high'


# ii. Create a Door FSM that controls Procedure and Priority of
#     the door subsystem
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
    # Emergency states
    detected_emerg_1 = door_open.to(Emergency)
    detected_emerg_2 = door_close.to(Emergency)
    detected_emerg_3 = idle.to(Emergency)
    emerg_unresolved = Emergency.to(Emergency)

    # Methods for the states
    # executed when the state transition (defined above) is triggered
    def on_keep_idling(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'low'

    def on_start_open(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'OpenDoor'
        self.airlock_door_ss.priority = 'low'

    def on_start_close(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'CloseDoor'
        self.airlock_door_ss.priority = 'low'

    def on_done_open(self, airlock_door_ss):
        self.airlock_door_ss = self.airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'low'

    def on_done_close(self, airlock_door_ss):
        self.airlock_door_ss = self.airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'low'

    def on_keep_opening(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'OpenDoor'
        self.airlock_door_ss.priority = 'low'

    def on_keep_closing(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = "CloseDoor"
        self.airlock_door_ss.priority = 'low'

    def on_detected_emerg_1(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'high'

    def on_detected_emerg_2(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'high'

    def on_detected_emerg_3(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'high'

    def on_emerg_unresolved(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'
        self.airlock_door_ss.priority = 'high'


# iii. Create FSM for Lighting that controls the state
#      of the lighting subsystem
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

# _________________________________________________________________________
# NOW SET UP SOME THINGS FOR LOOP_FSMS AND RUN LOOP
# _________________________________________________________________________

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
def loop_FSMs(subsystems):
    emergency = False
    pressure = 0  # Pressure variable
    # Set the subsystems to idle initially

    while(emergency is False):
        # i and j are used for door logic
        i = 0
        j = 0
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
            while (i is 0 and emergency is False):
                fsm_door.keep_opening(airlock_door_ss)
                # i var represents when the door is in the process of opening
                i = 1
                if(i is 1):
                    fsm_door.done_open(airlock_door_ss)
        elif (emergency is True):
            # if theres an emerg we gotta handle it unfortunately
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
    # The following two lines were for debugging purposes
    # print(fsm_pressure.current_state)
    # print(fsm_door.current_state)


loop_FSMs(subsystems)
