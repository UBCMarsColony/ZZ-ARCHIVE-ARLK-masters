import smbus
import time
# for RPI version 1, use “bus = smbus.SMBus(0)”
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x0A

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    number = bus.read_byte(address)
    # number = bus.read_byte_data(address, 1)
    return number

while True:
    test_string = str(input("Give me a string to send: \n"))
    #filter_string_1 = test_string.lower()
    #filter_string_2 = test_string.strip()
    final_string = test_string

    return_str = []
    #use ord(char a) to turn it to byte
    #use chr(byte b) to turn it to char
    for char in final_string:
        writeNumber(ord(char))
        print("Pi sending ascii code for: " + str(char))
        time.sleep(1)

    for index in range(120):
        num = readNumber()
        if num != 0:
            return_str.append(chr(num))

    str_ret = ''.join(return_str)
    print(str_ret)
    time.sleep(1)
    
    



#while True:
#    var = int(input("Enter 0 – 255: "))
#    if not var:
#        continue

#    writeNumber(var)
#    print("Pi writing: " + str(var) )
    # sleep one second
#    time.sleep(1)

#    number = readNumber()
#    print ("Number from Arduino: " + str(number))
