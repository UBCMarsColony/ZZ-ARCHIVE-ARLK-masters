//constants and libs
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <SPI.h>
#include <cJSON.h>
#include <interrupt.h>

//slave address
const int ID_device=46; //MUST BE IN HEX

typedef struct pinNumber{
    int pin_RX=10;
    int pin_TX=11;
    int pin_button_open=5;
    int pin_button_close=6;
    int pin_button_stop=7;
} pin;

typedef struct envStatus{
    double conc_O2;
    double conc_CO2;
    double temperature;
    double pressure;
    char status_door;
    char status_pump;
} env;

void setup(){
    cli();//clear interrupts

    PCICR=0; //clear pin change interrupt control
    PCIFR=0; //clear pin change interrupt flags

    sei();//set interrupts

    Serial.begin(9600);
    Wire.begin(ID_device);
    Wire.onReceive(inputHandler);
}

void loop(){

}

//handler for Wire.requestFrom(address,bytes,stop) from master:
//what should be the reply if master requests data?
void inputHandler(howMany){

}