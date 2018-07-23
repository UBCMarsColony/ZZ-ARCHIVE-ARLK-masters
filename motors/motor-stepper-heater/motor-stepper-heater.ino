//constants
const int pinPUL_low = 11;
const int pinDIR_low = 12;
const int pinENA_low = 13;
const int pinSEN_open = 10;
const int pinSEN_closed = 9;

const int gearRatio = 47;
const int pulseWidth = 1;
const int ON = 1;
const int OFF = 0;

// const int INDETERMINATE = 404;
// const int CLOSED = 500;
// const int OPEN = 600;
// const int TRANSIT = 700;

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

//special enum of type state, to report on door status
enum doorState{
    open=1,closed=2,transit=3,unknown=-1
    };
enum doorState doorStatus;

int currentAngle;
int datumClosed;
int datumOpen;

void setup() {

    //pin mode setups
    pinMode(pinPUL_low, OUTPUT);
    pinMode(pinDIR_low, OUTPUT);
    pinMode(pinSEN_closed, INPUT_PULLUP);
    pinMode(pinSEN_open, INPUT_PULLUP);

    //initial conditions for motor
    digitalWrite(pinDIR_low, LOW);
    digitalWrite(pinPUL_low, LOW);
    digitalWrite(pinENA_low, LOW);
    Serial.begin(9600);

    //statuses
    doorStatus=unknown;

}

void loop() {
    // put your main code here, to run repeatedly:
    //starting definitions
    int rotateAngle=30;

    // motorPower(ON);
    int shake=0;
    while(shake<4){
        stepperAngleRotate(rotateAngle,'R');
        stepperAngleRotate(rotateAngle,'L');
        shake++;
        Serial.println("Shaking!");
    }
    delay(2000);
    doorOpen();
    delay(5000);
    doorClose();

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
        digitalWrite(pinDIR_low,HIGH);
    }
    else{
        digitalWrite(pinDIR_low,LOW);
    }

    //pulse generator routine
    while(index<=requiredPulses){
        //beware of low side switching, pinPUL_low,HIGH); //STOPPING PULSE LOW
        digitalWrite(pinPUL_low, HIGH);
        delay(pulseWidth);
        digitalWrite(pinPUL_low, LOW);
        delay(pulseWidth);
        // Serial.print("This is increment: ");
        // Serial.print(index);
        // Serial.print(" out of: ");
        // Serial.println(requiredPulses);
        index++;
    }
    return
}

//increments the stepper motor by one tick. Can be used for a different function that tracks angle.
void stepperAngleIncrement(char direction){
    digitalWrite(pinDIR_low,direction);
    digitalWrite(pinPUL_low,LOW);
    delay(pulseWidth);
    digitalWrite(pinPUL_low,HIGH);
    delay(pulseWidth);
}

int doorOpen(void){

    Serial.println("Open commanded");
    delay(1000);

    if(doorStatus!=closed){
        while(digitalRead(pinSEN_closed)==HIGH){
            stepperAngleIncrement('R');
            doorStatus=transit;
            Serial.println("Closing!");
        }
        doorStatus=CLOSED;
        Serial.println("Door closed!");
    }

    while(digitalRead(pinSEN_open)!=LOW){
        stepperAngleRotate(1,'L');
        doorStatus=transit;
        Serial.println("Door opening!");
    }
    doorStatus=open;
    Serial.println("Door opened!");
    return;
}

int doorClose(void){

    Serial.println("Close commanded");
    delay(1000);

    if(doorStatus==closed){
        Serial.println("Door already closed!");
        return 0;
    }
    while(digitalRead(pinSEN_closed)!=LOW){
        stepperAngleIncrement('R');
        doorStatus=transit;
        Serial.println("Door closing!");
    }
    doorStatus=closed;
    Serial.println("Door closed!");
    return;
}

//Function motorPower takes integer status and switches the motor on or off
void motorPower(int status){
    if(status==ON){
        digitalWrite(pinENA_low,LOW);
    }
    else{
        digitalWrite(pinENA_low,HIGH);
    }
}

// int modeLUT(string mode){
//     enum motorMode{
//         '0111'=400,'1011'=800,'0011'=1600,'1101'=3200,'0101'=6400,'1001'=12800,'0001'=25600,'1110'=1000,'0110'=2000,'1010'=4000,'0010'=5000,'1100'=8000,'0100'=10000,'1000'=20000,'0000'=25000
//     } motorMode;
    
//     return stepsToRev_raw
// }