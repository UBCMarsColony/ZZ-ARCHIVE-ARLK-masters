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
    #Procedures based on pressurization .ino code
    # Procedure is NOT THAT IMPORTANT, purpose is to give a general idea of what state the Py is in
        Depressurize = 0 #depressurize
        Pressurize = 1 #pressurize
        InProgress = 2 #in_progress
        # and so on...  
    
    class priority(Enum):
        priority0 = 0 # Low priority actions; for all normal operations pri=0
        priority1 = 1 # High priority actions; for aborting pri=1

    #Replaced Procedure as the important state-teller
    class TargetState(Enum):
        close = 0 
        Pressurize = 1
        Depressurize = 2
        Idle = 3

    #PSEUDOCODE FOR SUBROUTINES
        #if close, then hold pressure and change valves

        #if Pressure/Depressure, do so accordingly

        #if Idle, hold pressure at current state
        #break
        


    def __init__(self, name=None, thread_id=None):
        super().__init__(name, thread_id)
        
        self.new_state = None

    #Task to run in a seperate thread
    def loop(self):        
        # Check if a new valve state has been requested
        with self:
            # Stub: Implement as shown below (and any extra if needed)
            # Proceed if:
            #       A new state has been requested 
            #       and the valve subsystem is not currently applying another state.

                # Send the new state information to the Arduino - package data according to protocol.
                if self.new_state is not None:
                    self.data = struct.pack(self.priority, self.TargetState)
                    #self.new_message = generate_intra_protocol_message(action=action1, procedure=self.Procedure.Procedure1)      
                    self.IntraModCommMessage.generate(action=self.IntraModCommAction.ExecuteProcedure,
                                                procedure=self.Procedure.GetLatestInput.value, 
                                                data=self.data)
                    intra_write(self.new_message) # send new_message to arduino

        # Set next_state to None, which will make sure the loop doesn't run again until the next request.
        self.next_state = None
        
    def request_new_state(self, new_state):

        if not isinstance(self.new_state, self.Procedure): # new_state is not the expected object type:
            raise TypeError("Type Error message")
        
        # the following is a data validity check (not an official error detection). Checks if data is out of range
        if self.new_state < 0:
            raise ValueError("Value error message.  Value out of range.") 

        #Any other checks that are needed - may want to discuss with team! 

        # This should only run so long as all other condiitons pass.
        with self:
            self.next_state = new_state

    def DoSomething():



if __name__ == "__main__":
