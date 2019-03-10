/** DATASHEETS
 * O2 Sensor Controller Manual: http://co2meters.com/Documentation/Manuals/Manual-EC200-Sensors%20rev%20P%20TMP.pdf
 * CO2 Sensor UART Interface Manual: http://www.co2meters.com/Documentation/AppNotes/AN126-K3x-sensor-arduino-uart.pdf
 */

#include "SoftwareSerial.h"
#include <EEPROM.h>
#include <Wire.h>

#define SLAVE_ADDRESS 10
#define LOOP_DELAY 1500
#define SENSOR_TIMEOUT 10000

// Bitmask: O2 ✔ | Humidity ✔ | Temperature ✔ | Pressure | CO2 ✔ | ? | ? | ? 
#define SENSOR_BITMASK 0b11101000

enum Procedure {
    GetSensorData = 1
};

enum SensorCommand {
    GET_FILTERED_GAS_CONC   = 'Z',
    GET_TEMPERATURE         = 'T',
    GET_RELATIVE_HUMIDITY   = 'H',
    GET_BAROM_PRESSURE      = 'B'
};

const byte GET_CO2_CONC[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};

typedef struct Header_t {
    byte action;
    byte procedure;
    byte priority;
};

typedef struct GetSensorData_t {
    Header_t header;
    uint8_t  dataMask;      // Valid data bitmask (See #defines)
    uint8_t  o2;            // Oxygen, in percent
    uint8_t humidity;       // Humidity, in percent
    int16_t temperature;    // Temperature, in degrees Celsius
    uint16_t pressure;      // Barometric pressure, in dekaPascals.
    uint16_t co2;           // CO2, in parts per million
};

typedef union I2CMessage_t {
    GetSensorData_t getSensorData;
};

//multiplier for K30 CO2 read value. Default is 1. Set to 3 for K-30 3% and 10 for K-33 ICB
#define K_30_MULTIPLIER 1

// SoftwareSerial pins are used to interface 
// with the sensors over UART.
SoftwareSerial K_30_Serial(12, 13);
SoftwareSerial O2_Serial(8, 9);

// byte readCO2[7] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25};  //Command packet to read Co2 (see app note)
// byte response[7] = {0};  //create an array to store the response


namespace LatestSensorValues {
    uint8_t o2;             // Oxygen, in percent
    uint8_t humidity;       // Humidity, in percent
    int16_t temperature;    // Temperature, in degrees Celsius
    uint16_t pressure;      // Barometric pressure, in dekaPascals. 
    uint16_t co2;           // CO2, in parts per million
}

void setup() {
    Serial.begin(9600);         // Open Serial Debugging Port
    O2_Serial.begin(9600);      // Open O2 Comm Port
    K_30_Serial.begin(9600);    // Open CO2 Comm Port

    Wire.begin(SLAVE_ADDRESS); // initialize i2c as slave
    Serial.print("ADDRESS:");
    Serial.println(SLAVE_ADDRESS);
    /* define callbacks for i2c communication*/
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    // send_index = 0; //Initialize the index for I2C sending strings
    // send_length = 0; //Initialize length of I2C send string
    // recieved_cmd = byte(0); //initialized the I2C recieved cmd byte
    Serial.println("Setup Complete");
}

void loop() {
    static unsigned long lastTime = 0;

    if (millis() - lastTime > LOOP_DELAY) {
        //Serial.print("Input:\t");
        //Serial.println(analogRead(A0)*5.0/1023);
        Serial.println("Polling");
        pollAll();
        lastTime = millis();
        // if(count > 3){
            //EEPROM_readall(4);
        // }
    }
}

void pollAll(void){
    O2_Serial.listen();
    delay(100);
    
    Serial.print("O2: ");
    LatestSensorValues::o2 = getO2();
    Serial.println(LatestSensorValues::o2);

    Serial.print("Humidity: ");
    LatestSensorValues::humidity = getHumidity();
    Serial.println(LatestSensorValues::humidity);

    Serial.print("Temp: ");
    LatestSensorValues::temperature = getTemp();
    Serial.println(LatestSensorValues::temperature);

//    LatestSensorValues::pressure = getPressure();

    // CO2
    K_30_Serial.listen();
    delay(100);

//    Serial.print("CO2: ");
//    LatestSensorValues::co2 = getCO2();
//    Serial.println(LatestSensorValues::co2);

    Serial.println("-------------");

}

