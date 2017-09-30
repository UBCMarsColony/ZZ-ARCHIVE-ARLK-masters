/*
 * Author: Thomas Richmond
 * Written in: Sept 2017
 */

#define MIN_VOLTAGE 400
#define ERROR_CODE -555

//INCREASE VALUES BELOW TO DECREASE PRINT FREQUENCY, AND VICE VERSA
#define PREHEAT_PRINT_COUNTER_MOD 20
#define DATA_PRINT_COUNTER_MOD 10

enum AV{
  STATUS_CLEAR,
  STATUS_MINOR_WARN,
  STATUS_MODERATE_WARN,
  STATUS_SERIOUS_WARN
};

//A variable that stores sensor integrity. Uses values of enumerated AV
int integrityAlertLevel = 0;

int loopCounter = 0;

int getCo2Values(int sensorIn){
  //Read sensor report.
  int sensorValue = analogRead(sensorIn); 

  //Check and handle the sensor integrity.
  int integrityLevel = checkSensorIntegrity(sensorValue);
  switch(integrityLevel){
    case -1:
      Serial.println("ERROR: Sensor is faulty.");
      return ERROR_CODE;
    case STATUS_MINOR_WARN:
      //Continue to moderate warn
    case STATUS_MODERATE_WARN:
      Serial.println("WARNING: Sensor integrity may be compromised. Please standby until further notice.");
      break;
    case STATUS_SERIOUS_WARN:
      Serial.println("WARNING: Sensor integrity compromised. Awaiting fix...");
      delay(500);
      return ERROR_CODE;
    default:
      break;
  }

  // Convert analog signal to voltage.
  float voltage = sensorValue*(5000/1024.0); 

  //Choose action to perform given the voltage.
  if(voltage < MIN_VOLTAGE)
  {
    //PREHEATING
    if(loopCounter%PREHEAT_PRINT_COUNTER_MOD == 0){ //Controls data printing per loop set.
      Serial.print("Preheating. Current voltage: ");
      Serial.print(voltage);
      Serial.println("mv");
    }
  } 
  else
  {
    //DATA REPORT
    if(loopCounter%DATA_PRINT_COUNTER_MOD == 0){ //Controls data printing per loop set.

      //Calculate the voltage difference and, by extension, the CO2 concentration.
      int voltage_diference = voltage - MIN_VOLTAGE;
      float concentration = voltage_diference*50.0/16.0;
      
      // Print Voltage
      Serial.print("voltage: ");
      Serial.print(voltage);
      Serial.println("mv");
      
      //Print CO2 concentration
      Serial.print("Concentation: ");
      Serial.print(concentration);
      Serial.println("ppm");
    }
  }  
  
  //Increment the print controlling counter.
  loopCounter++;

  return concentation;
}

//Integrity check variables that cannot be bound to function scope.
int sensorValueOccuranceCounter = 0;
int lastSensorValue = -1; //Initialized with a sentinal value.

int checkSensorIntegrity(int sensorValue){
  
  //Ensure the sensor is not faulty.
  if(sensorValue == 0)
  {
    //FAULT
    return -1;
  }
  //Make sure lastSensorValue has been defined.
  else if(lastSensorValue < 0){
      lastSensorValue = sensorValue;
  }
  else if(sensorValue == lastSensorValue){
    
    sensorValueOccuranceCounter++;

    if(sensorValueOccuranceCounter > 1000)
      integrityAlertLevel = STATUS_SERIOUS_WARN;
    else if(sensorValueOccuranceCounter > 150)
      integrityAlertLevel = STATUS_MODERATE_WARN;
    else if(sensorValueOccuranceCounter > 50)
      integrityAlertLevel = STATUS_MINOR_WARN;
  }
  else{
    if(integrityAlertLevel != 0)
      Serial.println("Sensor integrity reestablished.");
    integrityAlertLevel = STATUS_CLEAR;
    lastSensorValue = sensorValue;
    sensorValueOccuranceCounter = 0;
  }

  return integrityAlertLevel;
}

