import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')
door_ss = importlib.import_module('pi-systems_door-subsystem')

import json
from enum import Enum


class DoorInputSubsystem(comms.IntraModCommMixin, subsys.Subsystem):

    class Procedure(Enum):
        GetLatestInput=1
        DisplayMessage=2

    def __init__(self, *, name, thread_id, address, linked_door):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.address = address

        # The door subsystem to which this input subsystem is linked.
        if not linked_door or not instanceof(linked_door, door_ss.DoorSubsystem):
            raise TypeError("DoorInputSystem must have a valid linked_door parameter of type %s!" % (door_ss.DoorSubsystem.__name__))
        self.linked_door = linked_door


    def loop(self):
        response = self.check_buttons()

        if response:
            print("Message received from %s: \n%s" % (self.linked_door.name, repr([chr(x) for x in reponse])))
            
            if response.action is comms.ExecuteProcedure:
                if response.procedure is self.Procedure.GetLatestInput:
                    if ord(b'o') in response.data or ord(b'O') in response.data:
                        self.linked_door.request_door_state(self.linked_door.Procedure.OpenDoor)
                    if ord(b'c') in response.data or ord(b'C') in response.data:
                        self.linked_door.request_door_state(self.linked_door.Procedure.CloseDoor)
        


    def check_buttons(self) -> comms.IntraModCommMixin.IntraModCommMessage:
        self.intra_write(self.address,
           self.IntraModCommMessage.generate(
               action=self.IntraModCommAction.ExecuteProcedure,
               procedure=self.Procedure.GetLatestInput.value
           )
        )

        return self.intra_read(self.address)


if __name__ == "__main__":
    c = DoorInputSubsystem("test", 12, A)
    c.check_buttons()
