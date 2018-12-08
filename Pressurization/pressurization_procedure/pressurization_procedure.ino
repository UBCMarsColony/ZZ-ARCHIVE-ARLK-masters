#include <Wire.h>

// Arduino I2C Things
#define SLAVE_ADDRESS 0x14
void receiveData(int);
void sendData();

// Arduino GPIO
#define VALVE_1 8 
#define VALVE_2 9

// Other constants
#define MSG_LENGTH 32

enum Procedure {
  Calibrate     = 2,
  SetPressure   = 3,
  NumMessages
};

typedef struct Calibrate_t {
  byte action;
  byte procedure;
};

typedef struct SetPressure_t {
  byte action;
  byte procedure;
  float priority;
  float pTarget;      // Target pressurization (kPA to 1 decimal place)
  float pTolerance;   // Target pressurization tolerance (%)
  byte overhead[21];
};

volatile byte messages[NumMessages][MSG_LENGTH] = {0};  // Messages are stored in the element corrsponding to 
                                                        //their procedure ID (as specified in the Procedure enum)
volatile byte msg = 0; // Points to a message to be evaluated.

int currentPressure = -1; // TODO Replace later; Currently a placeholder name to represent a procedure in loop.

void setup(){
  Serial.begin(9600);

  // Register valves
  pinMode(VALVE_1, OUTPUT);
  pinMode(VALVE_2, OUTPUT);

  // Set up I2C
  Serial.print("Using address: ");
  Serial.println(SLAVE_ADDRESS);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}


void loop() {
  // The purpose of this loop is to evaluate next message in the messages array.
  // If a message needs immediate evaluations, the 'msg' value can be set to that message.

  if (messages[msg][1] == 0) {
    Serial.print("Evaluating message type ");
    Serial.println(msg);

    // Evaluate the message specified by 'msg'.
    switch (msg) {
      case Calibrate: {
        Calibrate_t *c = (Calibrate_t*) messages[msg];

        }
        break;
      
      case SetPressure: {
        SetPressure_t *sp = (SetPressure_t*) messages[msg];

        digitalWrite(VALVE_1, (sp->pTarget > currentPressure) ? INPUT : OUTPUT);
        digitalWrite(VALVE_2, (sp->pTarget < currentPressure) ? INPUT : OUTPUT);
        }
        break; 
    }
    
    // Clear the message from the queue
    memset(messages[msg], 0, sizeof(messages[msg]));
  }

  // Cycles over existing message types
  msg = (msg + 1) % NumMessages;
}

// I2C Things
void receiveData(int byteCount)
{
  Serial.println("Received transmission from Master");
  byte data[MSG_LENGTH] = {};

  // Read the incoming message.
  for (int i = 0; Wire.available(); i++) {
      data[i] = Wire.read();
      Serial.println(data[i]);
  }

  // Run checks if needed.

  // Put message into the queue
  for (int i = 0; i < MSG_LENGTH; i++)
    messages[data[1]][i] = data[i];
}

void sendData() {
  Serial.println("sendData stub called");
}

