import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

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
        self.linked_door = linked_door


    def loop(self):
        self.check_buttons()


    def check_buttons(self):
        self.intra_write(self.address,
           self.generate_protocol_message(
               action=self.IntraModCommAction.ExecuteProcedure,
               procedure=self.Procedure.GetLatestInput.value
           )
        )

        response = self.intra_read(self.address)
        print(response)

        if response:
            self.write_json_dict(
                self.generate_protocol_message(
                    action=1,
                    procedure=self.Procedure.DisplayMessage.value,
                    data=[ord(x) for x in "Sending Disp Data"]
                )
            )

if __name__ == "__main__":
    c = DoorInputSubsystem("test", 12, A)
    c.check_buttons()
