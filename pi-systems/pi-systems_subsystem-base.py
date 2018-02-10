import threading
from abc import ABC, abstractmethod

"""
The purpose of the Subsystem class is to ease system thread management.
In general, we would like airlock subsystems to function under a similar
command flow. This enables better subsystem management in the future.
"""
class Subsystem(ABC):
    @attribute
    isRunning = False

    def __init__(self, name, threadID = None):
        if(threadID is None):
            threadID = 5
        
        self.name = name
        self.subsystem_thread = SubsystemThread(self, threadID, name)
        print("Initialized new subsystem:\n\tName=" + str(name) + "\n\tID=" + str(threadID))
        
    def start(self):
        self.subsystem_thread.start()
        
    def join(self):
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
        print("Subsystem thread started: <" + self.name + ">\n")
        self.subsystem.thread_task()
        self.subsystem.isRunning = True