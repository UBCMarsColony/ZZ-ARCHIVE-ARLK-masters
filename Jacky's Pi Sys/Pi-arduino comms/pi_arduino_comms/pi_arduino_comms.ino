#include <Wire.h>
#include <string.h>

#define SLAVE_ADDRESS 10
typedef unsigned char   BYTE;
int send_index;
int send_length;
BYTE recieved_cmd;

String send_string;
BYTE send_val;
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
    send_string = "Hello!";
    send_length = send_string.length();
    if(send_index >= send_length)   //resets the index and loops the msg
        send_index = 0;
    
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
