#include <Wire.h>

//constants
#define MSG_LEN 32
#define KEEP_MSG true
#define CLEAR_MSG false

struct pin{
    int PUL=10;
    int DIR=11;
    int ENA=12;
    int strike = 9;
    int LIM_open=9;
    int LIM_closed=8;

    int HEATER_motor=13;
    int HEATER_gears=13;
    int SENSOR_motor=A1;
    int SENSOR_gears=A1;
} pinNumber;

const int gearRatio = 47;
const int pulseWidth = 1;
const int ON = 1;
const int OFF = 0;

const int address_slave = 45; //address must be in HEX!

//Motor heater assembly using TMP36 temperature sensor.
//temperature thresholds
const int tempMax = 80;
const int tempMin = 0;
const int tempStatusLow = -1;
const int tempStatusOK = 0;

//motor and gears temperatures

double tempStatus[2];
double temp_motor;
double temp_gears;

//special enum of type state, to report on door status
enum tempState{
    low=-1,ok=0,overheat=1
};
enum tempState tempStatusEnum;


enum Priority {
    priorityLow = 0,
    priorityHigh = 1
};

enum DoorState {
    unknown = 0,
    transit = 3,
    close = 99,
    open = 111
};
enum DoorState doorState;

enum Procedure {
    setDoorState = 3,
    numMessages
};

typedef struct SetDoorState_t {
  byte action;
  byte procedure;
  byte priority;
  byte targetState;
};

volatile byte messages[numMessages][MSG_LEN] = {0};
volatile byte msgIndex = 0;

int currentAngle, datumClosed, datumOpen;

void setup() {
    Serial.begin(9600);
    
    Serial.print("Using address ");
    Serial.println(address_slave);
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
    pinMode(pinNumber.PUL, OUTPUT);
    pinMode(pinNumber.DIR, OUTPUT);
    pinMode(pinNumber.strike, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(pinNumber.strike), ISR_stopDoor, FALLING);
//    pinMode(pinNumber.LIM_open, INPUT_PULLUP);
//    attachInterrupt(digitalPinToInterrupt(pinNumber.LIM_open), ISR_stopDoor, FALLING);
    pinMode(13, OUTPUT);
    Serial.println("Pin modes set");

    //initial conditions for motor
    digitalWrite(pinNumber.DIR, LOW);
    digitalWrite(pinNumber.PUL, LOW);
    digitalWrite(pinNumber.ENA, LOW);
    doorState=0;
    Serial.println("Door status and pinNumber set, testing motor");
    motorTest();

    Wire.onReceive(commandHandler); //function to call when command received
//    Wire.onRequest(requestHandler);
    Serial.println("System setup complete, starting...");
}

void ISR_stopDoor() {
    doorState = ((SetDoorState_t*) messages[setDoorState])->targetState;
}

//ISR (interrupt service request): poll for temperature then enable heaters as required
ISR(TIMER1_COMPA_vect){

    temp_motor=getTemperature(pinNumber.SENSOR_motor);
    temp_gears=getTemperature(pinNumber.SENSOR_gears);
    // Serial.print("Motor temperature: ");
    // Serial.println(temp_motor);
    // Serial.print("Gearbox temperature: ");
    // Serial.println(temp_gears);

    getTempStatus(tempStatus,temp_gears,temp_motor);
    motorHeatRoutine(tempStatus);
}

void loop() {
    // MESSAGE PARSING & EVALUATION  
    if (evaluateMessage(messages[msgIndex], msgIndex) == CLEAR_MSG)
        memset(messages[msgIndex], 0, sizeof(messages[msgIndex])); // Clear message from 'messages' array
    msgIndex = (msgIndex + 1) % numMessages;

    // LIFE CYCLE EVENTS
    if (doorState == transit) {
        switch (((SetDoorState_t*) messages[setDoorState])->targetState) {
            case open:
                stepperAngleRotate(1,'L');
                break;
            case close:
                stepperAngleRotate(1,'R');
                break;
        }
    }
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
        digitalWrite(pinNumber.DIR,HIGH);
    }
    else{
        digitalWrite(pinNumber.DIR,LOW);
    }

    //pulse generator routine
    while(index<=requiredPulses){
        //beware of low side switching, pinNumber.PUL,HIGH);
        digitalWrite(pinNumber.PUL, HIGH);
        delay(pulseWidth);
        digitalWrite(pinNumber.PUL, LOW);
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
    digitalWrite(pinNumber.DIR,direction);
    digitalWrite(pinNumber.PUL,LOW);
    delay(pulseWidth);
    digitalWrite(pinNumber.PUL,HIGH);
    delay(pulseWidth);
}

