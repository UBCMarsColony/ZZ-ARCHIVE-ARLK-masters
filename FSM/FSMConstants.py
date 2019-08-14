# File to store all the pins and thread id's for the FSM systems
# All IDs and Pins names correspond to those in fsm.py


class Pins:
    """
    Input pins.  Names should be refactored to whatever makes sense for your project.
    """
    pressure_pin = 29
    depressure_pin = 31
    lights_pin = pin = 32
    door_open_pin = 33
    door_close_pin = 35
    emergency_pin = 36
    power_pin = 37
    pause_pin = 38
    confirm_pin = 40

    """
    Output pins
    """
    out1_pin = 11
    out2_pin = 12
    out3_pin = 13
    out4_pin = 15
    out5_pin = 16
    out6_pin = 18
    out7_pin = 19


class ThreadIDs:
    """
    Thread IDs for Subsystems and Interface(s).  (Don't think threading is used anyway)
    """
    interface_thread_id = 49
    airlock_press_ss_thread_id = 50
    airlock_door_ss_thread_id = 51
    airlock_light_ss_thread_id = 52
    airlock_sensor_ss_thread_id = 53
    airlock_sensor_ss_address = 10


class subsysID:
    pressure = 0
    door = 1
    lights = 2
