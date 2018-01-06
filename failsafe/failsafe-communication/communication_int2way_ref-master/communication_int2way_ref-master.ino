
//Master Arduino, Writing 4 to the slave and recieving 2

#include <Wire.h>

#define SLAVE_ADDRESS 12345
#define N 3
void setup()
{
  Wire.begin(); 
  Serial.begin(9600);  
}

int numrecieved[N];
int numsent[N]={0,1,1};
void loop()
{
  Serial.print("Sending The Slave:");
  Serial.print("\n");
  
  Wire.beginTransmission(SLAVE_ADDRESS);   
  for(int i=0; i<N; i++){
  Serial.print(numsent[i]);
  Serial.print("\n");
  Wire.write(numsent[i]);     
  }           
  Wire.endTransmission();   
  delay(500);


  

  for(int k=0; k<N; k++){
  Serial.println("Requesting Data"); 
  Wire.requestFrom(SLAVE_ADDRESS, 1);

  int bytes = Wire.available();
  
  Serial.print("Slave sent ");
  Serial.print(bytes);
  Serial.print(" bytes of information\n");
  
  numrecieved[k] = Wire.read();
 //  Serial.print("Slave Sent: ");
 //  Serial.print(numrecieved[k]);
 //  Serial.print("\n");
 //  Serial.print(k);
 //  Serial.print("\n");
  }
  for(int u=0; u<N; u++){
    Serial.print(numrecieved[u]);
    Serial.print("\n");
  }
  memset(numrecieved,0,sizeof numrecieved);// Clearing array
  delay(500);
}
