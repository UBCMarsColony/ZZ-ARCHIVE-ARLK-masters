
//Master Arduino, Writing "Jacky" and Recieving "Jiang" from Slave

#include <Wire.h>

#define SLAVE_ADDRESS 1

void setup()
{
  Wire.begin(); 
  Serial.begin(9600);  
}

char x=" ";

void loop()
{
  Serial.print("Sent: ");
  Serial.print(SLAVE_ADDRESS);
  Serial.print("\n");
  Wire.beginTransmission(SLAVE_ADDRESS);   
  Wire.write("Jacky");                
  Wire.endTransmission();   
  delay(500);

  
  Serial.println("Requesting Data"); 
  Wire.requestFrom(SLAVE_ADDRESS, 5);

  int bytes = Wire.available();
  Serial.print("Slave sent ");
  Serial.print(bytes);
  Serial.print(" of information\n");
  for(int i = 0; i< bytes; i++)
  {
    x = Wire.read();
    Serial.print("Slave Sent: ");
    Serial.print(x);
    Serial.print("\n");
  }  
  delay(500);
}
