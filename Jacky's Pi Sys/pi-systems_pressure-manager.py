try:
    import RPi.GPIO as gpio
except ImportError:
    print("Could not find the GPIO library. Are you on a Pi machine?")

from collections import namedtuple
from enum import Enum, auto

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')


class PressureSubsystem(subsys.Subsystem):
    
    class Procedure(Enum):
        Procedure1 = 1
        # and so on...


    def __init__(self, name=None, thread_id=None):
        super().__init__(name, thread_id)
        
        self.next_state = None


    #Task to run in a seperate thread
    def loop(self):        
        # Check if a new valve state has been requested
        with self:
            # Stub: Implement as shown below (and any extra if needed)

            # Proceed if:
            #   A new state has been requested; and
            #   The valve subsystem is not currently applying another state.

                # Send the new state information to the Arduino - make sure data is packaged according to protocol.

                # Set next_state to None, which will make sure the loop doesn't run again until the next request.
                self.next_state = None
        
    
    def request_new_state(self, new_state):
        if # new_state is not the expected object type:
            raise TypeError("Type Error message")
        
        if # new_state's value/s is/are invalid.
            raise ValueError("Value error message")

        if # Any other checks that are needed - may want to discuss with team!

        # This should only run so long as all other condiitons pass.
        with self:
            self.next_state = new_state

