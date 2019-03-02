The modular_integrated_sensors software uses a bitmask to determine indicate valid data for the pi.

The format of the bitmask is as indicated below, starting from the leftmost (high) bit.

1. O2 (Percent)
2. Humidity (Percent)
3. Temperature (degrees Celsius)
4. Pressure (dekaPascals, Barometric)
5. CO2 (Parts per Million)
