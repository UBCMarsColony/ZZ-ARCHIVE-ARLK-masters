sysThread = importlib.import_module('pi-systems_service-base')

class DoorThread(sysThread.Service):
    def thread_task(self):
        print(self.service_thread.name + " is running!")

def runSequence():
    dThread = DoorThread("Door Thread", 2)
    #start new thread to open doors
        #continuously update a state variable accessible anywhere
