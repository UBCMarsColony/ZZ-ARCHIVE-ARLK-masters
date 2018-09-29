#include "SoftwareSerial.h"
#include "string.h"
#include <EEPROM.h>
#include <Wire.h>

SoftwareSerial K_30_Serial(12,13);  //Sets up a virtual serial port
                                    //Using pin 12 for Rx and pin 13 for Tx
SoftwareSerial O2_Serial(8,9); //Software Serial port with pin 8 as Rx
                            //and pin 9 as Tx
#define SIZE 100
#define strsize 10
#define maxval 6
//Setup is all good
#define SLAVE_ADDRESS 10
typedef unsigned char   BYTE;
int send_index;
int send_length;
BYTE recieved_cmd;

String send_string;
BYTE send_val;
int transmission_size = 6;

byte readCO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};  //Command packet to read Co2 (see app note)
byte response[] = {0,0,0,0,0,0,0};  //create an array to store the response

//multiplier for value. default is 1. set to 3 for K-30 3% and 10 for K-33 ICB
int valMultiplier = 1;
char response_O2 [SIZE];
char value[maxval];
int count = 0;

char O2_string[strsize];
char temperature_string[strsize];
char humidity_string[strsize];
char pressure_string[strsize];
char CO2_string[strsize];

String  O2;
String  temperature;
String  humidity;
String  pressure;
String  CO2;




void setup()
{
    //Initial setup
    count = 0;
    Serial.begin(9600);
    O2_Serial.begin(9600);
    K_30_Serial.begin(9600);    //Opens the virtual serial port with a baud of 9600

    Wire.begin(SLAVE_ADDRESS); // initialize i2c as slave

    /* define callbacks for i2c communication*/
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    send_index = 0; //Initialize the index for I2C sending strings
    send_length = 0; //Initialize length of I2C send string
    recieved_cmd = byte(0); //initialized the I2C recieved cmd byte

    Serial.println("Setup Complete");
}
void loop(){
    if( count > 2){
        poll_all();
        count += 1;
        if(count > 3){
            EEPROM_readall(4);
        }
    }
    else{
        Serial.println("Please wait...");
        count += 1;
        delay(1000);
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
    O2_Serial.listen();

    get_O2();
    Serial.print("Oxygen: ");
    Serial.print(O2_string);
    Serial.print(" % \n");  
    EEPROMstore(0, O2_string, strsize);
    O2 = String(O2_string);

    get_Temp();
    Serial.print("Temperature: ");
    Serial.print(temperature_string);
    Serial.print(" C \n");
    EEPROMstore(1, temperature_string, strsize);
    temperature = String(temperature_string);

    get_Humidity();
    Serial.print("Humidity: ");
    Serial.print(humidity_string);
    Serial.print(" % \n");
    EEPROMstore(2, humidity_string, strsize);
    humidity = String(humidity_string);

    get_Pressure();
    Serial.print("Pressure: ");
    Serial.print(pressure_string);
    Serial.print(" KPa \n");
    EEPROMstore(3, pressure_string, strsize);
    pressure = String(pressure_string);

         K_30_Serial.listen();
         delay(2000);
         sendRequest(readCO2);
         unsigned long valCO2 = getValue(response);
         dtostrf(valCO2,3,0,CO2_string);
         Serial.print("CO2: ");
         Serial.print(CO2_string);
         Serial.print(" ppm \n");
         EEPROMstore(4, CO2_string, strsize);
         CO2 = String(CO2_string);
         

    Serial.println("_________________________");

    String c = format_for_transmission(CO2,transmission_size);
    String o = format_for_transmission(O2,transmission_size);
    String t = format_for_transmission(temperature,transmission_size);
    String p = format_for_transmission(pressure,transmission_size);
    String h = format_for_transmission(humidity,transmission_size);

    send_string = "{\"CO2\":\"" + c +"\",\"O2\":\""+ o +"\",\"temperature\":\""+ t +"\",\"pressure\":\""+p+"\",\"humidity\":\"" + h + "\"}";
    //Serial.println(send_string);
    send_length = send_string.length();     //This value is 64
    Serial.println(send_length);
    //Serial.print("index: ");
    //Serial.println(send_index);
    Serial.print("Python Dict:\t");
    Serial.println(send_string);
    if(send_index >= send_length)   //resets the index and loops the msg
        send_index = 0;  
    delay(1000);
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

bool EEPROMstore(int t, char str[], int size){
    for (int i = size*t; i < size*(t+1); i++){
        EEPROM.write(i, str[i-size*t]);
        //Serial.print("EEPROM written to address:\t");
        //Serial.println(i);
    }
    return true;
}

bool EEPROM_readall(int t){
    int value;
    for(int l = 0; l <= t; l++){
        switch(l){
            case 0:
                Serial.print("O2: ");
                break;
            case 1:
                Serial.print("Temperature: ");
                break;
            case 2:
                Serial.print("Humidity: ");
                break;
            case 3:
                Serial.print("Pressure: ");
                break;
            case 4:
                Serial.print("CO2: ");
        }
        for (int i = strsize*l; i < strsize*(l+1); i++){
            value = EEPROM.read(i);
            Serial.print(char(value));
        }
        switch(l){
            case 0:
                Serial.println("%");
                break;
            case 1:
                Serial.println("C");
                break;
            case 2:
                Serial.println("%");
                break;
            case 3:
                Serial.println("Kpa");
                break;
            case 4:
                Serial.print("ppm");
        }
    Serial.println();
    Serial.println("_____________________");
    delay(500);
    }
}


String format_for_transmission(String input, int size){
    String i = input;
    int val = i.length();

    while(val < size){
        i = "0"+i ;
        val = i.length();
    }

    if(val > size){
        i = "ERROR:" + i;
    }
    return i;
}

void receiveData(int byteCount)
{
    Serial.println("receiving data");
    while(Wire.available())
    {
        recieved_cmd = Wire.read();
        Serial.print("data received: ");
        Serial.println(recieved_cmd);
    }
}

// callback for sending data
void sendData()
{
    send_val = byte(send_string[send_index]);
    Wire.write(send_val);     
    send_index++; 
}
