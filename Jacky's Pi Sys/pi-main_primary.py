import sys
import importlib
from time import sleep, time
import keyboard

<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
=======

>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the subsystem pool for use
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

# Import all subsystem files so we can create new instances of each one.
#sensor_ss = importlib.import_module('pi-systems_sensor-reader')
#door_input_ss = importlib.import_module('pi-systems_door-input-subsystem')
#lights_ss = importlib.import_module('pi-systems_lights-manager')
pressure_ss = importlib.import_module('pi-systems_pressure-manager')
#door_ss = importlib.import_module('pi-systems_door-subsystem')

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

    # DO THESE WORK!!!!!!!

    subsystems.append(sensor_ss.SensorSubsystem(
       name="airlock1_sensors",
       thread_id=0xDE7EC7,
       address=0x0A))

    subsystems.append(lights_ss.LightingSubsystem(
       name="airlock1_lights-internal",
       thread_id=0x5EE,
       pins=18))

    subsystems.append(door_ss.DoorSubsystem(
       name="airlock1_door_col",
       thread_id=0xD00121,
       address=0))

    subsystems.append(pressure_ss.PressureSubsystem(
        name="airlock1_pressurization",
        thread_id=0xAE120))
    #     door_input_ss.DoorInputSubsystem(
    #         name="airlock1_doorinput_col",
    # thread_id=0xC01, address="FILL ME IN", linked_door=door_col),
    # )

    # door_mars = door_ss.DoorSubsystem(
    #   name="airlock1_door_mars",
    #   thread_id=0xD00122,
    #   address="FILL ME IN")
    #
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
    valves.start()

    lights = light_ss.LightingSubsystem("lights", 4)
    lights.start()

    print("---AIRLOCK SYSTEMS INITIALIZED---\n")

    print("---STARTING SUBSYSTEMS---")
    for subsystem in subsystems:
        try:
            subsystem.start()
        except Exception as e:
            print(
                "WARNING: Subsystem could not start as due to an" +
                "unexpected exception:\n\t", e)

    print("\n---ALL SUBSYSTEMS STARTED---")

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
    # <<<<<<< HEAD
    # if cmd is 'o' or cmd is 'O':
    #     print("Requesting door open")
    #     subsystems["airlock1_doors"].request_door_state(subsystems["airlock1_doors"].Procedure.OpenDoor)
    # elif cmd is 'c' or cmd is 'C':
    #     print("Requesting door close")
    #     subsystems["airlock1_doors"].request_door_state(subsystems["airlock1_doors"].Procedure.CloseDoor)
=======
    if cmd is 'o' or cmd is 'O':
        print("Requesting door open")
        subsystems["airlock1_doors"].request_door_state(
            subsystems["airlock1_doors"].Procedure.OpenDoor)
    elif cmd is 'c' or cmd is 'C':
        print("Requesting door close")
        subsystems["airlock1_doors"].request_door_state(
            subsystems["airlock1_doors"].Procedure.CloseDoor)
<<<<<<< HEAD
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
=======
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74

    # Pressure Toggles
    if cmd is 'p' or cmd is 'P':
        print("Pressurizing...")
        subsystems['airlock1_pressurization'].request_new_state(
            subsystems['airlock1_pressurization'].TargetState.Pressurize)

    elif cmd is 'd' or cmd is 'D':
        subsystems['airlock1_pressurization'].request_new_state(
            subsystems['airlock1_pressurization'].TargetState.Depressurize)
        print("Depressurizing")

<<<<<<< HEAD

    # # Sensors SS Debugging
    # elif cmd is 's':
    #     with subsystems["airlock1_sensors"] as sensors:
    #         sensors.print_updates = not sensors.print_updates
    #         print('Sensors printout %s' % ("enabled" if sensors.print_updates else "disabled"))

    # # Light SS Debugging
    # elif cmd is 'l':
    #     with subsystems['airlock1_lights-internal'] as lights:
    #         lights.toggle()
    #         print('\nLights %s' % ('on' if lights.light_state else 'off'))
    
=======
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

<<<<<<< HEAD
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
=======
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
    # General System Information/
    elif cmd is "i":
        print("Current subsystem pool items:\n---------\n")
        for key in subsystems.keys():
            print(key)
    elif cmd is "I":
        print("Current subsystem pool items:\n---------\n")
        print(repr(subsystems))
    elif cmd is '?':
<<<<<<< HEAD
<<<<<<< HEAD
        print("----- KEYBOARD COMMANDS -----" +
            #"\no: Request door open\nc: Request door close" +
            #"\nl: Toggle Lights" + 
            #"\ns: Toggle sensor debug printing" +
            "\ni: Show items in subsystem pool" +
            "\nI: Show details of items int the subsystem pool" +
            "\n!: Stop Colony" +
            "\n?: Help window (this text)" + 
=======
=======
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
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
<<<<<<< HEAD
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
=======
>>>>>>> 6786c97cdd78e5f78e38495af5685a0b98cdab74
            "\n-------------------")
    elif cmd is '!':
        print('---STOPPING COLONY---')
        ss_pool.stop_all()
        exit(0)
