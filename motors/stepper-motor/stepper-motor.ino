const int PULpinH = 10;
const int PULpinL = 11;
const int DIRpinH = 12;
const int DIRpinL = 13;
// const int ENApinH = 998;
// const int ENApinL = 999;
const int gearRatio = 47;

void setup() {
  
  //pin mode setups
  pinMode(PULpinH, OUTPUT);
  pinMode(PULpinL, OUTPUT);
  pinMode(DIRpinH, OUTPUT);
  pinMode(DIRpinL, OUTPUT);

  //initial conditions for motor
  digitalWrite(DIRpinH, HIGH);
  digitalWrite(DIRpinL, LOW);

  digitalWrite(PULpinH, HIGH);
  digitalWrite(PULpinL, LOW);
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

  //debug pulser
  // delay(2000);
  // digitalWrite(PULpinL,LOW);
  // delay(2000);
  // digitalWrite(PULpinL,HIGH);
}

//motor is low side switching! 5V from arduino 5v rail. logical disable is pulling the L pin to 5V.
void stepperAngleRotate(int angle, char direction){
  
  //defins
  int index=0;
  float stepsToRevCurrentMode=400.0; //this is per stepper raw rotation, not gearboxed rotation
  float requiredPulses=(angle*gearRatio/360.0)*stepsToRevCurrentMode;

  //direction switching routine
  if (direction=='R'){
    digitalWrite(DIRpinL,HIGH);
  }
  else{
    digitalWrite(DIRpinL,LOW)
  }

  //beware of low side switching, PULpinL MUST BE LOW to enable
  while(index<=requiredPulses){
    digitalWrite(PULpinL,LOW); //MOVING PULSE HIGH
    delay(1);//i need a routine for pulse width etc
    digitalWrite(PULpinL,HIGH); //STOPPING PULSE LOW
    delay(1);

    // print debugging is the only debugging
    // Serial.print("This is increment: ");
    // Serial.print(index);
    // Serial.print(" out of: ");
    // Serial.println(requiredPulses);
    
    index++;
  }
}

/* void motorPower(string power){
  if (power=='ON'){
    digitalWrite(ENApinL,LOW)
  }
  else{
    digitalWrite(ENApinL,HIGH)
  }
} */