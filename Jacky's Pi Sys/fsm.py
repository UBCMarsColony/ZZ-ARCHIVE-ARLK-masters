# This file initializes all relevant modules (interface in/out, airlock subsystems, etc) for the FSMs
# Do not change the hierarchy of this file in project.

import time
import importlib
try:
    import RPi.GPIO as GPIO
    print("Detected Pi Machine. Running AIRLOCK MODE\n\n")
except RuntimeError:
    print("RuntimeError. Detected non-pi machine. Running SIMULATION MODE\n\n")
except ModuleNotFoundError:
    print("RuntimeError. Detected non-pi machine. Running SIMULATION MODE\n\n")

# Import the pins/IDs, Mock classes, FSMs
from FSM.FSMConstants import Pins, ThreadIDs, subsysID
from FSM.FSMMockClasses import MockInput, MockOutput, MockLightSubsystem
from FSM.FSMDefinitions import PressureFSM, DoorFSM, LightFSM


# State values for writing to mock output class LEDs
ON = 1
OFF = 0

# Set target values for pressure FSM.
target_p = 20  # 101.3 - Earth atmosphere roughly 101.3kPa =
target_d = 10    # 6 - Martian Atmosphere 600 Pascals

#  Create an instance of each FSM
fsm_pressure = PressureFSM()
fsm_lights = LightFSM()
fsm_door = DoorFSM()


# Create lists (or use other immutable data struct) to store inputs, outputs and subsystems.
airlock_inputs = []
airlock_outputs = []
subsystems = []

# Import the subsystems & relevant modules
try:
    FSM = importlib.import_module('FSM.FSMDefinitions')
    door_ss = importlib.import_module('pi-systems_door-subsystem')
    subsys_pool = importlib.import_module("pi-systems_subsystem-pool")
    pressure_ss = importlib.import_module('pi-systems_pressure-manager')
    light_ss = importlib.import_module('pi-systems_lights-manager')
    comms = importlib.import_module('pi-systems_communications')
    subsys_base = importlib.import_module('pi-systems_subsystem-base')
    sensor_ss = importlib.import_module('pi-systems_sensor-reader')
    subsys_inter = importlib.import_module('pi-systems_interface-subsystem')
except ModuleNotFoundError:
    print("ModuleNotFoundError while importing one of the libs!")

#  Define the pins used for the following button/switch command
#  inputs to the FSMs
p = Pins()
t = ThreadIDs()

try:
    pressure_butt = subsys_inter.InputComponent(name='Pressurize', pin=p.pressure_pin, subtype='Button')
    depressure_butt = subsys_inter.InputComponent(name='Depressurize', pin=p.depressure_pin, subtype='Button')
    lights_toggle = subsys_inter.InputComponent(name='Lights', pin=p.lights_pin, subtype='Switch')
    door_open_butt = subsys_inter.InputComponent(name='Open', pin=p.door_open_pin, subtype='Button')
    door_close_butt = subsys_inter.InputComponent(name='Close', pin=p.door_close_pin, subtype='Button')
    emergency_butt = subsys_inter.InputComponent(name='Emergency', pin=p.emergency_pin, subtype='Button')
    power_toggle = subsys_inter.InputComponent(name='Enable', pin=p.power_pin, subtype='Switch')
    pause_butt = subsys_inter.InputComponent(name='Pause', pin=p.pause_pin, subtype='Button')
    confirm_butt = subsys_inter.InputComponent(name='Confirm door', pin=p.confirm_pin, subtype='Button')
    # Add to inputs list
    airlock_inputs.append(emergency_butt)
    airlock_inputs.append(pressure_butt)
    airlock_inputs.append(depressure_butt)
    airlock_inputs.append(lights_toggle)
    airlock_inputs.append(door_open_butt)
    airlock_inputs.append(door_close_butt)
    airlock_inputs.append(power_toggle)
    airlock_inputs.append(pause_butt)
    airlock_inputs.append(confirm_butt)
except NameError:
    print("NameError while declaring inputs. Using Mock Input Class.")
    # Using mock classes on non-pi machine.  Also for debugging purposes.
    # CHANGE STATES TO SIMULATE DIFFERENT INPUTS
    in0 = MockInput("Emergency", p.emergency_pin, 1)  # Emergency button (INVERSE LOGIC) is not enabled when state 1
    in1 = MockInput("Pressurize", p.pressure_pin, 0)
    in2 = MockInput("Depressurize", p.depressure_pin, 0)
    in3 = MockInput("Light Toggle", p.lights_pin, 1)
    in4 = MockInput("Open", p.door_open_pin, 0)
    in5 = MockInput("Close", p.door_close_pin, 0)
    in6 = MockInput("Enable", p.power_pin, 1)
    in7 = MockInput("Pause", p.pause_pin, 0)
    in8 = MockInput("Confirm", p.confirm_pin, 0)

    # Add the inputs to a list
    airlock_inputs = [in0,  # Emerg
                      in1,  # Pressure
                      in2,  # Depressure
                      in3,  # Lights
                      in4,  # Open
                      in5,  # Close
                      in6,  # Enable
                      in7,  # Pause
                      in8]  # Confirm

