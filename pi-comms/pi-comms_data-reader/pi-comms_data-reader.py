#JSON raspberry pi data reader code, take sserial data from python 

#initial setup
import serial
import json

#function de
def getDecodedJsonString(encodedJson):
    return json.loads(encodedJson)

ser=serial.Serial('/dev/ttyACM1',9600)
ser.readline()

while True:
    ser.readline()
    truedata=ser.readline()
    print("Next line: "+truedata)
    decodedString=getDecodedJsonString(truedata)
    print("CO2: "+truedata[])
    
    