#ifndef SENSOR_BITMASK
    #error SENSOR_BITMASK is not defined - no messages i2c messages cannot be sent!
#endif

/**
 * Author: Thomas Richmond
 * Purpose: Interrupt method used to receive I2C data.
 */
void receiveData(int byteCount) {

    // NO CURRENT IMPLEMENTATIONS NEEDED
    Serial.println("receiving data");
    while(Wire.available())
    {
        int recieved_cmd = Wire.read();
        Serial.print("data received: ");
        Serial.println(recieved_cmd);
    }
}

/**
 * Author: Thomas Richmond
 */
void sendData(enum Procedure procedure) {
    I2CMessage_t* data = new I2CMessage_t();
    
    switch(procedure) {
        case GetSensorData:
            data->getSensorData.dataMask = SENSOR_BITMASK;
            data->getSensorData.o2 = LatestSensorValues::o2;
            data->getSensorData.humidity = LatestSensorValues::humidity;
            // DISALBED PRESSURE: Doesn't work over ~1.4 atm
            // data.getSensorData.pressure = LatestSensorValues::pressure;
            data->getSensorData.temperature = LatestSensorValues::temperature;
            data->getSensorData.co2 = LatestSensorValues::co2;
            break;
    }

    Wire.write((byte*) data ,sizeof(data));
    //for(int i =0; i< max_index; i++){
    //    Serial.println(send_bytes[i]);
    //}
}
