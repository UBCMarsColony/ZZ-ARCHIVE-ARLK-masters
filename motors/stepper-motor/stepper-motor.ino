//constants
const int pinPUL_low = 11;
const int pinDIR_low = 13;
const int pinENA_low = 999;
const int pinSEN_open = ;
const int pinSEN_closed = ;

const int gearRatio = 47;
const int ON = 1;
const int OFF = 0;

const int INDETERMINATE = 404
const int CLOSED = 500
const int OPEN = 600
const int TRANSIT = 700

int currentAngle;
int datumClosed;
int datumOpen;
int doorStatus=INDETERMINATE;

void setup() {
  
  //pin mode setups
  pinMode(PULpinH, OUTPUT);
  pinMode(pinPUL_low, OUTPUT);
  pinMode(DIRpinH, OUTPUT);
  pinMode(pinDIR_low, OUTPUT);

  //initial conditions for motor
  digitalWrite(DIRpinH, HIGH);
  digitalWrite(pinDIR_low, LOW);

  digitalWrite(PULpinH, HIGH);
  digitalWrite(pinPUL_low, LOW);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  //starting definitions
  char rotateDirection='L';
  int rotateAngle=90;

  stepperAngleRotate(rotateAngle,'L');
  delay(3000);
  stepperAngleRotate(rotateAngle,'R');
  delay(3000);

}

//motor is low side switching! 5V from arduino 5v rail. logical disable is pulling the L pin to 5V.

void doorCalibratePosition(void){

}

void doorOpen(void){
    if(doorStatus!=CLOSED){
        while(digitalRead(pinSEN_closed==LOW)){
            stepperAngleRotate(90,'R');
            delay(3000);
            doorStatus=CLOSED;
        }
    }
    else
        if(doorStatus==OPEN){
            break;
    }
    else 
        while(digitalRead(pinSEN_open==LOW){
            stepperAngleRotate(90,'L');
            delay(3000);
            doorStatus=OPEN;
    }
}

void doorClose(void){
    if(doorStatus==OPEN){
        break;
    }
    else 
        while(digitalRead(pinSEN_closed==LOW){
            stepperAngleRotate(90,'R');
            delay(3000);
            doorStatus=OPEN;
    }
}

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
  else{pinDIR_low
    digitalWrite(DIRpinL,LOW)
  }

  //beware of low side switching, pinPUL_low,HIGH); //STOPPING PULSE LOW
    delay(2);
    
    index++;
  }
}

//Function motorPower takes integer status and switches the motor on or off
void motorPower(int status){
  if (status==ON){
    digitalWrite(pinENA_low,HIGH)
  }
}

int modeLUT(string mode){
    return stepsToRev_raw
}