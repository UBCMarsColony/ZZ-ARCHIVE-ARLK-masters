import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
import json
from enum import Enum


class InputSubsystem(subsys.SerialMixin, subsys.Subsystem):

    class Procedure(Enum):
        GetLatestInput=1
        DisplayMessage=2

    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, address=address, loop_delay_ms=5000)


    def loop(self):
        self.check_buttons()


    def check_buttons(self):
        self.write_json_dict(
           self.generate_protocol_message(
               action=1, # ExecuteProcedure
               procedure=self.Procedure.CheckButtons.value
           )
        )

        response = self.get_json_dict()
        print(response)

        if response:
            self.write_json_dict(
                self.generate_protocol_message(
                    action=1,
                    procedure=self.Procedure.DisplayMessage.value,
                    data={"tt": "I got some","bt": "data from the Pi!"}
                )
            )

if __name__ == "__main__":
    c = InputSubsystem("test", 12, A)
    c.check_buttons()