uint8_t getO2(void) {
    byte response[7] = {0};
    getSerialSensorDataO2(response, sizeof response, GET_FILTERED_GAS_CONC);

    //O2 gas: 20030 -> 20.030 % , or 200300 ppm
    uint16_t processedO2 = 0;
    for (int i = 2; i < 7; i++) {  // Parse digits as byte
        Serial.println((char)response[i]);// - '0'));
        processedO2 = (processedO2 + (response[i] - '0')) * 10;
    }
    return processedO2 / 1000;
    // O2_percentage = atof(buffer)/1000;
    // dtostrf(O2_percentage,5,2,O2_string);

}

int16_t getTemp(void) {
    byte response[7] = {0};
    getSerialSensorDataO2(response, sizeof response, GET_TEMPERATURE);

    //Temperature: 01255 -> 25.5 degrees celcius
    int16_t processedTemp = 0;
    for (int i = 2; i < 7; i++)  // Parse digits as byte
        processedTemp = (processedTemp + (response[i] - '0')) * 10;

    return processedTemp;
    // temperature_celsius = atof(buffer)/1000;
    // dtostrf(temperature_celsius,5,2,temperature_string);
}

uint8_t getHumidity(void) {
    byte response[7] = {0};
    getSerialSensorDataO2(response, sizeof response, GET_RELATIVE_HUMIDITY);

    uint8_t processedHumidity = 0;
    for (int i = 2; i < 7; i++)  // Parse digits as byte
        processedHumidity = (processedHumidity + (response[i] - '0')) * 10;
    
    return processedHumidity / 10;
}

uint16_t getPressure(void) {
    byte response[7] = {0};
    getSerialSensorDataO2(response, sizeof response, GET_FILTERED_GAS_CONC);

    // Pressure: 01011 -> 101.1 kpa == 1011 hPA 
    uint16_t processedPressure = 0;
    for (int i = 2; i < 7; i++)  // Parse digits as byte
        processedPressure = (processedPressure + (response[i] - '0')) * 10;
    
    return processedPressure;
    // pressure_kpa = atof(buffer)/10;
    // dtostrf(pressure_kpa, 5,1,pressure_string);
}

uint16_t getCO2() {
    byte response[7] = {0};
    getSerialSensorDataCO2(response, sizeof response, GET_CO2_CONC);

    // See K-30 documentation to see why this is done.
    int high = response[1]; //high byte for value is 4th byte in the response (or 2nd here, due to truncation)
    int low = response[2]; //low byte for value is 5th byte in the response (or 3rd here, due to truncation)

    return ((high * 256) + low) * K_30_MULTIPLIER;
}

/* Purpose: Sends a command over Serial to a sensor module and reads the data
 * returned by the module in the format 'X 0123<cr><lf>', where we
 * care about the digits found in indeces 2-6 (our value of interest)
 * Param: target - A four-byte array in which to store the result of the function call
 * Param: ser - SoftwareSerial object to use
 * Param: command - Character command to send over serial. Valid commands are specified
 *                  in the SensorCommands enum
 */
int getSerialSensorDataCO2(char buffer[], int length, byte command[7]) {
    //stub;
    return 0;
}

/* Overloaded funciton definition which takes in an array instead of a single value.
 */
int getSerialSensorDataO2(byte buffer[], int length, char command) {
    Serial.println("START");
    O2_Serial.println(command);
    
    long startTime = millis();
    while(!O2_Serial.available()) {
        if(millis() - startTime > SENSOR_TIMEOUT) {
            Serial.println("SENSOR TIMEOUT!");
            return 1;
        }
    }
    delay(100);

    for (int i = 0; O2_Serial.available(); i++) {
        buffer[i++] = O2_Serial.read();
        Serial.print((char)buffer[i - 1]);
        Serial.print(" ");    
    }
    Serial.println();
    
    return 0;
}

