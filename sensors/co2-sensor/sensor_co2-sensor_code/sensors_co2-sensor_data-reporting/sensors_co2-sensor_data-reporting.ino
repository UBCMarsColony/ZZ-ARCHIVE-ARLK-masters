/*
 * Author: Thomas Richmond
 * Written in: Sept 2017
 */

#define ADC_PORT A0

//Increase values to print less often, and vice versa.
#define PREHEAT_PRINT_COUNTER_FREQ 20
#define DATA_PRINT_COUNTER_FREQ 10

//Some constants
#define REFERENCE_VOLTAGE_mV 5000.0
#define MIN_VOLTAGE_mV 400
#define ERROR_CODE -555

//The loopCounter variable and all sections of code based on it can be removed when implemented with master
unsigned short loopCounter = 0;

double getCo2Value(int sensorIn){
  double voltageIn, concentration;
  
  //Read sensor report.
  short sensorValue = analogRead(sensorIn); 

  // Convert analog signal to voltage.
  voltageIn = sensorValue * ( REFERENCE_VOLTAGE_mV / 1024.0 ); 

  //Choose action to perform given the voltage:
  if(voltageIn == 0) //Error in reporting.
    return ERROR_CODE;
    
  if(voltageIn < MIN_VOLTAGE_mV) //Sensor is preheating:
  {
    if(loopCounter % PREHEAT_PRINT_COUNTER_FREQ == 0){ //Controls data printing per loop set.
      Serial.print("Preheating. Current voltage: ");
      Serial.print(voltageIn);
      Serial.println("mv");
    
      loopCounter = 0;
    }
  } 
  else // Sensor report successful
  {
    
    //Calculate the voltage difference and, by extension, the CO2 concentration.
    short voltage_diference = voltageIn - MIN_VOLTAGE_mV;
    concentration = voltage_diference * 50.0 / 16.0;

    //Determine if data should be printed to the serial monitor.
    if(loopCounter % DATA_PRINT_COUNTER_FREQ == 0){ //Controls data printing per loop set.
      
      // Print Voltage
      Serial.print("voltage: ");
      Serial.print(voltageIn);
      Serial.println("mv");
      
      //Print CO2 concentration.
      Serial.print("Concentation: ");
      Serial.print(concentration);
      Serial.println("ppm");

      loopCounter = 0;
    }
  }  

  loopCounter++;
  return concentration;
}

/*THE FUNCTIONS setup() AND loop() SHOULD NOT BE INCLUDED IN THE UPLOAD CODE
* They are here so that the code can run independantly of the main system for debug & development purposes.*/
void setup(){  
  Serial.begin(9600);  
  // Set the default voltage of the reference voltage
  analogReference(DEFAULT); 
}

void loop(){
  getCo2Value(ADC_PORT);
  delay(100); 
}


