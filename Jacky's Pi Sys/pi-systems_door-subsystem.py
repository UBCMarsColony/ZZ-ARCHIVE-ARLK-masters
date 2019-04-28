import importlib
from enum import IntEnum
subsys = importlib.import_module('pi-systems_subsystem-base')
comms = importlib.import_module('pi-systems_communications')


class DoorSubsystem(subsys.Subsystem):

    class Procedure(IntEnum):
        calibrate = 2
        setDoorState = 3
        getDoorState = 4

    class DoorState(IntEnum):
        unknown = 0
        transit = 3
        open = 111
        close = 99
        manualCalibrate = 113

    class DoorPosition(IntEnum):
        doorIsOpen = 2 * (2308)  # Arduino-encoded value for right.
        doorIsClosed = 0
        doorInTransit = 1

    def __init__(self, name=None, thread_id=None, address=None):
        super().__init__(name=name, thread_id=thread_id, loop_delay_ms=5000)

        self.new_state = None
        self.address = address

    def loop(self):
        with self.lock:
            if self.new_state is not None:
                print("Door state updating (%s)" %
                      (self.Procedure(self.new_state).name))

                # Check sensors and things

                comms.intra_write(self.address,
                                  comms.generate
                                  (action=comms.IntraModCommAction.
                                   ExecuteProcedure, procedure=self.new_state))

                self.new_state = None

    # function to get current door state from door control arduino using I2C
    # return: doorState and doorAngle as a tuple
    def get_current_door_state(self):
        doorStateRaw = comms.intra_read(self.address,
                                        self.Procedure.getDoorState.value)
        # March9doorcontrol_I2C.ino struct returns 4 bytes and a short struct
        doorStateVals = struct.unpack('cccch', bytes(doorStateRaw.raw_array[
                                      0:struct.calcsize('cccch')]))

        doorState = doorStateVals[3]
        doorAngle = doorStateVals[4]

        return doorState, doorAngle

    #add calibrate message to be sent to doorcontrol
    #def calibrateDoor(self):
    #   comms.intra_write(self.address, )

    # other subsystems use this function to get the door subsys to get
    # the door state form the arduino controller through I2C on the loop
    def request_door_state(self, state=None):
        if not state:
            raise TypeError("Door state must be an integer defined in DoorSubsystem.Procedure")

        if not isinstance(state, int):
            if isinstance(state, self.Procedure):
                state = state.value
            else:
                raise TypeError("Door state must be an integer or alias defined by DoorSubsystem.Procedure")

        if state not in set(p.value for p in self.Procedure):
            raise ValueError("Door state must be defined in DoorSubsystem.Procedure")

        self.new_state = state

        print("Door state requested: %s" % (self.Procedure(state).name))
