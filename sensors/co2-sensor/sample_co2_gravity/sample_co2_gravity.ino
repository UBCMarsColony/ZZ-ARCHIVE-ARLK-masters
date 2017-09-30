/***************************************************
 * Infrared CO2 Sensor0-5000ppm 
 * ****************************************************
 * This example The sensors detect CO2
 * 
 * @author lg.gang(lg.gang@qq.com)
 * @version  V1.0
 * @date  2016-7-6
 * 
 * GNU Lesser General Public License.
 * See <http://www.gnu.org/licenses/> for details.
 * All above must be included in any redistribution
 * ****************************************************/
int sensorIn = A0;  

void setup(){  
  Serial.begin(9600);  
  // Set the default voltage of the reference voltage
  analogReference(DEFAULT); 
}

void loop(){ 
  //Read voltage
  int sensorValue = analogRead(sensorIn);  

  // The analog signal is converted to a voltage 
  float voltage = sensorValue*(5000/1024.0); 
  if(voltage == 0)
  {
    Serial.println("Fault");
  }
  else if(voltage < 400)
  {
    Serial.println("preheating");
    Serial.print("Voltage is: ");
    Serial.print(voltage);
  }
  else
  {
    int voltage_diference=voltage-400;
    float concentration=voltage_diference*50.0/16.0;
    // Print Voltage
    Serial.print("voltage:");
    Serial.print(voltage);
    Serial.println("mv");
    //Print CO2 concentration
    Serial.print(concentration);
    Serial.println("ppm");
  }
  delay(300); 
}
