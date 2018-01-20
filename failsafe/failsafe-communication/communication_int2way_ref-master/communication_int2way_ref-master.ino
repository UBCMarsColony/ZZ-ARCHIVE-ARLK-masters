
//Master Arduino, Writing 4 to the slave and recieving 2

#include <Wire.h>
#include <BaroSensor.h>

#define SLAVE_ADDRESS 12345
#define SIZE 5 //data being sent

//DEFINITIONS FOR LOGIC SENSOR SECTION
//pin location and number definitions, redefine before each run!
#define PINOXYGEN A1
#define PINCO2 A0

//data array constants
#define ENV_TEMP 0
#define ENV_PRES 1

//array indices for everything array
#define DATA_CONC_O2 0
#define DATA_CONC_CO2 1
#define DATA_TEMP 2
#define DATA_PRES 3

//reporting codes
#define CODE_ERROR_GENERIC -555 //generic error code returned by sensors that screw up
#define CODE_PREHEAT -600
#define CODE_ERROR_INIT_FAILURE -666

//subroutine specific constants
#define SENTINEL -1

//co2 data gathering constants
#define CO2_REFERENCE_VOLTAGE 5000
#define CO2_MIN_VOLTAGE 400 //minimum voltage for CO2 sensor subroutine

//o2 data gathering constants
#define O2_REFERENCE_VOLTAGE 5 //reference voltage for conversion in getOxygen()

//pressure data gathering constants
#define mBAR_TO_KPA 0.1

//PIN DEF for IR sensor
#define MotionSensor 4
int ledPin = 13;                // choose the pin for the LED
int inputPin = 2;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
int detected = 1;               //variable to send to PI that encodes if motion is detected (1=detected, 0=not detected)

void setup()
{
  Wire.begin();
  //UPDATE
    // put your setup code here, to run once:
    pinMode(PINOXYGEN, INPUT);
    pinMode(PINCO2, INPUT); //CO2 sensor takes analog values, check pin assignments!
    pinMode(ledPin, OUTPUT);      // declare LED as output
    pinMode(inputPin, INPUT);     // declare sensor as input
    BaroSensor.begin(); 
    //end
  Serial.begin(9600);  
}

//INITIALIZE arrays with -1's
//int numrecieved[SIZE];
/*int numsent[SIZE];
for(int j=0; j<SIZE; j++){
  numrecieved[j]=SENTINEL;
  numsent[j]=SENTINEL;
}*/

