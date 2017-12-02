# Lighting
All airlock lighting is controlled by the Pi. Lighting dynamically changes based on the current state of the airlock.

## Details

### Light Identifiers
Lights will be controlled by a LightScheme object, which specifies how the lights should be turned on. LightScheme elements are manipulated in the generate_light_scheme() inside manager.py.

A full list of light identifiers is included below:

<details>
  <summary>Light Identifiers</summary>
  • OVERHEAD_1<br/>
  • OVERHEAD_2<br/>
  • DOOR_COLN1<br/>
  • DOOR_MARS1<br/>
</details>