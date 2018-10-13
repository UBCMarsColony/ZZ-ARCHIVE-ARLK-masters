subsys = importlib.import_module('pi-systems_subsystem-base')

class DoorSubsystem(subsys.Subsystem):

    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id)

    def loop(self):
        
        #WARNING: MASS PSEUDOCODE
        #-------------------------
        # This is an example of logic
        # that could be used for the door.
        #-------------------------
        sData = getLatestSensorData()
        
        if sData is good:
            move door
            specify target switch
            
            while(door is running):
            
                #Error checks
                if override is requested
                    disconnect the motor 
                    set a callback listener until the motor is reset
                    break
                
                if the door is timing out
                    get last requested door state
                    run course of action logic
                
                if a sensor problem is encountered:
                    run course of action logic
                    
                #Target state logic
                if target switch is pressed:
                    stop the door
                    run security measures
        close()


def runSequence():
    dThread = DoorThread("Door Thread", 2)
    dThread.start()
    
    dThread.join()
    #start new thread to open doors
        #continuously update a state variable accessible anywhere