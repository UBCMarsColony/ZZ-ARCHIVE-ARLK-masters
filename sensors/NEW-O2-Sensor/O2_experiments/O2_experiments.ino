#include "SoftwareSerial.h"

SoftwareSerial O2_Serial(8,9); //Software Serial port with pin 8 as Rx
                            //and pin 9 as Tx
#define SIZE 100

//Setup is all good
void sendchar(char);
char response [100];

void setup()
{
    //Initial setup
    Serial.begin(9600);
    O2_Serial.begin(9600);

}
void loop(){
        sendchar('Z'); //O2 gas: 20030 -> 20.030 % (? double check)

    delay(2000);
    return_char();
    Serial.println(response);

        sendchar('T'); //Temperature: 01255 -> 25.5 degrees celcius

    delay(2000);
    return_char();
    Serial.println(response);

        sendchar('H'); //Relative humidity in tenths of percent
                        // 00427 -> 42.7 %  (double check)

    delay(2000);
    return_char();
    Serial.println(response);

        sendchar('B'); //Pressure: 01011 -> 101.1 kpa (?)

    delay(2000);
    return_char();
    Serial.println(response);
    
}

void sendchar(char letter){
    O2_Serial.println(letter); //USE for carriage return and line feed in addition to letter
}


void return_char(void){
    int index = 0;
    int i =0;

    Serial.print("Number of Bytes available:");
    Serial.print(O2_Serial.available());
    Serial.print("\n");
    while(O2_Serial.available()>0){
        response [i++] = O2_Serial.read();
    }

}
