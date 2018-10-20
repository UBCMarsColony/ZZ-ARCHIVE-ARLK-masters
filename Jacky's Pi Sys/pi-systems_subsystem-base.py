import threading
from abc import ABC, abstractmethod
import importlib
import random
try:
    import smbus
except ModuleNotFoundError:
    print("RPi not being used, skipping smbus import...")

import time
from enum import Enum
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")

"""
The purpose of the Subsystem class is to ease task management.
In general, we would like the airlock tasks to be split up into single,
maintainable components. This enables better subsystem management in the future.
More information on this is included in the README file in this directory.
"""


class Subsystem(ABC):
    def __init__(self, thread_id, name, *, loop_delay_ms=750):
        if thread_id is None:
            pass
            #raise TypeError("Subsystem parameter thread_id is not defined!")

        self.name = name or (self.__class__.__name__ + str(random.randint(0, 0xFFFF)))
        self.thread_id = thread_id
        
        self.running = False
        self.loop_delay_ms = loop_delay_ms
        self.thread = Subsystem.SubsystemThread(self)
            
        subsys_pool.add(self)

        print("Subsystem initialized:\n\tName: %s\n\tID: %i" % (self.name, self.thread_id))


    # Allows "with" statement to be used on a subsystem, granting the "with" block
    # secure access to subsystem data.
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
        with self:
            self.running = False
        self.thread.join()
    

    # Definition contains the code which will be looped over during the threads life.
    @abstractmethod
    def loop(self):
        pass


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
                # Time.time() uses seconds, so convert loop_delay_ms to seconds.
                if time.time() - last_runtime >= (self.subsystem.loop_delay_ms / 1000):
                    self.subsystem.loop()


import json


#SerialMixin class enables the subsystem to use serial methods. This allows direct data transfer
#between arduino and pi.
class IntraModCommMixin:
    # Static bus object
    bus = smbus.SMBus(1) # NOTE: for RPI version 1, use “bus = smbus.SMBus(0)”

    class IntraModCommAction(Enum):
        ExecuteProcedure = 1

# WRITING
    def intra_write(self, address=0x0A, message):
        for char in message:
            IntraModCommMixin.bus.write_byte(address, ord(char))
            time.sleep(1)


    # Generates a valid protocol message.
    def generate_intra_protocol_message(self, *, action=-1, procedure=-1, data=None, is_response=False):
        # TODO Abstract this later on
        high_bit = 1<<7
        max_value = high_bit - 1

        # Verify and modify data
        if action > max_value and action in set(action.value for action in IntraModCommMixin.IntraModCommAction):
            raise ValueError("action must not use the signing bit!")
        if is_response:
            action += high_bit
        
        if procedure > max_value:
            raise ValueError("procedure must not use the signing bit!")
        if data is not None:
            procedure += high_bit

        # Format protocol message
        protocol_message = [action, procedure]
        if data is not None:
            protocol_message.append(data)

        protocol_message.insert(0, len(protocol_message))
        return protocol_message


# READING
    def intra_read(self, address):
        return_str = []
        # use ord(char a) to turn it to byte
        # use chr(byte b) to turn it to char

        for index in range(93):
            num = IntraModCommMixin.bus.read_byte(address)
            if num:
                return_str.append(chr(num))

        str_ret = ''.join(return_str)
        return json.loads(str_ret)
