import sys
import importlib
from time import sleep, time
import keyboard

# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the subsystem pool for use
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

# Import all subsystem files so we can create new instances of each one.
sensor_ss = importlib.import_module('pi-systems_sensor-reader')
#door_input_ss = importlib.import_module('pi-systems_door-input-subsystem')
lights_ss = importlib.import_module('pi-systems_lights-manager')
pressure_ss = importlib.import_module('pi-systems_pressure-manager')
door_ss = importlib.import_module('pi-systems_door-subsystem')
hexdisplay_ss = importlib.import_module('pi-systems_hexdisplay-subsystem')
interface_ss = importlib.import_module('pi-systems_interface-subsystem')

"""
Purpose: Performs initial system setup and begins airlock loop cycle.
    Handles any breakouts within the loop cycle.
Parameter: runtime_params - The Namespace returned by the argument parser
    in init.py
"""


def begin(runtime_params):
    start_time = time()
    print("\n\n---INITIALIZING AIRLOCK SYSTEMS---")

    # Start initializing the vital airlock systems
    subsystems = []

    sensors = sensor_ss.SensorSubsystem(
      name="airlock1_sensors",
      thread_id=0xDE7EC7,
      addresses=0x0A)
    subsystems.append(sensors)

    subsystems.append(lights_ss.LightingSubsystem(
       name="airlock1_lights-internal",
       thread_id=0x5EE,
       pins=18))

    #global incrementer
    #incrementer = 0
    #def p(base):
    #    global incrementer
    #    return base + incrementer
    #subsystems.append(hexdisplay_ss.HexDisplaySubsystem(
  #    name="hexdisplay_internal",
   #   thread_id=0x1EDB0A12D1,
  #    address=41,
  #    display_data_fns=[
   #       lambda: p(12),
  #        lambda: p(13),
   #       lambda: p(22),interface_ss
   #       lambda: p(101)
  #    ]
   # ))

    # door_col = door_ss.DoorSubsystem(
    #   name="airlock1_door_col",
    #   thread_id=0xD00121,
    #   address=0)
    # subsystems.append(door_col)

    #subsystems.append(pressure_ss.PressureSubsystem(
    #    name="airlock1_pressurization",
    #    thread_id=0xAE120))
    #     door_input_ss.DoorInputSubsystem(
    #         name="airlock1_doorinput_col",
    # thread_id=0xC01, address="FILL ME IN", linked_door=door_col),
    # )

    # door_mars = door_ss.DoorSubsystem(
    #   name="airlock1_door_mars",
    #   thread_id=0xD00122,
    #   address="FILL ME IN")
    #

<<<<<<< HEAD
    valves = pressure_ss.PressureSubsystem("valves", 6)
=======
    subsystems.append(
        door_mars,
        door_input_ss.DoorInputSubsystem(
           name="airlock1_doorinput_mars",
           thread_id=0x12ED,
           address="FILL ME IN",
           linked_door=door_mars))

    input = input_ss.InputSubsystem("input", 5)
    input.start()

    valves = valve_ss.PressureSubsystem("valves", 6)
>>>>>>> 4cb0545f1026152ad0cc31525840d4140de77a9c
    valves.start()

    lights = lights_ss.LightingSubsystem("lights", 4)
    lights.start()

    subsystems.append(hexdisplay_ss.HexDisplaySubsystem(
      name="hexdisplay_internal",
      thread_id="hexdisp",
      address=0x29,
      display_data_fns=[
          lambda: sensors.sensor_data['O2'],
          lambda: sensors.sensor_data['CO2'],
          lambda: sensors.sensor_data['temperature'],
          lambda: sensors.sensor_data['pressure']
      ]
    ))

<<<<<<< HEAD
    
    
=======
    subsystems.append(interface_ss.InterfaceSubsystem(
        name="airlockInternalInterface",
        thread_id=12,
        inputs=[
            interface_ss.InputComponent(
                'manualoveride',
                12,
                interface_ss.InputComponent.Subtype.Switch
            ),
            interface_ss.InputComponent(
                'pressurize',
                16,
                interface_ss.InputComponent.Subtype.Button,
                on_change_callbacks={
                    1: lambda state: None if state == 0 else print("pressure")
                       #subsystems['airlock1_pressurization'].request_new_state(
                        #    subsystems['airlock1_pressurization'].TargetState.Pressurize)
                }
            ),
            interface_ss.InputComponent(
                'depressurize',
                20,
                interface_ss.InputComponent.Subtype.Button,
                on_change_callbacks={
                    1: lambda state: None if state == 0 else print("depressure")
                        #subsystems['airlock1_pressurization'].request_new_state(
                            #subsystems['airlock1_pressurization'].TargetState.Depressurize)
                }
                    
            ),
            interface_ss.InputComponent(
                'pause',
                21,
                interface_ss.InputComponent.Subtype.Button,
                on_change_callbacks={
                    1: lambda state: None if state == 0 else print("close")
                        #subsystems['airlock1_pressurization'].request_new_state(
                         #   subsystems['airlock1_pressurization'].TargetState.Close)
                }
            )
        ],
        outputs=[
            interface_ss.OutputComponent(
                n,
                p,
                interface_ss.OutputComponent.Subtype.LED)
            for n, p in [
                ["test", 14]
            ]
        ]
    ))
