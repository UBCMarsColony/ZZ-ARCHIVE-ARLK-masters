# JSON raspberry pi data reader code, take serial data from python

try:
    import serial
except ModuleNotFoundError:
    print("Could not import serial.")
import json
import time

# THE VARIABLE THAT MATTERS
__sensor_data = {}

try:
    serial_conn = serial.Serial('/dev/ttyACM1',9600)
except NameError:
    pass

def get_sensor_data(string_name = None):
    if string_name is None:
        return __sensor_data
    else:
        try:
            return __sensor_data[string_name]
        except KeyError as ve:
            print("Failed to find a value associated with the key " + string_name + ". Returning entire dictionary instead...")
            return __sensor_data
        except Exception as e:
            print("An unexpected exception occurred while trying to retrieve sensor data.\n\tStack Trace: " + str(e))
    
    return None

    
def update_sensor_data():
    try:    
        next_line = serial_conn.readline()
        global __sensor_data
        __sensor_data = __get_decoded_json_string(next_line)

    except ValueError as ve:
        print("Failed to parse JSON data.\n\tStack Trace: " + str(ve) + "\n\tSkipping line...")
    except Exception as e:
        print("An unexpected exception occurred while trying to update Pi sensor data. \n\tStack Trace: " + str(e))


# function that securely decodes a JSON string
def __get_decoded_json_string(encoded_json):
    try:
        return json.loads(encoded_json)
    except ValueError:
        raise ValueError
