//constants
const int pinPUL_low = 11;
const int pinDIR_low = 12;
const int pinENA_low = 13;
const int pinSEN_open = 10;
const int pinSEN_closed = 9;

const int gearRatio = 47;
const int pulseWidth = 2;
const int ON = 1;
const int OFF = 0;

const int INDETERMINATE = 404;
const int CLOSED = 500;
const int OPEN = 600;
const int TRANSIT = 700;

int currentAngle;
int datumClosed;
int datumOpen;
int doorStatus;
int shake;

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
    doorStatus=INDETERMINATE;

}

void loop() {
    // put your main code here, to run repeatedly:
    //starting definitions
    int rotateAngle=2;

    // motorPower(ON);
    shake=0;
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
    float stepsToRevCurrentMode=400.0; //this is per stepper raw rotation, not gearboxed rotation
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

    if(doorStatus!=CLOSED){
        while(digitalRead(pinSEN_closed)==HIGH){
            stepperAngleIncrement('R');
            doorStatus=TRANSIT;
            Serial.println("Closing!");
        }
        doorStatus=CLOSED;
        Serial.println("Door closed!");
    }

    while(digitalRead(pinSEN_open)!=LOW){
        stepperAngleRotate(1,'L');
        doorStatus=TRANSIT;
        Serial.println("Door opening!");
    }
    doorStatus=OPEN;
    Serial.println("Door opened!");
    return;
}

int doorClose(void){

    Serial.println("Close commanded");
    delay(1000);

    if(doorStatus==CLOSED){
        Serial.println("Door already closed!");
        return 0;
    }
    while(digitalRead(pinSEN_closed)!=LOW){
        stepperAngleIncrement('R');
        doorStatus=TRANSIT;
        Serial.println("Door closing!");
    }
    doorStatus=CLOSED;
    Serial.println("Door closed!");
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
//     enum motorMode{'0111'=400,'1011'=800,'0011'=1600}
//     return stepsToRev_raw
// }