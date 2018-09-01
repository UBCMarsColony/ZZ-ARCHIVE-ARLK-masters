//Procedure Primitives
#define open true
#define close false 
#define pressurize true
#define depressurize false

//Procedure flags
#define entry 1
#define exit 0

#define x 'x'
#define in_progress 'p'

#define initial_airlock depressurize
#define initial_valve_a close
#define initial_valve_b close

//Common data value definitions
#define one_atm 101.3   // in kpa
#define mars_atm    0.6 // in kpa
#define epsilon 5   //Range to set control flags, + or - 5 kPa

//Control buttons
#define button_colonyside       2
#define button_marsside         3

//Display pin definitions
#define status_press            0
#define status_press_progress   1
#define status_depress          2
#define status_depress_progress 3

//DEBUGGING definitions
#define pressure_data           101.3 // in kpa

////////////////// Function Definitions /////////////////////
bool get_airlock_state(int pressure);
///////////////// Procedure and primitive definitions////////
void procedure();
bool hold_press();
bool DPR();
bool PR();
//////////////// Other definitions //////////////////////////
int led_status_display();

//TO IMPLEMENT
void colonyhandler();
void marshandler();



//type definitions
typedef struct{
    byte state;
    int pressure;
}airlock_state;
	
//variable declaration
airlock_state u_airlock;
bool valve_a;
bool valve_b;
int pressure_val;

//debug assignments
int pressure_val = pressure_data;

void setup(){
    //put setup code here
    Serial.begin(9600);

    //////////Button and interrupts////////
    //There's no software debouncing, so build button debouncing circuits
    pinMode(button_colonyside, INPUT_PULLUP);
    pinMode(button_marsside, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(button_colonyside), procedure(colonyhandler), FALLING);
    attachInterrupt(digitalPinToInterrupt(button_marsside),procedure(marshandler), FALLING); 

    u_airlock.pressure = pressure_val;
    u_airlock.state = get_airlock_state(pressure_val);

    valve_a = initial_valve_a;
    valve_b = initial_valve_b;
}

void loop() {
    //Looping code 
    u_airlock.pressure = pressure_val;
    u_airlock.state = get_airlock_state(pressure_val);

}

//Entering the airlock from mars is called entry, and leaving the airlock called exit
void procedure(bool select_procedure){
    if(select_procedure == entry){
        PR();
        Serial.println("Opening colony -> airlock door");
        DPR();
        Serial.println("Opening airlock -> mars door");
    }
    else if(select_procedure == exit){
        Serial.println("Opening airlock -> mars door");
        PR();
        Serial.println("Opening colony -> airlock door");
        DPR();
    }
}

///////////// Simple Procedures ////////////////
bool PR(){
    while(u_airlock.state != pressurize){
        valve_a = close;
        valve_b = open;
    }
    hold_press();
}
bool DPR(){
    while(u_airlock.state != depressurize){
        valve_a = open;
        valve_b = close;
    }
    hold_press();
}
bool hold_press(){
    valve_a = close;
    valve_b = close;
}
//////////////////////////////////////////////


bool get_airlock_state(int pressure){
    BYTE state;
    if (mars_atm - epsilon < pressure < mars_atm + epsilon){
        state = depressurize;
    }
    else if(one_atm - epsilon < pressure < one_atm + epsilon)
        state = pressurize;
    else
        state = in_progress;
    return state;
}