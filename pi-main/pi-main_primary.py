def begin(config_data_dict):
    loop()

def loop():
    while True:
        data_reader.update_sensor_data()
        print(str(data_reader.get_sensor_data))
        
        #updateLights()
        
        time.sleep(0.1)

#initialization
import sys
import importlib
import time

print("STARTING SYSTEM")
    
sys.path.insert(0, '../pi-comms/pi-comms_data-reader')
data_reader = importlib.import_module('pi-comms_data-reader-v2')

print("SYSTEM READY\n-------------\n-------------\n\n")