/* Author: Thomas Richmond
 * Written: October 2017
 */

#define REFERENCE_VOLTAGE 3.3 // voltage of adc reference

//Increase values below to decrease print frequency.
#define DATA_PRINT_COUNTER_MOD 10

double getO2Concentration(int sensorIn){
  long sum = 0;
  for(int i = 0; i<32; i++){
    sum += analogRead(sensorIn);
  }

  sum >>= 5;

  float voltage = sum * (REFERENCE_VOLTAGE / 1023.0);

  float concentration = voltage * 0.21 / 2.0;
  Serial.print("Concentration: ");
  Serial.print(concentration);
  Serial.println("ppm");
  //float concentrationPercentage = concentration * 100;
  return concentration;
}


/*THE FUNCTIONS setup() AND loop() SHOULD NOT BE INCLUDED IN THE UPLOAD CODE
* They are here so that the code can run independantly of the main system for debug & development purposes.*/
void setup(){
    // put your setup code here, to run once:
    Serial.begin(9600);
    Serial.println("Grove - Gas Sensor Test Code...");
}


void loop(){
  getO2Concentration(A5);
}


