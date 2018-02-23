import sys
import os
import importlib
import argparse
import configparser


def parse_args():
    parser = argparse.ArgumentParser(description="Mars Colony Airlock Emulator by The Electrical Team!", epilog="See https://github.com/UBCMarsColony/airlock-masters for the full documentation!")
    parser.add_argument("--gui", type=int, choices=['0','1'], default=0, help="Use GUI: 0 = No, 1 = Yes. NOTE: By using GUI, all other command link arguments are overwritten!")
    parser.add_argument("--simulator", choices=['0','1'], default=0, help="Simulation versions: 0 = Hardware Only, 1 = Fully Simulated")
    parser.add_argument("--ssd", choices=['0','1'], default=0, help="Choose to spoof polled sensor data (temperature, pressure, o2 concentration) or not. 0 = No, 1 = Yes")
    parser.add_argument("--loop_del", type=int, default = 100, help="Time delay between system loops, in milliseconds.")
    parser.add_argument("--log_lev", choices=['0','1','2','3','4','5'],default = 0, help="The level at which colony debug printing will occur. 0 = Verbose, 1 = Info, 2 = Debug, 3 = Warning, 4 = Error, 5 = WTF")

    # CL ARG PARSING
    args = parser.parse_args()

    if args.gui != None and int(args.gui) == 1:
        run_gui()
    else:
        config_data = {}
        config_data["Simulator"] = int(args.simulator)
        config_data["ssd"] = int(args.ssd)
        config_data["loop_delay"] = int(args.loop_del) / 1000
        
        log_config = [True, True, True, True, True]
        for i in range(0,int(args.log_lev)):
            log_config[i] = False
        config_data["log_level"] = log_config
    
    return config_data
    
    
def system_begin():
    # Go to main system loop
    sys.path.insert(0, '../pi-main')

    global config_data
    if config_data["Simulator"] == 0:
        pi_main_sys = importlib.import_module('pi-main_primary')
    elif config_data["Simulator"] == 1:
        pi_main_sys = importlib.import_module('pi-main_simulated')

    pi_main_sys.begin(config_data)
    
    
def run_gui():
    import tkinter as tk

    class MainApplication(tk.Frame):
        def __init__(self, e, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.parent = parent

          # <create the rest of your GUI here>

    if __name__ == "__main__":
        root = tk.Tk()
        MainApplication(root).pack(side="top", fill="both", expand=True)
        root.mainloop()

        
""" -------- MAIN CODE IS BELOW --------
The code below runs (in a highly abstracted form) the initialization sequence of the colony.
All functions are defined below this chunk.
"""
#Pars
config_data = parse_args()

os.system("Title UBC Mars Colony Dialog")
os.system("cls")

print("\n-----------------------\n")
print("Mars Colony Airlock will begin initializing momentarily...")
print("\n-----------------------\n")
os.system("PAUSE")

system_begin()