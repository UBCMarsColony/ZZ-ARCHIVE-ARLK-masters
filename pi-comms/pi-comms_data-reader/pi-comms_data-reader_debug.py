#sJSON raspberry pi data reader code, take sserial data from python 

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
ser=serial.Serial('COM4',9600)
filename="debugReading.txt"
file=open(filename,mode="w")
ser.readline()
ser.readline()

#loop
while True:
	truedata=ser.readline()
	decodedString = getDecodedJsonString(truedata)
	
	if decodedString != None:
		gasCO2=str(decodedString["GasComposition"]["CO2"])
		gasO2=str(decodedString["GasComposition"]["O2"])
		temperature=str(decodedString["Temperature"])
		pressure=str(decodedString["Pressure"])
		print("CO2: " + gasCO2)
		print("O2: " + gasO2)
		print("Temperature: " + temperature)
		print("Pressure: " + pressure)
		#we write to file for analysis purposes, csv for category newline per entry
		file.write(gasCO2+','+gasO2+','+temperature+','+pressure+'\n')
	else:
		print("Failed to parse JSON data. Skipping line...")
