
/* Written By: Thomas Richmond
 * Email: Thomas.joakim@gmail.com
 * 
 * This program is meant to decide how to set up the lights. It starts by deciding what lighting scheme to use - that is, 
 * what lights are on, which are off, and what other associated logic. Once the lighting scheme has been decided, the
 * lights can be set by passing the LightScheme structure returned by the decideLighting() fuction into the controlLights()
 * function.
 * 
 * In the event of an error, lights may flash. This has yet to be implemented.
 */

//Function prototypes
struct LightScheme decideLighting(int);
int controlLights(struct LightScheme);

//LightScheme structure
struct LightScheme {
  int lightState_1;
  int lightState_2;
};

//Deduce, using current data, the best lighting scheme to apply to the airlock.
struct LightScheme decideLighting(int errorCode){
  //Check if the passed in errorCode.
    //If the errorCode supports a valid error, return error to flash the lights 3 times.
  
  //Get PIR sensor data
    //If somebody is in range of the PIR sensor, return lights on scheme.

  //If nobody is detected, check the time since somebody was last seen.
    //If it is greater than the time limit, return lights off scheme.
}

//Set all lights according to a lighting scheme
int controlLights(struct LightScheme lightScheme){
  
}
