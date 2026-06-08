# Hardware Bring-Up v0

Date: 2026-06-05

## Summary

This is the first electronics validation workflow for SaltScale after the first hardware order.

The goal is not to build product firmware. The goal is only to prove that four load sensors, the SparkFun Load Sensor Combinator, the SparkFun HX711, and the Seeed Studio XIAO ESP32C3 can produce sensible raw readings over USB serial.

Important source-of-truth note: `hardware/loadcell-spec.md` and the redesign documents describe the current four-sensor architecture. `hardware/bom.md` still contains older single-point-loadcell assumptions and should not guide this bring-up.

## Expected hardware

- 5x 50 kg Kiwi/SparkFun-style load sensors.
- SparkFun Load Sensor Combinator.
- SparkFun HX711 load cell amplifier.
- Seeed Studio XIAO ESP32C3.
- USB-C data cable.
- Connector cables or temporary jumper wiring.
- Optional button and LED, not used yet.

Use four sensors for the first bridge. Keep the fifth sensor as a spare and dimensional reference.

## 1. Bench setup overview

Build the first electronics stack on the bench, separate from the printed platform:

```text
4x load sensors
-> SparkFun Load Sensor Combinator
-> SparkFun HX711
-> XIAO ESP32C3
-> computer over USB-C
-> serial monitor
```

Do the first test with sensors loose on the bench or lightly held in a simple test fixture. Do not install the electronics into an enclosure, scale body, or utility-closet location yet.

Recommended bench conditions:

- Clean, dry table.
- USB power only.
- Short sensor wires where practical.
- No battery connected.
- No salt container on the sensors.
- No button or LED connected.
- One wiring change at a time.

## 2. Wiring plan

### Four load sensors to combinator

Wire four 50 kg load sensors into the SparkFun Load Sensor Combinator according to the combinator board labels and SparkFun wiring guide.

Conceptually:

- One sensor per combinator corner/input.
- Keep sensor orientation consistent.
- Route all four sensors the same way if possible.
- Leave the fifth sensor unconnected as a spare.

Before powering anything:

- Check that no bare wire strands bridge adjacent pads.
- Check that each sensor has strain relief during bench handling.
- Label sensors `S1`, `S2`, `S3`, and `S4` with tape.
- Record which physical sensor is connected to each combinator input.

### Combinator to HX711

Wire the combinator bridge output to the HX711 input.

Use the board labels rather than wire color assumptions. Typical bridge labels are:

```text
Combinator E+  -> HX711 E+
Combinator E-  -> HX711 E-
Combinator S+  -> HX711 A+
Combinator S-  -> HX711 A-
```

Use HX711 channel A for the first test. Do not use channel B yet.

### HX711 to XIAO ESP32C3

Power the HX711 from the XIAO so signal levels match the microcontroller:

```text
HX711 VCC -> XIAO 3V3
HX711 GND -> XIAO GND
HX711 DT  -> XIAO digital input pin
HX711 SCK -> XIAO digital output pin
```

Suggested first firmware pin mapping:

```text
HX711 DT  -> XIAO D2
HX711 SCK -> XIAO D3
```

This mapping is only a bring-up default. Verify the XIAO ESP32C3 pinout before soldering or making a permanent harness.

### XIAO to computer over USB-C

Connect the XIAO ESP32C3 to the computer with a USB-C data cable.

Confirm the board appears as a serial device before connecting the sensor bridge. Charge-only USB-C cables are a common failure mode.

## 3. Power and safety warnings

Do not use battery power yet.

First bring-up rules:

- Power the XIAO from USB-C only.
- Power the HX711 from the XIAO `3V3` pin.
- Do not connect a battery.
- Do not connect a charger module.
- Do not connect the optional button.
- Do not connect the optional LED.
- Do not connect Wi-Fi or network services in firmware.
- Disconnect USB before rewiring the sensor bridge.

If any board becomes hot, unplug USB immediately and inspect wiring.

## 4. First test firmware goal

The first firmware should do only this:

- Initialize the HX711.
- Read raw HX711 values.
- Print raw values over USB serial.
- Optionally print a simple running average.

Explicitly do not include:

- Wi-Fi.
- Deep sleep.
- Battery measurement.
- MQTT.
- Calibration factor.
- Tare persistence.
- Salt percentage calculation.
- Button handling.
- LED status behavior.

Good first output is boring:

```text
raw: 8421310
raw: 8421288
raw: 8421362
```

The absolute number does not matter yet. Direction, stability, and sensor contribution matter.

## 5. Test procedure

### Step 1: visual inspection

Before USB power:

1. Confirm all four sensors are connected to the combinator.
2. Confirm combinator bridge output goes to HX711 channel A.
3. Confirm HX711 power is from XIAO `3V3` and `GND`.
4. Confirm HX711 `DT` and `SCK` go to the selected XIAO digital pins.
5. Confirm no optional button, LED, battery, or charger is connected.

