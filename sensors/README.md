# Sensors
Sensors are the systems that will allow for polling of the location at which the airlock is located. In general, sensors get their data and relay the information to the master Arduino. When appropriate, the master converts the data to JSON and sends it to the mastery Raspberry Pi, where it is used to make decisions. 

For a complete list of sensors, refer to the list below:
<details>
  <summary>Sensor List</summary>
  • <a href="co2-sensor">Gravity IR CO₂ Sensor</a> <br/>
  • <a href="o2-sensor">Grove O₂ Sensor</a><br/>
  • <a href="temperature-pressure-sensor">Temperature/Pressure Sensor</a><br/>
  • <a href="PIR-motion-sensor">Passive IR Sensor</a><br/>
</details>

## Sensor Ports
To interface with the main system, each sensor will take an ADC port on the arduino. These should be standardized whenever possible. A full list of taken ADC Ports is listed below:


<details>
  <summary>ADC Ports</summary>
  • <b>AO</b>: CO₂ Sensor </br>
  • <b>A1</b>: O₂ Sensor </br>
  • <b>A3</b>: T/P Sensor </br>
  • <b>A4</b>: PIR Sensor
</details>

## Universal Sensor Details
To make sensor code as maintainable as possible, standardizations are in place to reduce code arbitrarity. These should be followed at all times unless otherwise explicitly specified.

### Unit Standards
All sensors and logic systems should use data expressed in the same, standardized units. Unit conventions are listed below: 

<details>
  <summary>Unit Standards</summary>
  • <b>O2 Concentration</b>: Percentage (%)<br/>
  • <b>CO2 Concentration</b>: Parts per million (ppm)<br/>
  • <b>Temperature</b>: Degrees Celsius (°C)<br/>
  • <b>Pressure</b>: kiloPascals (kPa)
</details>

### Encoded Reports
Oftentimes, sensors encountering an expected situation will relay the situation to the master using a raw integer value. These values are listed below:

<details>
  <summary>Report Codes</summary>
  • <b>-500</b>: Data out of bounds<br/>
  • <b>-555</b>: Generic error<br/>
  • <b>-600</b>: Preheating in progress<br/>
  • <b>-666</b>: Initialization Error
</details>
