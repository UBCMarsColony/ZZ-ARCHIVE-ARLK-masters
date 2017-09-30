//pin location and number definitions
#define PINOXYGEN 3
#define PINCO2 4
#define PINENV 5
#define ERRORCODE -555

//Setup subroutine

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(PINOXYGEN, INPUT);
  pinMode(PINCO2, INPUT);
  pinMode(PINENV, INPUT);
}

//Main logic

void loop() {
  //declare vars, should we use global?
  double conc_o2=-1;
  double conc_co2=-1;
  double env_temp=-1;
  double env_humidity=-1;
  char JSONBourne [1024]; //check string possible length and overflow behavior

  //we check for preheat status (further error handlong
  while (env_temp==-1 || env_humidity==-1 || conc_co2==-1 || conc_o2==-1 ){
    Serial.println("Preheating sensors!");
  }
  JSONBourne=sprintf(JSONBourne, "{"GasComposition":{"CO2":"%d" "O2":"%d"}"Temperature":"%d" "Pressure":"%d"}", CO2, O2, temperature, pressure);
  Serial.println(JSONBourne);
}

//Functions to be referred to
//Environment polling data should return 

double pollAverage(){
  //wip
}

double getOxygen(){
  
  return concentrationOxygen;
}

double getCO2(){
  return concentrationCO2;
}

double getTemperature(){
  return temperature;
}

double getPressure(){
  return pressure;
}

