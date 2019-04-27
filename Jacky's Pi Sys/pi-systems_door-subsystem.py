import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')
from enum import IntEnum

class DoorSubsystem(subsys.Subsystem):

    class Procedure(IntEnum):
        #OpenDoor = ord("o")
        #CloseDoor = ord("c")
        #Idle = ord("I")
        OpenDoor = 1
        CloseDoor = 2
        Idle = 0

    class priority(IntEnum):
        low = 0
        high = 1

    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.new_state = None
        self.address = address


    def loop(self):
        
        with self.lock:
            if self.new_state is not None:
                print("Door state updating (%s)" % (self.Procedure(self.new_state).name))

                # Check sensors and things

                comms.intra_write(self.address,
                    self.generate_intra_protocol_message(
                        action=comms.IntraModCommAction.ExecuteProcedure,
                        procedure=self.new_state
                ))

                self.new_state = None

    
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

        self.new_state = state

        print("Door state requested: %s" % (self.Procedure(state).name))
