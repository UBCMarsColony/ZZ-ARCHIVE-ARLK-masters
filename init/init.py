import sys
import os
import importlib
import argparse

parser = argparse.ArgumentParser(description="Mars Colony Airlock Emulator by The Electrical Team!", epilog="See https://github.com/UBCMarsColony/airlock-masters for the full documentation!")
parser.add_argument("--simulator", choices=[0,1], default=0, help="Simulation versions: 0 = Hardware Only, 1 = Fully Simulated")
    
parser.add_argument("--spoof_sensor_data", choices=[0,1], default=0, help="Choose to spoof polled sensor data (temperature, pressure, o2 concentration) or not. 0 = No, 1 = Yes")
parser.add_argument("--gui", type=int, choices=[0,1], default=0, help="Use GUI: 0 = No, 1 = Yes. NOTE: By using GUI, all other command link arguments are overwritten!")
parser.add_argument("--loop_delay", type=int, default = 100, help="Time delay between system loops, in milliseconds.")

args = parser.parse_args()

if args.gui != None and int(args.gui) == 1:
    run_gui()
else:
    config_data = {}
    config_data["Simulator"] = int(args.simulator)
    config_data["Spoof_Sensor_Data"] = int(args.spoof_sensor_data)
    config_data["Loop_Delay"] = int(args.loop_delay) / 1000
    

print("\n-----------------------\n")
print("Mars Colony Airlock will begin initializing momentarily...")
os.system("PAUSE")

# Go to main system loop
sys.path.insert(0, '../pi-main')
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