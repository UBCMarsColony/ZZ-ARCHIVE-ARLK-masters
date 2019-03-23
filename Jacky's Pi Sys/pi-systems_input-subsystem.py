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
            GPIO.setup(i.pin, GPIO.IN)
            for pp in i.pipe_pins:
                GPIO.setup(pp, GPIO.OUT)

        self.outputs = outputs if type(outputs) is list else [outputs]
        for o in self.outputs:
            GPIO.output(o.pin, GPIO.OUT)

    def loop(self):
        self._check_inputs()
        print(self.inputs, self.outputs)

    def _check_inputs(self):
        for i in self.inputs:
            i.read()

    def get_input_component(self, name):
        return [i for i in self.inputs if i.name == name].pop()

    # def read_input(self, component):
    #     return GPIO.input(component.pin)

    def get_output_component(self, name):
        return [o for o in self.outputs if o.name == name].pop()

    def get_component(self, name):
        return \
            self.get_output_component(name) \
            or self.get_input_component(name) \
            or None

    # def write_output(self, component, state):
    #     GPIO.output(component.pin, state)


class InputComponent:
    class Subtype(Enum):
        Push = "Push Button"  # State is 1 or 0
        Switch = "Switch"     # State is 1 or 0

    def __init__(self, name, pin, subtype, initial=False, pipe_pins=None):
        self.name = name
        self.pin = pin
        self.subtype = subtype if type(subtype) is str else subtype.value
        self.state = initial

        # The Pi will automatically forward signals to these pins.
        # If negative, forwads the inverted signal.
        self.pipe_pins = pipe_pins
        self._read = self._get_reader()
        self.on_change_callbacks = {}

    def __repr__(self):
        return "%s (name=%s, pin=%i, state=%i)" % (
            self.subtype, self.name, self.pin, int(self.state))

    def _get_reader():
        if self.subtype is InputComponent.Subtype.Push:
            return lambda: GPIO.input(self.pin)
        elif self.subtype is InputComponent.Subtype.Switch:
            return lambda: GPIO.input(self.pin)

    def _read(self):
        return GPIO.input(self.pin)

    def read(self):
        prev_state = self.state
        self.state = self._read()
        if prev_state != self.state:
            for cb in self.on_change_callbacks:
                cb(self.state)

            for pin in self.pipe_pins:
                GPIO.output(abs(pin), 1 if pin > 0 else 0)

        return self.state

    def attach_callback(self, callback, id):
        self.on_change_callbacks[id] = callback
        return id

    def detach_callback(self, id):
        del self.on_change_callbacks[id]
        return id


class OutputComponent:
    class Subtype(Enum):
        LED = "LED"
        Buzzer = "Buzzer"

    def __init__(self, name, pin, subtype, initial=False):
        self.name = name
        self.pin = pin
        self.subtype = subtype if type(subtype) is str else subtype.value
        self.state = initial

    def __repr__(self):
        return "%s (name=%s, pin=%i, state=%i)" % (
            self.subtype, self.name, self.pin, int(self.state))

    def write(self, value):
        GPIO.output(self.pin, value)
        return value


if __name__ == "__main__":
    print("START TEST")
    marsInter = InterfaceSubsystem("marsSide", 12, inputs=[
        InputComponent("Door Toggle", 12, InputComponent.Subtype.Push),
        InputComponent("Lights", 13, InputComponent.Subtype.Switch)
    ], outputs=[
        OutputComponent("Emergency", 9, OutputComponent.Subtype.LED),
        OutputComponent("Alarm", 5, OutputComponent.Subtype.Buzzer)
    ])

    print(marsInter.inputs)
    print(marsInter.outputs)

    print(marsInter.get_input_component("Door Toggle").name)
    print(marsInter.get_input_component("Door Toggle").pin)
    print(marsInter.get_input_component("Door Toggle").subtype)

    print(marsInter.get_input_component("Lights").name)
    print(marsInter.get_output_component("Emergency").name)
    print(marsInter.get_output_component("Emergency").pin)

    id = marsInter.get_input_component("Door Toggle").attach_callback(
        123, lambda state: print(state)
    )
    marsInter.get_input_component("Door Toggle").detach_callback(id)

    interInter = InterfaceSubsystem("internalSide", 12, inputs=[
        InputComponent("Inter_I1", 12, InputComponent.Subtype.Push.value),
        InputComponent("Inter_I2", 13, InputComponent.Subtype.Switch.value)
    ], outputs=[
        OutputComponent("Inter_O1", 9, OutputComponent.Subtype.LED.value)
    ])

    colonyInter = InterfaceSubsystem("colonySide", 12, inputs=[
        InputComponent("colony_I1", 12, InputComponent.Subtype.Push.value),
        InputComponent("colony_I2", 13, InputComponent.Subtype.Switch.value)
    ], outputs=[
        OutputComponent("colony_O1", 9, OutputComponent.Subtype.LED.value)
    ])

    marsInter.start()
    interInter.start()
    colonyInter.start()

    from time import sleep

    sleep(5)

    marsInter.stop()
    interInter.stop()
    colonyInter.stop()
    print("Test complete!")
