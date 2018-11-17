import importlib
import time
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

from collections import namedtuple
    
import struct


class SensorSubsystem(comms.IntraModCommMixin, subsys.Subsystem):    
    
    # SensorData = namedtuple("SensorData", ["CO2", "O2", "temperature", "humidity", "pressure"])
    
    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=2000)

        # namedtuple is temporarily a dict for pickling purposes.
        self.sensor_data = {}#self.SensorData(0,0,0,0,0)
        self.address = address
        self.print_updates = False


    def loop(self):
        self.__update_sensor_data()


    def __update_sensor_data(self):
        # return

        try:
            # self.intra_write(self.address, self.IntraModCommMessage.generate(
            #     action=self.IntraModCommAction.ExecuteProcedure,
            #     procedure=1
            # ))
            sensor_data_raw = self.intra_read(self.address)
        
            sensor_data = struct.unpack('>xxBBHHH', bytes(sensor_data_raw.raw_array[0:struct.calcsize('xxBBHHH')]))

        except ValueError as ve:
            print("Invalid object read from I2C.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
            return

        with self:
            # TODO make this work - accessors are invalid since protocol version.
            self.sensor_data = {
                'O2':sensor_data[0],
                'humidity':sensor_data[1],
                'temperature':sensor_data[2],
                'pressure':sensor_data[3],
                'CO2':sensor_data[4]
            }

            if self.print_updates:
                print(self.sensor_data)


    def error_check(self):
        with self:
            CO2 = self.sensor_data.CO2
            O2 = self.sensor_data.O2
            TEMP = self.sensor_data.temperature
            HUM = self.sensor_data.humidity
            PRESS = self.sensor_data.pressure

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
    dict_str = self.get_json_dict()
    print("Str:\t" + dict_str)

    ss=SensorSubsystem(thread_id=5)
    ss.start()
    time.sleep(5)

    for i in range(10):
        with ss.thread.lock:
            t = ss.get_data()
            print(t)
            t = ss.get_data("O2")
            print(t)
        
        time.sleep(2)
    ss.stop()