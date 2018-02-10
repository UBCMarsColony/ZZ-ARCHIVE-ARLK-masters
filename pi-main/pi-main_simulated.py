def begin(config_data_dict):
    loop(config_data_dict)

def loop(config_data):
    while True:
    
        if config_data["Spoof_Sensor_Data"] == 1:
            data_reader.update_sensor_data()
        else:
            #SPOOF UPDATES THE "LOCAL" VARIABLE
            data_reader.__sensor_data = {"GasComposition":{"CO2":450, "O2":21.3},"Temperature":25, "Pressure":100000000000, "Motion Detector":0}
            
        print(str(data_reader.get_sensor_data()))
        
        #updateLights()
        
        time.sleep(config_data["Loop_Delay"])

#initialization
import sys
import importlib
import time

print("STARTING SYSTEM")
    
sys.path.insert(0, '../pi-comms/pi-comms_data-reader')
data_reader = importlib.import_module('pi-comms_data-reader-v2')

print("SYSTEM READY\n-------------\n-------------\n\n")