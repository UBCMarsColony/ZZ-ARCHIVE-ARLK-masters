from statemachine import StateMachine, State


class PressureFSM(StateMachine):
    #   State Definitions
    idle = State("idle", initial=True)
    pressurize = State("pressurize")
    depressurize = State("depressurize")
    done = State("done")

    #   State Transitions
    keep_idling = idle.to(idle)
    start_pressurize = idle.to(pressurize)
    done_pressurize = pressurize.to(done)
    start_depressurize = idle.to(depressurize)
    done_depressurize = depressurize.to(done)
    back_to_start = done.to(idle)

    # Methods for the states
    #   executed when the state transition (defined above) is triggered
    def on_keep_idling(self):
        print("I AM IDLING")

    def on_start_pressurize(self):
        print("I AM PRESSURIZING")

    def on_done_pressurize(self):
        print("I AM DONE PRESSURIZING")

    def on_start_depressurize(self):
        print("I AM DEPRESSURIZING")

    def on_done_depressurize(self):
        print("I AM DONE DEPRESSURIZING")

    def on_back_to_start(self):
        print("I AM GOING BACK TO IDLE")


# Create FSM for Doors
class DoorFSM(StateMachine):
    #   State Definitions
    idle = State("Idle", initial=True)
    door_open = State("Open")
    door_close = State("Close")
    done = State("completed door process")

    #   State Transitions
    keep_idling = idle.to(idle)
    start_open = idle.to(door_open)
    done_open = door_open.to(done)
    start_close = door_open.to(door_close)
    done_close = door_close.to(done)
    back_to_start = done.to(idle)

    # Methods for the states
    #   executed when the state transition (defined above) is triggered
    def on_keep_idling(self):
        print("I AM IDLING")

    def on_start_open(self):
        print("I AM OPENING")

    def on_done_open(self):
        print("I AM DONE OPENING")

    def on_start_close(self):
        print("I AM CLOSING")

    def on_done_close(self):
        print("I AM DONE CLOSING")

    def on_back_to_start(self):
        print("I AM GOING BACK TO IDLE")


class LightFSM():
    # State Defintions.  Lights either on or off
    on = State("Lights on")
    off = State("Lights off")  

    turn_off = on.to(off)
    turn_on = off.to(on)

    def on_on(self):
        print("Turn the lights on")

    def on_off(self):
        print("Turn the lights off")


class SensorsFSM():
    # State defintions.  Sensors either enabled (reading) or disabled (not reading)
    enable = State("enable")
    disable = State("disable")

    enable_sensors = disable.to(enable)
    disable_sensors = enable.to(disable)

    def on_enable(self):
        print("Sensors have been enabled")

    def on_disable(self):
        print("Sensors have been disabled")


# Create loop for PressureFSM to test if it is working as expected
def loop():
    # Create instance of the Pressure FSM
    fsm_pressure = PressureFSM()
    # Run through state transitions
    # Test 1: Verify states go: idle -> idle -> pressure -> done -> idle
    print("State is in idle? ", fsm_pressure.is_idle)
    fsm_pressure.keep_idling()
    print("State is still in idle? ", fsm_pressure.is_idle)    
    fsm_pressure.start_pressurize()
    print("State is in pressurize?", fsm_pressure.is_pressurize)
    fsm_pressure.done_pressurize()
    print("State is in done_pressurize?", fsm_pressure.is_done)
    fsm_pressure.back_to_start()
    print("State is in idle?", fsm_pressure.is_idle)
    # Verify illegal transition not possible (DOES NOT ALLOW!!!! GOOD)
    # fsm_pressure.done_depressurize()


loop()
