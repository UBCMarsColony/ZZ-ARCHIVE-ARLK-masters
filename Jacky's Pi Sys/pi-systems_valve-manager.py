"""
Written By: Thomas Richmond
Purpose: The valve manager controls all airlock valves. While the thread is running, 
         a new state can be assigned using request_new_state() and inputting a tuple 
         of size $num_valves. The next time the thread runs its loop, it will apply
         this new new state.
         Valve ports are kept in a tuple so as to work with both for loops and GPIO.

"""

try:
    import RPi.GPIO as gpio
except ImportError:
    print("Could not find the GPIO library. Are you on a Pi machine?")

from collections import namedtuple

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')


Valve = namedtuple("Valve", "state port")

# TODO Change field names (param 2) to something more obvious (ie ColonyValve)
ValveState = namedtuple("ValveState", "v1 v2 v3")


class ValveManager(subsys.Subsystem):

    __valves = {
        "Valve1": Valve(state=0, port=23),
        "Valve2": Valve(state=0, port=24)
        "Valve3": Valve(state=0, port=25)
    }
    

    #Standard states: 
    #init = initialization, eafc = enter airlock from colony, emfa = enter mars from airlock, 
    #eafm = enter airlock from mars, ecfa = enter colony from airlock
    __std_state = {
        "open": ValveState(1, 1, 1),
        "close": ValveState(0,0,0),
        "init": ValveState(1,0,0), 
        "eafc": ValveState(0,1,0), 
        "emfa": ValveState(0,0,1), 
        "eafm": ValveState(0,0,1), 
        "ecfa": ValveState(0,1,0)
    }


    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id)
        
        self.next_state = None
    
    #Task to run in a seperate thread
    def loop(self):        
        # Check if a new valve state has been requested
        with self.thread.lock:
            if self.next_state is not None:
                
                #If there is a new state, apply it
                for i in range(len(ValveManager._valve_ports)):
                
                    #Write to each GPIO port to set the valve state
                    gpio.output(ValveManager._valve_ports[i], ValveManager.next_state[i])
                
                #Reset the valve state so this doesn't run again
                self.next_state = None
        
    
    def request_new_state(self, new_state):
        #Check that new_state is a tuple, is a valid length, and has all valid entries
        if isinstance(new_state, tuple) and len(new_state) == len(ValveManager._valve_ports):
            for state in new_state:
                if not isinstance(state, int) or (state == 1 or state == 0):
                    print("Invalid entry in new valve state in ValveManager")
                    return
            
            self.next_state = new_state
            
        else:
            print("Invalid valve state entered in ValveManager - Should be a tuple of length %i" % (len(_valve_ports)))

