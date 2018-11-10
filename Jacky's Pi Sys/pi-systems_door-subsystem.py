import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')
from enum import IntEnum

class DoorSubsystem(comms.IntraModCommMixin, subsys.Subsystem):

    class Procedure(IntEnum):
        OpenDoor = ord("o")
        CloseDoor = ord("c")


    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.new_state = None
        self.address = address


    def loop(self):
        
        with self:
            if self.new_state is not None:
                print("Door state updating (%s)" % (self.Procedure(self.new_state).name))

                # Check sensors and things

                self.intra_write(self.address,
                    self.generate_intra_protocol_message(
                        action=self.IntraModCommAction.ExecuteProcedure,
                        procedure=self.new_state
                ))

                self.new_state = None

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
    
    def request_door_state(self, state=None):
        if not state:
            raise TypeError("Door state must be an integer defined in DoorSubsystem.Procedure")

        if not isinstance(state, int):
            if isinstance(state, self.Procedure):
                state = state.value
            else:
                raise TypeError("Door state must be an integer or alias defined by DoorSubsystem.Procedure")

        if state not in set(p.value for p in self.Procedure):
            raise ValueError("Door state must be defined in DoorSubsystem.Procedure")

        with self:
            self.new_state = state

        print("Door state requested: %s" % (self.Procedure(state).name))


# TEST CODE
if __name__ == "__main__":
    import time
    door = DoorSubsystem(name="door_test", thread_id=7357)

    door.request_door_state(DoorSubsystem.Procedure.OpenDoor)
    time.sleep(7500)
    door.toggle_door(DoorSubsystem.Procedure.CloseDoor)
