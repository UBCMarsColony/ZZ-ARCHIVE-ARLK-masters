/* Author: Thomas Richmond
 * Written: October 2017
 */

//Parameters for running. Delete these and replace their references in master.
#define ADC_PORT A0
#define PRINT_ON 1 //1 for true, 0 for false

#define REFERENCE_VOLTAGE_V 5 // voltage of ADC reference.
#define ERROR_CODE -555

//Increase values below to decrease print frequency.
#define DATA_PRINT_COUNTER_MOD 10

/* Get the CO2 concentration from the CO2 sensor. Return it, in ppm.
 * Param: sensorIn - The ADC Port to which this port is attached.
 * Param: printOn - Specifies if printing should occur (set to 1 if this is the case). Overload parameter
 */
double getO2Concentration(int sensorIn, short printOn = 0){
  //Collect 32 samples of O2 data from the sensor. Then, divide by 32 to get the representative average. 
  //(NOTE: Bitwise shift 5 right (>>5) is equivalent to dividing by 2^(5), which is 32).
  //During this process, make sure the sensor is functioning properly, and return an error code otherwise.
  long sensorValue = 0;
  for(int i = 0; i<32; i++){
    int nextVal = analogRead(sensorIn);
    
    if (nextVal == 0){
      if (printOn == 1)
        Serial.print("ERROR: Sensor is not functioning as expected. Cannot read O2 data.");
      return ERROR_CODE;
    }
   
    sensorValue += nextVal;
  }
  //Didive by 2^(5) to get the average
  sensorValue >>= 5;
  
  //Convert received sensorValue to voltage, and concentrationPercentage.
  float voltage = ( sensorValue / 1024.0 ) * REFERENCE_VOLTAGE_V;
  float concentrationPercentage = (voltage * 0.21 / 2.0) * 100;

  //Print out O2 concentration data.
  if(printOn == 1){
    Serial.print("Concentration: ");
    Serial.print(concentrationPercentage);
    Serial.println("%");
  }
  
  return concentrationPercentage;
}


/*THE FUNCTIONS setup() AND loop() SHOULD NOT BE INCLUDED IN THE UPLOAD CODE
* They are here so that the code can run independantly of the main system for debug & development purposes.*/
void setup(){
    // put your setup code here, to run once:
    Serial.begin(9600);
    Serial.println("Grove - O₂ Sensor Test Code...");
}


void loop(){
  getO2Concentration(ADC_PORT, PRINT_ON);
}


