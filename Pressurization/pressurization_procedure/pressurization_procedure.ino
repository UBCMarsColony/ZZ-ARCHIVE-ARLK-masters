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
#define status_press            4
#define status_progress         5
#define status_depress          6

//DEBUGGING definitions
float pressure_data = 0; // in kpa

////////////////// Get State from Pressure data from Pi/////////////////////
byte get_airlock_state(int pressure);

///////////////// Procedure and primitive definitions////////
byte cmd_sel;
void procedure();
bool hold_press();
bool DPR();
bool PR();
void colonyside(){
    cmd_sel = 'o';
    //procedure(exit);
}
void marside(){
    cmd_sel = 'i';
    //procedure(entry);
}
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
    //procedure flag
    cmd_sel = 'x';
    //There's no software debouncing, so build button debouncing circuits
    pinMode(button_colonyside, INPUT_PULLUP);
    pinMode(button_marsside, INPUT_PULLUP);

    //LED display pins
    pinMode(status_press,OUTPUT);
    pinMode(status_progress,OUTPUT);
    pinMode(status_depress,OUTPUT);

    //Button interrupts
    attachInterrupt(digitalPinToInterrupt(button_colonyside), colonyside, RISING);
    attachInterrupt(digitalPinToInterrupt(button_marsside), marside, RISING); 
    u_airlock.valve_a = initial_valve_a;
    u_airlock.valve_b = initial_valve_b;



}
void loop() {
    //Looping code 
    u_airlock.pressure = pressure_data;
    u_airlock.state = get_airlock_state(u_airlock.pressure);

    Serial.print("Pressure is:\t");
    Serial.println(u_airlock.pressure);
    Serial.print("State is:\t");
    Serial.println(u_airlock.state);
    Serial.print("cmd_sel is:\t");
    Serial.println(char(cmd_sel));
    if(cmd_sel == 'i'){
        procedure(entry);
    }
    else if (cmd_sel == 'o'){
        procedure(exit);
    }
    cmd_sel = 'x';
    led_status_display(u_airlock.state);
    delay(1000);

}
int led_status_display(byte state){
    if(state == pressurize){
        Serial.println("Pressruized");
        digitalWrite(status_press, HIGH);
        digitalWrite(status_depress, LOW);
        digitalWrite(status_progress, LOW);
    }
    else if (state == depressurize){
        Serial.println("dePressruized");
        digitalWrite(status_press, LOW);
        digitalWrite(status_depress, HIGH);
        digitalWrite(status_progress, LOW);
    }
    else if (state == in_progress){
        Serial.println("inprogress");
        digitalWrite(status_press, LOW);
        digitalWrite(status_depress, LOW);
        digitalWrite(status_progress, HIGH);
    }
    return 1;
}
//Entering the airlock from mars is called entry, and leaving the airlock called exit
void procedure(bool select_procedure){
    if(select_procedure == exit){
        PR();
        Serial.println("Opening colony -> airlock door");
        Serial.println("Detect airlock door close");
        DPR();
        Serial.println("Opening airlock -> mars door");
        Serial.println("Detect mars door close");
    }
    else if(select_procedure == entry){
        Serial.println("Opening airlock -> mars door");
        Serial.println("Detect mars door close");
        PR();
        Serial.println("Opening colony -> airlock door");
        Serial.println("Detect airlock door close");
        DPR();
    }
}

///////////// Simple Procedures ////////////////
bool PR(){
    while(u_airlock.state != pressurize){
        u_airlock.valve_a = close;
        u_airlock.valve_b = open;
        u_airlock.state = get_airlock_state(pressure_data++);
    }
    hold_press();
}
bool DPR(){
    while(u_airlock.state != depressurize){
        u_airlock.valve_a = open;
        u_airlock.valve_b = close;
        u_airlock.state = get_airlock_state(pressure_data--);
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
    Serial.print("Inside Get airlock state");
    Serial.println(pressure);
    if (mars_atm - epsilon < pressure && pressure < mars_atm + epsilon){
        state = depressurize;
    }
    else if(one_atm - epsilon < pressure && pressure < one_atm + epsilon)
        state = pressurize;
    else
        state = in_progress;
    return state;
}