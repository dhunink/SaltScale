# Concept v3 Print-Optimized Candidate

Date: 2026-06-06

## Summary

`concept_v3_print_optimized` is a print-efficiency candidate derived from the active `concept_v2` architecture. It is not a redesign of the measurement principle. It keeps the four-sensor floating upper/lower architecture and changes only the printable decomposition where that appears likely to reduce print plates.

The main changes are:

- 8 upper ring sectors instead of 4.
- 8 lower ring sectors instead of 4.
- Four alternating lower sectors include sensor stations.
- Four alternating upper sectors include sensor contact lands.
- The support grate is split into two half-lap bars instead of one cross-shaped part.

## What Stayed The Same

- Four load sensors.
- Floating upper carrier over lower base.
- Upper and lower remain mechanically separate.
- No upper-to-lower fasteners or bridges.
- Captured M3 nuts plus printed bridge plates remain the default segment joining method.
- Support-grate tab/slot clearance remains `0.4 mm per side`.
- v3-style low sensor locator remains the sensor-station direction.
- Engraved labels remain the default.
- Sensors remain serviceable from the outside after upper parts are lifted or removed.

## Printable Parts

Active concept v3 STLs:

- `cad/exports/active/stl/concept_v3_lower_sensor_segment_0.stl`
- `cad/exports/active/stl/concept_v3_lower_plain_segment_1.stl`
- `cad/exports/active/stl/concept_v3_upper_sensor_segment_0.stl`
- `cad/exports/active/stl/concept_v3_upper_plain_segment_1.stl`
- `cad/exports/active/stl/concept_v3_support_grate_bar_x.stl`
- `cad/exports/active/stl/concept_v3_support_grate_bar_y.stl`
- `cad/exports/active/stl/concept_v3_lower_bridge_plate.stl`
- `cad/exports/active/stl/concept_v3_upper_bridge_plate.stl`
- `cad/exports/active/stl/concept_v3_lower_pad.stl`
- `cad/exports/active/stl/concept_v3_upper_pad.stl`
- `cad/exports/active/stl/concept_v3_sensor_placeholder.stl`

Repeat counts for a full mechanical prototype:

- 4x lower sensor segments.
- 4x lower plain segments.
- 4x upper sensor segments.
- 4x upper plain segments.
- 8x lower bridge plates.
- 8x upper bridge plates.
- 4x lower pads.
- 4x upper pads.
- 4x sensors or placeholders.
- 1x support grate bar X.
- 1x support grate bar Y.

## Approximate Part Dimensions

Measured from CAD bounding boxes:

| Part | Approximate envelope |
| --- | ---: |
| Lower sensor segment | 108 x 113 x 21 mm |
| Lower plain segment | 111 x 108 x 8 mm |
| Upper sensor segment | 102 x 107 x 14 mm |
| Upper plain segment | 107 x 102 x 14 mm |
| Support grate bar X | 178 x 22 x 4 mm |
| Support grate bar Y | 22 x 178 x 4 mm |
| Bridge plates | 64 x 30 x 4 mm |

## Expected Plate Count

`concept_v2` likely needs about 9 practical large-part plates: four lower, four upper, and one support grate.

`concept_v3` should be closer to about 6 practical plates if the slicer can place two to three sectors per bed and nest the support-grate bars and small parts into remaining space. This depends on brim settings, PETG spacing, and user comfort with multi-part plates.

## Assembly Logic

The full ring alternates segment types:

```text
lower sensor, lower plain, lower sensor, lower plain, ...
upper sensor, upper plain, upper sensor, upper plain, ...
```

Each sensor lower segment has the low-profile sensor locator. Each matching upper sensor segment has the upper contact land. Plain segments are structural ring continuation pieces.

The support grate uses two bars with a center half-lap. Both bars are upper-only. They must never contact the lower base.

## Assembly Order

1. Print sensor and plain lower segments.
2. Press captured M3 nuts into lower segments from the underside.
3. Assemble the lower ring with lower-only bridge plates and M3 bolts.
4. Place lower pads, sensors, and upper pads in the four sensor stations.
5. Print sensor and plain upper segments.
6. Press captured M3 nuts into upper segments from the top side.
7. Assemble the upper ring separately with underside upper-only bridge plates and M3 bolts.
8. Install the two support-grate bars into the upper-only receivers.
9. Lower the upper ring assembly onto the four upper pads.
10. Confirm that upper and lower parts touch only through the sensor stacks in normal unloaded assembly.

## Verification Checks Already Done In CAD

Quick boolean checks on the initial v3 CAD showed:

- Support grate bar X vs upper sensor segment: `0.0 mm^3` overlap.
- Support grate bar Y vs upper sensor segment: `0.0 mm^3` overlap.
- Support grate bar X vs lower sensor segment: `0.0 mm^3` overlap.
- Upper sensor segment vs lower sensor segment: `0.0 mm^3` overlap.
- Support grate bar X vs bar Y half-lap: `0.0 mm^3` overlap.

## Risks

- More seams and fasteners than concept_v2.
- More parts to sort and orient.
- Smaller segments may be less self-aligning during assembly.
- Split support grate needs physical validation.
- Bridge plate behavior at eight seams is not yet physically validated as a full ring.

## Recommendation

Inspect this candidate before printing:

```text
cad/exports/active/step/concept_v3_one_section_assembly.step
```

If it looks coherent, inspect these STLs in PrusaSlicer:

```text
cad/exports/active/stl/concept_v3_lower_sensor_segment_0.stl
cad/exports/active/stl/concept_v3_upper_sensor_segment_0.stl
cad/exports/active/stl/concept_v3_support_grate_bar_x.stl
```

Do not retire `concept_v2` until one v3 sensor section and one v3 seam pair are physically checked.
