import threading
from abc import ABC, abstractmethod
import importlib
import random
import time
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")

"""
The purpose of the Subsystem class is to ease task management.
In general, we would like the airlock tasks to be split up into single,
maintainable components. This enables better subsystem management in the future.
More information on this is included in the README file in this directory.

Param: gpio - The RPi.GPIO reference that will be used by the subsystem to control pins
Param: name - The thread's unique name
Param: thread_id - The thread's unique ID that will be used to reference it
Param: add_to_pool - Boolean that indicates whether or not to add the subsystem to the pool
"""
class Subsystem(ABC):
    

    def __init__(self, thread_id, name=None, add_to_pool=True):
        if thread_id is None:
            #raise NameError("Subsystem parameter thread_id is not defined!")
            self.thread_id = random.seed(int(time.time()))

        self.name = name if name is not None else self.__class__.__name__
        self.thread = None
        self.running = False
            
        # By default, add the subsystem to the pool.
        if add_to_pool is True:
            subsys_pool.add(self)

        print("Subsystem initialized:\n\tName: %s\n\tID: %s", self.name, str(self.thread_id))

                
    def start(self):
        if self.thread is None:
            self.thread = SubsystemThread(self)
        
        print("Subsystem starting:\n\tName: %s\n\tID: %s", self.name, str(self.thread_id))
        self.thread.start() 
        self.running = True
        

    def stop(self):
        self.running = False
        print("Subsystem stopping:\n\tName: %s\n\tID: %s", self.name, str(self.thread_id))
        self.thread.join()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def run(self):
        pass


class SubsystemThread(threading.Thread):
    def __init__(self, subsystem): 
        super().__init__()
        self.subsystem = subsystem
        self.subsystem.running = True
        
    def run(self):
        self.subsystem.run()
