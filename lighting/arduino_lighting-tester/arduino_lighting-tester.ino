#define PIN_TEST 7
void setup(){
    pinMode(PIN_TEST, OUTPUT);
    Serial.begin(9600);
}

void loop(){
    digitalWrite(PIN_TEST,HIGH);
    Serial.println("on");
    // delay(4000);
    // digitalWrite(PIN_TEST,LOW);
    // Serial.println("off");
    // delay(4000);
}