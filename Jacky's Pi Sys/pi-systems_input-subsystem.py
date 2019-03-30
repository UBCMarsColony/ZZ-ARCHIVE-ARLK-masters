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

    def __init__(
        self,
        name,
        thread_id,
        inputs=[],
        outputs=[],
        loop_delay_ms=100,
        on_loop=None
    ):
        super().__init__(
            name=name,
            thread_id=thread_id,
            loop_delay_ms=loop_delay_ms,
            on_loop=on_loop)

        self.inputs = inputs if type(inputs) is list else [inputs]
        for i in self.inputs:
            GPIO.setup(i.pin, GPIO.IN)
            for pp in i.pipe_pins:
                GPIO.setup(pp, GPIO.OUT)

        self.outputs = outputs if type(outputs) is list else [outputs]
        for o in self.outputs:
            GPIO.setup(o.pin, GPIO.OUT)

    def loop(self):
        self._check_inputs()

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
        Button = "Button"  # State is 1 or 0
        Switch = "Switch"     # State is 1 or 0

    def __init__(self, name, pin, subtype, initial=False, pipe_pins=[]):
        self.name = name
        self.pin = pin
        self.subtype = subtype if type(subtype) is str else subtype.value
        self._state = initial or 0

        # The Pi will automatically forward signals to these pins.
        # If negative, forwads the inverted signal.
        self.pipe_pins = pipe_pins
        self._read = self._get_reader()
        self.on_change_callbacks = {}

    def __repr__(self):
        return "%s (name=%s, pin=%i, state=%i)" % (
            self.subtype, self.name, self.pin, int(self.state))

    def _get_reader(self):
        if self.subtype == InputComponent.Subtype.Button.value:
            def btn_reader():
                GPIO.input(self.pin)
                return self.state
            return btn_reader
        elif self.subtype == InputComponent.Subtype.Switch.value:
            def swt_reader():
                GPIO.input(self.pin)
                return False

    def read(self):
        self.state = self._read()
        return self.state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        prev_state = self.state
        self._state = value
        if prev_state != self.state:
            for id in self.on_change_callbacks:
                self.on_change_callbacks[id](self.state)
            for pin in self.pipe_pins:
                GPIO.output(abs(pin), 1 if pin > 0 else 0)

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
    from unittest.mock import Mock
    GPIO = Mock()
    print("USING MOCK GPIO")

    airlockInterface = InterfaceSubsystem(
        name="airlockInternalInterface",
        thread_id=12,
        inputs=[
            *[
                InputComponent(n, p, InputComponent.Subtype.Button)
                for n, p in [
                    ["LightsToggle", 4],
                    ["DoorTrigger", 5],
                    ["DoorToggle", 6],
                    ["Pressurize", 8],
                    ["Depressurize", 9],
                    ["Confirm", 10],
                    ["EmergencyStop", 11],
                ]
            ],
            InputComponent(
                "ManualOverride",
                11,
                InputComponent.Subtype.Button)
        ],
        outputs=[
            OutputComponent(n, p, OutputComponent.Subtype.LED)
            for n, p in [
                ["isPressurizing", 12],
                ["isInProgress", 13],
                ["isDepressurizing", 14],
                ["EmergencyStopOn", 15],
                ["confirmedIndicator", 16]
            ]
        ],
        on_loop=lambda: print("loop!")
    )

    marsInterface = InterfaceSubsystem(
        name="marsInterface",
        thread_id=13,
        inputs=[
            InputComponent(n, p, InputComponent.Subtype.Button)
            for n, p in [
                ["Entry", 17],
                ["EmergencyStop", 18],
                ["ExitDemo", 19]
            ]
        ]
    )

    airlockInterface.start()
    marsInterface.start()

    import time
    time.sleep(5)

    airlockInterface.get_input_component('Confirm').attach_callback(
        lambda st: print("Called back with state %s!" % st), 12
    )
    for i in range(5):
        airlockInterface.get_input_component('Confirm').state = \
            not airlockInterface.get_input_component('Confirm').state
        time.sleep(1)

    airlockInterface.get_input_component('Confirm').detach_callback(
        12
    )

    airlockInterface.stop()
    marsInterface.stop()

    print("END TEST")
