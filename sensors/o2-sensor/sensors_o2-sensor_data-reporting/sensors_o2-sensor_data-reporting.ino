/* Author: Thomas Richmond
 * Written: October 2017
 */

#define ADC_PORT A0

#define REFERENCE_VOLTAGE_V 5 // voltage of ADC reference
#define ERROR_CODE -555

//Increase values below to decrease print frequency.
#define DATA_PRINT_COUNTER_MOD 10

double getO2Concentration(int sensorIn){
  //Read O2 sensor data
  long sum = 0;
  for(int i = 0; i<32; i++){
    sum += analogRead(sensorIn);
  }
  sum >>= 5;

  //Convert O2 sensor data to voltage.
  float voltage = sum * (REFERENCE_VOLTAGE_V / 1023.0);

  if( voltage == 0 )
    return ERROR_CODE;
    
  float concentrationPercentage = (voltage * 0.21 / 2.0) * 100;
  Serial.print("Concentration: ");
  Serial.print(concentrationPercentage);
  Serial.println("%");
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
  getO2Concentration(ADC_PORT);
}


