# airlock-masters <img align="right" src="artwork/ubcmc-logo-transparent_small.png">
UBC Mars Colony airlock repository. All source code, datasheets, and other materials related to the airlock are found here.

## Naming convention
To ensure the repository is quick to navigate, all Mars Colony files should follow a standardized naming convention. This naming convention extends to both files and folders, as outlined below:

### Files
All code, documentation, and other files related to the project follow a standardized naming convention. They should follow a general structure, as outlined below:

*Project-Module_Project-Part_Description(_Sample).extension*.

Separate the descrete name elements using underscores, and use hypens instead of spaces. (Although this may cause errors in importing, it is generally avoidable through a bit of fanagling - see the wiki for more details.)

### Folders
Folders should be broken up into logical parts, to ensure code can be found as quickly as possible. Use hyphens instead of spaces in folder names. Additionally, avoid the use of capital letters in the folder names unless absolutely necessary. For instance, the path to a CO2 Sensor file may be:

*airlock-masters/sensors/co2-sensor/co2file.py*

## Directories
<details>
<summary><b>Artwork</b></summary>
  Contains all visuals used in the repository. See wiki for information on how to use them.</br>
</details>

<details>
  <summary><b>Documentation</b></summary>
  Contains documentation, datasheets and more for hardware and software used in the project. </br>
</details>

<details>
<summary><b>Failsafe</b></summary>
  Contains the code used to process sensor data on the Arduino board and send it via I2C to the main Raspberry Pi system. /br>
</details>

<details>
<summary><b>Lighting</b></summary>
  Contains code and data about lighting systems in the airlock. /br>
</details>

<details>
<summary><b>Motors</b></summary>
  Contains code and data about the motors in the airlock. /br>
</details>

<details>
<summary><b>Pi-Comms</b></summary>
   Contains the code used by the Raspberry Pi to process and store sensor data received from the Arduino. </br>
</details>

<details>
<summary><b>Pi-Systems</b></summary>
   Contains code used by the Raspberry Pi to run services within the airlock. Such services may include pressurization, lighting and door management. </br>
</details>

<details>
<summary><b>Sensors</b></summary>
   Contains embedded systems code related to sensor functionality. </br>
</details>

<details>
<summary><b>User Interface (UI)</b></summary>
   Contains code and outlines of on-airlock user interface systems.</br>
</details>
