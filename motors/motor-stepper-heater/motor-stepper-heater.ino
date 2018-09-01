#include <Wire.h>

//constants
const int pin_PUL_low = 10;
const int pin_DIR_low = 11;
const int pin_ENA_low = 12;
const int pin_LIM_OPEN = 9;
const int pin_LIM_CLOSED = 8;

const int pin_HEATER_MOTOR = 13;
const int pin_HEATER_GEARS = 13;
const int pin_SENSOR_MOTOR = 0;
const int pin_SENSOR_GEARS = 0;

const int gearRatio = 47;
const int pulseWidth = 1;
const int ON = 1;
const int OFF = 0;

const int address_slave = 45; //address must be in HEX!

//Motor heater assembly using TMP36 temperature sensor.
// temperature thresholds
const int tempMax = 80;
const int tempMin = 0;
const int tempStatusLow = -1;
const int tempStatusOK = 0;

//motor and gears temperatures

double tempStatus[2];
double temp_motor;
double temp_gears;

//special enum of type state, to report on door status
enum doorState{
    open=1,closed=2,transit=3,unknown=-1
    };
enum doorState doorStatus;

int currentAngle;
int datumClosed;
int datumOpen;

void setup() {
    Serial.begin(9600);
    Wire.begin(address_slave); //fucking slaves get your ass back here
    Serial.println("UBC Mars Colony Airlock program");
    Serial.println("Door control and heater system");
    delay(2000);

    Serial.println("First time initialization...");
    //preparation of timer interrupts, we will use timer 1 for 16 bit resolution. some bitwise operations ahead!, check the microcontroller manual for register descriptions!
    cli(); //clear interrupts before writing to registers

    TCCR1A=0; //clear TC control register 0 A (COMn register settings), set all to 0 and never written!
    TCCR1B=0; //clear TC control register 0 B (prescaler settings)
    TCNT1=0; //clear TC tick counter

    OCR1A=15624; //set Output Compare Register to value calculated (see notes)
    TCCR1B|=(1<<WGM12); //enable CTC mode (clear timer on trip) by enabling bits WGM12 on B-register
    TCCR1B|=(1<<CS12)|(1<<CS10); //enable prescaler 1024 by enabling bits CS12 and CS10 on B-register

    TIMSK1|=(1<<OCIE1A); //enable timer by setting mask bit to 1
    
    sei(); //set interrupts
    Serial.println("Interrupts set");

    //pin mode setups
    pinMode(pin_PUL_low, OUTPUT);
    pinMode(pin_DIR_low, OUTPUT);
    pinMode(pin_LIM_CLOSED, INPUT_PULLUP);
    pinMode(pin_LIM_OPEN, INPUT_PULLUP);
    pinMode(13, OUTPUT);
    Serial.println("Pin modes set");

    //initial conditions for motor
    digitalWrite(pin_DIR_low, LOW);
    digitalWrite(pin_PUL_low, LOW);
    digitalWrite(pin_ENA_low, LOW);
    doorStatus=unknown;
    Serial.println("Door status and pins set");
    motorTest();
    Serial.println("System setup complete, starting...");
}

//ISR (interrupt service request): poll for temperature then enable heaters as required
ISR(TIMER1_COMPA_vect){

    temp_motor=getTemperature(pin_SENSOR_MOTOR);
    temp_gears=getTemperature(pin_SENSOR_GEARS);

    getTempStatus(tempStatus,temp_gears,temp_motor);
    motorHeatRoutine(tempStatus);

}

void loop() {
    Wire.onReceive(commandHandler); //function to call when command received
}

//motor is low side switching! 5V from arduino 5v rail. logical disable is pulling the L pin to 5V.

