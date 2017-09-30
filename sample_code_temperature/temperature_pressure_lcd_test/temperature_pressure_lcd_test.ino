#include "SmallLCD.h"
  
#define READ_INTERVAL 250    // In milliseconds
#define SAMPLES         10    // Number of samples per reading
int tempPin= A0;
int pressurePin = A4;
float tempVolts;                       
float pressureVolts;                        
float celsius;
float pressure;
char  LCDstring[17];
float getAverageAnalog(int);
pinMode(7, OUTPUT);
digitalWrite(7,LOW);
pinMode(6, OUTPUT);
digitalWrite(6,LOW);

void setup() {
  Serial.begin(9600);
  LCD_4BIT();         // Initialize LCD
                      // NOTE: The following connections are hard-coded in the SmallLCD library, must be correctly connected
                      // Connections:           (Yellow)     (Green) (2k resistor) (Red) (Black)
                      //             Wires -   |  |  |  |    |  |  |       |         |      |    
                      //             Pins -   13 12 11 10    9 GND 8      GND       5V     GND
}

void loop() {
  tempVolts = getAverageAnalog(tempPin); 
  celsius= tempVolts*100 - 273.15;                // T = (Vout * 100)-273.15

  
  pressureVolts = getAverageAnalog(pressurePin);
  pressure = (pressureVolts+0.2)/0.02;                // P = (Vout + 0.2)/0.02 
  
  Serial.print("Temperature:");
  Serial.print(celsius);
  Serial.println(" degrees Celsius");
  Serial.print("Pressure: ");
  Serial.print(pressure);
  Serial.println(" kPA");
  Serial.println(" ");
  
  // NOTE: sprintf() on Arduino can't properly format floats, so this workaround below should display a float to 2 decimal places
  sprintf(LCDstring, "Temp: %d.%02dC", (int)celsius, (int)(celsius*100)%100);
  Serial.println(LCDstring);
  LCDprint(LCDstring, 1, true);
  sprintf(LCDstring, "Pres: %d.%02dkPA", (int)pressure, (int)(pressure*100)%100);
  Serial.println(LCDstring);
  LCDprint(LCDstring, 2, true);

  // Should expect to see:
  //  ________________________________
  // | T e m p :   x x . x C          |
  // | P r e s :   x x . x k P A      |
  //  --------------------------------
  
  delay(READ_INTERVAL);     // Wait READ_INTERVAL ms before taking another set of readings
}

// Function:    float getAverageAnalog(int pin)
// Parameters:  pin - analog pin number to read from
// Returns:     float - analog pin reading in volts, averaged from 'SAMPLES' number of readings

float getAverageAnalog(int pin){
  int i;
  float reading = 0;
  
  for( i = 0; i < SAMPLES; i++ )
    reading += analogRead(pin)*5.0/1024.0;    // Digital back to analog -> Analog voltage was originally mapped from 0-5V to range of 0-1023 
  reading /= SAMPLES;
  
  return reading;
}
