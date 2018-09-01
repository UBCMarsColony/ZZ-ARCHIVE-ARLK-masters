const int sensorAddress = A0;

void setup(){
    Serial.begin(9600);
}

void loop(){
    getTemperature(sensorAddress);
    delay(500);
}


double getTemperature(int sensorAddress){
    double voltageRaw=analogRead(sensorAddress)*5/1024.0;

    Serial.print(voltageRaw);
    Serial.println(" volts");

    double temperature=(voltageRaw-0.5)*100; //sensor offset inbuilt

    Serial.print(temperature);
    Serial.println(" degrees Celsius");
}