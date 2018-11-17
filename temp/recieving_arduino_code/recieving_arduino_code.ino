#include <Wire.h>

void setup()
{
  Wire.begin(15); 
  Serial.begin(9600);
  Wire.onReceive(receiveEvent); 

}

String data = "";

void loop()
{
delay(100);
sendMessage();
}

void receiveEvent(int howMany)
{
  data = "";
  while( Wire.available()){
    data += (char)Wire.read();
    Serial.println(data);
  }
}
void sendMessage()
 {
  Wire.beginTransmission(A2);
  Wire.write("test ");
  Wire.endTransmission();
  delay(100);
 }
