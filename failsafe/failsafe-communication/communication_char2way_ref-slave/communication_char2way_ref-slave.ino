//Slave Arduino recieving "Jacky" from Master and Writing "Jiang"

#include <Wire.h>


#define SLAVE_ADDRESS 1
char x = ' ';
char string[]="";
void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}

void loop()
{
  delay(100);
}

void requestEvent() 
{
  Serial.print("Request from Master. Sending: ");
  Serial.print("Jiang");
  Serial.print("\n");

  Wire.write("Jiang");
}

void receiveEvent(int bytes)
{
  if(Wire.available() != 0)
  {
    for(int i = 0; i< bytes; i++)
    {
      x = Wire.read();
      Serial.print("Received: ");
      Serial.print(x);
      Serial.print("\n");
    }
  }
}
