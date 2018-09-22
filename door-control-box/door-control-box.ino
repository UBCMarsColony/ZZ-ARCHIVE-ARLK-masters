//constants and libs
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <SPI.h>
#include <cJSON.h>

#define pin_RX 10
#define pin_TX 11

const int ID_device=46; //MUST BE IN HEX

typedef struct env;
struct env{
    double conc_O2;
    double conc_CO2;
    double temperature;
    double pressure;
    char door;
    char pump;
};

void setup(){
    Serial.begin(9600);
    Wire.begin(ID_device);
}

void loop(){
    Wire.onReceive(inputHandler);
}

void inputHandler(howMany){

}