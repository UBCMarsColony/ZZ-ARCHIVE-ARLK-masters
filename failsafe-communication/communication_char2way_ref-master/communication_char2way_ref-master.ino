
//Master Arduino, Writing "Jacky" and Recieving "Jiang" from Slave

#include <Wire.h>

#define SLAVE_ADDRESS 1

void setup()
{
  Wire.begin(); 
  Serial.begin(9600);  
}

char x1;             // Stores the read character
char x2[6];          // Array used to store string of characters read
char x3[] = "Jiang"; // Array used for comparison
int a = 0;           // Used to store index position

void loop()
{
  Serial.print("Sent: ");
  Serial.print(SLAVE_ADDRESS);
  Serial.print("\n");
  Wire.beginTransmission(SLAVE_ADDRESS);   
  Wire.write("Jacky");    // Sending string to slave            
  Wire.endTransmission();   
  delay(500);

  
  Serial.println("Master Requesting Data"); //Requesting data from slave.
  Wire.requestFrom(SLAVE_ADDRESS, 5);

  int bytes = Wire.available();
  Serial.print("Slave sent ");
  Serial.print(bytes);
  Serial.print(" bytes of information \n");
   
  for(int i = 0; i< bytes; i++)
  {
    
    x1 = Wire.read();
    x2[a] = x1;
    Serial.print("Slave Sent: ");
    Serial.print(x1);
    Serial.print("\n");
    
    if (strcmp(x2,x3) == 0){  // Prints Full name if x2 matches x3
    Serial.print("Full name is Jacky ");
    Serial.print(x2);
    Serial.print("\n IF \n");
    
    a = 0;  // Resets Index to 0
    memset(x2, 0, sizeof x2); // Resets x2 char array
    }
    
    else if(a < (bytes-1)) {
    Serial.print(x2);
    Serial.print("\n ELSE IF \n");
    
    a++;  // Increases Index
    }
    
    else {
    a = 0;  // Resets Index to 0
    memset(x2, 0, sizeof x2); // Resets x2 char array
    
    Serial.print(x2);
    Serial.print("\n ELSE \n");
    }
  }  
  delay(500);
}
