import threading
from abc import ABC, abstractmethod
import importlib
import smbus
import time
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")

"""
The purpose of the Subsystem class is to ease task management.
In general, we would like the airlock tasks to be split up into single,
maintainable components. This enables better subsystem management in the future.
More information on this is included in the README file in this directory.
"""


class Subsystem(ABC):
    def __init__(self, thread_id, name=self.__class__.__name__, *, loop_delay_ms=750):
        if thread_id is None:
            pass
            #raise TypeError("Subsystem parameter thread_id is not defined!")

        if name is None:
            raise TypeError("Cannot pass None as value for subsystem name!")

        self.name = name
        
        self.running = False
        self.loop_delay_ms = loop_delay_ms
        self.thread = Subsystem.SubsystemThread(self)
        self.thread_id = thread_id
            
        subsys_pool.add(self)

        print("Subsystem initialized:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))


    def __enter__(self):
        self.thread.lock.acquire()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.thread.lock.release()


    def start(self):
        if self.running is True:
            raise threading.ThreadError("Tried starting a thread that was still running!")

        self.thread.start() 
        self.running = True
        print("Subsystem started: \n\tName: %s\n\tID: %i" % (self.name, self.thread_id))
        

    def stop(self):
        print("Subsystem stopping:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))
        self.running = False
        self.thread.join()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def loop(self):
        pass

    # """
    # Locks the thread while running the method. Useful when accessing data that is modified by the thread.
    # """
    # def get_threadsafe(self, async_method):
    #     with self.thread.lock:
    #         async_method()

    class SubsystemThread(threading.Thread):
        def __init__(self, subsystem): 
            super().__init__()

            self.subsystem = subsystem
            self.setName(self.subsystem.name)
            self.lock = threading.Lock()
            self.subsystem.running = True


        def run(self):
            last_runtime = time.time()

            while self.subsystem.running:
                # Time.time() uses seconds, so divide loop_delay_ms by 1000 to convert to seconds.
                if time.time() - last_runtime >= (self.subsystem.loop_delay_ms / 1000):
                    self.subsystem.loop()


"""
SerialMixin class enables the subsystem to use serial methods. This allows direct data transfer
between arduino and pi.
"""
class SerialMixin:

    def __init__(self, address):
        # for RPI version 1, use “bus = smbus.SMBus(0)”
        self.bus = smbus.SMBus(1)
    
        # This is the address we setup in the Arduino Program
        self.slave_address = address or 0x0A


# WRITING
    def write_number(value):
        bus.write_byte(address, value)
        # bus.write_byte_data(address, 0, value)
        return -1


    def write_json_dict(json_str):
        for char in json_str:
            writeNumber(ord(char))
            time.sleep(1)


# READING
    def read_number():
        return self.bus.read_byte(self.slave_address)
        # number = bus.read_byte_data(slave_address, 1)
        

    def get_json_dict():
        return_str = []
        # use ord(char a) to turn it to byte
        # use chr(byte b) to turn it to char

        for index in range(93):
            num = self.read_number()
            if num:
                return_str.append(chr(num))

        str_ret = ''.join(return_str)
        return str_ret

    #t = get_json_dict()
    #import json
    #d = json.loads(t)
    #print(d)
