import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')

class InputManager(subsys.Subsystem):
    
    _input_pins = [12,13,14,15] #TODO actually assign proper pins
    
    def thread_task(self):
        while self.is_running():
            print(str(check_buttons()))
            
        
    def check_buttons(self):
        for pin in InputManager._input_pins:
            if self.gpio.input(pin)
                return pin
        
        return None
        
        
    def send_instructions(self):
        #Implement me
        pass