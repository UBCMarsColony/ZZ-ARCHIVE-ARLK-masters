
#######################################################################################
#           CODE FOR A PRESSURE VALVE TEST WITH SIMPLE GUI
#######################################################################################

import sys
import importlib
import time
import tkinter as tk

# Begin systems get
sys.path.insert(0, '../pi-systems/')

# Import the subsystem pool for use
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

# Import all subsystem files so we can create new instances of each one
pressure_ss = importlib.import_module('pi-systems_pressure-manager')


"""
Purpose: Performs initial system setup and begins airlock loop cycle. Handles any breakouts within the loop cycle.
Parameter: runtime_params - The Namespace returned by the argument parser in init.py
"""
def begin(runtime_params):
    start_time = time() 
    print("\n\n---INITIALIZING AIRLOCK SYSTEMS---")
    
    # Start initializing the vital airlock systems
    subsystems = []

    subsystems.append(pressure_ss.PressureSubsystem(name="airlock1_pressurization", thread_id=0xAE120))
    
    print("---AIRLOCK SYSTEMS INITIALIZED---\n")

    print("---STARTING SUBSYSTEMS---")
    for subsystem in subsystems:
        try:
            subsystem.start()
        except Exception as e:
            print("WARNING: Subsystem could not start as due to an unexpected exception:\n\t", e)
    
    print("\n---ALL SUBSYSTEMS STARTED---")

    keyboard.on_press(handle_cmd)
    print("\n---COMMAND INPUT ENABLED---\n.")

    print("\n---AIRLOCK SETUP COMPLETE.---\nElapsed Setup Time: %i" % (start_time - time()))
    
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

def Pressurize():
    SetValve(1)

def Depressure():
    SetValve(2)

def Abort():
    #noah fill me in pls!!!
    pass

def MakeButton():
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    #Create a button to start the pressurization.
    button1 = tk.Button(frame, text="Quit", fg="red", command=quit)
    button1.pack(side=tk.LEFT)
    slogan = tk.Button(frame,text="Pressurization",fg="blue", command=Pressurize)
    slogan.pack(side=tk.LEFT)

    #Create a button to start the depressurization.
    button2 = tk.Button(frame, text="Depressurization", fg="green", command=Depressure)
    button2.pack(side=tk.RIGHT)

    try:
        root.mainloop()
    except SystemExit:
        print("\nThe user has exited pressurization process!")


def SetValve(cmd):
    subsystems = ss_pool.get_all()
    countP = 0 # counter for Pressurization loop iterations
    countD = 0 
    limitP = 5 # Pressure cycle repeats for 5 cycles
    limitD = 5 

    if (cmd == 1):
        print("Set P valve")
        #subsystems['airlock1_pressurization'].request_new_state(subsystems['airlock1_pressurization'].TargetState.Pressurize)

        # Start counting 
        while(countP < limitP):
            print(countP)
            time.sleep(1)
            countP = countP + 1
    
        if(countP == limitP):
            print("Set to Idle ") # comment this out when testing (uncomment line below)
            #subsystems['airlock1_pressurization'].request_new_state(subsystems['airlock1_pressurization'].TargetState.Idle)
            cmd = 0 # Gotta reset cmd so it doesnt go back and pressurize again
            print("~~ DONE PRESSURIZATION ~~~")

    elif (cmd == 2):
        print("Set D valve") # comment this out when testing (uncomment line below)
        #subsystems['airlock1_pressurization'].request_new_state(subsystems['airlock1_pressurization'].TargetState.Depressurize)

        while(countD < limitD):
            print(countD)
            time.sleep(1)
            countD = countD + 1
    
        if(countD == limitD):
            print("Set to Idle ")
            #subsystems['airlock1_pressurization'].request_new_state(subsystems['airlock1_pressurization'].TargetState.Idle)
            cmd = 0
            print("DONE")

cmd = 0
MakeButton()
SetValve(cmd)







