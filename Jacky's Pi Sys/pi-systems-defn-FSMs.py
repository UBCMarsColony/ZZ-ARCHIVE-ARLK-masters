# _________________________________________________________________________
# DEFINE THE FSM CLASSES:
# i.   PressureFSM
# ii.  DoorFSM
# iii. LightFSM
# _________________________________________________________________________

from statemachine import StateMachine, State
import time


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
        self.airlock_press_ss.TargetState = 'Idle' # int 3
        self.airlock_press_ss.priority = 'low'      #   int 0 

    def on_start_pressurize(self, range, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize' # int 1
        self.airlock_press_ss.priority = 'low'          # int 0
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_pressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize' # int 1
        self.airlock_press_ss.priority = 'low'          # int 0

    def on_done_pressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'  # int 3
        self.airlock_press_ss.priority = 'low'      # int 0

    def on_start_depressurize(self, range, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = "Depressurize" # int 2
        self.airlock_press_ss.priority = 'low'              # int 0
        self.range = range
        target_pressure = range[0] + ((range[1]-range[0])/2)
        self.target = int(target_pressure)
        return self.target

    def on_keep_depressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Depressurize'  # int 2
        self.airlock_press_ss.priority = 'low'              # int 0

    def on_done_depressurize(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = "Idle"           # int 3
        self.airlock_press_ss.priority = 'low'              # int 0

    def on_detected_emerg_1(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'          # int 3
        self.airlock_press_ss.priority = 'high'              # int 1

    def on_detected_emerg_2(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'          # int 3
        self.airlock_press_ss.priority = 'high'              # int 1

    def on_detected_emerg_3(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'          # int 3
        self.airlock_press_ss.priority = 'high'              # int 1

    def on_emerg_unresolved(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'          # int 3
        self.airlock_press_ss.priority = 'high'              # int 1


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
        self.airlock_door_ss.Procedure = 'Idle'  # int 0
        self.airlock_door_ss.priority = 'low'  # same int value as pressure FSM
                                                # (see directly above)

    # Note to self: Include the priority later
    def on_start_open(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'OpenDoor'  # int 1
        self.priority = 'low'

    def on_start_close(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'CloseDoor'  # int 2
        self.priority = 'low'

    def on_done_open(self, airlock_door_ss):
        self.airlock_door_ss = self.airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'  # int 0
        self.priority = 'low'

    def on_done_close(self, airlock_door_ss):
        self.airlock_door_ss = self.airlock_door_ss
        self.airlock_door_ss.Procedure = 'Idle'  # int 0
        self.priority = 'low'

    def on_keep_opening(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'OpenDoor'  # int 1
        self.priority = 'low'

    def on_keep_closing(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = "CloseDoor"  # int 2
        self.priority = 'low'

    def on_detected_emerg_1(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'

    def on_detected_emerg_2(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'

    def on_detected_emerg_3(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'

    def on_emerg_unresolved(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'


# iii. Create FSM for Lighting that controls the state
#      of the lighting subsystem
class LightFSM(StateMachine):
    # State Defintions.  Lights either on or off
    on = State("ON")
    off = State("OFF", initial=True)

    # Define the state transitions
    turn_off = on.to(off)
    turn_on = off.to(on)

    def on_turn_off(self, airlock_light_ss):
        self.airlock_light_ss = airlock_light_ss
        self.airlock_light_ss.toggle()
        self.airlock_light_ss.loop()
        print("Turn the lights off")

    def on_turn_on(self, airlock_light_ss):
        self.airlock_light_ss = airlock_light_ss
        self.airlock_light_ss.toggle()
        self.airlock_light_ss.loop()
        print("Turn the lights on")