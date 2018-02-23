import threading
from abc import ABC, abstractmethod
import importlib
subsys_pool = importlib.import_module("pi-systems_subsystem-pool")

"""
The purpose of the Subsystem class is to ease system thread management.
In general, we would like airlock subsystems to function under a similar
command flow. This enables better subsystem management in the future.
"""
class Subsystem(ABC):

    def __init__(self, name, threadID = None):
        if(threadID is None):
            threadID = 5
            
        self.is_running = False
        self.name = name
        self.subsystem_thread = SubsystemThread(self, threadID, name)
        print("Initialized new subsystem:\n\tName=" + str(name) + "\n\tID=" + str(threadID))
        subsys_pool.add(self)
                
                
    def start(self):
        print("STARTING THREAD <" + self.name + ">")
        self.is_running = True
        self.subsystem_thread.start() 
        
        
    def join(self):
        print("JOINING THREAD <" + self.name + ">")
        self.is_running = False
        self.subsystem_thread.join()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def thread_task(self):
        pass

class SubsystemThread(threading.Thread):
    def __init__(self, subsystem, threadID, name): 
        threading.Thread.__init__(self)
        self.subsystem = subsystem
        self.threadID = threadID
        self.name = name
        
    def run(self):
        self.subsystem.isRunning = True
        print("Subsystem <" + self.name + "> started on thread: <" + str(self.threadID) + ">\n")
        self.subsystem.thread_task()
