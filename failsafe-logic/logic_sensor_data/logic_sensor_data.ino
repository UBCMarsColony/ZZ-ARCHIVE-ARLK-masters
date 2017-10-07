/*
Overall logic to to gather and pass on sensor data to the raspberry pin
getCO2, getOxygen written by Thomas Richmond
getTemperature, getPressure licensed under GNU GPL V3, modified by Teryn Tsang
This wrapper code written by Kevin Oesef
All code licensed under GNU GPL V3
*/

//pin location and number definitions, redefine before each run!
#define PINOXYGEN 3
#define PINCO2 4
#define PINENV 5

//subroutine specific constants
#define ERROR_CODE -555 //universal error code returned by sensors that screw up
#define REF_VOLT_33 3.3 //reference voltage for 3,3 volt sensors

//co2 data gathering constants
#define MIN_VOLTAGE 400 //minimum voltage for CO2 sensor subroutine
#define SENTINAL -1
#define PREHEAT -600
#define PREHEAT_PRINT_COUNTER_MOD 20

//o2 data gathering constants
#define REFERENCE_VOLTAGE 3.3
#define DATA_PRINT_COUNTER_MOD 10 //what is this for? shared with O2 and CO2

//Setup subroutine
void setup() {
  // put your setup code here, to run once:
  pinMode(PINOXYGEN, INPUT);
  pinMode(PINCO2, INPUT); //CO2 sensor takes analog values, check pin assignments!
  pinMode(PINENV, INPUT);
  Serial.begin(9600);
}

//Main logic
void loop() {
  //declare vars, should we use global?
  double conc_o2=-1;
  double conc_co2=-1;
  double env_temp=-1;
  double env_pres=-1;
  char JSONBourne [1024]; //check string possible length and overflow behavior

  //assigning data into vars
  conc_o2=getOxygen();
  conc_co2=getCO2();
  env_temp=getTemperature();
  env_pres=getPressure();

  //we check for preheat status (further error handling required)
  while (env_temp==-1 || env_pres==-1 || conc_co2==-1 || conc_o2==-1 ){
    Serial.print("Preheating sensors! ");
  }

  //printing into JSON variable then transmitting to serial
  sprintf(JSONBourne, "{GasComposition:{CO2:%d O2:%d}Temperature:%d Pressure:%d}", conc_co2, conc_o2, env_temp, env_pres);
  Serial.println(JSONBourne);
  
}

//Subroutine functions
//Environment polling data should return -555 as an agreed-upon error value (might be able to change with predefined value above)

double getOxygen(int sensorIn){
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
  float concentrationPercentage = concentration * 100;
  return concentrationPercentage; //this used to return concentration only, converted 2 percent (kevin)
}

double getCO2(int sensorIn){
  
    double voltage, concentration;
    //Read sensor report.
    short sensorValue = analogRead(sensorIn); 
  
    //Check and handle the sensor integrity. Commented out for now.
     short integrityLevel = checkSensorIntegrity(sensorValue);
    /*switch(integrityLevel){
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
    } */
  
    // Convert analog signal to voltage.
    voltage = sensorValue*(5000/1024.0); 
  
    //Choose action to perform given the voltage.
    if(voltage < MIN_VOLTAGE){
      //PREHEATING
      if(loopCounter % PREHEAT_PRINT_COUNTER_MOD == 0){ //Controls data printing per loop set.
        Serial.print("Preheating. Current voltage: ");
        Serial.print(voltage);
        Serial.println("mv");
      }
      return PREHEAT; //return PREHEAT value for function, for handling in master function
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

double getTemperature(){
  //return temperature;
}

double getPressure(){
  //return pressure;
}