void loop()
{
  //Serial.print("Sending The Slave:");
  //Serial.print("\n");
  //Logic Sensor Integration Code HERE
  //declare vars
  int conc_o2 = SENTINEL;
  int conc_co2 = SENTINEL;
  int environment_array [2]; //2 row array of environment conditions: [TEMPERATURE|PRESSURE], required for function to return 2 values
  int everything_array [5];//4 row array of every condition in order: [CO2|O2|TEMPERATURE|PRESSURE]
  char JSONBourne [1024]; //check string possible length and overflow behavior

  //assigning data into vars
  conc_o2 = getOxygen(PINOXYGEN);
  conc_co2 = getCO2(PINCO2);
  getEnvironment(environment_array);

  /* ________________________________________
      IR SENSOR CODE
    _________________________________________
  */
   val = digitalRead(inputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (pirState == LOW) {
      // we have just turned on
      //Serial.println("Motion detected!");
      detected=1;
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH){
      // we have just turned of
      //Serial.println("Motion ended!");
      detected=0;
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
  //environment data is passed by ref directly to the array from the function

  //we check for preheat status (further error handling required)
  //while (env_temp==-1 || env_pres==-1 || conc_co2==-1 || conc_o2==-1 ){
  //  Serial.println("Preheating sensors! ");
  //}

  //compile everything into array
  everything_array[DATA_CONC_O2]=conc_o2;
  everything_array[DATA_CONC_CO2]=conc_co2;
  everything_array[DATA_TEMP]=environment_array[ENV_TEMP];
  everything_array[DATA_PRES]=environment_array[ENV_PRES];
  everything_array[MotionSensor]=detected;
  //printing into JSON variable then transmitting to serial
  sprintf(JSONBourne, "{\"GasComposition\":{\"CO2\":%d, \"O2\":%d},\"Temperature\":%d, \"Pressure\":%d, \"Motion Detector\":%d }", conc_co2, conc_o2, environment_array[ENV_TEMP], environment_array[ENV_PRES], detected);
  Serial.println(JSONBourne);
  

  //sending slave data. All data elements from all sensors must be stored in numsent array by this point
  Wire.beginTransmission(SLAVE_ADDRESS);   
  for(int i=0; i<SIZE; i++){
  //Serial.print(everything_array[i]);
  //Serial.print("\n");
  Wire.write(everything_array[i]); 
  }           
  Wire.endTransmission();   
  delay(500);

/*
  //requesting data from slave
  for(int k=0; k<SIZE; k++){
  Serial.println("Requesting Data"); 
  Wire.requestFrom(SLAVE_ADDRESS, 1);

  int bytes = Wire.available();
  
  Serial.print("Slave sent ");
  Serial.print(bytes);
  Serial.print(" bytes of information\n");
  
  numrecieved[k] = Wire.read();
  }
  for(int u=0; u<SIZE; u++){
    Serial.print(numrecieved[u]);
    Serial.print("\n");
  }
  memset(numrecieved,0,sizeof numrecieved);// Clearing array
  delay(500);
  */
}

//Subroutine functions
//Environment polling data should return -555 as an agreed-upon error value (might be able to change with predefined value above)

//getOxygen(char sensorIn) returns the oxygen percentage in the air
int getOxygen(char sensorIn){
  //Collect 32 samples of O2 data from the sensor. Then, divide by 32 to get the representative average. 
  //(NOTE: Bitwise shift 5 right (>>5) is equivalent to dividing by 2^(5), which is 32).
  //During this process, make sure the sensor is functioning properly, and return an error code otherwise.
  long sum = 0;
  for(int i = 0; i<32; i++){
    sum += analogRead(sensorIn);
  }

  sum >>= 5;

  //Convert received sensorValue to voltage, and concentrationPercentage.
  float voltage = (sum / 1024.0) * O2_REFERENCE_VOLTAGE; //change it for your used voltage!
  float concentrationPercentage = (voltage * 0.21 / 2.0) * 100;
  return concentrationPercentage; //this used to return concentration only, converted to percent (kevin)
}

//getCO2(char sensorIn) takes the pin assignment number sensorIn and returns the CO2 concentration in ppm (parts per million)
int getCO2(char sensorIn){
    double voltage, concentrationPpm;
    //Read sensor report.
    short sensorValue = analogRead(sensorIn); 
    // Convert analog signal to voltage.
    voltage = (sensorValue / 1024.0) * CO2_REFERENCE_VOLTAGE ; 
  
    //Choose action to perform given the voltage.
    if(voltage < CO2_MIN_VOLTAGE){
      return CODE_PREHEAT; //return PREHEAT value for function, for handling in master function
    } 
    
    short voltage_diference = voltage - CO2_MIN_VOLTAGE;
    concentrationPpm = voltage_diference*50.0/16.0;
  
    return concentrationPpm;
}

//getEnvironment passes by array the values of temperature and pressure, pressure converted to kilopascals, temperature in 
//degrees Celsius.
double getEnvironment(int environment_array[]){
  double temp;
  double pressure;
  
  //Check if sensor is working properly
  if(!BaroSensor.isOK()) {
    environment_array[ENV_TEMP] = CODE_ERROR_INIT_FAILURE;
    environment_array[ENV_PRES] = CODE_ERROR_INIT_FAILURE;
    BaroSensor.begin(); // Try to reinitialise the sensor if we can
  }
  
  else {
    temp = BaroSensor.getTemperature();
    pressure = BaroSensor.getPressure(); //Pressure in millibars (mBar)
    
    //Error checking: Temp range of sensor: -40 to +85 degrees celcius
    if(temp < -40 || temp > 85){
      environment_array[ENV_TEMP] = CODE_ERROR_GENERIC; //return error code if temperature out of range
    }
    else { 
      environment_array[ENV_TEMP] = temp;
    }
   
    //Error checking: pressure range of sensor: 10 to 2000 mbar
    if(pressure <10 || pressure >2000){
      environment_array[ENV_PRES] = CODE_ERROR_GENERIC;
    }
    else {
      environment_array[ENV_PRES] = pressure * mBAR_TO_KPA;
    }
  }
}
