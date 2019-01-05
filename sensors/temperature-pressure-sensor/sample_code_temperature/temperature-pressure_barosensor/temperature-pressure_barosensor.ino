#include <Wire.h>
#include <BaroSensor.h>
#include <EEPROM.h>

//getError - error codes from freetronics library
#define NO_ERR 0          //No error, sensor working fine
#define NACK_ADDRESS 2      //Received NACK on transmit of address (sensor may not be connected/powered properly.)
#define NACK_DATA           //Received NACK on transmit of data (sensor connections may not be good enough quality.)
#define WIRE_I2C_ERR 4      //Received NACK on transmit of data (sensor connections may not be good enough quality.)
#define NO_BEGINFCN -3         //begin() hasn't been called yet  
#define NO_READBACK_VAL -2  //Failed to read back values from sensor (sensor connections may not be good enough quality.)

int address = 0;  
double value;
int count = 0;

void setup()
{
  Serial.begin(9600);
  BaroSensor.begin();
}

void loop()
{
  double temp;
  double pressure;

  delay (300000);

  //Check if sensor is working properly
  if(!BaroSensor.isOK()) {
    Serial.println("Error");
    BaroSensor.begin(); // Try to reinitialise the sensor if we can
  }
  
  else {
    while (count < 30) {
       Serial.println("currently collecting data");
       temp=BaroSensor.getTemperature();
       pressure=BaroSensor.getPressure();
    
      //Error checking:
      //Temp range of sensor: -40 to +85 degrees celcius
      if(temp < -40 || temp > 85){
      Serial.println(-556);
      }
      else { 
        EEPROM.write(address, pressure/8);
        value = EEPROM.read(address)*0.8;
        Serial.println(value);
        address++;
      }
   
      //Error checking:
      //Pressure range of sensor: 10 to 2000 mbar
      if(pressure < 10 || pressure > 2000){
        Serial.println(-500);
      }
      else {
        EEPROM.write(address, temp);
        value = EEPROM.read(address);
        Serial.println(value);
      address++;
      }

      if (address == EEPROM.length())
        address = 0;

      count++;
      delay(1000);
    }
  }

  delay(1000);

}
