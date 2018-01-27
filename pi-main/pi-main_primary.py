"""
PRIMARY MAIN LOOP RUNS FROM HERE
"""

#initialization
serialPort = serial.Serial('/dev/ttyACM1',9600)
    
    
while True:
    
    update_sensor_data()
    print(str(get_sensor_data))
    
    updateLights()
    
    time.sleep(0.1)