//function stepperAngleRotate takes int angle, char direction, rotates angle degrees in specified direction. 
void stepperAngleRotate(int angle, char direction){

    //defins
    int index=0;
    float stepsToRevCurrentMode=400.00; //this is per stepper raw rotation, not gearboxed rotation
    float requiredPulses=(angle*gearRatio/360.0)*stepsToRevCurrentMode;

    //direction switching routine
    if (direction=='R'){
        digitalWrite(pin_DIR_low,HIGH);
    }
    else{
        digitalWrite(pin_DIR_low,LOW);
    }

    //pulse generator routine
    while(index<=requiredPulses){
        //beware of low side switching, pin_PUL_low,HIGH); //STOPPING PULSE LOW
        digitalWrite(pin_PUL_low, HIGH);
        delay(pulseWidth);
        digitalWrite(pin_PUL_low, LOW);
        delay(pulseWidth);
        // Serial.print("This is increment: ");
        // Serial.print(index);
        // Serial.print(" out of: ");
        // Serial.println(requiredPulses);
        index++;
    }
    return;
}

//increments the stepper motor by one tick. Can be used for a different function that tracks angle.
void stepperAngleIncrement(char direction){
    digitalWrite(pin_DIR_low,direction);
    digitalWrite(pin_PUL_low,LOW);
    delay(pulseWidth);
    digitalWrite(pin_PUL_low,HIGH);
    delay(pulseWidth);
}

void motorTest(void){
    // Serial.println("Motor self test routine...");
    int i=0;
    for(i=0;i<4;i++){
        int angle=45;
        stepperAngleRotate(angle, 'R');
        stepperAngleRotate(angle, 'L');
    }
}

int doorOpen(void){

    int i=0;
    Serial.println("Open commanded");
    delay(1000);

    if(doorStatus!=closed){
        while(digitalRead(pin_LIM_CLOSED)==HIGH){
            stepperAngleIncrement('R');
            doorStatus=transit;
            Serial.println("Closing!");
        }
        doorStatus=closed;
        Serial.println("Door closed!");
    }

    while(digitalRead(pin_LIM_OPEN)!=LOW){
        stepperAngleRotate(1,'L');
        doorStatus=transit;
        for(i=0;i<1;i++){
        Serial.println("Door opening!");
        }
        
    }
    doorStatus=open;
    Serial.println("Door opened!");
    return 0;
}

int doorClose(void){
    int i=0;
    Serial.println("Close commanded");
    delay(1000);

    if(doorStatus==closed){
        Serial.println("Door already closed!");
        return 0;
    }
    while(digitalRead(pin_LIM_CLOSED)!=LOW){
        stepperAngleIncrement('R');
        doorStatus=transit;
        for(i=0;i<1;i++){
        Serial.println("Door closing!");
        }
    }
    doorStatus=closed;
    Serial.println("Door closed!");
    return 0;
}

//Function motorPower takes integer status and switches the motor on or off
void motorPower(int status){
    if(status==ON){
        digitalWrite(pin_ENA_low,LOW);
    }
    else{
        digitalWrite(pin_ENA_low,HIGH);
    }
}

//temperature controls
double getTemperature(int sensorAddress){
    double voltageRaw=analogRead(sensorAddress)*5/1024.0;
    double temperature=(voltageRaw-0.5)*100; //sensor offset inbuilt
    return temperature;
}

void getTempStatus(double statusArray[], double tempGears, double tempMotor){
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

void motorHeatRoutine(double tempStatus[]){
    if(tempStatus[0]==tempStatusLow){
        digitalWrite(pin_HEATER_GEARS,HIGH);
    }
    else{
        digitalWrite(pin_HEATER_GEARS,LOW);
    }
    if(tempStatus[1]==tempStatusLow){
        digitalWrite(pin_HEATER_MOTOR,HIGH);
    }
    else{
        digitalWrite(pin_HEATER_MOTOR,LOW);
    }
}

void commandHandler(int howMany){
    char command=Wire.read();
    switch(command){
        case 'o':
            doorOpen();
            break;
        case 'c':
            doorClose();
            break;
    }
}