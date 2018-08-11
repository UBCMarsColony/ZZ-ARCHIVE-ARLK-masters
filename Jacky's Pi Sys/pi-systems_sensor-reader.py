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
    
    def __init__(self, gpio, name=None, threadID=None):

        #self.serial_in = serial.Serial('/dev/ttyACM1',9600)

        super().__init__(gpio, name=name, threadID=threadID)
        self.debug = ''
        self.sensor_dat = {}
        self.rdy_flag = False

    
    def get_data(self, string_name = None):
        return self.__sensor_data[string_name]
    
    
    def thread_task(self):
        while self.is_running:
            self.__update_sensor_data()
            if self.debug != '':
                self.__sensor_data = json.loads(self.debug)
                #print(self.__sensor_data)
            self.error_check()
            time.sleep(1)
    

    def __update_sensor_data(self):
        try:    
            self.debug = sensorget.get_json_dict()
        except ValueError as ve:
            print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
        except Exception as e:
            print("An unexpected exception occurred while trying to update Pi sensor data. \n\tStack Trace: " + str(e))

    def error_check(self):
        CO2 = self.get_data('CO2')
        O2 = self.get_data('O2')
        TEMP = self.get_data('Temperature')
        #HUM = self.get_data('Humidity')
        PRESS = self.get_data('Pressure')

        if(15 < O2 < 25):
            print("O2 is nominal")
        if(300 < CO2 < 800):
            print("CO2 is nominal")
        if(-15 < TEMP < 40):
            print("Temperature is nominal")
        if(80 < PRESS < 140):
            print("Pressure is nominal")
            

#The following proves that I am sending sensor data succesffuly from arduino to pi
#dict_str = sensorget.get_json_dict()
#print("Str:\t" + dict_str)

ss=SensorSubsystem(gpio)
ss.start()
time.sleep(2)

while True:
    t = ss.get_data('O2')
    print(t)
    time.sleep(2)
    pass