void motorTest(void){
    Serial.println("Motor self test routine...");
    int i=0;
    for(i=0;i<4;i++){
        int angle=45;
        stepperAngleRotate(angle, 'R');
        stepperAngleRotate(angle, 'L');
    }
}


//Function motorPower takes integer status and switches the motor on or off
void motorPower(int status){
    switch(status){
        case ON:
            digitalWrite(pinNumber.ENA,HIGH);
            return ON;
        case OFF:
            digitalWrite(pinNumber.ENA,LOW);
            return OFF;
    }
}

//temperature controls for TMP36 sensor
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
        digitalWrite(pinNumber.HEATER_gears,HIGH);
    }
    else{
        digitalWrite(pinNumber.HEATER_gears,LOW);
    }
    if(tempStatus[1]==tempStatusLow){
        digitalWrite(pinNumber.HEATER_motor,HIGH);
    }
    else{
        digitalWrite(pinNumber.HEATER_motor,LOW);
    }
}


bool evaluateMessage(byte message[], int type) {   
    switch(type){
        case setDoorState: 
        {
            SetDoorState_t *sds = (SetDoorState_t*) message;
            
            if (sds->targetState == doorState) {
                Serial.print("Requested door state ");
                Serial.print(sds->targetState);
                Serial.println("Has been reached. Removing request from queue");
                return CLEAR_MSG;
            }

            switch(sds->targetState) {
                case 'o':
                    return doorOpen() ? CLEAR_MSG : KEEP_MSG;
                case 'c':
                    return doorClose() ? CLEAR_MSG : KEEP_MSG;
            }
        }
    }
    return KEEP_MSG;
}


void commandHandler(int howMany){
    Serial.println("Received transmission from Master");
    byte data[MSG_LEN] = {};

    // Read the incoming message.
    for (int i = 0; Wire.available(); i++) {
        data[i] = Wire.read();
        Serial.println(data[i]);
    }


    if (data[1] >= numMessages) {
        Serial.println("CRITICAL ERROR: Received message of unknown type! This should never happen.");
        return;
    }

    // Check if there is already an existing message of this type, and if the incoming message takes priority
    if (messages[data[1]][0] != 0 && data[2] != priorityHigh) {
        Serial.print("Message of type ");
        Serial.print(data[2]);
        Serial.println(" already exists. Ignoring...");
        return;
    }

    // Run other checks if needed.

    // Put message into the queue
    for (int i = 0; i < MSG_LEN; i++)
        messages[data[1]][i] = data[i];
}

/*void requestHandler(){
    //Wire.beginTransmission();
    //Wire.write()
    //Wire.endTransmission();
}*/



/* ****************
 * UNUSED FUNCTIONS
 * ****************
 * */
int doorOpen(void){

    Serial.println("Open commanded");
    delay(1000);

    if(doorState==open){
        Serial.println("Door already open!");
        return 0;
    }

    Serial.println("Door opening!");
    while(digitalRead(pinNumber.LIM_open)!=LOW){
        stepperAngleRotate(1,'L');
        doorState=transit;
    }
    doorState=open;
    Serial.println("Door opened!");
    return 0;
}

int doorClose(void){

    Serial.println("Close commanded");
    delay(1000);

    if(doorState == close){
        Serial.println("Door already closed!");
        return 0;
    }

    Serial.println("Door closing!");
    while(digitalRead(pinNumber.LIM_closed)!=LOW){
        stepperAngleIncrement('R');
        doorState=transit;
    }

    doorState = close;
    Serial.println("Door closed!");
    return 0;
}
