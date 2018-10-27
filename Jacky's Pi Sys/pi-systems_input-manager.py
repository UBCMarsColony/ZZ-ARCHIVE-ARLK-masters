import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
import json
from enum import Enum


class InputSubsystem(subsys.IntraModCommMixin, subsys.Subsystem):

    class Procedure(Enum):
        GetLatestInput=1
        DisplayMessage=2

    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)


    def loop(self):
        self.check_buttons()


    def check_buttons(self):
        self.intra_write("ADDRESS HERE",
           self.generate_protocol_message(
               action=self.IntraModCommAction.ExecuteProcedure,
               procedure=self.Procedure.GetLatestInput.value
           )
        )

        response = self.intra_read("ADDRESS HERE")
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
    c = InputSubsystem("test", 12, A)
    c.check_buttons()
