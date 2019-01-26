try:
    import RPi.GPIO as gpio
except ImportError:
    print("Could not find the GPIO library. Are you on a Pi machine?")

from collections import namedtuple
from enum import Enum

import importlib
import struct
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')

class PressureSubsystem(comms.IntraModCommMixin, subsys.Subsystem):
# For the Py ic2 protol structure
# Modelled after the structure in the pressurization-procedure.ino

    class Procedure(Enum):
    #Procedures based on pressurization .ino code
    # Procedure is NOT THAT IMPORTANT, purpose is to give a general idea of what state the Py is in
<<<<<<< HEAD
       # Depressurize = 0 #depressurize
=======
        #Depressurize = 0 #depressurize
>>>>>>> 576a998d1dcaf8dd7c04cf281e60ff6fd905fc64
        #Pressurize = 1 #pressurize
        #InProgress = 2 #in_progress
        SetPressure = 3
        # and so on...  
    
<<<<<<< HEAD
    class Priority(Enum):
        LowPri = 0 # Low priority; for all normal operations pri=0
        HighPri = 1 # High priority; for aborting pri=1
        
=======
    class priority(Enum):
        Low_pri = 0 # Low priority; for all normal operations pri=0
        High_pri = 1 # High priority; for aborting pri=1


    @classmethod
    def pressure_control(cls, flag):
        pass    

>>>>>>> 576a998d1dcaf8dd7c04cf281e60ff6fd905fc64
    #Replaced Procedure as the important state-teller
    class TargetState(Enum):
        Close = 0 
        Pressurize = 1
        Depressurize = 2
        Idle = 3 

    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id)
        
        self.new_state = None

    @classmethod
    def pressure_control_flow(cls, pressure, temp, O2, C02):
        pass

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
<<<<<<< HEAD

                    self.data = struct.pack(self.priority, self.TargetState)
                    #self.new_message = generate_intra_protocol_message(action=action1, procedure=self.Procedure.Procedure1)      
                    self.IntraModCommMessage.generate(action=self.IntraModCommAction.ExecuteProcedure,
=======
                    self.data = [self.priority.Low_pri.value, self.new_state.value]
                    #self.new_message = generate_intra_protocol_message(action=action1, procedure=self.Procedure.Procedure1)      
                    self.new_message = self.IntraModCommMessage.generate(action=self.IntraModCommAction.ExecuteProcedure.value,
>>>>>>> 576a998d1dcaf8dd7c04cf281e60ff6fd905fc64
                                                procedure=self.Procedure.SetPressure.value, 
                                                data=self.data)
                    self.intra_write(0x14,self.new_message) # send new_message to arduino

        # Set next_state to None, which will make sure the loop doesn't run again until the next request.
        self.new_state = None
        
    def request_new_state(self, new_state):

        if not isinstance(new_state, self.TargetState): # new_state is not the expected object type:
            raise TypeError("Type Error message")
        
        # the following is a data validity check (not an official error detection). Checks if data is out of range
        if new_state.value < 0:
            raise ValueError("Value error message.  Value out of range.") 

        #Any other checks that are needed - may want to discuss with team! 

        # This should only run so long as all other condiitons pass.
        with self:
            self.new_state = new_state




if __name__ == "__main__":
    pass
