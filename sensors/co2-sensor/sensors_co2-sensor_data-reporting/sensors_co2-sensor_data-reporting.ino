/*
 * Author: Thomas Richmond
 * Written in: Sept 2017
 */

#define MIN_VOLTAGE 400
#define ERROR_CODE -555
#define SENTINAL -1

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
short integrityAlertLevel = 0;

long loopCounter = 0;

double getCo2Values(int sensorIn){

  double voltage, concentration;
  //Read sensor report.
  short sensorValue = analogRead(sensorIn); 

  //Check and handle the sensor integrity.
  short integrityLevel = checkSensorIntegrity(sensorValue);
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
  voltage = sensorValue*(5000/1024.0); 

  //Choose action to perform given the voltage.
  if(voltage < MIN_VOLTAGE){
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
      short voltage_diference = voltage - MIN_VOLTAGE;
      concentration = voltage_diference*50.0/16.0;
      
      // Print Voltage
      Serial.print("voltage: ");
      Serial.print(voltage);
      Serial.println("mv");
      
      //Print CO2 concentration.
      Serial.print("Concentation: ");
      Serial.print(concentration);
      Serial.println("ppm");
    }
  }  
  
  //Increment the print controlling counter.
  loopCounter++;

  return concentration;
}

//Integrity check variables that cannot be bound to function scope.
short sensorValueOccuranceCounter = 0;
short lastSensorValue = SENTINAL;

short checkSensorIntegrity(int sensorValue){
  
  //Ensure the sensor is not faulty.
  if(sensorValue == 0)
  {
    //FAULT
    return -1;
  }
  //Make sure lastSensorValue has been defined.
  else if(lastSensorValue == SENTINAL){
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

/*THE FUNCTIONS setup() AND loop() SHOULD NOT BE INCLUDED IN THE UPLOAD CODE
* They are here so that the code can run independantly of the main system for debug & development purposes.*/
void setup(){  
  Serial.begin(9600);  
  // Set the default voltage of the reference voltage
  analogReference(DEFAULT); 
}

void loop(){
  getCo2Values(A0);
  delay(100); 
}


/***************************************************
 * Infrared CO2 Sensor0-5000ppm 
 * ****************************************************
 * This example The sensors detect CO2
 * 
 * @author lg.gang(lg.gang@qq.com)
 * @version  V1.0
 * @date  2016-7-6
 * 
 * GNU Lesser General Public License.
 * See <http://www.gnu.org/licenses/> for details.
 * All above must be included in any redistribution
 * ****************************************************/

