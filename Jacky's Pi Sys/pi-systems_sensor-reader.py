import importlib
import time
subsys = importlib.import_module('pi-systems_subsystem-base')
from collections import namedtuple
    



class SensorSubsystem(subsys.IntraModCommMixin, subsys.Subsystem):    
    
    SensorData = namedtuple("SensorData", ["CO2", "O2", "temperature", "humidity", "pressure"])
    
    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=2000)

        self.sensor_data = self.SensorData(0,0,0,0,0)


    def loop(self):
        print("Running thread!")
        self.__update_sensor_data()


    def __update_sensor_data(self):
        try:
            self.intra_write(0x0A, self.generate_intra_protocol_message(
                action=self.IntraModCommAction.ExecuteProcedure,
                procedure=1
            ))
            sensor_data_msg = self.intra_read(0x0A)
        except ValueError as ve:
            print("Invalid object read from I2C.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
            return

        with self:
            # TODO make this work - accessors are invalid since protocol version.
            self.sensor_data = self.SensorData(
                CO2=sensor_data_msg.CO2,
                O2=sensor_data_msg.O2,
                temperature=sensor_data_msg.temperature,
                humidity=sensor_data_msg.humidity,
                pressure=sensor_data_msg.pressure
            )


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