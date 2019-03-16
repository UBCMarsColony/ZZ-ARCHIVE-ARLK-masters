# import RPi.GPIO as GPIO
from enum import Enum

import importlib
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')


class InterfaceSubsystem(subsys.Subsystem):
    """
    Author: Thomas Richmond
    Purpose: Handle any interfacing with physical in/out boards.
    Can use the following methods:
        - get_input_component(name): Get the input component
            with a specified name
        - read_input(component): Get the GPIO input of a selected component
        - get_output_component(name): Get the input component
            with a specified name
        - write_output(component, state): Write GPIO output
            to a selected component
        - InputComponent.attachCallback(callback, id): Places a state change
            callback on an input component
    """

    def __init__(self, name, thread_id, inputs, outputs):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=100)

        self.inputs = inputs if type(inputs) is list else [inputs]
        for i in self.inputs:
            # pass
            print(i)
            # GPIO.input(input.pin)

        self.outputs = outputs if type(outputs) is list else [outputs]
        for o in self.outputs:
            # GPIO.output(output.pin)
            print(o)

    def loop(self):
        self._check_inputs()

    def _check_inputs(self):
        for i in inputs:
            prev_state = i.state
            i.state = GPIO.input(i.pin)
            if prev_state != i.state:
                for callback in i.on_change_callbacks:
                    callback(i.state)

    def get_input_component(self, name):
        return [i for i in self.inputs if i.name == name].pop()

    def read_input(self, component):
        return GPIO.input(component.pin)

    def get_output_component(self, name):
        return [o for o in self.outputs if o.name == name].pop()

    def write_output(self, component, state):
        GPIO.output(component.pin, state)


class InputComponent:
    class Type(Enum):
        Push = "Push Button"
        Switch = "Switch"

    def __init__(self, name, pin, type, initial=False):
        self.name = name
        self.pin = pin
        self.type = type
        self.state = initial
        self.on_change_callbacks = {}

    def __repr__(self):
        return "%s (name=%s, pin=%i, state=%i)" % (
            self.type, self.name, self.pin, int(self.state))

    def attach_callback(self, callback, id):
        self.on_change_callbacks[id] = callback
        return id

    def detach_callback(self, id):
        del self.on_change_callbacks[id]
        return id


class OutputComponent:
    class Type(Enum):
        LED = "LED"

    def __init__(self, name, pin, type, initial=False):
        self.name = name
        self.pin = pin
        self.type = type
        self.state = initial

    def __repr__(self):
        return "%s (name=%s, pin=%i, state=%i)" % (
            self.type, self.name, self.pin, int(self.state))


if __name__ == "__main__":
    print("START TEST")
    marsInter = InterfaceSubsystem("marsSide", 12, inputs=[
        InputComponent("Door Toggle", 12, InputComponent.Type.Push.value),
        InputComponent("Lights", 13, InputComponent.Type.Switch.value)
    ], outputs=[
        OutputComponent("Emergency", 9, OutputComponent.Type.LED.value)
    ])

    print(marsInter.inputs)
    print(marsInter.outputs)

    print(marsInter.get_input_component("Door Toggle").name)
    print(marsInter.get_input_component("Door Toggle").pin)
    print(marsInter.get_input_component("Door Toggle").type)

    print(marsInter.get_input_component("Lights").name)
    print(marsInter.get_output_component("Emergency").name)
    print(marsInter.get_output_component("Emergency").pin)

    id = marsInter.get_input_component("Door Toggle").attach_callback(
        123, lambda state: print(state)
    )
    marsInter.get_input_component("Door Toggle").detach_callback(id)

    print("Test complete!")
