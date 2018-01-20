#JSON raspberry pi data reader code, take serial data from python 

import serial
import json
import time

#function defined to read JSON
def getDecodedJsonString(encodedJson):
	try:
		return json.loads(encodedJson)
	except ValueError as e:
		raise ValueError

#TODO Relocate lines 14-34 into own file

sensor_data = {}

def get_sensor_data():
    return sensor_data

def update_sensor_data():
    try:    
        next_line = ser.readline()
        json_data = getDecodedJsonString(next_line)

        sensor_data = json_data
    
        #if its time to update lights
            # update lights based on sensor data
        
    except ValueError as ve:
    	print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
    except Exception as e:
        print("Unexpected exception has occurred. \n\tStack Trace: " + str(e))
    
        
#initialization
ser = serial.Serial('/dev/ttyACM1',9600)

# MAIN LOOPS

while True:
    
    update_sensor_data()
    
    print(str(get_sensor_data))
    
    time.sleep(0.1)

