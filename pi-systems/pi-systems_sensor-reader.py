subsys = importlib.import_module('pi-systems_subsystem-base')

try:
    import serial
except ModuleNotFoundError:
    print("Could not import serial.")

import json
    
# JSON raspberry pi data reader code, take serial data from python

class SensorSubsystem(subsys.Subsystem):
    
    __sensor_data = {}
    
    def __init__(self, gpio, name=None, threadID=None):

        self.serial_in = serial.Serial('/dev/ttyACM1',9600)

        super().__init__(gpio, name, threadID)

    
    def get_data(self, string_name = None):
        if string_name is None:
            return SensorSubsystem.__sensor_data
        else:   
            try:
                return SensorSubsystem.__sensor_data[string_name]
            except KeyError as ve:
                print("Failed to find a value associated with the key " + string_name + ". Returning entire dictionary instead...")
                return SensorSubsystem.__sensor_data
            except Exception as e:
                print("An unexpected exception occurred while trying to retrieve sensor data.\n\tStack Trace: " + str(e))
        
        return None
    
    
    def thread_task(self):
        self.__update_sensor_data()
    

    def __update_sensor_data(self):
        try:    
            next_line = self.serial_in.readline()
            
            SensorSubsystem.__sensor_data = __get_decoded_json_string(next_line)

        except ValueError as ve:
            print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
        except Exception as e:
            print("An unexpected exception occurred while trying to update Pi sensor data. \n\tStack Trace: " + str(e))
            
    
    # function that securely decodes a JSON string
    def __get_decoded_json_string(self, encoded_json):
        try:
            return json.loads(encoded_json)
        except ValueError:
            raise ValueError
