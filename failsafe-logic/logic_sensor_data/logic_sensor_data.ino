//pin location and number definitions CHECK AND REDEFINE BEFORE EACH RUN
#define PINOXYGEN 3
#define PINCO2 4
#define PINENV 5
#define ERRORCODE -555

//Setup subroutine

void setup() 
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
  JSONBourne=sprintf(JSONBourne, "{"GasComposition":{"CO2":"%d" "O2":"%d"}"Temperature":"%d" "Pressure":"%d"}", conc_co2, conc_o2, env-temp, env_pres);
  Serial.println(JSONBourne);
  
}

//Functions to be referred to
//Environment polling data should return -555 as an agreed-upon error value (might be able to change with predefined value above)

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

