from enum import Enum

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
    except ModuleNotFoundError:
        print("RPi not being used, skipping RPi imports...")

    class IntraModCommAction(Enum):
        ExecuteProcedure = 1

# WRITING
    @classmethod
    def intra_write(cls, address, message):
        for byte in message:
            cls.__bus.write_byte(address, ord(byte))
            time.sleep(1)


    # Generates a valid protocol message.
    @classmethod
    def generate_intra_protocol_message(cls, *, action=-1, procedure=-1, data=None, is_response=False):
        # TODO Abstract this later on
        high_bit = 1<<7
        max_value = high_bit - 1

        # Verify and modify data
        if isinstance(action, cls.IntraModCommAction):
            action = action.value
        if action > max_value and action in set(action.value for action in cls.IntraModCommAction):
            raise ValueError("action must not use the signing bit!")
        if is_response:
            action += high_bit
        
        if procedure > max_value:
            raise ValueError("procedure must not use the signing bit!")
        if data is not None:
            procedure += high_bit

        # Format protocol message
        protocol_message = [action, procedure]
        if data is not None:
            protocol_message.append(data)

        protocol_message.insert(0, len(protocol_message))
        return protocol_message


# READING
    @classmethod
    def intra_read(cls, address):
        for index in range(93):
            num = cls.__bus.read_byte(address)
            if num:
                return_str.append(chr(num))


class InterModCommMixin:
    pass
    # TODO Implement