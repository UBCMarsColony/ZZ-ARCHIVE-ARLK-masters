#include <Wire.h>
#include <string.h>

#define SLAVE_ADDRESS 10
typedef unsigned char   BYTE;
int number = 0;
int state = 0;

bool ready_flag = false;
String send_string;
BYTE send_val;
void setup()
{
    //Serial.begin(9600);
    //Wire.begin(addr);

    pinMode(13, OUTPUT);
    pinMode(7, OUTPUT);
    Serial.begin(9600); // start serial for output
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");

}
void loop()
{   BYTE c;
    send_string = "There, out in the darkness, a fuggggitive running, fallen from God";
    //ready_flag = false;
    delay(100);

//TESTING, not needed for actual program
    String ttt = "hello, my name is elder cummingham!";
    BYTE send_byte;
    int len = ttt.length();

    for(int i = 0;  i < len ; i++){
        send_byte = byte(ttt[i]);
        Serial.println(ttt[i]);
        Serial.print(send_byte);
    }
    /*      THE INITIAL "ECHO" CODE
    // send data only when you receive data:
    if (Serial.available() > 0) {
            // read the incoming byte:
            c = Serial.read();

            // say what you got:
            Serial.print("I received: ");
            Serial.println(c, DEC);
    }
    if(c){
        send_val = byte(c);
        ready_flag = true;
        Serial.print("The byte value is");
        Serial.println((char)send_val);
    }
    */


    delay(1000);
}

void receiveData(int byteCount)
{
    while(Wire.available())
    {
        number = Wire.read();
        Serial.print("data received: ");
        Serial.println(number);
        /*
        if (number == 1)
        {
            if (state == 0)
            {
            digitalWrite(13, HIGH); // set the LED on
            state = 1;
            }
            else
            {
            digitalWrite(13, LOW); // set the LED off
            state = 0;
            }
        }
        */
    }
}

// callback for sending data
void sendData()
{
    //Wire.write(send_string);      //send entire string option
    //BYTE BY BYTE OPTION
    BYTE send_byte;
    int len = send_string.length();

    for(int i = 0;  i < len ; i++){
        send_byte = send_string[i];
        Serial.println(send_byte);
        Wire.write(send_byte);
    }
    //Wire.write(number);      
}