>>>>>>> 4cb0545f1026152ad0cc31525840d4140de77a9c

    print("---AIRLOCK SYSTEMS INITIALIZED---\n")

    print("---STARTING SUBSYSTEMS---")
    for subsystem in subsystems:
        try:
            subsystem.start()
        except Exception as e:
            print(
                "WARNING: Subsystem could not start as due to an" +
                "unexpected exception:\n\t", e)

    print("\n---ALL SUBSYSTEMS STARTED---\n")
    print("\n---STARTING FSMs---")
    fsms = importlib.import_module('pi-systems-subsys_FSMs')
    print("\n---FSM HAS STARTED---")

    keyboard.on_press(handle_cmd)
    print("\n---COMMAND INPUT ENABLED---\n.")

    print(
        "\n---AIRLOCK SETUP COMPLETE.---\nElapsed Setup Time: %i"
        % (start_time - time()))

    print("\n---STARTING LOOPER SEQUENCE---\n")

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
    pass


def handle_cmd(cmd):
    cmd = cmd.name
    subsystems = ss_pool.get_all()
    
    # Door Toggles
    if cmd is 'o' or cmd is 'O':
        print("Requesting door open")
        subsystems["airlock1_doors"].request_door_state(
            subsystems["airlock1_doors"].Procedure.OpenDoor)
    elif cmd is ',' or cmd is '.':
        print("Requesting door close")
        subsystems["airlock1_doors"].request_door_state(
            subsystems["airlock1_doors"].Procedure.CloseDoor)

    # Pressure Toggles
    if cmd is 'p' or cmd is 'P':
        print("Pressurizing...")
        subsystems['airlock1_pressurization'].request_new_state(
            subsystems['airlock1_pressurization'].TargetState.Pressurize)

    elif cmd is 'd' or cmd is 'D':
        subsystems['airlock1_pressurization'].request_new_state(
            subsystems['airlock1_pressurization'].TargetState.Depressurize)
        print("Depressurizing")

    elif cmd is 'c' or cmd is 'C':
        subsystems['airlock1_pressurization'].request_new_state(
            subsystems['airlock1_pressurization'].TargetState.close)
        print("Closing")

    # Sensors SS Debugging
    elif cmd is 's':
        with subsystems["airlock1_sensors"] as sensors:
            sensors.print_updates = not sensors.print_updates
            print(
                'Sensors printout %s'
                % ("enabled" if sensors.print_updates else "disabled"))

    # Light SS Debugging
    elif cmd is 'l':
        with subsystems['airlock1_lights-internal'] as lights:
            lights.toggle()
            print('\nLights %s' % ('on' if lights.light_state else 'off'))

    # General System Information/
    elif cmd is "i":
        print("Current subsystem pool items:\n---------\n")
        for key in subsystems.keys():
            print(key)
    elif cmd is "I":
        print("Current subsystem pool items:\n---------\n")
        print(repr(subsystems))
    elif cmd is '-':
        print(
            "----- KEYBOARD COMMANDS -----" +
            "\no: Request door open\nc: Request door close" +
            "\nl: Toggle Lights" +
            "\ns: Toggle sensor debug printing" +
            "\ns: Print sensor subsystem updates" +
            "\ni: Show items in subsystem pool" +
            "\nI: Show details of items int the subsystem pool" +
            "#n!: Stop Colony" +
            "\n?: Help window (this text)" +
            "\n-------------------")
    elif cmd is 'q':
        print("Incrementing")
        global incrementer
        incrementer = incrementer + 1
        print(incrementer)
    elif cmd is 'f':
        import os
        os.system('i2cdetect -y 1')
    elif cmd is '!':
        print('---STOPPING COLONY---')
        ss_pool.stop_all()
        exit(0)
