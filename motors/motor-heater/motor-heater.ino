//Motor heater assembly using TMP36 temperature sensor.
//pin assignments
#define PIN_HEATER_MOTOR 1
#define PIN_HEATER_GEARB 2

#define PIN_SENSOR_MOTOR 11
#define PIN_SENSOR_GEARB 12
// temperature thresholds
const int tempMax=80;
const int tempMin=0;
const int tempStatusLow=1;
const int tempStatusOK=0;

//temperature status array for [gears,motor], 0 for gears, 1 for motor
int tempStatus[2];

void setup(){
    pinMode(PIN_HEATER_MOTOR, OUTPUT);
    pinMode(PIN_HEATER_GEARB, OUTPUT);
    pinMode(PIN_SENSOR_MOTOR, INPUT);
    pinMode(PIN_SENSOR_GEARB, INPUT);
    Serial.begin(9600);
}

void loop(){

    int tempGears=getTemperature(PIN_SENSOR_GEARB);
    int tempMotor=getTemperature(PIN_SENSOR_MOTOR);

    getTempStatus(tempStatus,tempGears,tempMotor);

    
}

//Temperature polling on each sensor
int getTemperature(int sensorAddress){
    double voltageRaw=analogRead(sensorAddress)*5/1024.0;

    Serial.print(voltageRaw);
    Serial.println(" volts");

    double temperature=(voltageRaw-0.5)*100; //sensor offset inbuilt

    Serial.print(temperature);
    Serial.println(" degrees Celsius");
}

void getTempStatus(int tempStatus, int tempGears, int tempMotor){
    if(tempGears>=tempMin){
        tempStatus[0]=tempStatusOK;
    }
    else{
        tempStatus[0]=tempStatusLow;
    }
    if(tempMotor>=tempMin){
        tempStatus[1]=tempStatusOK;
    }
    else{  
        tempStatus[1]=tempStatusLow;
    }
}