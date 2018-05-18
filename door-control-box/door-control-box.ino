//constants and libs
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <SPI.h>
#include <../../cJSON/cJSON.h>

SoftwareSerial COML0(10,11); //(Rx,Tx)

double env_conc.O2;
double env_conc.CO2;
double env_temp;
double env_pres;
int stringLength_required; //beware of global variables
char serialInput_raw[512]; //beware of global variables

void setup(){
 Serial.begin(9600);// begin physical uart comms via USB
 COML0.begin(9600);// begin logical serial port COML0 at pins above
}

void loop(){
    //conditioning string for the cJSON parser
    stringLength_required=stringReader(serialInput_raw[]);
    char serialInput_forParser[stringLength_required+1];
    strncpy
    // int stringLength_index=0;
    // for(stringLength_index<stringLength_required){ //copy string char by char
    //     serialInput_forParser[stringLength_index]=serialInput_forParser[stringLength_index];
    // }
    // serialInput_forParser[stringLength_index+1]='\0'; //string terminator with null

    
}

//self-defined functions

/* void stringReader(void)
    TAKES: reference to string stringInput of predetermined length
    RETURNS: number of bytes written to stringInput
    FUNCTION: reads a single data frame from serial, enclosed by start character frame_start and end character frame_end
*/
int stringReader(char stringInput[]){

    char COM_readChar;
    char frame_start="\a"
    char frame_end="\n"
    
    int readLength=0;
    int TRIGGER=0;//fuse function (?)
    
    //does blank reads from strim until alert character \a is found. fused so it runs at most once
    while(COM_readChar!=frame_start && TRIGGER!=1){
        COM_readChar=COML0.read(); //run continuously to discard from strim
        if(COM_readChar==frame_start){
            TRIGGER=1; //fuse if frame_start detected
            break;
        }
    }

    //read until end of frame
    while(COM_readChar!=frame_end){
        COM_readChar=COML0.read();
        stringInput[readLength]=COM_readChar;
        readLength++;
    }

    return readLength;
}