from enum import Enum
from threading import Lock


# SerialMixin class enables the subsystem to use I2C methods for data transfer
# between arduino and pi.
class IntraModCommMixin:

    try:
        # Initialization needed for the class to run properly
        import smbus
        import RPi.GPIO as gpio

        # Static bus object
        gpio.setmode(gpio.BCM)
        __bus = smbus.SMBus(1) # NOTE: for RPI version 1, use “bus = smbus.SMBus(0)”
        __lock = Lock()
    except ModuleNotFoundError:
        print("RPi not being used, skipping RPi imports...")

    class IntraModCommMessage:
        def __init__(self, raw_array):
            self.raw_array = raw_array


        @property
        def action(self):
            # Gets the action without the signed bit.
            return self.raw_array[0] & ~(1 << 7)


        @property
        def is_response(self):
            return (self.raw_array[0] >> 7) & 0b1

        @property
        def procedure(self):
            # Gets the procedure byte without the signed bit.
            return self.raw_array[1] & ~(1 << 7)


        @property
        def has_data(self):
            # Checks the high-bit of the procedure byte. If set, more data is present.
            return (self.raw_array[1] >> 7) & 0b1


        @property
        def data(self):
            return self.raw_array[2:]


        def validate(self):
            # Check if the specified action is a valid integer value.
            if self.action not in set(a.value for a in IntraModCommMixin.IntraModCommAction):
                return False

            # TODO Implement this at a later date
            # Check if:
                # Procedure is within the expected range of [0, 127]
                # The high bit of the Procedure byte is signed if there is data present
                # Length of message is within maximum length (32)
                # Each byte in the range is within the valid range of [0, 255]
            
            return True
        

        @staticmethod
        def generate(*, action=-1, procedure=-1, data=None, is_response=False):
            max_value = 1 << 7
            high_bit = 1 << 7
            
            if isinstance(action, IntraModCommMixin.IntraModCommAction):
                action = action.value

            if action > max_value:
                raise ValueError("action must not use the signing bit!")
            
            if action not in set(action.value for action in IntraModCommMixin.IntraModCommAction):
                raise ValueError("specified action %i is not defined!" % (action))

            if is_response:
                action += high_bit
            
            if procedure > max_value:
                raise ValueError("procedure must not use the signing bit!")
            
            if data is not None:
                procedure += high_bit

            generated_message = [action, procedure]
            if data is not None:
                generated_message.extend(data)

            return IntraModCommMixin.IntraModCommMessage(generated_message)


    class IntraModCommAction(Enum):
        ExecuteProcedure = 1
        SelfCheck = 2
        Restart = 3
        Shutdown = 4


# WRITING
    @classmethod
    def intra_write(cls, address, message):
        if isinstance(message, IntraModCommMixin.IntraModCommMessage):
            message = message.raw_array

        cmd, data = message.pop(0), message
        with cls.__lock:
            cls.__bus.write_i2c_block_data(address, cmd, data)
        # for byte in message:
            # cls.__bus.write_byte(address, ord(byte))
            # time.sleep(1)


# READING
    @classmethod
    def intra_read(cls, address) -> IntraModCommMixin.IntraModCommMessage:
        with cls.__lock:
            msg = cls.__bus.read_i2c_block_data(address, 0)
        # for index in range(93):
        #     num = cls.__bus.read_byte(address)
        #     if num:
        #         msg.append(num)
        
        if not msg:
            print('I2C message expected but not read. Discarding')
            return
        
        message = IntraModCommMixin.IntraModCommMessage(msg)
        if message.validate():
            return message

class InterModCommMixin:
    pass
    # TODO Implement