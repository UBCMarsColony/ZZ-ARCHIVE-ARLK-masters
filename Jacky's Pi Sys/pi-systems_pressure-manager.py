try:
    import RPi.GPIO as gpio
except ImportError:
    print("Could not find the GPIO library. Are you on a Pi machine?")

from collections import namedtuple
from enum import Enum

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

class PressureSubsystem(comms.IntraModCommMixin, subsys.Subsystem):
    
    class Procedure(Enum):
        Procedure1 = 1
        Procedure2 = 2
        Procedure3 = 3
        Procedure4 = 4
        # and so on...


    def __init__(self, name=None, thread_id=None):
        super().__init__(name, thread_id)
        
        self.new_state = None


    #Task to run in a seperate thread
    def loop(self):        
        # Check if a new valve state has been requested
        with self:
            # Stub: Implement as shown below (and any extra if needed)
            # Proceed if:
            #       A new state has been requested; and
            #       The valve subsystem is not currently applying another state.

            # Send the new state information to the Arduino - make sure data is packaged according to protocol.
            if self.new_state is not None:
                self.intra_write(self.IntraModCommMessage.generate(
                    action=self.IntraModCommAction.ExecuteProcedure, 
                    procedure=self.new_state.value)
                ) # send new_message to arduino

        # Set new_state to None, which will make sure the loop doesn't run again until the next request.
        self.new_state = None
        
    def request_new_state(self, new_state):

        if not isinstance(new_state, self.Procedure): # new_state is not the expected object type:
            raise TypeError("Type Error message")
        
        # the following is a data validity check (not an official error detection). Checks if data is out of range
        MAX = 4
        if new_state < 1 or new_state > MAX:  # MAX will need to be defined 
            raise ValueError("Value error message.  Value out of range.") 

        #Any other checks that are needed - may want to discuss with team! 
        #if #implement error detection/correction 

        # This should only run so long as all other condiitons pass.
        with self:
            self.new_state = new_state