try:
    out1 = subsys_inter.OutputComponent(name='Pressurize LED',
                                        pin=p.out1_pin,
                                        subtype='LED')  # LEDs initial state OFF
    out2 = subsys_inter.OutputComponent(name='In Progress LED',
                                        pin=p.out2_pin,
                                        subtype='LED')
    out3 = subsys_inter.OutputComponent(name='Depressurize LED',
                                        pin=p.p.out3_pin,
                                        subtype='LED')
    out4 = subsys_inter.OutputComponent(name='Enable LED',
                                        pin=p.out4_pin,
                                        subtype='LED')
    out5 = subsys_inter.OutputComponent(name='Confirm LED',
                                        pin=p.out5_pin,
                                        subtype='LED')
    out6 = subsys_inter.OutputComponent(name='Emergency LED',
                                        pin=p.out6_pin,
                                        subtype='LED')
    out7 = subsys_inter.OutputComponent(name='Pause LED',
                                        pin=p.out7_pin,
                                        subtype='LED')
    # Add outputs to the list
    airlock_outputs.append(out1)
    airlock_outputs.append(out2)
    airlock_outputs.append(out3)
    airlock_outputs.append(out4)
    airlock_outputs.append(out5)
    airlock_outputs.append(out6)
    airlock_outputs.append(out7)
except NameError:
    print("NameError while declaring outputs. Using Mock Output class")
    out1 = MockOutput(name="Pressurize LED", pin=p.out1_pin)
    out2 = MockOutput(name="In Progress LED", pin=p.out2_pin)
    out3 = MockOutput(name="Depressurized LED", pin=p.out3_pin)
    out4 = MockOutput(name='Enable', pin=p.out4_pin)
    out5 = MockOutput(name="Confirm LED", pin=p.out5_pin)
    out6 = MockOutput(name="Emergency LED", pin=p.out6_pin)
    out7 = MockOutput(name="Pause LED", pin=p.out7_pin)

    airlock_outputs = [out1,  # LED x
                       out2,  # LED x
                       out3,  # LED x
                       out4,  # LED x
                       out5,  # LED x
                       out6,  # LED x
                       out7]   # LED x

#  Now create the user interface for inputs and outputs
try:
    interface = subsys_inter.InterfaceSubsystem(name="Airlock-Colony",
                                                thread_id=t.interface_thread_id,
                                                inputs=airlock_inputs,
                                                outputs=airlock_outputs)
    interface.start()
except NameError:
    print("NameError. Skipping interface declarations\n")

try:
    # Initiate PressureSubsystem
    airlock_press_ss = pressure_ss.PressureSubsystem(name="Airlock Pressure",
                                                     thread_id=t.airlock_press_ss_thread_id)
    subsystems.append(airlock_press_ss)
    airlock_press_ss.start()
except ModuleNotFoundError:
    print("ModuleNotFoundError. Skipping Pressure subsystem initialization... ")
except NameError:
    print("NameError. Skipping Pressure subsystem initialization... ")

try:
    # Initiate the DoorSubsystem
    airlock_door_ss = door_ss.DoorSubsystem(name="Airlock Door",
                                            thread_id=t.airlock_door_ss_thread_id)
    subsystems.append(airlock_door_ss)
    airlock_door_ss.start()
except ModuleNotFoundError:
    print("ModuleNotFoundError. Skipping Door subsystem initialization... ")
except NameError:
    print("NameError. Skipping Door subsystem initialization... ")

# Initiate the LightingSubsystem.
# NOTE Throws an exception while not running on RaspPi machine
try:
    airlock_light_ss = light_ss.LightingSubsystem(name="Airlock Lights",
                                                  thread_id=t.airlock_light_ss_thread_id)
    subsystems.append(airlock_light_ss)
    airlock_light_ss.start()

except NameError:
    print("NameError. Skipping Lights subsystem declaration...")
    mock_light_ss = MockLightSubsystem(name="AirMock Lights")
    subsystems.append(mock_light_ss)

except ModuleNotFoundError:
    print("ModuleNotFoundError. Skipping Lights subsystem declaration...")
    mock_light_ss = MockLightSubsystem(name="AirMock Lights")
    subsystems.append(mock_light_ss)

