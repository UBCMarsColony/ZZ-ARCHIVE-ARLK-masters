#JSON raspberry pi data reader code, take serial data from python 

import serial
import json
import time

#THE VARIABLE THAT MATTERS
sensor_data = {}


def get_sensor_data(string_name = None):
    if string_name = None:
        return sensor_data
    else
        try:
            return sensor_data[string_name]
        except KeyError as ve:
            print("Failed to find a value associated with the key " + string_name + ". Returning entire dictionary instead...")
            return sensor_data
        except Exception as e:
            print("An unexpected exception occurred while trying to retrieve sensor data.\n\tStack Trace: " + str(e))

def update_sensor_data():
    try:    
        sensor_data = getDecodedJsonString(next_line)
    
    except ValueError as ve:
    	print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
    except Exception as e:
        print("An unexpected exception occurred while trying to update Pi sensor data. \n\tStack Trace: " + str(e))

#function that securely decodes a JSON string
def __getDecodedJsonString(encodedJson):
	try:
		return json.loads(encodedJson)
	except ValueError as e:
		raise ValueError