#include <Wire.h>

#define SLAVE_ADDRESS 0x05

// Bitmask: O2 | Humidity | Temperature | Pressure ✔ | CO2 | ? | ? | ? 
#define SENSOR_BITMASK 0b00010000

void setup() {
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    // STUB
}

void loop() {
    // STUB
}

