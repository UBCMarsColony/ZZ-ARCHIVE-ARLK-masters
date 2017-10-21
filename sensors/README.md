# Sensors
Sensors are the systems that will allow for polling of the location at which the airlock is located. In general, sensors get their data and relay the information to the master Arduino. When appropriate, the master converts the data to JSON and sends it to the mastery Raspberry Pi, where it is used to make decisions. 

For a complete list of sensors, refer to the list below:
<details>
  <summary>Sensor List</summary>
  Gravity IR Co2 Sensor
  Grove O2 Sensor
  Temperature/Pressure Sensor
</details>

## Universal Sensor Details

### Error Report
When a sensor encounters an error, it should return the standardized sensor error code **-555**. This will allow the main system to take appropriate action.
