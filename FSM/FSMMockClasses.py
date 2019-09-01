# Written by Noah Caleanu (noahcaleanu152@gmail.com)
# This file contains the mock classes for the airlock interface when running on a non-pi machine.


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
        else:
            self.state = 0

    @property
    def __bool__(self):
        if self.state is 0:
            return False
        else:
            return True


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
    """
    Class to simulate the Lighting Subsystem.
    No need for a mock pressure or door class, as they initialize without hardware specific libraries
    """
    def __init__(self, name):
        self.name = name
        self.state = 0

    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0


if __name__ == "__main__":
    inputs = [MockInput("in1", pin=1, state=1),
              MockInput("in2", pin=2, state=0),
              MockInput("in3", pin=3, state=0)]

    print(inputs[0].__bool__)

    print(1 == inputs[0].__bool__)

