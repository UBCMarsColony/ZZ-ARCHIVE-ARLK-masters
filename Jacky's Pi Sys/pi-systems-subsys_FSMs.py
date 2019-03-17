# FSMs
# Pressure - Working
# Lights - Not working yet
# Door - Working

from statemachine import StateMachine, State


class PressureFSM(StateMachine):

    #   State Definitions
    idle = State("idle", initial=True)
    pressurize = State("pressurize")
    depressurize = State("depressurize")
    done = State("done")
    emergency = State("Emergency")

    #   Next State Transitions
    keep_idling = idle.to(idle)
    start_pressurize = idle.to(pressurize)
    keep_pressurize = pressurize.to(pressurize)
    done_pressurize = pressurize.to(idle)
    start_depressurize = idle.to(depressurize)
    keep_depressurize = depressurize.to(depressurize)
    done_depressurize = depressurize.to(idle)
    detected_emerg_1 = pressurize.to(emergency)
    detected_emerg_2 = depressurize.to(emergency)
    detected_emerg_3 = idle.to(emergency)

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
        print("EMERGENCY OF TYPE 1 DETECTED")

    def on_detected_emerg_2(self):
        print("EMERGENCY OF TYPE 2 DETECTED")

    def on_detected_emerg_3(self):
        print("EMERGENCY OF TYPE 3 DETECTED")


# Create FSM for Doors
class DoorFSM(StateMachine):
    #   State Definitions
    idle = State("Idle", initial=True)
    door_open = State("Open")
    door_close = State("Close")
    keep_idling = State("Continuing to idle")
    # opening = State("Continuing to open")
    # closing = State("Continuing to close")
    done = State("completed door process")

    #   State Transitions
    keep_idling = idle.to(idle)
    start_open = idle.to(door_open)
    keep_opening = door_open.to(door_open)
    done_open = door_open.to(idle)
    start_close = idle.to(door_close)
    keep_closing = door_close.to(door_close)
    done_close = door_close.to(idle)

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


class LightFSM(StateMachine):
    # State Defintions.  Lights either on or off
    on = State("ON")
    off = State("OFF", initial=True)

    # Define the state transitions
    turn_off = on.to(off)
    turn_on = off.to(on)
    change = on.to(off)
    change2 = off.to(on)
    # stay_on = on.to(on)
    # stay_off = off.to(off)
    # off2_on = off.to(on)
    # on2_off = on.to(off)

    def on_turn_off(self):
        print("Turn the lights off")

    def on_turn_on(self):
        print("Turn the lights on")
  '''  
    def on_stay_on(self):
        print("keeping lights on")

    def on_stay_ofF(self):
        print("keeping lights off")
        '''
'''
    def on_off2_on(self):
        print("going from off to on")   

    def on_on2_off(self):
        print("going from on to off")
'''

class SensorsFSM(StateMachine):
    # State defintions.
    # Sensors either enabled (reading) or disabled (not reading)
    enable = State("enable", initial=True)
    disable = State("disable")

    enable_sensors = disable.to(enable)
    disable_sensors = enable.to(disable)

    # Enable the sensors to read data
    def on_enable(self):
        print("Sensors have been enabled")

    # disabling the sensors from reading
    def on_disable(self):
        print("Sensors have been disabled")

fsm_pressure = PressureFSM()
fsm_lights = LightFSM()
fsm_door = DoorFSM()

# Fill an array of size 100 to 0, 1, 2, 3, ..., 100
mock_press_data = [None]*100
for i in range(100):
    mock_press_data[i] = i
# Specify range of target pressures to pressurize/depressurize to
t_range_p = [70, 75]
t_range_d = [30, 35]

# Fill an array of size 10
mock_door_data = [None]*10
for i in range(10):
    mock_door_data[i] = 0
mock_door_data[5] = 1
mock_door_data[9] = 1


# Create loop to run all FSMs
def loop_all():
    emergency = False
    pressure = 0  # Pressure variable

    while(emergency is False):
        i = 0
        j = 0
        print("Command list:\n p: pressurize\n d: depressurize\n o: open door\n c: close door\n 0: turn on/off")
        command = input("Enter command: ")
        #
        # PRESSURE COMMANDS
        if(command == 'p' or command == 'P'):
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
        print("I am in idle again? ", fsm_pressure.current_state == fsm_pressure.idle)
        if(command == 'd' or command == 'D'):
            target_d = fsm_pressure.start_depressurize(t_range_d)
            # fsm_pressure.start_depressurize()
            while(pressure > target_d):
                fsm_pressure.keep_depressurize()
                pressure = pressure - 1
            fsm_pressure.done_depressurize()
        else:
            fsm_pressure.keep_idling
        print("I am in idle again? ", fsm_pressure.current_state == fsm_pressure.idle)
        #
        # LIGHT COMMANDS
        l = 0
        if(command == '0'):
            fsm_lights.change()      
        #
        # DOOR COMMANDS
        print("we idling? ", fsm_door.current_state == fsm_door.idle)
        if (command == 'o' or command == 'O'):
            fsm_door.start_open()
            while (i is 0):
                fsm_door.keep_opening()
                i = 1
                if(i is 1):
                    fsm_door.done_open()
        else:
            fsm_door.keep_idling()
        if(command == 'c' or command == 'C'):
            fsm_door.start_close()
            while(j is 0):
                fsm_door.keep_closing()
                j = 1
                if(j is 1):
                    fsm_door.done_close()
        else:
            fsm_door.keep_idling()
# Emergency is True WEEEOOO WEEEOO WEEOOO!!!
# we must handle accordingly
loop_all()

# The FSMs,their states and respective transitions have been defined
# Create loop for PressureFSM to test if it is working as expected
#       THIS HAS BEEN TESTED AND WORKS
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
#       THIS HAS BEEN TESTED AND WORKS
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
