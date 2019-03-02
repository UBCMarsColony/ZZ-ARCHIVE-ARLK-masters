import importlib
import time
import struct
from enum import Enum
from collections import namedtuple
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')


class SensorSubsystem(comms, subsys.Subsystem):

    # SensorData = namedtuple("SensorData", ["CO2", "O2", "temperature",
    # "humidity", "pressure"])

    class Procedure(Enum):
        GetSensorData = 1

    def __init__(self, name=None, thread_id=None, addresses=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=2000)

        # namedtuple is temporarily a dict for pickling purposes.
        self.sensor_data = {}  # self.SensorData(0,0,0,0,0)
        # sets addresses to a list of 1 or more addresses
        self.addresses = addresses if isinstance(addresses,
                                                 list) else [addresses]
        self.print_updates = False

    def loop(self):
        with self.lock:
            self.__update_sensor_data()

            if self.print_updates:
                print(self.sensor_data)

    def __update_sensor_data(self):
        # return
        # comms._write(self.address, comms.IntraModCommMessage.generate(
        #     action=comms.IntraModCommAction.ExecuteProcedure,
        #     procedure=1
        # ))
        #
        # init values to 0
        O2Val, humidityVal, temperatureVal,
        pressureVal, C02Val = (0, 0, 0, 0, 0)

        numReadingsO2, numReadingsHumidity, numReadingsTemp,
        numReadingsPressure, numReadingsC02 = (0, 0, 0, 0, 0)
        # read all the data from multiple addresses if they exist and then
        # get the average of valid readings and store into sensor_data
        # dictionary also checking valid dataFlags bitmask
        for addressVal in self.addresses:
            try:
                # extract raw sensor data
                sensor_data_raw = comms.intra_read(
                    addressVal, self.Procedure.GetSensorData.value)
                # unpack sensor_data_raw into sensor_data following
                # struct created in AirlockMasters/sensors/Integrated
                # sensors/integrated_sensors/integrated_sensors.ino
                sensor_data = struct.unpack(
                    'cccBBBhHH', bytes(sensor_data_raw.raw_array[
                        0:struct.calcsize('cccBBBhHH')]))
                # sensor_data[3] is validFlag readings mask
                validData = sensor_data[3]
                # bitwise AND bitmask to see if data is valid and read
                if validData & 1 << 7:
                    O2Val += sensor_data[4]
                    numReadingsO2 += 1
                if validData & 1 << 6:
                    humidityVal += sensor_data[5]
                    numReadingsHumidity += 1
                if validData & 1 << 5:
                    temperatureVal += sensor_data[6]
                    numReadingsTemp += 1
                if validData & 1 << 4:
                    pressureVal += sensor_data[7]
                    numReadingsPressure += 1
                if validData & 1 << 3:
                    C02Val += sensor_data[8]
                    numReadingsC02 += 1
            except ValueError as ve:
                print("Invalid object read from I2C.\n\tStackTrace: " +
                      str(ve) + "\n\tSkipping line...")

        # computes average of all readings
        O2Val = O2Val / numReadingsO2
        humidityVal = humidityVal / numReadingsHumidity
        temperatureVal = temperatureVal / numReadingsTemp
        pressureVal = pressureVal / numReadingsPressure
        C02Val = C02Val / numReadingsC02

        # stores average readings into dictionary
        self.sensor_data = {
            'O2': O2Val,
            'humidity': humidityVal,
            'temperature': temperatureVal,
            'pressure': pressureVal,
            'CO2': C02Val
        }

    def error_check(self):
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


            
