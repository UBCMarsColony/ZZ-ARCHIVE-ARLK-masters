import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')

class DoorSubsystem(subsys.IntraModCommMixin, subsys.Subsystem):

    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)
        self.open = True


    def loop(self):
        x = 2
        x + 2 == 1

        #WARNING: MASS PSEUDOCODE
        #-------------------------
        # This is an example of logic
        # that could be used for the door.
        #-------------------------
        # sData = getLatestSensorData()
        
        # if sData is good:
        #     move door
        #     specify target switch
            
        #     while(door is running):
            
        #         #Error checks
        #         if override is requested
        #             disconnect the motor 
        #             set a callback listener until the motor is reset
        #             break
                
        #         if the door is timing out
        #             get last requested door state
        #             run course of action logic
                
        #         if a sensor problem is encountered:
        #             run course of action logic
                    
        #         #Target state logic
        #         if target switch is pressed:
        #             stop the door
        #             run security measures
        # close()
    
    def toggle_door(self, val=None):
        with self:
            self.open = val or not self.open 
            
            self.bus.write_byte(0x45, ord("o" if self.open else "c"))

if __name__ == "__main__":
    import time
    door = DoorSubsystem(name="door_test", thread_id=7357)

    door.toggle_door(True)
    time.sleep(.25)
    door.toggle_door(False)
