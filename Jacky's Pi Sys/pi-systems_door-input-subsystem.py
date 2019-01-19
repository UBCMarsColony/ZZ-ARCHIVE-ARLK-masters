import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')
door_ss = importlib.import_module('pi-systems_door-subsystem')

from enum import Enum
from struct import Struct
import RPi.GPIO as GPIO
import time

butt1 = 11
butt2 = 13
butt3 = 15
led = 8

class DoorInputSubsystem(comms.IntraModCommMixin, subsys.Subsystem):

    class Procedure(Enum):
        GetLatestInput=1
        DisplayMessage=2

    #use the pins P.29 P.31 P.33 for the door input buttons
    #low when not pressed, high when pressed
    GPIO.setup(butt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(butt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(butt3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led, GPIO.OUT)

    def __init__(self, *, name, thread_id, address, linked_door):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.address = address

        # The door subsystem to which this input subsystem is linked.
        if not linked_door or not instanceof(linked_door, door_ss.DoorSubsystem):
            raise TypeError("DoorInputSystem must have a valid linked_door parameter of type %s!" % (door_ss.DoorSubsystem.__name__))
        self.linked_door = linked_door


    def loop(self):
        response = self.check_buttons()
       
        input2 = GPIO.input(butt2)
        input3 = GPIO.input(butt3)        
    
        while True:
            input1 = GPIO.input(butt1)
            if (input1 is True): # check button 1
                 print("Button 1 pressed")
                 GPIO.output(led, GPIO.HIGH) 
                 time.sleep(1)
                 GPIO.output(led, GPIO.LOW)
            else:
                 pass
        """#start_value1 = input1
        #time.sleep(0.05)
        
        if(not start_value2 and input2): # check butt2
             print("Button 2 pressed")
             GPIO.output(led, GPIO.HIGH)
             time.sleep(2)
             GPIO.output(led, GPIO.LOW)

        if(not start_value3 and input3): #check butt3
             print("Button 3 pressed")
             GPIO.output(led, GPIO.HIGH)
             time.sleep(3)
             GPIO.output(led, GPIO.LOW) """
            
        if response:
            print("Message received from %s: \n%s" % (self.linked_door.name, repr([chr(x) for x in reponse])))
            
            if response.action is comms.ExecuteProcedure:
                if response.procedure is self.Procedure.GetLatestInput:
                    if ord(b'o') in response.data or ord(b'O') in response.data:
                        self.linked_door.request_door_state(self.linked_door.Procedure.OpenDoor)
                    if ord(b'c') in response.data or ord(b'C') in response.data:
                        self.linked_door.request_door_state(self.linked_door.Procedure.CloseDoor)
        

    def check_buttons(self) -> comms.IntraModCommMixin.IntraModCommMessage:
        self.intra_write(self.address,
           self.IntraModCommMessage.generate(
               action=self.IntraModCommAction.ExecuteProcedure,
               procedure=self.Procedure.GetLatestInput.value
           )
        )

        return self.intra_read(self.address)


if __name__ == "__main__":
    c = DoorInputSubsystem("test", 12, A)
    c.check_buttons()