### Step 2: no-load serial reading

1. Connect the XIAO to the computer over USB-C.
2. Open the serial monitor.
3. Confirm raw values appear.
4. Leave the bench untouched for 30-60 seconds.
5. Watch whether the values are roughly stable.

Expected result:

- Values should update continuously.
- Small noise is normal.
- Large jumps without touching anything indicate wiring, power, or mechanical instability.

### Step 3: press each sensor by hand

Press each sensor gently, one at a time:

1. Press `S1`, release, observe raw value change.
2. Press `S2`, release, observe raw value change.
3. Press `S3`, release, observe raw value change.
4. Press `S4`, release, observe raw value change.

Expected result:

- Every sensor should affect the reading.
- Similar presses should produce the same sign of change.
- The magnitude does not need to match perfectly during hand tests.

### Step 4: check sign and direction

Choose one direction as positive for the first notes. For example:

```text
pressing down should increase raw value
```

If pressing down decreases raw value, that is not automatically a failure. The sign can be corrected later in firmware or by swapping signal polarity, but all four sensors should agree.

### Step 5: combined contribution check

Press two or more sensors at the same time.

Expected result:

- Combined pressing should create a larger change than pressing one sensor alone.
- If one sensor has no effect, troubleshoot before moving on.

### Step 6: document results

Record:

- Sensor labels and combinator inputs.
- HX711-to-XIAO pin mapping.
- No-load raw range.
- Direction of each sensor response.
- Any sensor that behaves differently.
- Photos of the wiring.

## 6. Troubleshooting

### No serial output

Likely causes:

- USB-C cable is charge-only.
- Wrong serial port selected.
- Board not flashed.
- Serial baud rate mismatch.
- XIAO not powered.

Checks:

- Try another USB-C data cable.
- Confirm the XIAO appears as a serial device.
- Upload a minimal serial test before involving HX711 code.

### Serial output appears, but no HX711 signal

Likely causes:

- HX711 `DT` or `SCK` pins swapped or mapped incorrectly.
- HX711 not powered.
- No common ground.
- Firmware pin definitions do not match wiring.

Checks:

- Measure HX711 `VCC` to `GND`.
- Confirm `DT` and `SCK` wiring against firmware.
- Confirm the HX711 board is connected to XIAO `GND`.

### Raw value stuck at one number

Likely causes:

- HX711 not ready.
- `DT` line stuck.
- Wrong GPIO selected.
- Broken jumper.

Checks:

- Try different XIAO GPIO pins.
- Re-seat jumpers.
- Inspect solder joints.

### Inverted signal

Likely causes:

- Bridge signal polarity is reversed.
- Sensor orientation differs from the assumed direction.

Checks:

- If all four sensors respond with the same inverted direction, note it and continue.
- If only one sensor is inverted, inspect that sensor's combinator input wiring and orientation.

Do not solve sign direction with calibration logic yet. First make all four sensors contribute consistently.

### Noisy signal

Likely causes:

- Loose bench wiring.
- Long unshielded sensor wires.
- Moving wires during measurement.
- USB power noise.
- Mechanically unstable sensors.

Checks:

- Keep wires still.
- Shorten temporary wiring where practical.
- Keep sensor wires away from USB and power wires.
- Use a simple average in the serial printout for readability.
- Test with the sensors resting on a firm surface.

### One sensor not contributing

Likely causes:

- Open sensor wire.
- Bad connector.
- Wrong combinator pad.
- Sensor damaged.
- Sensor connected with reversed or missing lead.

Checks:

- Move the suspect sensor to another combinator input.
- Move a known-good sensor to the suspect input.
- Inspect connector continuity.
- Use the fifth sensor as a substitute if needed.

Do not proceed to platform integration until all four active sensors affect the raw reading.

## 7. Pass criteria for bring-up v0

Bring-up v0 passes when:

- XIAO is powered over USB-C.
- HX711 is powered from XIAO `3V3`.
- Raw readings print over serial.
- No-load readings are reasonably stable on the bench.
- Pressing each of the four sensors changes the raw value.
- All four sensors have the same sign convention.
- Combined sensor presses produce a larger response than a single press.
- Wiring and pin mapping are documented.

## 8. What not to do yet

Do not do these during bring-up v0:

- No battery power.
- No battery optimization.
- No deep sleep.
- No enclosure electronics.
- No electronics mounting in the printed platform.
- No MQTT.
- No Wi-Fi.
- No final calibration.
- No salt-container fill estimate.
- No button or LED integration.
- No long-term unattended testing.

Only after raw readings are trustworthy should the project move to calibration, low-power firmware, enclosure planning, or platform-integrated electronics.
