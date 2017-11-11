#JSON raspberry pi data reader code, take sserial data from python 

#imports
import serial
import json

#function defined to read json
def getDecodedJsonString(encodedJson):
	try:
		return json.loads(encodedJson)
	except:
		return None

#initialization
ser=serial.Serial('/dev/ttyACM1',9600)

#loop
while True:
	decodedString = getDecodedJsonString(truedata)
	
	if decodedString != None:
		print("CO2: " + str(decodedString["GasComposition"]["CO2"]))
		print("O2: " + str(decodedString["GasComposition"]["O2"]))
		print("Temperature: " + str(decodedString["Temperature"]))
		print("Pressure: " + str(decodedString["Pressure"]))
	else
		print("Failed to parse JSON data. Skipping line...")
