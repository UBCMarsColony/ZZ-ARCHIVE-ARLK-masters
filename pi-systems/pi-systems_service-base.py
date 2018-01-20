import threading
from abc import ABC

class ServiceThread(ABC):
    
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run():
        print("Thread started:\n\t" + name)
        threadTask()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def thread_task(self, args=None):
        pass