# This file contains the mock classes for te airlock interface when running on a non-pi machine.
import importlib


# MAKE MOCK STRUCTURES FOR SIMULATION
class MockInput:
    """
    Class to simulate a button or switch input.
    The important attribute is the state, and method for toggling between on/off states. FOR SIMULATION/DEBUGGING ONLY.
    """
    def __init__(self, name, pin, state):
        self.name = name
        self.pin = pin
        self.state = state

    def toggle(self):
        if self.state == 0:
            self.state = 1
        self.state = 0


class MockOutput:
    """
    Class to simulate an output of subtype LED.
    The important function is the state 0 or 1 (off / on)
    """
    def __init__(self, name, pin, initial=False):
        self.name = name
        self.pin = pin
        self.state = initial

    def write(self, value):
        self.state = value


class MockLightSubsystem:
    def __init__(self, name):
        self.name = name
        self.state = 0

    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0


if __name__ == "__main__":
    print("YOU SHOULD SEE A STRING OF ALT 0's AND 1's RUNNING ME AS MAIN.")
    lights = MockLightSubsystem(name="AirMock Lights")
    print(lights.state)
    lights.toggle()
    print(lights.state)
    lights.toggle()
    print(lights.state)
    lights.toggle()
    print(lights.state)
    lights.toggle()
    print(lights.state)
