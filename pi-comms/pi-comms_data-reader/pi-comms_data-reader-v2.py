#JSON raspberry pi data reader code, take sserial data from python 

#imports
import serial
import json

#function defined to read json
def getDecodedJsonString(encodedJson):
	try:
		return json.loads(encodedJson)
	except ValueError as e:
		return None

#initialization
ser = serial.Serial('/dev/ttyACM1',9600)

#loop
while True:
	try:
        next_line = ser.readline()
        json_data = getDecodedJsonString(next_line)
        
        #Get some info
		print("CO2: " + str(json_data["GasComposition"]["CO2"]))
		print("O2: " + str(json_data["GasComposition"]["O2"]))
		print("Temperature: " + str(json_data["Temperature"]))
		print("Pressure: " + str(json_data["Pressure"]))
        #get PIR sensor data
    
        #if its time to update lights
            # update lights based on sensor data
        
    except Exception as e:
		print("Failed to parse JSON data.\n\tStack Trace: " + e + "\n\tSkipping line...")