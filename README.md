# airlock-masters <img align="right" src="artwork/ubcmc-logo-transparent_small.png">
UBC Mars Colony airlock repository. All source code, datasheets, and other materials related to the airlock are found here.

## Naming convention

### Files
To ensure the repository is quick to navigate, all Mars Colony files follow a naming convention, which include the project, subproject, functionality, etc. Separate components using underscores, and use hypens instead of spaces. The base file name convention is below:

*Project-Module_Project-Part_Description(_Sample).codetype*.

### Folders
Folders should be broken up into logical parts, to ensure code can be found as quickly as possible. Use hyphens instead of spaces in folder names. Additionally, avoid the use of capital letters in the folder names unless absolutely necessary. For instance, the path to a CO2 Sensor file may be:

*airlock-masters/sensors/co2-sensor/sensors-co2-data-reporting/sensors-co2-data-reporting*
