const int PULpinH = 10;
const int PULpinL = 11;
const int DIRpinH = 12;
const int DIRpinL = 13;
const int stepSpeed = 100; //input value between 0-255

void setup() {
  // put your setup code here, to run once:
  pinMode(PULpinH, OUTPUT);
  pinMode(PULpinL, OUTPUT);
  pinMode(DIRpinH, OUTPUT);
  pinMode(DIRpinL, OUTPUT);
  digitalWrite(PULpinH, HIGH);
  digitalWrite(DIRpinH, HIGH);
  digitalWrite(DIRpinL, HIGH);
  analogWrite(PULpinL, stepSpeed);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
}
