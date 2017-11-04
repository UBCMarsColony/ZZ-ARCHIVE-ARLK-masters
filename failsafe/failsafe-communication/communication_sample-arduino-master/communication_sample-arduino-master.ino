#include <Wire.h>

#define SLAVE_ADDRESS 0x60

void setup()
{
  Wire.begin(); 
  randomSeed(analogRead(3));
  Serial.begin(9600);  
}

byte x = 0;

void loop()
{
  x = random(0,255);
  Serial.print("Sent: ");
  Serial.print(x, HEX);
  Serial.print("\n");
  Wire.beginTransmission(0x60);   
  Wire.write(x);                
  Wire.endTransmission();   
  delay(500);
  Serial.println("Requesting Data"); 
  Wire.requestFrom(SLAVE_ADDRESS, 1);

  int bytes = Wire.available();
  Serial.print("Slave sent ");
  Serial.print(bytes);
  Serial.print(" of information\n");
  for(int i = 0; i< bytes; i++)
  {
    x = Wire.read();
    Serial.print("Slave Sent: ");
    Serial.print(x, HEX);
    Serial.print("\n");
  }  
  delay(500);
}
