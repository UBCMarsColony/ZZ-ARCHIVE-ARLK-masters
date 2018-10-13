import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
import json

class InputManager(subsys.SerialMixin, subsys.Subsystem):
    
    def __init__(self, name=None, thread_id=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

    def loop(self):
        self.check_buttons()    
        
    def check_buttons(self):
        self.write_json_dict(
           self.generate_protocol_message(
               action=1 # ExecuteProcedure
               procedure=1 # CheckButtons
           )
        )

        response = self.read_json_dict()
        print(response)