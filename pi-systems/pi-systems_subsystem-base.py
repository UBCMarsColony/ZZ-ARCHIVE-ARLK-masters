import threading
from abc import ABC, abstractmethod

"""
The purpose of the Service class is to ease system thread management.
In general, we would like airlock services to function under a similar
command flow.
"""
class Subsystem(ABC):
    def __init__(self, name, threadID = None):
        if(threadID = None):
            pass#generate a valid number
        
        self.subsystem_thread = self.ServiceThread(self, threadID, name)
        print("Initialized new subservice:\n\tName=" + str(name) + "\n\tID=" + str(threadID))
        
    class SubsystemThread(threading.Thread):
        def __init__(self, subsystem, threadID, name):
            threading.Thread.__init__(self)
            self.subsystem = subsystem
            self.threadID = threadID
            self.name = name
            
        def run(self):
            print("Thread started:\n\t" + self.name)
            self.subsystem.thread_task()
        
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
