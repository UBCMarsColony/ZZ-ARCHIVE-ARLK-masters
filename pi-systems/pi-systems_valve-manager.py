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

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')

class ValveManager(subsys.Subsystem):

    #Standard states: 
    #ip = initial pressurization, eafc = enter airlock from colony, emfa = enter mars from airlock, 
    #eafm = enter airlock from mars, ecfa = enter colony from airlock
    std_state = {"ip":(1,0,0), "eafc":(0,1,0), "emfa":(0,0,1), "eafm":(0,0,1), "ecfa":(0,1,0), "close":(0,0,0)}

    _num_valves = 3
    _valve_ports = (23,24,25)

    def __init__(self, gpio, name=None, threadID=None):
        super().__init__(name,gpio, name=name, threadID=threadID)
        
        self.next_state = None
    
    #Task to run in a seperate thread
    def thread_task(self):
        while self.is_running():
        
            # Check if a new valve state has been requested
            if self.next_state is not None:
                
                #If there is a new state, apply it
                for i in range(ValveManager._num_valves):
                
                    #Write to each GPIO port to set the valve state
                    gpio.output(ValveManager._valve_ports[i], ValveManager.next_state(i))
                
                #Reset the valve state so this doesn't run again
                self.next_state = None
        
    
    def request_new_state(self, new_state):
        #Check that new_state is a tuple, is a valid length, and has all valid entries
        if isinstance(new_state, tuple) and len(new_state) == self._num_valves:
            for state in new_state:
                if not isinstance(state, int) or (state == 1 or state == 0):
                    print("Invalid entry in new valve state in ValveManager")
                    return
            
            self.next_state = new_state
            
        else:
            print("Invalid valve state entered in ValveManager - Should be a tuple of length 3")
