# Concept v2 Review

Date: 2026-06-04

## Summary

`concept_v2` converts `concept_v1` from an architecture demonstrator into a realistic mechanical prototype candidate.

It keeps the preferred architecture:

- Four Kiwi/SparkFun style 50 kg sensors.
- One floating upper carrier.
- One separate lower floor base.
- Four replaceable sensor stations.
- No upper-to-lower fasteners.
- No electronics packaging yet.

It rejects one optimistic part of `concept_v1`: the fully open annular carrier. A pure annulus is clean and low-material, but it assumes the salt container bottom is stiff enough to span the center opening. That is not safe for a general domestic salt container. `concept_v2` adds a removable upper-only support grate. The grate supports uncertain container bottoms while remaining part of the floating upper structure, so it does not bypass the sensors.

CAD source:

- `cad/src/concept_v2.py`

Requested exports:

- `cad/exports/step/concept_v2_assembly.step`
- `cad/exports/stl/concept_v2_lower_segment_0.stl`
- `cad/exports/stl/concept_v2_upper_segment_0.stl`
- `cad/exports/stl/concept_v2_sensor_station.stl`

## Architecture

Normal load path:

```text
salt container
-> removable upper support grate and/or upper annular carrier
-> upper contact pad
-> 50 kg load sensor
-> lower contact pad
-> lower annular base
-> floor
```

`concept_v2` uses the same four-sensor measurement principle as `concept_v1`, but it adds the mechanical features needed for a real prototype:

- Four lower annular base segments.
- Four floating upper annular carrier segments.
- Four replaceable sensor stacks at 45, 135, 225, and 315 degrees.
- A removable upper support grate for center-bottom support.
- Lower-only seam bridge plates.
- Upper-only seam bridge plates.
- M3 heat-set insert pockets.
- 4 mm dowel sockets for alignment.
- Local overload stops.
- Open-sided sensor guide rails.

## Sensor realism

The model assumes a representative 38 x 38 x 12 mm sensor envelope. That matches the repository's current placeholder for Kiwi/SparkFun style 50 kg sensors, but it is not a vendor-verified final dimension.

Each sensor station includes:

- A lower contact pad.
- A sensor placeholder with an outward cable-exit tab.
- An upper contact pad.
- Tangential guide rails.
- An inner radial stop.
- An open outer side for removal.
- Four local overload stops.

The sensor is not screwed, glued, or trapped in the printed base. It is located laterally by the guide rails and vertically by the contact pad stack. In normal use, the upper carrier compresses the stack. For service, removing the upper carrier segment exposes the upper pad and sensor.

## Segment joining

### Lower ring

The lower ring segments include top-side M3 heat-set insert pockets and 4 mm dowel sockets near the radial seams. Separate lower seam bridge plates sit on the lower base only. These plates join lower-to-lower segments and never touch the upper carrier.

Purpose:

- Keep lower segments aligned on the floor.
- Resist seam spreading during handling.
- Avoid any upper-to-lower load bypass.

### Upper ring

The upper ring segments include underside M3 heat-set insert pockets and 4 mm dowel sockets. Separate upper seam bridge plates attach only to the underside of the floating upper carrier.

Purpose:

- Keep upper carrier segments aligned.
- Make the upper carrier removable as an assembly or by segment.
- Avoid hardware on the top surface where the container sits.
- Avoid any connection to the lower base.

### Dowel strategy

4 mm metal dowels are modeled as sockets, not permanent trapped pins. They should be used for alignment and repeatability, not as the primary structural clamp. M3 fasteners and bridge plates provide the clamp.

## Annular support review

`concept_v1` used an open annular upper carrier. That is attractive because it saves filament and keeps the load path visible.

For `concept_v2`, the open annulus is judged insufficient as the default prototype. The unknown is the salt container bottom. Many domestic containers have molded bottoms, feet, ribs, or flexible central regions. A 20-35 kg salt load can make an unsupported center sag, rock, or settle unevenly.

Decision: add a removable upper-only support grate.

The grate:

- Is part of the floating upper system.
- Is not connected to the lower base.
- Prints flat.
- Fits within the Prusa MK4 envelope.
- Can be removed for inspection or revised after testing.
- Supports the container center without changing the sensor architecture.

This is deliberately conservative. If physical testing proves the container bottom is rigid and only loads the perimeter, the grate can be omitted later.

## Load path review

The primary load path is clear:

- Upper parts carry load to upper pads.
- Upper pads load sensors.
- Sensors load lower pads.
- Lower pads load lower base.

Designed bypasses:

- Local overload stops engage only after approximately 1 mm of upper-pad travel.

Rejected bypasses:

- No M3 screw bridges from upper to lower.
- No dowels from upper to lower.
- No shared wall between upper and lower.
- No electronics bay ribs touching both structures.

The seam bridge plates are same-layer only: lower-to-lower or upper-to-upper.

## Printability

Measured from the current CAD:

- Full assembly envelope: about 320.0 x 320.0 x 39.0 mm.
- `concept_v2_lower_segment_0`: about 159.1 x 159.1 x 21.0 mm.
- `concept_v2_upper_segment_0`: about 153.1 x 153.1 x 14.0 mm.
- `concept_v2_sensor_station`: about 96.0 x 96.0 x 21.0 mm.
- Removable support grate: about 178.0 x 178.0 x 4.0 mm.

All listed parts fit within the Prusa MK4 200 x 200 x 200 mm envelope.

PETG-friendly choices:

- Flat lower and upper segments.
- No intentionally trapped support cavities.
- Thick guide rails.
- Simple vertical insert pockets.
- Simple cylindrical dowel sockets.
- Support grate prints flat.

Known printability caveat:

- The lower segment includes guide rails and overload stops rising from the base. These are support-free when printed flat, but their dimensional accuracy must be checked because they define sensor clearance and overload behavior.

## Why this is better than concept_v1

`concept_v1` proved the architecture. `concept_v2` adds the minimum real-world assembly features:

- Separate upper and lower segment joining.
- Heat-set insert locations.
- Dowel alignment.
- A real serviceable sensor station.
- An explicit answer to the flexible-container-bottom problem.
- A printable sensor-station coupon.

It remains simple. It avoids electronics. It does not chase cosmetic CAD.

## Why this is still not final

`concept_v2` is a prototype candidate, not release CAD.

Still missing:

- Exact purchased sensor dimensions.
- Exact metal contact pad choice.
- Screw lengths and insert part numbers.
- Dowel tolerance validation.
- Wiring strain relief.
- Salt/water protection.
- Full segmented production export set.
- Physical calibration data.

## Recommendation

Proceed to physical validation with `concept_v2_sensor_station.stl` first. Do not print the full four-segment assembly until one station proves sensor fit, pad seating, overload clearance, and repeatability.
