import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

from enum import Enum, unique


class InputSubsystem(comms.IntraModCommMixin, subsys.Subsystem):

    @unique()
    class Procedure(Enum):
        GetLatestInput = 1
        DisplayMessage = 2

    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.address = address

    def loop(self):
        self.check_buttons()

    def check_buttons(self):
        self.intra_write(
            self.address,
            self.IntraModCommMessage.generate(
               action=self.IntraModCommAction.ExecuteProcedure,
               procedure=self.Procedure.GetLatestInput.value
           )
        )

        response = self.intra_read(self.address)
        print(response)

        if response:
            self.write_json_dict(
                self.IntraModCommMessage.generate(
                    action=1,
                    procedure=self.Procedure.DisplayMessage.value,
                    data=[ord(x) for x in "Sending Disp Data"]
                )
            )
