# SaltScale v1 hardware shortlist

## Frozen direction

- MCU: Seeed Studio XIAO ESP32C3
- ADC: SparkFun Load Cell Amplifier HX711
- Loadcell: true 50 kg single-point loadcell, recommended first target: Henk Maas LA360-C-50kg
- Power: 3x AA lithium cells in side-access holder; final holder still to be selected by physical size and connector
- UI: 1 momentary pushbutton + 1 low-current LED

## Notes

Do not use the cheap SparkFun/Kiwi/TinyTronics 50 kg bathroom-scale load sensor as the primary mechanical target for this round platform. It is a 3-wire half-bridge style sensor normally used in sets, not the clean single-point platform loadcell wanted for SaltScale v1.

The CadQuery model currently assumes placeholder dimensions for the Henk Maas LA360-C-50kg. Verify the datasheet before final print.