# Now initiate the sensor subsystem
try:
    airlock_sensor_ss = sensor_ss.SensorSubsystem(name='Airlock Sensors',
                                                  thread_id=t.airlock_sensor_ss_thread_id,
                                                  address=t.airlock_sensor_ss_address)
    subsystems.append(airlock_sensor_ss)
    airlock_sensor_ss.start()
except TypeError:
    print("TypeError. Skipping sensors subsystem declaration, using mock data...")

except NameError:
    print("NameError. Skipping sensor subsystem declaration, using mock data...")


# Everything has been set up for either AIRLOCK MODE (Pi mode) or SIMULATION MODE (non-Pi mode)...
# Ensure review of the project documentation for
# the details on the fsm design
def fsm_loop(airlock_inputs, airlock_outputs, subsystems):
    #pressure = sensor_ss.sensor_data[3]  # Replace the line below for sensors
    pressure = 15

    try:
        airlock_press_ss = subsystems[subsysID.pressure]
        airlock_door_ss = subsystems[subsysID.door]
        airlock_light_ss = subsystems[subsysID.lights]
    except IndexError:
        print(f"Missing a subsystem.  Is len(subsystems) = 3? {len(subsystems)==3}")

    # This point in the program is handling all commands from user/airlock conditions.
    while True:
        # i and j are used for very general mock door state ...
        # i = 0 represents door not in desired state
        # i = 1 represents door in desired state

        # Check if user pressed Emergency button
        # NOTE EMERG LOGIC IS ACTIVE LOW
        if airlock_inputs[0].state == 0:
            emergency = True  # theres really no point in this besides an easier way to display Emergencies to user
            if(fsm_pressure.current_state.name == 'idle'):
                fsm_pressure.detected_emerg_3(airlock_press_ss, airlock_outputs)
            elif(fsm_pressure.current_state.name == 'Emergency'):
                fsm_pressure.emerg_unresolved(airlock_press_ss, airlock_outputs)
            if(fsm_door.current_state.name == 'Idle'):
                fsm_door.detected_emerg_3(airlock_door_ss)
            elif(fsm_door.current_state.name == 'Emergency'):
                fsm_door.emerg_unresolved(airlock_door_ss)

        # Check if the STSD switch enables the P/D/H buttons.  Doesnt effect lights
        if airlock_inputs[6].state == 1:
            out4.write(ON) # This turns on an LED

            # Check if user pressed P
            # AIR./SIM.: CHANGE THIS TO READ SENSOR DATA NOT MOCK DATA: pressure
            if airlock_inputs[1].state == 1 and airlock_inputs[0].state == 1:
                # Begin Pressurization sequence.
                fsm_pressure.start_pressurize(airlock_press_ss, airlock_outputs)

                # While not done pressurizing to target...
                #while (sensor_ss.sensor_data[3] < target_p):  # REPLACE LINE BELOW WITH THIS FOR SENSORS
                while (pressure < target_p):
                    if airlock_inputs[0].state == 1:  # check for emerg. while pressurizing
                        if airlock_inputs[7].state == 1:  # check if user wants to pause
                            if fsm_pressure.current_state.name == "pressurize":
                                fsm_pressure.pause_press(airlock_press_ss, airlock_outputs)
                                while airlock_inputs[7].state is 1:
                                    fsm_pressure.keep_pausing(airlock_press_ss)
                                fsm_pressure.resume_press(airlock_press_ss, airlock_outputs)
                        else:
                            # This is for no pausing & no emergencies.
                            fsm_pressure.keep_pressurize(airlock_press_ss, airlock_outputs)
                            time.sleep(0.001)           # Take this out when sensors implemented
                            pressure = pressure + 1     # Take this out when sensors implemented
                            #sensor_ss.__update_sensor_data()  # Not sure if the sensors are read continuously but update the sensor value
                            print("PRESSURIZING...")
                    else:
                        if(fsm_pressure.current_state == fsm_pressure.Emergency):
                            fsm_pressure.emerg_unresolved(airlock_press_ss, airlock_outputs) # Emerg to Emerg
                        else:
                            fsm_pressure.detected_emerg_1(airlock_press_ss, airlock_outputs) # Press to Emerg
                fsm_pressure.done_pressurize(airlock_press_ss, airlock_outputs)
            else:
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    fsm_pressure.emerg_unresolved(airlock_press_ss, airlock_outputs)
                else:
                    fsm_pressure.keep_idling(airlock_press_ss)

            # Check if user pressed D
            # CHANGE THIS TO READ SENSOR DATA NOT MOCK DATA
            if airlock_inputs[2].state == 1 and airlock_inputs[0].state == 1:
                fsm_pressure.start_depressurize(airlock_press_ss, airlock_outputs)
                #while (sensor_ss.sensor_data[3] < target_d):  # REPLACE LINE BELOW WITH THIS FOR SENSORS
                while(pressure > target_d):
                    if airlock_inputs[0].state == 1:
                        if airlock_inputs[7].state == 1:
                            if fsm_pressure.current_state.name == 'depressurize': # This is redundant!!!!
                                fsm_pressure.pause_depress(airlock_press_ss, airlock_outputs)
                                while airlock_inputs[7].state is 1:
                                    fsm_pressure.keep_pause(airlock_press_ss)
                                fsm_pressure.resume_depress(airlock_press_ss, airlock_outputs)
                        else:
                            fsm_pressure.keep_depressurize(airlock_press_ss, airlock_outputs)
                            time.sleep(0.001)            # Take this out when sensors implemented
                            pressure = pressure - 1  # Take this out when sensors implemented
                            print("DEPRESSURIZING")
                    else:
                        if(fsm_pressure.current_state == fsm_pressure.Emergency):
                            fsm_pressure.emerg_unresolved(airlock_press_ss, airlock_outputs)
                        else:
                            fsm_pressure.detected_emerg_2(airlock_press_ss, airlock_outputs)
                    # sensor_ss.__update_sensor_data()  # Might need to manually update. check how sensors are read
                fsm_pressure.done_depressurize(airlock_press_ss, airlock_outputs)
            else:
                if(fsm_pressure.current_state == fsm_pressure.Emergency):
                    fsm_pressure.emerg_unresolved(airlock_press_ss, airlock_outputs)
                else:
                    fsm_pressure.keep_idling(airlock_press_ss)

            print("I am in idle again? ",
                  fsm_pressure.current_state == fsm_pressure.idle)
        else:
            print("EN OFF. ")
            out4.write(OFF)

        # Check if user pressed L
        if airlock_inputs[3].state == 0:
            # we want the lights off and theyre on
            if fsm_lights.current_state.name == "ON":
                try:
                    fsm_lights.turn_off(airlock_light_ss)
                except NameError:
                    pass
            # else the light switch is ON
            else:
                pass
        else:
            if fsm_lights.current_state.name == "OFF":
                try:
                    fsm_lights.turn_on(airlock_light_ss)
                except NameError:
                    pass
            else:
                pass

        #Check if user pressed Door open
        if airlock_inputs[4].state == 1 and airlock_inputs[0].state == 1:
            fsm_door.start_open(airlock_door_ss)
            #door_state, door_angle = door_ss.get_current_door_state()

            # While the door is not open
            while airlock_inputs[8].state is 0:
                if airlock_inputs[0].state == 1:
                    fsm_door.keep_opening(airlock_door_ss)
                    airlock_inputs[8].state = 1  # Simulate user pressing button
                    #door_state, door_angle = door_ss.get_current_door_state(airlock_door_ss)
                else:
                    if fsm_door.current_state.name == "Open":
                        fsm_door.detected_emerg_1(airlock_door_ss)
                    elif fsm_door.current_state.name == "Emergency":
                        fsm_door.emerg_unresolved(airlock_door_ss)
            fsm_door.done_open(airlock_door_ss)
            airlock_inputs[8].state = 0  # Reset the confirm button for simulation
        else:
            if fsm_door.current_state == fsm_door.Emergency:
                fsm_door.emerg_unresolved(airlock_door_ss)
            else:
                # no code red so keep idling
                fsm_door.keep_idling(airlock_door_ss)

        # Check if user pressed Door Close
        if airlock_inputs[5].state == 1 and airlock_inputs[0].state == 1:
            fsm_door.start_close(airlock_door_ss)
            while airlock_inputs[8].state is 0:
                if airlock_inputs[0].state == 1:
                    fsm_door.keep_closing(airlock_door_ss)
                    airlock_inputs[8].state = 1  # Simulate the confirm button being pressed
                else:
                    if fsm_door.current_state == fsm_door.Emergency:
                        fsm_door.emerg_unresolved(airlock_door_ss)
                    else:
                        fsm_door.detected_emerg_2(airlock_door_ss)
            fsm_door.done_close(airlock_door_ss)
            airlock_inputs[8].state = 0  # Reset the confirm button for simulation
        else:
            if fsm_door.current_state == fsm_door.Emergency:
                fsm_door.emerg_unresolved(airlock_door_ss)
            else:
                fsm_door.keep_idling(airlock_door_ss)

        print(f"Current Pressure State: {fsm_pressure.current_state.name}")
        print(f"Current Door State: {fsm_door.current_state.name}")
        print(f"Current Light State: {fsm_lights.current_state.name}")
        print("Airlock input states:")
        for input in airlock_inputs:
            print(f"{input.name}: {input.state}")
        print("\n\n")


fsm_loop(airlock_inputs,
         airlock_outputs,
         subsystems)
