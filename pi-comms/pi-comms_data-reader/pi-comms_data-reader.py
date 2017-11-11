#JSON raspberry pi data reader code, take sserial data from python 

#initial setup
import serial
import json

#function defined to read json
def getDecodedJsonString(encodedJson):
    return json.loads(encodedJson)

ser=serial.Serial('/dev/ttyACM1',9600)
ser.readline()

while True:
    ser.readline()
    truedata=ser.readline()
    decodedString=getDecodedJsonString(truedata)
    print("CO2: "),
    print(truedata["GasComposition"]["CO2"])
    print("O2: "),
    print(truedata["GasComposition"]["O2"])
    print("Temperature: "),
    print(truedata["Temperature"])
    print("Pressure: "),
    print(+truedata["Pressure"])