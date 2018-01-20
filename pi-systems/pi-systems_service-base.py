import threading
from abc import ABC, abstractmethod


class Service(ABC):
    def __init__(self, threadID, name):
        self.service_thread = self.ServiceThread(self, threadID, name)

    class ServiceThread(threading.Thread):
        def __init__(self, service, threadID, name):
            threading.Thread.__init__(self)
            self.service = service
            self.threadID = threadID
            self.name = name
            
        def run(self):
            print("Thread started:\n\t" + self.name)
            self.service.thread_task()
        
    def start(self):
        self.service_thread.start()
        
    def join(self):
        self.service_thread.join()
    
    """
    Contains the code which will be run during the threads life.
    """
    @abstractmethod
    def thread_task(self):
        pass
