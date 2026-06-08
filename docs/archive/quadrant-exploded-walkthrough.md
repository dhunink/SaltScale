# Quadrant Exploded Walkthrough

Date: 2026-06-06

## Purpose

`concept_v2_one_quadrant_exploded.step` is a true exploded view of one `concept_v2` quadrant. It is a visual assembly reference, not a print plate.

The view separates the printed parts in the order a builder should understand them:

```text
support grate
upper segment
upper pad
sensor / placeholder
lower pad
lower segment
```

It also separates the lower and upper bridge plates and shows M3 bolt/nut marker geometry at the seam holes.

## Export

```text
cad/exports/active/step/concept_v2_one_quadrant_exploded.step
```

This STEP is for inspection in a CAD viewer. Slice the individual STLs in `cad/exports/active/stl/` instead.

## Printed Separately

Printed active parts represented in the exploded quadrant:

- `concept_v2_lower_segment_0.stl`
- `concept_v2_lower_pad.stl`
- `concept_v2_sensor_placeholder.stl` for validation only, replaced by a real sensor later
- `concept_v2_upper_pad.stl`
- `concept_v2_upper_segment_0.stl`
- `concept_v2_support_grate.stl`
- `concept_v2_lower_bridge_plate.stl`
- `concept_v2_upper_bridge_plate.stl`

The STEP also includes simple M3 bolt and nut visual markers. Those are not printed SaltScale parts.

## Assembly Order

1. Place the lower segment on the bench with the sensor station facing up.
2. Press standard M3 nuts into the lower segment captured pockets from the underside.
3. Fit the lower bridge plates over the lower seams.
4. Insert M3 bolts from above through the lower bridge plates into the captured nuts.
5. Place the lower pad in the sensor station.
6. Place the sensor or placeholder on the lower pad, with the cable exit facing outward.
7. Place the upper pad on top of the sensor.
8. Press standard M3 nuts into the upper segment captured pockets from the top side.
9. Fit the upper bridge plates to the underside of the upper seams.
10. Insert M3 bolts from below through the upper bridge plates into the captured nuts.
11. Place the support grate into the upper carrier. Use `0.4 mm per side` as the current default clearance. If the full upper carrier still feels too loose, test self-centering/tapered locator geometry later rather than loosening this default.
12. Lower the upper carrier assembly onto the upper pad.

## Where The Sensor Sits

The sensor sits between the lower pad and upper pad:

```text
upper segment
upper pad
sensor
lower pad
lower segment
```

The lower segment locator features only prevent sliding and rotation. They must not touch the upper pad or upper segment.

The sensor is removable from the outside after the upper segment and upper pad are lifted away.

## Where M3 Nuts Go

Lower seam nuts:

- Press into captured pockets in the lower segment.
- Enter from the underside of the lower segment.
- Do not touch the upper segment.

Upper seam nuts:

- Press into captured pockets in the upper segment.
- Enter from the top side of the upper segment.
- Do not touch the lower segment.

## Where M3 Bolts Go

Lower seam bolts:

- Insert from above.
- Pass through the lower bridge plate.
- Pass through lower segment clearance holes.
- Thread into captured nuts underneath the lower segment.

Upper seam bolts:

- Insert from below.
- Pass through the upper bridge plate.
- Pass through upper segment clearance holes.
- Thread into captured nuts on the top side of the upper segment.

## What Touches What

Normal load path:

```text
container
-> support grate / upper carrier
-> upper pad
-> sensor
-> lower pad
-> lower segment
-> floor
```

Same-layer seam hardware:

- Lower bridge plates touch only lower segments.
- Upper bridge plates touch only upper segments.
- M3 bolts and nuts clamp only their own layer.

## What Must Never Touch

The following must never connect upper to lower during normal operation:

- bridge plates
- M3 bolts
- M3 nuts
- sensor locator tabs
- support grate
- upper segment ribs or lips
- lower segment walls or overload stops

Overload stops are the only intentional upper-to-lower contact, and they should engage only after the designed overload clearance is consumed. If the upper segment or upper pad touches locator features or stops in normal unloaded assembly, the scale can bypass the sensors and give wrong readings.

## Inspection Checklist

In the exploded STEP, verify:

- Lower pad, sensor, and upper pad are aligned over the lower sensor station.
- The sensor cable exit points outward.
- Lower bridge plates are lower-only.
- Upper bridge plates are upper-only.
- M3 nut markers sit on the correct side of each segment.
- M3 bolt markers approach from the correct side.
- No hardware crosses the air gap between lower base and upper carrier.


## Upper Seam Service Note

The active design keeps underside upper bridge plates. This is the mechanically safer/simple choice for now because it keeps upper seam hardware upper-only and leaves the top surface available for the support grate and salt container.

A single upper segment is not meant to be loosened while the upper carrier is sitting on the sensor stack. For upper-segment service, remove the container and support grate, lift the upper carrier assembly, then access the underside bridge bolts on the bench.
