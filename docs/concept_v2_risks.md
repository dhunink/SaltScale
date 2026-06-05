# Concept v2 Risks

Date: 2026-06-04

## What is still uncertain

### Sensor dimensions

The CAD assumes a 38 x 38 x 12 mm sensor placeholder. Real Kiwi/SparkFun style 50 kg sensors may differ in body size, contact face, cable exit, and safe loading region.

Impact:

- Pocket clearance may be wrong.
- Guide rails may touch the sensor body.
- Contact pads may not align with the intended sensing region.

### Sensor loading behavior

Cheap bathroom-scale sensors are not always documented well. The exact intended compression/contact faces need to be confirmed with the purchased part.

Impact:

- Pads may load the wrong part of the sensor.
- Readings may be nonlinear.
- Sensors may be vulnerable to side loading.

### Contact pad material

The CAD shows generic pads. Printed PETG pads may creep or wear under continuous load.

Impact:

- Calibration drift.
- Poor repeatability after removing/reinstalling the salt container.

Preferred prototype direction:

- Test printed pads only as fit placeholders.
- Use metal washers or small metal plates for real measurement tests.

### Annular support and removable grate

`concept_v2` adds a removable upper support grate because the salt container bottom is unknown. The actual container may not need it, or it may need a different support pattern.

Impact:

- Without the grate, the container bottom may sag.
- With the grate, load may concentrate through the central support pattern if the bottom is uneven.

### Seam hardware

M3 insert pockets and 4 mm dowel sockets are modeled, but no exact insert, screw length, washer, or dowel tolerance is selected.

Impact:

- Inserts may be loose or split PETG.
- Dowel sockets may be too tight or too loose.
- Seam bridge plates may need different thickness or screw access.

### Overload stop clearance

The target is approximately 1 mm clearance before stop contact. Real printed Z tolerances, pad thickness, and sensor height variation can easily consume that margin.

Impact:

- Stops may touch during normal use and bypass sensors.
- Stops may sit too low and fail to protect sensors.

### Salt and moisture exposure

The CAD does not yet include drainage, sealing, or corrosion protection.

Impact:

- Sensor corrosion.
- Pad corrosion.
- Salt debris in pockets.
- Increased friction and sensor side loading.

## What should be physically tested first

Test `concept_v2_sensor_station.stl` before printing any full ring segments.

First test set:

1. Print `concept_v2_sensor_station.stl`.
2. Print or prepare lower and upper contact pads.
3. Install one real 50 kg sensor.
4. Check insertion/removal from the open outer side.
5. Check guide clearance with feeler gauges or paper strips.
6. Measure upper pad to overload stop clearance.
7. Apply 5 kg, 10 kg, and 20 kg loads.
8. Remove and reinstall the sensor three times.
9. Repeat measurements after reinstalling.

Second test set:

1. Print `concept_v2_lower_segment_0.stl`.
2. Print `concept_v2_upper_segment_0.stl`.
3. Check that the upper segment seats on the upper pad and not on guide rails/stops.
4. Confirm no upper-to-lower accidental contact.
5. Test one assembled quadrant with a known weight.

Third test set:

1. Print the removable support grate.
2. Place the actual salt container on the upper carrier/grate.
3. Check whether the container bottom contacts ring, grate, or both.
4. Repeat with partial and full salt load if safe.

## Assumptions that remain

- Four sensors wired into one HX711 bridge are acceptable for the required fill-level accuracy.
- A 320 mm outer footprint is acceptable in the installation location.
- The salt container can be removed for service.
- PETG is acceptable for long-term utility-closet loading if metal pads are used.
- The user can install heat-set inserts accurately.
- A 4 mm dowel slip fit is achievable after tuning print holes.
- The support grate is acceptable even if it adds one extra upper part.

## Go/no-go criteria for continuing

Continue to full-ring prototype only if:

- Sensor can be inserted and removed without force.
- Upper pad does not bind in the guide rails.
- Overload stops do not touch during normal load tests.
- Repeated sensor removal/reinstall changes readings only within acceptable prototype tolerance.
- One quadrant test shows stable readings over at least several hours under load.
- The real salt container bottom is supported without rocking.

Stop and revise if:

- Sensor pocket requires prying to remove the sensor.
- Stops touch under ordinary loading.
- PETG pad surfaces visibly dent or polish after short testing.
- Dowel insertion cracks seam bosses.
- The support grate carries load unevenly or causes rocking.
- Salt debris can fall directly into sensor contact areas.
