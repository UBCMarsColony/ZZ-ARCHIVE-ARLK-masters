try:
    import RPi.GPIO as gpio
except ImportError:
    print("Could not find the GPIO library. Are you on a Pi machine?")

from collections import namedtuple
from enum import Enum, auto

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')


class Valve:

    # Integer constant to specify what state the Valve is in.
    class State(Enum):
        Closed = 0
        Open = auto()
        # Add Enum values if needed


    def __init__(self, port, state):
        self.state = state or Valve.State.Closed

        if port is None:
            raise ValueError("Cannot create a Valve with no port reference!")
        self.port = port


    def open(self):
        # stub...

    
    def close(self):
        # stub...


class PressureManager(subsys.Subsystem):    

    __valves = {
        # Give valves correct ports and better, clearer names.
        "valve1": Valve(port=0),
        "valve2": Valve(port=1),
        "valve3": Valve(port=2) 
    }
    
    
    #Standard states: 
    #init = initialization, eafc = enter airlock from colony, emfa = enter mars from airlock, 
    #eafm = enter airlock from mars, ecfa = enter colony from airlock
    ValveState = namedtuple("ValveState", PressureManager.__valves.keys())
    __std_state = {
        state1: ValveState(
            valve1=Valve.State.Open, 
            valve2=Valve.State.Closed, 
            valve3=Valve.State.Open
        ),
        # Add standard states based on documentation on Google Drive
    }


    def __init__(self, name=None, thread_id=None):
        super().__init__(name, thread_id)
        
        self.next_state = None


    #Task to run in a seperate thread
    def loop(self):        
        # Check if a new valve state has been requested
        with self:
            if self.next_state is not None:
                
                #If there is a new state, apply it
                for valve in self.next_state:
                    # Do stuff
                    pass

                #Reset the valve state so this doesn't run again
                self.next_state = None
        
    
    def request_new_state(self, new_state):
        #Check that new_state is a valid state object and has only valid entries
        if not CHECK_CONDITIONS:
            raise RuntimeError("My conditional error 1")
        
        for state in new_state:
            if state not in Valve.State:
                raise ValueError("State has an invalid entry!")
        
        # This should only run so long as all other condiitons pass.
        with self:
            self.next_state = new_state

