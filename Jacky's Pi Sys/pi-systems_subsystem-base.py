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

Param: name - The thread's unique name
Param: thread_id - The thread's unique ID that will be used to reference it
Param: add_to_pool - Boolean that indicates whether or not to add the subsystem to the pool
"""


class Subsystem(ABC):
    def __init__(self, thread_id, name=None, add_to_pool=True):
        if thread_id is None:
            raise ValueError("Subsystem parameter thread_id is not defined!")

        self.name = name if name is not None else self.__class__.__name__
        self.thread = None
        self.thread_id = thread_id
        self.running = False
            
        # By default, add the subsystem to the pool.
        if add_to_pool is True:
            subsys_pool.add(self)

        print("Subsystem initialized:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))


    def start(self):
        if self.thread is None:
            self.thread = Subsystem.SubsystemThread(self)
        
        print("Subsystem starting:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))
        self.thread.start() 
        self.running = True
        

    def stop(self):
        self.running = False
        print("Subsystem stopping:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))
        self.thread.join()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def run(self):
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
            self.lock = threading.Lock()
            self.subsystem.running = True


        def run(self):
            self.subsystem.run()


"""
SerialUser class enables the subsystem to use serial methods. This allows direct data transfer
between arduino and pi.
"""
class SerialUser():

    def __init__(self, address):
        # for RPI version 1, use “bus = smbus.SMBus(0)”
        self.bus = smbus.SMBus(1)
    
        # This is the address we setup in the Arduino Program
        self.slave_address = 0x0A


    def readNumber():
        return self.bus.read_byte(self.slave_address)
        # number = bus.read_byte_data(slave_address, 1)
        

    def get_json_dict():
        return_str = []
        # use ord(char a) to turn it to byte
        # use chr(byte b) to turn it to char

        for index in range(93):
            num = readNumber()
            if num:
                return_str.append(chr(num))

        str_ret = ''.join(return_str)
        return str_ret

    #t = get_json_dict()
    #import json
    #d = json.loads(t)
    #print(d)
