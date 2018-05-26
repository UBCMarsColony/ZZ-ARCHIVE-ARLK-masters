//constants and libs
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>
#include <SPI.h>
//#include <../../cJSON/cJSON.h>

//SoftwareSerial COML0(10,11); //(Rx,Tx)

double env_conc_O2;
double env_conc_CO2;
double env_temp;
double env_pres;

void setup(){
Serial.begin(9600);// begin physical uart comms via USB
COML0.begin(9600);// begin logical serial port COML0 at pins above
}

void loop(){
    //conditioning string for the cJSON parser
    //stringLength_required=stringReader(serialInput_raw[]);
    Serial.println("Program start!");
    // set vars
    int stringLength_index=0;
    int stringLength_required; //beware of global variables
    char serialInput_raw[1024]="{\"title\":\"Person\",\"type\":\"object\",\"properties\":{\"firstName\":{\"type\":\"string\"},\"lastName\":{\"type\":\"string\"},\"age\":{\"description\":\"Age in years\",\"type\":\"integer\",\"minimum\": 0}},\"required\":[\"firstName\", \"lastName\"]}";

    Serial.print("JSON string to be decoded is: ");
    Serial.println(serialInput_raw);

    stringLength_required=strlen(serialInput_raw);

    char serialInput_forParser[stringLength_required+1];

    for(stringLength_index=0;stringLength_index<stringLength_required;stringLength_index++){ //copy string char by char
        serialInput_forParser[stringLength_index]=serialInput_raw[stringLength_index];
    }
    serialInput_forParser[stringLength_index+1]='\0'; //string terminator with null
    
    Serial.print("JSON string on smaller array is: ");
    Serial.println("serialInput_forParser");
    
    delay(1000);

}

//self-defined functions

/* void stringReader(void)
    TAKES: reference to string stringInput of predetermined length
    RETURNS: number of bytes written to stringInput
    FUNCTION: reads a single data frame from serial, enclosed by start character frame_start and end character frame_end
*/
// int stringReader(char stringInput[]){

//     char COM_readChar;
//     char frame_start="\a";
//     char frame_end="\n";
    
//     int readLength=0;
//     int TRIGGER=0;//fuse function (?)
    
//     //does blank reads from strim until alert character \a is found. fused so it runs at most once
//     while(COM_readChar!=frame_start && TRIGGER!=1){
//         COM_readChar=COML0.read(); //run continuously to discard from strim
//         if(COM_readChar==frame_start){
//             TRIGGER=1; //fuse if frame_start detected
//             break;
//         }
//     }

//     //read until end of frame
//     while(COM_readChar!=frame_end){
//         COM_readChar=COML0.read();
//         stringInput[readLength]=COM_readChar;
//         readLength++;
//     }

//     return readLength;
// }