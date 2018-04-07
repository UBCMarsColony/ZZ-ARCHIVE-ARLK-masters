import sys
import os
import importlib
import argparse
import configparser

def system_begin(runtime_params):
    # Go to main system loop
    sys.path.insert(0, '../pi-main')

    if runtime_params.simulator == 0:
        pi_main_sys = importlib.import_module('pi-main_primary')
    elif runtime_params.simulator == 1:
        pi_main_sys = importlib.import_module('pi-main_simulated')

    print("Preliminary setup completed.\n")
    os.system("PAUSE")
    
    pi_main_sys.begin(runtime_params)


def parse_args():
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

        
""" -------- MAIN CODE IS BELOW --------
The code below runs (in a highly abstracted form) the initialization sequence of the colony.
All functions are defined below this chunk.
"""
#Parsing parameters
runtime_params = parse_args()

os.system("Title UBC Mars Colony - Airlock Startup Dialog")
os.system("cls")

print("\n-----------------------\n")
print("Mars Colony Airlock preliminary systems initializing...")
print("\n-----------------------\n")

system_begin(runtime_params)