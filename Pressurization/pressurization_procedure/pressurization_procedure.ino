#include <Wire.h>

// Arduino I2C Things
#define SLAVE_ADDRESS 0x14
void receiveData(int);
void sendData();

// Arduino GPIO
#define VALVE_PRESSURIZER 8
#define VALVE_DEPRESSURIZER 9

// Other constants
#define MSG_LEN 32
#define KEEP_MSG true
#define CLEAR_MSG false


enum Procedure {
  SetPressure   = 3,
  NumMessages
};

enum TargetState {
  Close,
  Pressurize,
  Depressurize,
  Idle
};

typedef struct SetPressure_t {
  byte action;
  byte procedure;
  byte priority;
  byte targetState;
};

volatile byte messages[NumMessages][MSG_LEN] = {0};  // Messages are stored in the element corrsponding to
// their procedure ID (as specified in the Procedure enum)
volatile byte msgIndex = 0; // Points to a message to be evaluated.

// Pressure Data
SetPressure_t *currentPressureState;

typedef struct ValveState_t {
  bool pressurizer;
  bool depressurizer;

  ValveState_t(int p, int dp)
    : pressurizer(p)
    , depressurizer(dp) {}
};
const struct ValveState_t* PRESSURIZE = new ValveState_t(HIGH, LOW);
const struct ValveState_t* DEPRESSURIZE = new ValveState_t(LOW, HIGH);
const struct ValveState_t* CLOSE = new ValveState_t(LOW, LOW);


// Function Signatures
bool evaluateMessage(byte[], int);
void applyValveState(struct ValveState_t);
void receiveData(int);
void sendData();

void setup() {
  Serial.begin(9600);

  // Register valves
  pinMode(VALVE_PRESSURIZER, OUTPUT);
  pinMode(VALVE_DEPRESSURIZER, OUTPUT);

  // Set up I2C
  Serial.print("Using address: ");
  Serial.println(SLAVE_ADDRESS);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}


/*
   This loop is configured to:
      1. Evaluate next message in the messages array. If a message needs immediate evaluations, the 'msgIndex' value can be set to that message.
      2. Undergo any airlock actions.
*/
void loop() {
  // MESSAGE PARSING & EVALUATION
  if (evaluateMessage(messages[msgIndex], msgIndex) == CLEAR_MSG)
    memset(messages[msgIndex], 0, sizeof(messages[msgIndex])); // Clear message from 'messages' array

  msgIndex = (msgIndex + 1) % NumMessages;

//  TEST_ROUTINE();
}


/*
   Parse and evaluate a message.
   Parameter: message - Stored i2c message byte array.
   Parameter: type - The numerical value found in 'Procedure' associated with this data.
   Return: A boolean indicating if we should remove the message from queue.
*/
bool evaluateMessage(byte message[], int type) {
  if (message[0] != 0) {
    Serial.print("Evaluating message type ");
    Serial.println(type);

    switch (type) {
      case SetPressure:
        {
          currentPressureState = (SetPressure_t*) message;

          switch (currentPressureState->targetState) {
            case Pressurize:
              applyValveState(PRESSURIZE);
              break;
            case Depressurize:
              applyValveState(DEPRESSURIZE);
              break;
            case Close:
              applyValveState(CLOSE);
              break;
          }
          return CLEAR_MSG;
        }
        break;
    }
  }
  return KEEP_MSG;
}


void applyValveState(struct ValveState_t* state) {
  digitalWrite(VALVE_PRESSURIZER, state->pressurizer);
  delay(1000);
  digitalWrite(VALVE_DEPRESSURIZER, state->depressurizer);
}


/*
   I2C INTERRUPTS BEYOND THIS POINT
*/
void receiveData(int byteCount) {
  Serial.println("Received transmission from Master");
  byte data[MSG_LEN] = {};

  // Read the incoming message.
  for (int i = 0; Wire.available(); i++) {
    data[i] = Wire.read();
    Serial.println(data[i]);
  }


  if (data[1] % (1<<7) >= NumMessages) {
    Serial.println("CRITICAL ERROR: Received message of unknown type! This should never happen.");
    return;
  }
  // Run other checks if needed.

  // Put message into the queue
  for (int i = 0; i < MSG_LEN; i++)
    messages[data[1]][i] = data[i];
}

void sendData() {
  Serial.println("sendData stub called");
}


/*
   TEST ROUTINE CODE BELOW
   -----------------------
   Can be removed once system is
   confirmed working.
*/

bool t1 = false, t2 = false, t3 = false;;
void TEST_ROUTINE() {
  if (millis() > 5000 && !t1 ) {
    Serial.print("P:");
    Serial.print(PRESSURIZE->pressurizer);
    Serial.println(PRESSURIZE->depressurizer);
    t1 = true;
    applyValveState(PRESSURIZE);
  }
  if (millis() > 15000 && !t2 ) {
    Serial.print("D:");
    Serial.print(DEPRESSURIZE->pressurizer);
    Serial.println(DEPRESSURIZE->depressurizer);
    t2 = true;
    applyValveState(DEPRESSURIZE);
  }

  if (millis() > 25000 && !t3 ) {
    Serial.println("C");
    t3 = true;
    applyValveState(CLOSE);
  }
}

