import importlib
import RPi.GPIO as gpio
import time
subsys = importlib.import_module('pi-systems_subsystem-base')
sensorget = importlib.import_module('get_arduino_sensor')

try:
    import serial
except ModuleNotFoundError:
    print("Could not import serial.")

import json
    
# JSON raspberry pi data reader code, take serial data from python

class SensorSubsystem(subsys.Subsystem):
    
    __sensor_data = {}
    
    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id)


    def run(self):
        while self.running:
            with self.thread.lock:
                self.__update_sensor_data()
            time.sleep(2)


    def get_data(self, string_name=None):
        if string_name is None:
            for key in self.__sensor_data:
                self.__sensor_data[key] = float(self.__sensor_data[key])  #int to double
            return self.__sensor_data
        else:
            return float(self.__sensor_data[string_name])
    

    def __update_sensor_data(self):
        try:    
            sensor_json = sensorget.get_json_dict()
            if sensor_json != '':
                self.__sensor_data = json.loads(sensor_json)
        except ValueError as ve:
            print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
        except Exception as e:
            print("An unexpected exception occurred while trying to update Pi sensor data. \n\tStack Trace: " + str(e))


    def error_check(self):
        CO2 = self.get_data('CO2')
        O2 = self.get_data('O2')
        TEMP = self.get_data('Temperature')
        HUM = self.get_data('Humidity')
        PRESS = self.get_data('Pressure')

        if(15 < O2 < 25):
            print("O2 is nominal")
        if(300 < CO2 < 800):
            print("CO2 is nominal")
        if(-15 < TEMP < 40):
            print("Temperature is nominal")
        if(80 < PRESS < 140):
            print("Pressure is nominal")
        if(20 < HUM < 80):
            print("Humidity is nominal")
            
if __name__ == "__main__":
    #The following proves that I am sending sensor data succesffuly from arduino to pi
    dict_str = sensorget.get_json_dict()
    print("Str:\t" + dict_str)

    ss=SensorSubsystem(thread_id=5)
    ss.start()
    time.sleep(5)

    for i in range(10):
        t = ss.run_method_async(ss.get_data)
        print(t)
        t = ss.srun_method_async(lambda: ss.get_data("O2"))
        print(t)
        time.sleep(2)
    ss.stop()