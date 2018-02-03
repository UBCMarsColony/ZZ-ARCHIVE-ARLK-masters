import threading
import importlib
sys_thread = importlib.import_module('pi-systems_service-base')

"""
Run a sequence based on a preset end state. This will
be the easiest way to run the system.

Param: sequence_code - An integer value corresponding
                      to a preset state.
"""
def run_sequence_predefined(sequence_code):
    # Get all variables associated with sequence.
    
    return runSequence()
    

def run_sequence():
    pass
    # check sensors data, run error checks liberally

    
    # Start a new thread to begin pressurization
    # Continually run, cross-check with sensors, stop if needed. Prepare to revert.
    
    # return the start state of the sequence.

class PressureThread(sys_thread.Service):
    def thread_task(self):
        print(self.service_thread.name + " is running!")

thread1 = PressureThread("Thread_Pressure", 1)
thread1.start()
thread1.join()
