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
ser = serial.Serial('/dev/ttyACM1',9600)

#loop
while True:
    next_line = ser.readline()
	json_data = getDecodedJsonString(next_line)
	
	try:
		print("CO2: " + str(json_data["GasComposition"]["CO2"]))
		print("O2: " + str(json_data["GasComposition"]["O2"]))
		print("Temperature: " + str(json_data["Temperature"]))
		print("Pressure: " + str(json_data["Pressure"]))
	except Exception as e:
		print("Failed to parse JSON data.\n\tStack Trace: " + e + "\n\tSkipping line...")
