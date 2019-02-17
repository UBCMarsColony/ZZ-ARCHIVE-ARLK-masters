/*
Arduino Stepper Motor Test File

Using the AccelStopper library
*/

#include <AccelStepper.h>

// Define a stepper motor for arduino 
AccelStepper stepper(1, 12, 11); // pin 12 = step/pulse, pin 11 = direction

#define LEFT -2308
#define RIGHT 2308

char incomingdirection = 0;   // for incoming direction data


/*
Note: AccelStepper mystepper(1, pinStep, pinDirection); A stepper motor controlled by a dedicated driver board. In this case a DM542T
Source: https://www.pjrc.com/teensy/td_libs_AccelStepper.html

As a result pin 10 = enable is not used
*/

/* Sample code which causes motor to rotate 90 deg back and forth
void setup() 
{
  stepper.setMaxSpeed(10000);// Max Speed Limit in Steps per second
  stepper.setAcceleration(1000);// Acceleration in Steps per second^2
  stepper.moveTo(2308);// Note that 1 Step means angle 0.039 deg rotation for 23HS22-2804S-PG47
}

void loop()
{
    // If at the end of travel go to the other end
    if (stepper.distanceToGo() == 0){
      stepper.moveTo( -stepper.currentPosition() );
    }
    
    stepper.run();
}
*/

void setup() 
{
  Serial.begin(9600);
  stepper.setMaxSpeed(300);// Max Speed Limit in Steps per second
  stepper.setAcceleration(100);// Acceleration in Steps per second^2
  
}

void loop()
{
  Serial.println(stepper.currentPosition()); // Shows current absolute position for debug purposes
  stepper.setCurrentPosition(0); // Resets absolute position to current position. Also for some reason one needs to double the move value if this command is used 
  Serial.println("Choose rotation direction by pressing either 'A' (left) or 'D' (right) keys.\n");
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming direction data
    incomingdirection = Serial.read();
    // say what you got
    Serial.print("I received: ");
    Serial.println(incomingdirection);
    if (incomingdirection == 'a'){
      Serial.print("Turning left by 90 deg.\n");
      stepper.moveTo((2*LEFT));
      while (stepper.currentPosition() > (2*LEFT)){
        stepper.run();
      }
      Serial.println(stepper.currentPosition()); // Shows current absolute position for debug purposes
    }
    if (incomingdirection == 'd'){
      Serial.print("Turning right by 90 deg.\n");
      stepper.moveTo((2*RIGHT));
      while (stepper.currentPosition() < (2*RIGHT)){
        stepper.run();
      }
      Serial.println(stepper.currentPosition()); // Shows current absolute position for debug purposes
    }
    else Serial.print("Please enter 'A' or 'D' only !!!\n");
  }
}