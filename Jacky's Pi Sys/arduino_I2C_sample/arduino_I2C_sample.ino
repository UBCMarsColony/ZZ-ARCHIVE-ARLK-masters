#include <Wire.h>

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  int x = 0;
  while (Wire.available()) { // loop through all but the last
    x++;
    unsigned char c = Wire.read();

      //char c = Wire.read(); // receive byte as a character
      Serial.println(int(c));         // print the character
  }
}
//
void requestEvent() {
  char s[] ="abcdefghijklmn";//opqrstuvwsyz1234567890!@#$^&*()-=}{";
  Serial.print("num of bytes");
  Serial.print(sizeof(s));
  Wire.write(s); 
  // respond with message of 6 bytes
  // as expected by master
}