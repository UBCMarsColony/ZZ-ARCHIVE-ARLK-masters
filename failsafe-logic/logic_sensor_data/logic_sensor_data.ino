/*
Overall logic to to gather and pass on sensor data to the raspberry pin
getCO2, getOxygen written by Thomas Richmond
getEnvironment, getPressure licensed under GNU GPL V3, modified by Teryn Tsang
This wrapper code written by Kevin Oesef
All code licensed under GNU GPL V3
*/
#include <Wire.h>
#include <BaroSensor.h>

//pin location and number definitions, redefine before each run!
#define PINOXYGEN A1
#define PINCO2 A0

//subroutine specific constants
#define ERROR_CODE -555 //generic error code returned by sensors that screw up
#define ERROR_INIT_FAILURE -666

//co2 data gathering constants
#define MIN_VOLTAGE 400 //minimum voltage for CO2 sensor subroutine
#define SENTINAL -1
#define PREHEAT -600
#define PREHEAT_PRINT_COUNTER_MOD 20

//o2 data gathering constants
#define REFERENCE_VOLTAGE 5 //reference voltage for conversion in getOxygen()
#define DATA_PRINT_COUNTER_MOD 10 //what is this for? shared with O2 and CO2

//Setup subroutine
void setup() {
  // put your setup code here, to run once:
  pinMode(PINOXYGEN, INPUT);
  pinMode(PINCO2, INPUT); //CO2 sensor takes analog values, check pin assignments!
  BaroSensor.begin();
  Serial.begin(9600);
}

//Main logic
void loop() {
  //declare vars, should we use global?
  int conc_o2=-1;
  int conc_co2=-1;
  int environment_array [2]; //2 row array of environment conditions: [TEMPERATURE|PRESSURE]
  int everything_array [4];
  char JSONBourne [1024]; //check string possible length and overflow behavior

  //assigning data into vars
  conc_o2=getOxygen(PINOXYGEN);
  conc_co2=getCO2(PINCO2);
  getEnvironment(environment_array);
  //environment data is passed by ref directly to the array from the function

  //we check for preheat status (further error handling required)
  //while (env_temp==-1 || env_pres==-1 || conc_co2==-1 || conc_o2==-1 ){
  //  Serial.println("Preheating sensors! ");
  //}

  //compile everything into array
  // everything_array[0]=conc_o2;
  // everything_array[1]=conc_co2;
  // everything_array[2]=environment_array[0];
  // everything_array[3]=environment_array[1];

  //printing into JSON variable then transmitting to serial
  sprintf(JSONBourne, "{GasComposition:{CO2:%d O2:%d}Temperature:%d Pressure:%d}", conc_co2, conc_o2, environment_array[0], environment_array[1]);
  Serial.println(JSONBourne);
  
  //debugging printer
  // int i;
  // for(i=0;i>=3;i++){
  //   Serial.print(everything_array[i]);
  // }
  // i=0;
}

//Subroutine functions
//Environment polling data should return -555 as an agreed-upon error value (might be able to change with predefined value above)

//getOxygen(char sensorIn) returns the oxygen percentage in the air
int getOxygen(char sensorIn){
  long sum = 0;
  for(int i = 0; i<32; i++){
    sum += analogRead(sensorIn);
  }

  sum >>= 5;

  float voltage = sum * (REFERENCE_VOLTAGE / 1023.0); //change it for your used voltage!

  float concentration = voltage * 0.21 / 2.0;
  /*Serial.print("Concentration: ");
  Serial.print(concentration);
  Serial.println("ppm");*/
  float concentrationPercentage = concentration * 100;
  return concentrationPercentage; //this used to return concentration only, converted to percent (kevin)
}

//getCO2(char sensorIn) takes the pin assignment number sensorIn and returns the CO2 concentration in ppm (parts per million)
int getCO2(char sensorIn){
  
    double voltage, concentration;
    //Read sensor report.
    short sensorValue = analogRead(sensorIn); 
    // Convert analog signal to voltage.
    voltage = sensorValue*(5000/1024.0); 
  
    //Choose action to perform given the voltage.
    if(voltage < MIN_VOLTAGE){
      return PREHEAT; //return PREHEAT value for function, for handling in master function
    } 
    
    short voltage_diference = voltage - MIN_VOLTAGE;
    concentration = voltage_diference*50.0/16.0;
  
    return concentration;
}

//getEnvironment passes by array the values of temperature and pressure, pressure converted to kilopascals, temperature in 
//degrees Celsius.
double getEnvironment(int environment_array[]){
  double temp;
  double pressure;
  double factorKpa=0.1;
  
  //Check if sensor is working properly
  if(!BaroSensor.isOK()) {
    environment_array[0]=ERROR_INIT_FAILURE;
    environment_array[1]=ERROR_INIT_FAILURE;
    BaroSensor.begin(); // Try to reinitialise the sensor if we can
  }
  
  else {
    temp=BaroSensor.getTemperature();
    pressure=BaroSensor.getPressure();
    
    //Error checking: Temp range of sensor: -40 to +85 degrees celcius
    if(temp <-40 || temp >85){
      environment_array[0]=ERROR_CODE; //return error code if temperature out of range
    }
    else { 
      environment_array[0]=temp;
    }
   
    //Error checking: pressure range of sensor: 10 to 2000 mbar
    if(pressure <10 || pressure >2000){
      environment_array[1]=ERROR_CODE;
    }
    else {
      environment_array[1]=pressure*factorKpa;
    }
  }
}
