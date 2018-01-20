# airlock-masters <img align="right" src="artwork/ubcmc-logo-transparent_small.png">
UBC Mars Colony airlock repository. All source code, datasheets, and other materials related to the airlock are found here.

## Naming convention

### Files
To ensure the repository is quick to navigate, all Mars Colony files follow a naming convention, which include the project, subproject, functionality, etc. Separate components using underscores, and use hypens instead of spaces. The base file name convention is below:

*Project-Module_Project-Part_Description(_Sample).codetype*.

### Folders
Folders should be broken up into logical parts, to ensure code can be found as quickly as possible. Use hyphens instead of spaces in folder names. Additionally, avoid the use of capital letters in the folder names unless absolutely necessary. For instance, the path to a CO2 Sensor file may be:

*airlock-masters/sensors/co2-sensor/sensors-co2-data-reporting/sensors-co2-data-reporting*

## Directories
#### Artwork
Contains all visuals used in the repository. See wiki for information on how to use them.


#### Documentation
Contains documentation, datasheets and more for hardware and software used in the project.


#### Failsafe
Contains the code used to process sensor data on the Arduino board and send it via I2C to the main Raspberry Pi system. 


#### Lighting
Contains code and data about lighting systems in the airlock.


#### Motors
Contains code and data about the motors in the airlock.


#### Pi-Comms
Contains the code used by the Raspberry Pi to process and store sensor data received from the Arduino.


#### Pi-Systems
Contains code used by the Raspberry Pi to run services within the airlock. Such services may include pressurization, lighting and door management.


#### Sensors
Contains embedded systems code related to sensor functionality.

#### UI
Contains code and outlines of on-airlock user interface systems.
