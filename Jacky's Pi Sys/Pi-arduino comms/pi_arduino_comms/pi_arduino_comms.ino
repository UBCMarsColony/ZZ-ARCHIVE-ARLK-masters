#include <Wire.h>
#include <string.h>

#define SLAVE_ADDRESS 10
typedef unsigned char   BYTE;
int send_index;
int send_length;
BYTE recieved_cmd;

String send_string;
BYTE send_val;

int test_CO2 = 100;
int test_O2 = 10;
int test_temp = 0;
int test_pressure = 50;
void setup()
{
    Serial.begin(9600); // start serial for output
    Wire.begin(SLAVE_ADDRESS); // initialize i2c as slave

    /* define callbacks for i2c communication*/
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    send_index = 0; //Initialize the index for I2C sending strings
    send_length = 0; //Initialize length of I2C send string
    recieved_cmd = byte(0); //initialized the I2C recieved cmd byte

    Serial.println("Ready!");

}
void loop()
{   
    send_string = "{\"CO2\":" + String(test_CO2) +", \"O2\":"+String(test_O2)+",\"Temperature\":"+String(test_temp)+", \"Pressure\":"+String(test_pressure)+"}";
    send_length = send_string.length();
    Serial.println(send_length);
    Serial.print("index: ");
    Serial.println(send_index);
    if(send_index >= send_length)   //resets the index and loops the msg
        send_index = 0;
    //test_CO2 += 20;
    test_O2 += 1;
    //test_temp += 10;
    //test_pressure += 30;    
    delay(1000);
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
