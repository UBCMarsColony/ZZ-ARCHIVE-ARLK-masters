import smbus
import time
# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x0A

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

def get_json_dict(): 
    return_str = []
    #use ord(char a) to turn it to byte
    #use chr(byte b) to turn it to char

    for index in range(51):
        num = readNumber()
        if num != 0:
            return_str.append(chr(num))

    str_ret = ''.join(return_str)
    return str_ret
