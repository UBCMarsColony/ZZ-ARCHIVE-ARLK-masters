"""
Purpose: Setup all command line UI and available parameters to be set by the user. 
         Then, configure the parameters and return them for use.
Returns: A Namespace of all arguments.
"""
def parse_args():
    # Specify all available arguments 
    parser = argparse.ArgumentParser(description="Title UBC Mars Colony - Airlock Startup Dialog. All parameters outlined below:", epilog="See https://github.com/UBCMarsColony/airlock-masters for the full documentation!")
    #parser.add_argument("--gui", type=int, choices=['0','1'], default=0, help="Use GUI: 0 = No, 1 = Yes. NOTE: By using GUI, all other command link arguments are overwritten!")
    parser.add_argument("--simulator", choices=['0','1'], default=0, help="Simulation versions: 0 = Hardware Only, 1 = Fully Simulated")
    #parser.add_argument("--ssd", choices=['0','1'], default=0, help="Choose to spoof polled sensor data (temperature, pressure, o2 concentration) or not. 0 = No, 1 = Yes")
    parser.add_argument("--loop_delay", type=int, default = 100, help="Time delay between system loops, in milliseconds.")
    #parser.add_argument("--log_lev", choices=['0','1','2','3','4','5'],default = 0, help="The level at which colony debug printing will occur. 0 = Verbose, 1 = Info, 2 = Debug, 3 = Warning, 4 = Error, 5 = WTF")

    # CL ARG PARSING
    config_data = parser.parse_args()
    config_data.loop_delay = config_data.loop_delay/1000
    
    return config_data


#############################
#   P L E A S E   R E A D 
#############################
# The following initialization code must only be run once.
# However, the Process object that the base Subsystem class
# inherits tries to import the main module (this file).
# PROCESSES MUST NOT RUN THE CODE BELOW -
# If they do, they will recursively create new processes forever.
# To circumvent this, we place the code under the 
# if __name__ == "__main__" block.
if __name__ == "__main__":    
    import sys
    import os
    import importlib
    import argparse

    runtime_params = parse_args()

    os.system("Title UBC Mars Colony - Airlock Startup Dialog")
    os.system("cls")

    print("\n-----------------------")
    print("Mars Colony Airlock preliminary systems initializing...")
    print("-----------------------\n")

    #Start the initial system setup
    # Navigate to main system directory

    pi_main_sys = importlib.import_module('pi-main_primary')
    # Wait for new user input to proceediIsl
    print("Preliminary setup completed.\nSYSTEM READY")
    # os.system("PAUSE")

    # Move to the main system file. System begins lifecycle here.
    pi_main_sys.begin(runtime_params)