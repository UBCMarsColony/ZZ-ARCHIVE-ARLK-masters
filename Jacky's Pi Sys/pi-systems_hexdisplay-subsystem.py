from enum import Enum
import struct
import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

"""
Author: Thomas Richmond
Purpose: Interact with an Arduino which has controls several hex displays.
Parameter: display_data_fns - A list of functions, each returning an int16.
                              Each cycle, these functions are called and sent,
                              IN ORDER OF THE LIST, to the Arduino at the
                              I2C address specified.
"""


class HexDisplaySubsystem(subsys.Subsystem):

    class Procedure(Enum):
        UpdateDisplays = 1

    def __init__(
        self,
        name,
        thread_id,
        address,
        display_data_fns,
        loop_delay_ms=100
    ):
        super().__init__(
            name=name,
            thread_id=thread_id,
            loop_delay_ms=loop_delay_ms)
        self.address = address
        self.display_data_fns = \
            display_data_fns if isinstance(display_data_fns, list) \
            else [display_data_fns]

    def loop(self):
        data = []
        for d in self.display_data_fns:
            data.extend(struct.unpack('BB', struct.pack('h', int(d()))))

        comms.intra_write(
            self.address,
            comms.IntraModCommMessage.generate(
                action=1,
                procedure=self.Procedure.UpdateDisplays.value,
                data=data
            )
        )
        
    # Define any other methods here.

if __name__ == "__main__":
    hds = HexDisplaySubsystem(
      name="hexdisplay_internal",
      thread_id=0x1EDB0A12D1,
      address="FILL ME IN",
      display_data_fns=[
          lambda: 12,
          lambda: 13
      ]
    )

    hds.start()
