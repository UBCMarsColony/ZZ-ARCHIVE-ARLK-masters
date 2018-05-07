#include "SoftwareSerial.h"
#include "string.h"
SoftwareSerial O2_Serial(8,9); //Software Serial port with pin 8 as Rx
                            //and pin 9 as Tx
#define SIZE 100
#define maxval 6
//Setup is all good
void sendchar(char);
char* printbytes(char bytes[]);
char* get_temp(char bytes[]);
char response [100];
char value[maxval];

void setup()
{
    //Initial setup
    Serial.begin(9600);
    O2_Serial.begin(9600);

}
void loop(){
    char* buffer;
    char* subbuffer;
    char O2_string[10];
    char temperature_string[10];
    char humidity_string[10];
    char pressure_string[10];
    float O2_percentage;
    float temperature_celsius;
    float humidity_percentage;
    float pressure_kpa;
    

        sendchar('Z'); //O2 gas: 20030 -> 20.030 % , or 200300 ppm 

    delay(2000);
    return_char();
    buffer=printbytes(response);
    O2_percentage = atof(buffer)/1000;
    dtostrf(O2_percentage,5,2,O2_string);
    Serial.println(O2_string);


        sendchar('T'); //Temperature: 01255 -> 25.5 degrees celcius

    delay(2000);
    return_char();
    buffer=get_temp(response);
    temperature_celsius = atof(buffer)/1000;
    dtostrf(temperature_celsius,5,2,temperature_string);
    Serial.println(temperature_string);

        sendchar('H'); //Relative humidity in tenths of percent
                        // 00427 -> 42.7 %  (double check)

    delay(2000);
    return_char();
    buffer=printbytes(response);
    humidity_percentage = atof(buffer)/10;
    dtostrf(humidity_percentage, 5, 2, humidity_string);
    Serial.println(humidity_string);

        sendchar('B'); //Pressure: 01011 -> 101.1 kpa 

    delay(2000);
    return_char();
    buffer=printbytes(response);
    pressure_kpa = atof(buffer)/10;
    dtostrf(pressure_kpa, 5,1,pressure_string);
    Serial.println(pressure_string);
    
    
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

char* printbytes(char bytes[]){
    
        for(int j = 2; j < 7; j++){
            value[j-2] = bytes [j];
        }      
    return value;
}

char* get_temp(char bytes[]){
    for(int i = 4; i < 7; i++){
        value[i-4] = bytes [i];
    }
    return value;
}