//if O is pressed, open the door
//if C is pressed, close the door
//if Q is pressed, recalibrate positioning of open vs closed
//if K is pressed, enter custom mode


#include <AccelStepper.h>
#include <Wire.h>

// Define a stepper motor for arduino
AccelStepper stepper(1, 12, 11); // pin 12 = step/pulse, pin 11 = direction
/*
Note: AccelStepper mystepper(1, pinStep, pinDirection); A stepper motor controlled by a dedicated driver board. In this case a DM542T
Source: https://www.pjrc.com/teensy/td_libs_AccelStepper.html

As a result pin 10 = enable is not used
*/

#define LEFT -2308
#define RIGHT 2308
#define PRESSED 1

enum Procedure {
    calibrate       = 2,
    setDoorState    = 3,
    getDoorState    = 4,
    numMessages
};

enum DoorState {
    unknown = 0,
    transit = 3,
    close = 99,
    open = 111,
    manualCalibrate = 113,
} doorState;

enum Position{
    doorIsOpen=2*RIGHT,
    doorIsClosed=0,
    doorInTransit
} doorPosition;

enum Priority {
    priorityLow = 0,
    priorityHigh = 1
};

typedef struct Header_t {
    byte action;
    byte procedure;
    byte priority;
};

typedef struct Calibrate_t {
  Header_t header;
};

typedef struct SetDoorState_t {
  Header_t header;
  byte targetState;
};

typedef struct GetDoorState_t {
    Header_t header;
    byte DoorState;
    short angle;
};

typedef union I2CMessage_t {
    Calibrate_t calibrate;
    SetDoorState_t setDoorState;
    GetDoorState_t getDoorState;
};

volatile I2CMessage_t* messages[numMessages] = {0};
volatile byte msgIndex = 0;

int speed=400;            //initial speed of the motor
int customAngle = 0;      //inital custom angle
String tempstring = "";   //initializing string to hold input
const int exitButton=2;   //pin that the button is connected to
int buttonState=0;        //the button is initially not pressed
int factor;               //used in custom mode to determine direction and angle being turned
int whatToDo;              //hopefully helps read string data???
int msg[32] = {};

const int Open=111;
const int Close=99;
const int ManualCalibrate=113;

const int address_slave=45;
volatile int incomingdirection = 0;

void setup(){

  Wire.begin(address_slave); //fucking slaves get your ass back here     !!!!
  Wire.onReceive(commandHandler); //function to call when command received    !!!!
  Wire.onRequest(requestHandler);
//    Wire.onRequest(requestHandler);
  Serial.print("I2C systems online. Using address ");
  Serial.println(address_slave);

  Serial.println("----------------------");
  Serial.println("System setup complete!");
  Serial.println("----------------------\n");

  Serial.begin(9600);
  stepper.setAcceleration(500);
  stepper.setMaxSpeed(speed);

}

void loop(){
  // MESSAGE PARSING & EVALUATION

 // if (Serial.available() > 0) {
      // read the incoming direction data
     // incomingdirection = Serial.read();
      // say what you got
     // Serial.print("I received: ");
     // Serial.print(incomingdirection);
     // Serial.print(".\n");
 // }
 // Serial.println(stepper.currentPosition()); // Shows current absolute position for debug purposes

  switch(msg[1]){//uses msg1 for I2C instead of incomingdirection for serial input
    //To open the door
    case Open:
    Serial.print("Opening door.\n");
    stepper.moveTo(doorIsOpen); //turns 90 degrees clockwise
    while (stepper.currentPosition() < doorIsOpen && digitalRead(exitButton)!=HIGH  ){
      doorState=transit;  //sets the door state as being in transit
      stepper.run();    //runs until the door reaches the open position or the emergency exit button is pressed
    }
    break;

    //To close the door
    case Close:
    Serial.print("Closing door.\n");
    stepper.moveTo(doorIsClosed); //turns 90 degrees counterclockwise
    while (stepper.currentPosition()!=doorIsClosed && digitalRead(exitButton)!=HIGH ){
      doorState=transit;  //sets the door state as being in transit
      stepper.run();    //runs until the door is closed or the emergency exit button is pressed
    }
    break;

    //To manually calibrate the door and input a new location for "closed"
    case ManualCalibrate:
    Serial.print("Closing door. Press the emergency exit button to stop when the door is closed.\n");
    stepper.moveTo(4*LEFT); //closes door for a full 180 degree rotation
    while(digitalRead(exitButton)!=HIGH){
      doorState=transit;  //sets the door state as being in transit
      stepper.run();    //runs until the emergency exit button is pressed
    }
    stepper.setCurrentPosition(0);    //sets the door position to zero
    break;

    default:
      doorState=unknown;
  }

  msg[1]=0;

  // goes back to the starting position if the emergency exit button has been pressed
  if(digitalRead(exitButton)== HIGH){
    Serial.print("Closing door.\n");
    stepper.moveTo(0);  //goes to starting position
    while (stepper.currentPosition()!=doorIsClosed){
      doorState=transit;    //sets the door state as being in transit
      stepper.run();}   //runs until the door is closed
  }

  //takes the current door position and calculates the anagle it's open, with closed=0 degrees
  doorPosition=stepper.currentPosition()/RIGHT*90;
    switch(stepper.currentPosition()){
    case doorIsOpen:
      doorState=open;
      break;
    case doorIsClosed:
      doorState=close;
      break;
    default:
      doorState=unknown;
      break;
  }
}

void commandHandler(int ignorefornow){
  //int msg[32] = {};
  int count = 0;
  while(Wire.available()){
    msg[count] = Wire.read();
    count++;
  }
  Serial.print("Message1: ");
 Serial.println(msg[1]);
  switch(msg[1]){
    case setDoorState: //set door state
    incomingdirection=  msg[3];
    break;
  }
  // SetDoorState_t* sds = (SetDoorState_t*) msg;
  //
  // switch(sds->targetState) {
  //
  // }

  //  case 2:   //CALIBRATE
}
// //
// Clear loop
// -add all commonds to command HANDLERS
// -add an on request method

void requestHandler(int type){
  switch (type){
    case getDoorState:
      //byte gds[]={0,getDoorState,priorityLow,doorState,stepper.currentPosition()};
      GetDoorState_t gds=GetDoorState_t();
       gds.DoorState=doorState;
       gds.angle=stepper.currentPosition(); //placeholder
       gds.header.action=0; //placeholder
       gds.header.procedure=getDoorState;
       gds.header.priority=priorityLow;
      Wire.write((byte *) &gds, sizeof (gds));
  }
}

    // Serial.println("Received transmission from Master");
    // byte data[MSG_LEN] = {};
    //
    // // Read the incoming message.
    // for (int i = 0; Wire.available(); i++) {
    //     data[i] = Wire.read();
    //     Serial.println(data[i]);
    // }
    //
    //
    // if (data[1] >= numMessages) {
    //     Serial.println("CRITICAL ERROR: Received message of unknown type! This should never happen.");
    //     return;
    // }
    //
    // // Check if there is already an existing message of this type, and if the incoming message takes priority
    // if (messages[data[1]]->calibrate.header.action != 0 && data[2] != priorityHigh) {
    //     Serial.print("Message of type ");
    //     Serial.print(data[2]);
    //     Serial.println(" already exists. Ignoring...");
    //     return;
    // }
