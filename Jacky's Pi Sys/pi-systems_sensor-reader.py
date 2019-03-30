import importlib
import time
import struct
from enum import Enum
from collections import namedtuple
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')


class SensorSubsystem(subsys.Subsystem):

    # SensorData = namedtuple("SensorData", ["CO2", "O2", "temperature",
    # "humidity", "pressure"])

    class Procedure(Enum):
        GetSensorData = 1

    def __init__(self, name=None, thread_id=None, addresses=None, segment_addresses=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=2000)

        self.segment_addresses = segment_addresses
        # namedtuple is temporarily a dict for pickling purposes.
        self.sensor_data = {}  # self.SensorData(0,0,0,0,0)
        # sets addresses to a list of 1 or more addresses
        self.addresses = addresses if isinstance(addresses,
                                                 list) else [addresses]
        self.print_updates = False
        # initialize readings lists in constructor
        # index 0 is oldest reading
        self.O2_readings = []
        self.C02_readings = []
        self.temp_readings = []
        self.humidity_readings = []
        self.pressure_readings = []

        keep_track_seconds = 5

    def loop(self):
        with self.lock:
            self.__update_sensor_data()

            if self.print_updates:
                print(self.sensor_data)
                # use seven_segment_addresses dict here to
                # print proper info to displays
                # remember to convert sensor data to proper format
                # eg. comms.write(self.sensor_data['C02'],
                # segment_address['C02'])

    def __update_sensor_data(self):
        # return
        # comms._write(self.address, comms.IntraModCommMessage.generate(
        #     action=comms.IntraModCommAction.ExecuteProcedure,
        #     procedure=1
        # ))

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
                # and put into readings list as a list with time associated
                # in index 1 of sublists in readings list
                if validData & 1 << 7:
                    self.O2_readings.append([sensor_data[4], time.time()])
                if validData & 1 << 6:
                    self.humidity_readings.append([sensor_data[5], time.time()])
                if validData & 1 << 5:
                    self.temp_readings.append([sensor_data[6], time.time()])
                if validData & 1 << 4:
                    self.pressure_readings.append([sensor_data[7], time.time()])
                if validData & 1 << 3:
                    self.C02_readings.append([sensor_data[8], time.time()])
            except ValueError as ve:
                print("Invalid object read from I2C.\n\tStackTrace: " +
                      str(ve) + "\n\tSkipping line...")

        # loop through each readings list and check last element with current
        # element time, and if diff greater than keep_track_seconds, remove
        # current element list from readings list and then sums value
        # of all readings after trim
        O2_val = self.trim_sum_list(self.O2_readings)
        humidity_val = self.trim_sum_list(self.humidity_readings)
        temperature_val = self.trim_sum_list(self.temp_readings)
        pressure_val = self.trim_sum_list(self.pressure_readings)
        C02_val = self.trim_sum_list(self.C02_readings)

        # computers average of all readings after sum computed
        # and stores average readings into dictionary
        self.sensor_data = {
            'O2': O2_val / len(self.O2_readings),
            'humidity': humidity_val / len(self.humidity_readings),
            'temperature': temperature_val / len(self.temp_readings),
            'pressure': pressure_val / len(self.pressure_readings),
            'CO2': C02_val / len(self.C02_readings)
        }

    # function to check amount of time we want to keep history of readings
    # and remove sublists in list that have expired in terms of time to
    # keep data and then sums value of valid readings and returns
    def trim_sum_list(self, list):
        val = 0
        last = list.index(-1)
        for curr in list:
            if (last.index(1) - curr.index(1) > keep_track_seconds):
                list.remove(curr)

        for curr in list:
            val += curr.index(0)

        return val

    # DEPRECEATED : NOT USING FUNCTION CURRENTLY
    '''def error_check(self):
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
            print("Humidity is nominal")'''
        
