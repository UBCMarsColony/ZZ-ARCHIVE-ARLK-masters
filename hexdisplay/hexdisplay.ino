/*
 * TM1637.cpp
 * A library for the 4 digit display
 *
 * Copyright (c) 2012 seeed technology inc.
 * Website    : www.seeed.cc
 * Author     : Frankie.Chu
 * Create Time: 9 April,2012
 * Change Log :
 *
 * The MIT License (MIT)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include "TM1637.h"
#include <Wire.h>

#define SLAVE_ADDRESS 41
#define MSG_LEN 32

namespace Disp {
    // Params: CLK, DAT
    TM1637 o2(2, 3);
    TM1637 co2(4, 5);
    TM1637 pressure(6, 7);
    TM1637 temperature(8, 9);
}

typedef struct UpdateDisplay_t {
    byte action;
    byte procedure;
    byte priority;
    int16_t o2;
    int16_t co2;
    int16_t temperature;
    int16_t pressure;
};
volatile UpdateDisplay_t updateDisplay = UpdateDisplay_t();

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(onReceive);
//  initDisp(Disp::o2);
//  initDisp(Disp::co2);
  Disp::o2.init();
  Disp::o2.set(BRIGHT_TYPICAL);
  Disp::co2.init();
  Disp::co2.set(BRIGHT_TYPICAL);
  Disp::temperature.init();
  Disp::temperature.set(BRIGHT_TYPICAL);
  Disp::pressure.init();
  Disp::pressure.set(BRIGHT_TYPICAL);
  
  updateDisplay.o2 = 21;
  updateDisplay.co2 = 31;
  updateDisplay.temperature = 10;
  updateDisplay.pressure = 101;  
}

void loop() {
  displayWrite(Disp::o2, updateDisplay.o2);
  displayWrite(Disp::co2, updateDisplay.co2);
  displayWrite(Disp::temperature, updateDisplay.temperature);
  displayWrite(Disp::pressure, updateDisplay.pressure);

  delay(500);
}

void displayWrite(TM1637 disp, int16_t output) {
  int8_t NumTab[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};//0~9,A,b,C,d,E,F
  disp.display(0, NumTab[output / 1000 % 10]);
  disp.display(1, NumTab[output / 100 % 10]);
  disp.display(2, NumTab[output / 10 % 10]);
  disp.display(3, NumTab[output / 1 % 10]);
}

void onReceive(int firstByte) {
//    Serial.println("Received transmission from Master");
    byte data[MSG_LEN] = {};
    
    // Read the incoming message.
    for (int i = 0; Wire.available(); i++) {
        data[i] = Wire.read();
//        Serial.println(data[i]);
    }
        
//    if (data[1] % (1<<7) >= NumProcedures) {
//        Serial.println("CRITICAL ERROR: Received message of unknown type! This should never happen.");
//        return;
//    }
    // Run other checks if needed.
    
//    // Put message into the queue
    byte * p = (byte*) &updateDisplay;
    for (int i = 0; i < sizeof updateDisplay; i++)
        *p++ = data[i];
}


