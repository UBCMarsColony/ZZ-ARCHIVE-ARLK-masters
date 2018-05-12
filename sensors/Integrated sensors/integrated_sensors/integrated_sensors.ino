#include "SoftwareSerial.h"
#include "string.h"

SoftwareSerial K_30_Serial(12,13);  //Sets up a virtual serial port
                                    //Using pin 12 for Rx and pin 13 for Tx
SoftwareSerial O2_Serial(8,9); //Software Serial port with pin 8 as Rx
                            //and pin 9 as Tx
#define SIZE 100
#define maxval 6
//Setup is all good

byte readCO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};  //Command packet to read Co2 (see app note)
byte response[] = {0,0,0,0,0,0,0};  //create an array to store the response

//multiplier for value. default is 1. set to 3 for K-30 3% and 10 for K-33 ICB
int valMultiplier = 1;
char response_O2 [100];
char value[maxval];
int count = 0;
char O2_string[10];
char temperature_string[10];
char humidity_string[10];
char pressure_string[10];

void setup()
{
    //Initial setup
    count = 0;
    Serial.begin(9600);
    O2_Serial.begin(9600);
    K_30_Serial.begin(9600);    //Opens the virtual serial port with a baud of 9600

}
void loop(){
    if( count > 1){
        O2_Serial.listen();
        poll_all();

         K_30_Serial.listen();
         sendRequest(readCO2);
         unsigned long valCO2 = getValue(response);
         Serial.print("Co2 ppm = ");
         Serial.println(valCO2);
         delay(2000);

    }
    else{
        Serial.println("Please wait...");
        count += 1;
    }

}
void sendRequest(byte packet[])
{
  while(!K_30_Serial.available())  //keep sending request until we start to get a response
  {
    K_30_Serial.write(readCO2,7);
    delay(50);
  }
  
  int timeout=0;  //set a timeoute counter
  while(K_30_Serial.available() < 7 ) //Wait to get a 7 byte response
  {
    timeout++;  
    if(timeout > 10)    //if it takes to long there was probably an error
      {
        while(K_30_Serial.available())  //flush whatever we have
          K_30_Serial.read();
          
          break;                        //exit and try again
      }
      delay(50);
  }
  
  for (int i=0; i < 7; i++)
  {
    response[i] = K_30_Serial.read();
  }  
}

unsigned long getValue(byte packet[])
{
    int high = packet[3];                        //high byte for value is 4th byte in packet in the packet
    int low = packet[4];                         //low byte for value is 5th byte in the packet

  
    unsigned long val = high*256 + low;                //Combine high byte and low byte with this formula to get value
    return val* valMultiplier;
}


void poll_all(void){
    get_O2();
    Serial.print("Oxygen: ");
    Serial.print(O2_string);
    Serial.print(" % \n");  

    get_Temp();
    Serial.print("Temperature: ");
    Serial.print(temperature_string);
    Serial.print(" C \n");

    get_Humidity();
    Serial.print("Humidity: ");
    Serial.print(humidity_string);
    Serial.print(" % \n");

    get_Pressure();
    Serial.print("Pressure: ");
    Serial.print(pressure_string);
    Serial.print(" KPa \n");

    Serial.println("_________________________");
}

void get_O2(void){
    float O2_percentage;
    char* buffer;
        sendchar('Z'); //O2 gas: 20030 -> 20.030 % , or 200300 ppm 

    delay(2000);
    return_char();
    buffer=printbytes(response_O2);
    O2_percentage = atof(buffer)/1000;
    dtostrf(O2_percentage,5,2,O2_string);
    //return O2_string;
}

void get_Temp(void){
    float temperature_celsius;
    char* buffer;
    
        sendchar('T'); //Temperature: 01255 -> 25.5 degrees celcius

    delay(2000);
    return_char();
    buffer=byte_temp(response_O2);
    temperature_celsius = atof(buffer)/1000;
    dtostrf(temperature_celsius,5,2,temperature_string);
}
void get_Humidity(void){
    float humidity_percentage;
    char* buffer;

        sendchar('H'); //Relative humidity in tenths of percent
                        // 00427 -> 42.7 %  (double check)

    delay(2000);
    return_char();
    buffer=printbytes(response_O2);
    humidity_percentage = atof(buffer)/10;
    dtostrf(humidity_percentage, 5, 2, humidity_string);
}

void get_Pressure(void){
    float pressure_kpa;
    char* buffer;

       sendchar('B'); //Pressure: 01011 -> 101.1 kpa 

    delay(2000);
    return_char();
    buffer=printbytes(response_O2);
    pressure_kpa = atof(buffer)/10;
    dtostrf(pressure_kpa, 5,1,pressure_string);

}

void sendchar(char letter){
    O2_Serial.println(letter); //USE for carriage return and line feed in addition to letter
}


void return_char(void){
    int index = 0;
    int i =0;
    /*
    Serial.print("Number of Bytes available:");
    Serial.print(O2_Serial.available());
    Serial.print("\n");
    */
    while(O2_Serial.available()>0){
        response_O2 [i++] = O2_Serial.read();
    }

}

char* printbytes(char bytes[]){
    
        for(int j = 2; j < 7; j++){
            value[j-2] = bytes [j];
        }      
    return value;
}

char* byte_temp(char bytes[]){
    for(int i = 4; i < 7; i++){
        value[i-4] = bytes [i];
    }
    return value;
}