#include <Wire.h>
#include <string.h>

#define SLAVE_ADDRESS 10
typedef unsigned char   BYTE;
int send_index;
int send_length;
BYTE recieved_cmd;

String send_string;
BYTE send_val;
int transmission_size = 4;

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
    
    String c = format_for_transmission(test_CO2,transmission_size);
    String o = format_for_transmission(test_O2,transmission_size);
    String t = format_for_transmission(test_temp,transmission_size);
    String p = format_for_transmission(test_pressure,transmission_size);


    send_string = "{\"CO2\":\"" + c +"\",\"O2\":\""+ o +"\",\"Temperature\":\""+ t +"\",\"Pressure\":\""+p+"\"}";
    //Serial.println(send_string);
    send_length = send_string.length();     //This value is 64
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

String format_for_transmission(int input, int size){
    String i = String(input);
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
