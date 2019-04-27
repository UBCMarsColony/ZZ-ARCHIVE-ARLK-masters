# OLD CODE
# Control logic with FSM/subsys logic implemented
# Interface logic not implemented


# Create loop to run all FSMs
def loop_FSMs(subsystems):
    # Force start loop with False
    emergency = False
    pressure = 0  # Pressure variable.  Will be sensor data
    #emergency_status = emergency_butt.read()

    #while(emergency_status == 0)
    while(emergency is False):
        # i and j are used for door logic
        i = 0
        j = 0
'''
        # Get button States
        # Assume buttons are always pressed by user one at a time
        # logic: 0 if not pressed, 1 if pressed.
        try:
            emergency_status = emergency_butt.read()
            start_pressurize = pressure_butt.read()
            start_depressurize = depressure_butt.read()
            switch_position = lights_toggle.read()
            door_open = door_open_butt.read()
            door_close = door_close_butt.read()
        except NameError:
            print("Skipping button reading...Module GPIO not found")
'''
        # These print statements will change to button interfaces on the switch box.
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
        # say user pushes the EMERG button.  Set the Loop variable 
        # if(emergency_status == 1)
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
            while (pressure < target_p) and emergency is False:  # SPLIT THE while() LOGIC 
                # ... we loop back into our current state
                fsm_pressure.keep_pressurize(airlock_press_ss)
                time.sleep(1)
                pressure = pressure + 1
                print("PRESSURIZING...")
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
            door_state = airlock_door_ss.loop()
            print(door_state)
            while (i is 0 and emergency is False):
                fsm_door.keep_opening(airlock_door_ss)
                # i var represents when the door is in the process of opening
                i = 1
                if(i is 1):
                    fsm_door.done_open(airlock_door_ss)
        elif (emergency is True):
            # if theres an emerg we gotta handle it
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