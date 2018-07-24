//constants
const int pin_PUL_low = 11;
const int pin_DIR_low = 12;
const int pin_ENA_low = 13;
const int pin_LIM_OPEN = 10;
const int pin_LIM_CLOSED = 9;

const int pin_HEATER_MOTOR 1
const int pin_HEATER_GEARS 2

const int pin_SENSOR_MOTOR 11
const int pin_SENSOR_GEARS 12

const int gearRatio = 47;
const int pulseWidth = 1;
const int ON = 1;
const int OFF = 0;

//Motor heater assembly using TMP36 temperature sensor.
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

    //preparation of timer interrupts, we will use timer 1 for 16 bit resolution. some bitwise operations ahead!
    cli(); //clear interrupts
    TCCR1A=0; //clear TC control register 0 A (prescaler)
    TCCR1B=0; //clear TC control register 0 B (prescaler)
    TCNT1=0; //clear TC tick counter
    OCR1=15624; //set Output Compare Register to value calculated (see notes)
    //please check the microcontroller manual for register descriptions!
    
    sei(); //set interrupts

    //pin mode setups
    pinMode(pin_PUL_low, OUTPUT);
    pinMode(pin_DIR_low, OUTPUT);
    pinMode(pin_LIM_CLOSED, INPUT_PULLUP);
    pinMode(pin_LIM_OPEN, INPUT_PULLUP);

    //initial conditions for motor
    digitalWrite(pin_DIR_low, LOW);
    digitalWrite(pin_PUL_low, LOW);
    digitalWrite(pin_ENA_low, LOW);
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
    return
}

//increments the stepper motor by one tick. Can be used for a different function that tracks angle.
void stepperAngleIncrement(char direction){
    digitalWrite(pin_DIR_low,direction);
    digitalWrite(pin_PUL_low,LOW);
    delay(pulseWidth);
    digitalWrite(pin_PUL_low,HIGH);
    delay(pulseWidth);
}

int doorOpen(void){

    Serial.println("Open commanded");
    delay(1000);

    if(doorStatus!=closed){
        while(digitalRead(pin_LIM_CLOSED)==HIGH){
            stepperAngleIncrement('R');
            doorStatus=transit;
            Serial.println("Closing!");
        }
        doorStatus=CLOSED;
        Serial.println("Door closed!");
    }

    while(digitalRead(pin_LIM_OPEN)!=LOW){
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
    while(digitalRead(pin_LIM_CLOSED)!=LOW){
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
        digitalWrite(pin_ENA_low,LOW);
    }
    else{
        digitalWrite(pin_ENA_low,HIGH);
    }
}

// int modeLUT(string mode){
//     enum motorMode{
//         '0111'=400,'1011'=800,'0011'=1600,'1101'=3200,'0101'=6400,'1001'=12800,'0001'=25600,'1110'=1000,'0110'=2000,'1010'=4000,'0010'=5000,'1100'=8000,'0100'=10000,'1000'=20000,'0000'=25000
//     } motorMode;
    
//     return stepsToRev_raw
// }