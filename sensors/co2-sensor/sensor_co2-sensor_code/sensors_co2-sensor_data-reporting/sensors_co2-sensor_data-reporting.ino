/*
 * Author: Thomas Richmond
 * Written in: Sept 2017
 */

//Parameters for running. Delete these and replace their references in master
#define ADC_PORT A0
#define PRINT_ON 1 //1 for true, 0 for false.

//Some constants
#define REFERENCE_VOLTAGE_mV 5000.0
#define MIN_VOLTAGE_mV 400

#define ERROR_CODE -555

double getCo2Value(int sensorIn, short printOn = 0){
  double sensorVoltage, concentrationPpm;
  
  //Read sensor report.
  short sensorValue = analogRead(sensorIn); 

  // Convert analog signal to voltage.
  sensorVoltage = sensorValue * ( REFERENCE_VOLTAGE_mV / 1024.0 ); 

  if(sensorVoltage == 0){  //Error in reporting.
    if(printOn == 1)
      Serial.println("ERROR: Sensor is not functioning as expected. Cannot read O2 data.");
    return ERROR_CODE;
  }

  //Check if sensor is preheating.
  //If it is, print this and return sensorVoltage.
  if(sensorVoltage < MIN_VOLTAGE_mV) 
  {
    if(printOn == 1){
      Serial.print("Preheating. Current voltage: ");
      Serial.print(sensorVoltage);
      Serial.println("mv");
    }
    
    return sensorVoltage;
  }    
    
  //Calculate the voltage difference and, by extension, the CO2 concentration.
  short voltage_diference = sensorVoltage - MIN_VOLTAGE_mV;
  concentrationPpm = voltage_diference * 50.0 / 16.0;

  //Determine if data should be printed to the serial monitor.
  if(printOn == 1){ //Controls data printing per loop set.
    // Print Voltage
    Serial.print("voltage: ");
    Serial.print(sensorVoltage);
    Serial.println("mv");
    
    //Print CO2 concentration.
    Serial.print("Concentation: ");
    Serial.print(concentrationPpm);
    Serial.println("ppm");
  }  

  return concentrationPpm;
}

/*THE FUNCTIONS setup() AND loop() SHOULD NOT BE INCLUDED IN THE UPLOAD CODE
* They are here so that the code can run independantly of the main system for debug & development purposes.*/
void setup(){  
  Serial.begin(9600);  
  // Set the default voltage of the reference voltage
  analogReference(DEFAULT); 
}

void loop(){
  getCo2Value(ADC_PORT, PRINT_ON);
  delay(100); 
}


