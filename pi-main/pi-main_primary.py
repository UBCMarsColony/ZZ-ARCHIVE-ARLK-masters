def begin(config_data_dict):
    log.print_config(config_data_dict["log_level"])

    light_thread = light_ss.LightingThread("LightThread", 3)
    light_thread.start()
    
    loop(config_data_dict)

def loop(config_data):
    while True:
        data_reader.update_sensor_data()
        print(str(data_reader.get_sensor_data))
        
        #updateLights()
        
        time.sleep(config_data["loop_delay"])

#initialization
TAG = "pi-main_simulated"

import sys
import importlib
import time

print("STARTING SYSTEM")

#Data Reader
sys.path.insert(0, '../pi-comms')
log = importlib.import_module("pi-comms_log")

sys.path.insert(0, '../pi-comms/pi-comms_data-reader')
data_reader = importlib.import_module('pi-comms_data-reader-v2')

#Lighting
sys.path.insert(0, '../pi-systems/')
light_ss = importlib.import_module('pi-systems_lighting_lights-manager')
ss_pool = importlib.import_module('pi-systems_subsystem-pool')

print("SYSTEM READY\n-------------\n-------------\n\n")