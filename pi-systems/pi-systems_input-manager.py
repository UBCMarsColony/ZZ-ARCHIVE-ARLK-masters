import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')

class InputManager(subsys.Subsystem):
    
    def thread_task(self):
        print("R-r-r-r-r-running!")
        
    def check_buttons(self):
        pass
        #IMPLEMENT ME
        
    def send_instructions(self):
        pass