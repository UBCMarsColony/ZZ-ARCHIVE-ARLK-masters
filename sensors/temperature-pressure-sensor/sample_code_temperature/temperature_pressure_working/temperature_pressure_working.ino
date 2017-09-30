#define READ_INTERVAL 1000    // In milliseconds
#define SAMPLES         10    // Number of samples per reading
int tempPin= A0;
int pressurePin = A4;
float tempVolts;                       
float pressureVolts;                        
float celsius;
float pressure;

float getAverageAnalog(int);

void setup() {
  Serial.begin(9600);
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
