#include <Wire.h>
#include <BaroSensor.h>

//getError - error codes from freetronics library
#define NO_ERR 0          //No error, sensor working fine
#define NACK_ADDRESS 2      //Received NACK on transmit of address (sensor may not be connected/powered properly.)
#define NACK_DATA           //Received NACK on transmit of data (sensor connections may not be good enough quality.)
#define WIRE_I2C_ERR 4      //Received NACK on transmit of data (sensor connections may not be good enough quality.)
#define NO_BEGINFCN -3         //begin() hasn't been called yet  
#define NO_READBACK_VAL -2  //Failed to read back values from sensor (sensor connections may not be good enough quality.)

void setup()
{
  Serial.begin(9600);
  BaroSensor.begin();
}

void loop()
{
  double temp;
  double pressure;
  
  //Check if sensor is working properly
  if(!BaroSensor.isOK()) {
    return BaroSensor.getError();
    BaroSensor.begin(); // Try to reinitialise the sensor if we can
  }
  
  else {
    BaroSensor.getTempAndPressure(&temp, &pressure);
    
    //Error checking:
    //Temp range of sensor: -40 to +85 degrees celcius
    if(temp <-40 || temp >85){
      return -555;
    }
    else { 
      return temp;
    }
   
    //Error checking:
    //Pressure range of sensor: 10 to 2000 mbar
    if(pressure <10 || pressure >2000){
      return -555;
    }
    else {
      return pressure;
    }
  }
  delay(1000);
}
