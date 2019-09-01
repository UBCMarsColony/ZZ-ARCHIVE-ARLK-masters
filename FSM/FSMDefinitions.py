# Written by Noah Caleanu (noahcaleanu152@gmail.com)
# Defining all the FSMs and their states/methods.
from statemachine import StateMachine, State

ON = 1
OFF = 0

# _________________________________________________________________________
# DEFINE THE FOLLOWING FSM CLASSES:
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
    pause = State("pause")
    Emergency = State("Emergency")

    #   Next State Transitions
    keep_idling = idle.to(idle)
    start_pressurize = idle.to(pressurize)
    keep_pressurize = pressurize.to(pressurize)
    pause_press = pressurize.to(pause)
    resume_press = pause.to(pressurize)
    done_pressurize = pressurize.to(idle)
    start_depressurize = idle.to(depressurize)
    keep_depressurize = depressurize.to(depressurize)
    pause_depress = depressurize.to(pause)
    resume_depress = pause.to(depressurize)
    keep_pausing = pause.to(pause)
    done_depressurize = depressurize.to(idle)
    detected_emerg_1 = pressurize.to(Emergency)
    detected_emerg_2 = depressurize.to(Emergency)
    detected_emerg_3 = idle.to(Emergency)
    detected_emerg_4 = pause.to(Emergency)
    emerg_unresolved = Emergency.to(Emergency)

    # Methods for the states actions
    # executed when the state transition (defined above) is triggered
    def on_keep_idling(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        #self.airlock_press_ss.request_new_state(3)          # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'

    def on_pause_press(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'close'
        #self.airlock_press_ss.request_new_state(0)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[6].write(ON)

    def on_pause_depress(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'close'
        #self.airlock_press_ss.request_new_state(0)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[6].write(ON)

    def on_resume_press(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize'
        #self.airlock_press_ss.request_new_state(1)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[6].write(OFF)

    def on_resume_depress(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Depressurize'
        #self.airlock_press_ss.request_new_state(2)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[6].write(OFF)

    def on_keep_pausing(self, airlock_press_ss):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'close'
        #self.airlock_press_ss.request_new_state(0)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'

    def on_start_pressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize'
        #self.airlock_press_ss.request_new_state(1)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(OFF)  # All LEDs off except In_progress LED
        self.leds[1].write(ON)
        self.leds[2].write(OFF)

    def on_keep_pressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Pressurize'
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(OFF)  # All LEDs off except In_progress LED
        self.leds[1].write(ON)
        self.leds[2].write(OFF)
        self.leds[6].write(OFF)  # hold LED off when we keep depressurizing

    def on_done_pressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Idle'
        #self.airlock_press_ss.request_new_state(3)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(ON)  # All LEDs off except Pressurized LED
        self.leds[1].write(OFF)
        self.leds[2].write(OFF)

    def on_start_depressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = "Depressurize"
        #self.airlock_press_ss.request_new_state(2)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(OFF)  # All LEDs off except In_progress LED
        self.leds[1].write(ON)
        self.leds[2].write(OFF)

    def on_keep_depressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Depressurize'
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(OFF)  # All LEDs off except In_progress LED
        self.leds[1].write(ON)
        self.leds[2].write(OFF)
        self.leds[6].write(OFF)  # hold off when we keep depressurizing

    def on_done_depressurize(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = "Idle"
        #self.airlock_press_ss.request_new_state(3)         # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'low'
        self.leds = leds
        self.leds[0].write(OFF)  # All LEDs off except Depressurized LED
        self.leds[1].write(OFF)
        self.leds[2].write(ON)

    def on_detected_emerg_1(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'
        #self.airlock_press_ss.request_new_state(0)        # UNCOMMENT FOR VALVES TO WORK
        self.airlock_press_ss.priority = 'high'
        self.leds = leds
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_detected_emerg_2(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'
        self.airlock_press_ss.priority = 'high'
        #self.airlock_press_ss.request_new_state(0)        # UNCOMMENT FOR VALVES TO WORK
        self.leds = leds
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_detected_emerg_3(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'
        self.airlock_press_ss.priority = 'high'
        #self.airlock_press_ss.request_new_state(0)        # UNCOMMENT FOR VALVES TO WORK
        self.leds = leds
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_detected_emerg_4(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'
        self.airlock_press_ss.priority = 'high'
        #self.airlock_press_ss.request_new_state(0)        # UNCOMMENT FOR VALVES TO WORK
        self.leds = leds
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_emerg_unresolved(self, airlock_press_ss, leds):
        self.airlock_press_ss = airlock_press_ss
        self.airlock_press_ss.TargetState = 'Emergency'
        self.airlock_press_ss.priority = 'high'
        #self.airlock_press_ss.request_new_state(0)        # UNCOMMENT FOR VALVES TO WORK
        self.leds = leds
        self.leds[5].write(ON) # Turn on emergency LED


# ii. Create a Door FSM that sets Procedure and Priority of
#     the door subsystem
class DoorFSM(StateMachine):
    #   State Definitions
    idle = State("Idle", initial=True)
    door_open = State("Open")
    door_close = State("Close")
    keep_idling = State("Continuing to idle")
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

    # Note to self: Include the priority later
    def on_start_open(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # We wish to Set Door State
        #self.airlock_door_ss.DoorState = 111  # We wish to Set Door State
        self.airlock_door_ss.Procedure = 'OpenDoor'  # int 1
        self.priority = 'low'

    def on_start_close(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # We wish to Set Door State
        #self.airlock_door_ss.DoorState = 99  # We wish to Set Door State
        self.airlock_door_ss.Procedure = 'CloseDoor'  # int 2
        self.priority = 'low'

    def on_done_open(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 4  # We dont wanna set state, so we will just get state.
        self.airlock_door_ss.Procedure = 'Idle'  # int 0
        self.priority = 'low'
        self.leds = leds
        # self.leds[4].write(ON)
        # sleep(1)  # Pause so user can see confirm led on
        # self.leds[4].write(OFF)


    def on_done_close(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        # self.airlock_door_ss.Procedure.value = 4  # We dont wanna set state, so we will just get state.
        self.airlock_door_ss.Procedure = 'Idle'  # int 0
        self.priority = 'low'
        # self.leds[4].write(ON)
        # sleep(1)  # Pause so user can see confirm led on
        # self.leds[4].write(OFF)

    def on_keep_opening(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 3  # We set state to transit
        self.airlock_door_ss.Procedure = 'OpenDoor'  # int 1
        self.priority = 'low'

    def on_keep_closing(self, airlock_door_ss):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 3  # We set state to transit
        self.airlock_door_ss.Procedure = "CloseDoor"  # int 2
        self.priority = 'low'

    def on_detected_emerg_1(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 0  # Emergency door state is unknown to us.
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'
        self.leds = leds
        # self.leds[4].write(OFF) # Turn off confirm if its on
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_detected_emerg_2(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 0  # Emergency door state is unknown to us.
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'
        self.leds = leds
        #self.leds[4].write(OFF) # Turn off confirm if its on
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_detected_emerg_3(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 0  # Emergency door state is unknown to us.
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'
        self.leds = leds
        #self.leds[4].write(OFF) # Turn off confirm if its on
        self.leds[5].write(ON)  # Turn on emergency LED

    def on_emerg_unresolved(self, airlock_door_ss, leds):
        self.airlock_door_ss = airlock_door_ss
        #self.airlock_door_ss.Procedure.value = 3  # Set Door State to keep opening
        #self.airlock_door_ss.DoorState = 0  # Emergency door state is unknown to us.
        self.airlock_door_ss.Procedure = 'Emergency'  # int 0
        self.priority = 'high'
        self.leds = leds
        # self.leds[4].write(OFF) # Turn off confirm if its on
        self.leds[5].write(ON)  # Turn on emergency LED


# iii. Create FSM for Lighting that controls the state
#      of the lighting subsystem
class LightFSM(StateMachine):
    # State Defintions.  Lights either on or off.
    # NOTE No need for emergency state it will just stay in the same position when emergency triggered.
    on = State("ON")
    off = State("OFF", initial=True)

    # Define the state transition.
    turn_off = on.to(off)
    turn_on = off.to(on)

    def on_turn_off(self, airlock_light_ss):
        self.airlock_light_ss = airlock_light_ss
        self.airlock_light_ss.toggle()

    def on_turn_on(self, airlock_light_ss):
        self.airlock_light_ss = airlock_light_ss
        self.airlock_light_ss.toggle()
