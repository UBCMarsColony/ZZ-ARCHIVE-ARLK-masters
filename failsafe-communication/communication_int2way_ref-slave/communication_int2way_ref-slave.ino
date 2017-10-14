//Slave Arduino recieving an array of integer values, and echoing it back to master

#include <Wire.h>

#define N 3
#define SLAVE_ADDRESS 5

int numsent[N]={7,0,1};
int numrecieved[N];
int s;
int r;
int j=0;
void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);
}

void loop()
{
  delay(100);
}

void requestEvent() 
{
  if (j < N){
  s=numsent[j];
  j++;
  Serial.print("Request from Master. Sending: ");
  Serial.print(s);
  Serial.print("\n");
  Wire.write(s);
  if (j == N)
    j=0;
  }
}


/*Data Recieved from the Master*/
void receiveEvent(int bytes)
{
  if(Wire.available() != 0)
  {
    for(int i = 0; i< N; i++)
    {
      numrecieved[i] = Wire.read();
      Serial.print("Received: ");
      Serial.print(numrecieved[i]);
      Serial.print("\n");
    }
  }
  Serial.print("I hope this is printing the array: \n");
  for(int t=0; t<N; t++ ){
  Serial.print(numrecieved[t]);
  Serial.print("\n");
  }
}
