//Common data value definitions
#define one_atm     101.3   // in kpa
#define mars_atm    0.6 // in kpa
#define epsilon     5   //Range to set control flags, + or - 5 kPa

//Opening & Closing Valves
#define open true
#define close false 

//The two main procedures, entering and leaving the airlock
#define entry 1
#define exit 0

//Initial state of the valves
#define initial_valve_a close
#define initial_valve_b close

//Airlock States
#define in_progress 2
#define pressurize 1
#define depressurize 0


//Control buttons
#define button_colonyside       2
#define button_marsside         3

//LED display
#define status_press            0
#define status_progress         1
#define status_depress          2

//DEBUGGING definitions
#define pressure_data           101.3 // in kpa

////////////////// Get State from Pressure data from Pi/////////////////////
byte get_airlock_state(int pressure);

///////////////// Procedure and primitive definitions////////
void procedure();
bool hold_press();
bool DPR();
bool PR();

//////////////// Display driver //////////////////////////
int led_status_display();

//Airlock Pressurization System
typedef struct{
    byte state;
    int pressure;
    bool valve_a;
    bool valve_b;
}airlock;
	
//Airlock System Initialization
airlock u_airlock;
void setup(){
    //put setup code here
    Serial.begin(9600);

    //////////Button and interrupts////////
    //There's no software debouncing, so build button debouncing circuits
    pinMode(button_colonyside, INPUT_PULLUP);
    pinMode(button_marsside, INPUT_PULLUP);

    //LED display pins
    pinMode(status_press,OUTPUT);
    pinMode(status_progress,OUTPUT);
    pinMode(status_depress,OUTPUT);

    //Button interrupts
    attachInterrupt(digitalPinToInterrupt(button_colonyside), colonyside, FALLING);
    attachInterrupt(digitalPinToInterrupt(button_marsside), marside, FALLING); 
    u_airlock.valve_a = initial_valve_a;
    u_airlock.valve_b = initial_valve_b;


}
void colonyside(){
    procedure(exit);
}
void marside(){
    procedure(entry);
}
void loop() {
    //Looping code 
    u_airlock.pressure = pressure_data;
    u_airlock.state = get_airlock_state(u_airlock.pressure);
    led_status_display(u_airlock.state);
    delay(1000);

}
int led_status_display(byte state){
    if(state == status_press){
        digitalWrite(status_press, HIGH);
        digitalWrite(status_depress, LOW);
        digitalWrite(status_progress, LOW);
    }
    else if (state == status_depress){
        digitalWrite(status_press, LOW);
        digitalWrite(status_depress, HIGH);
        digitalWrite(status_progress, LOW);
    }
    else if (state == status_progress){
        digitalWrite(status_press, LOW);
        digitalWrite(status_depress, LOW);
        digitalWrite(status_progress, HIGH);
    }
    return 1;
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
        u_airlock.valve_a = close;
        u_airlock.valve_b = open;
    }
    hold_press();
}
bool DPR(){
    while(u_airlock.state != depressurize){
        u_airlock.valve_a = open;
        u_airlock.valve_b = close;
    }
    hold_press();
}
bool hold_press(){
    u_airlock.valve_a = close;
    u_airlock.valve_b = close;
}
//////////////////////////////////////////////


byte get_airlock_state(int pressure){
    byte state;
    if (mars_atm - epsilon < pressure < mars_atm + epsilon){
        state = depressurize;//0
    }
    else if(one_atm - epsilon < pressure < one_atm + epsilon)
        state = pressurize;//1
    else
        state = in_progress;
    return state;
}