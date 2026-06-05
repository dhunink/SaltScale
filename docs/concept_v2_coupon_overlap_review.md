# Concept v2 Coupon Overlap Review

Date: 2026-06-05

## Summary

The reported `UPPER PAD` and `SENSOR DUMMY` overlap was caused by the printable coupon layout, not by the `concept_v2` architecture.

The overlap existed in the labeled multi-body print-kit coupon:

- `sensor_station_coupon_v2`

The same layout issue also existed in:

- `upper_lower_stack_coupon_v1`

It did not exist in the actual `concept_v2` assembled load stack.

## What caused the overlap

The coupon exports place separate printable bodies on one print plate. In the previous layout, the `UPPER PAD` body was placed too close to the `SENSOR DUMMY`.

Previous `sensor_station_coupon_v2` layout:

```text
SENSOR DUMMY center: (52, 8)
UPPER PAD center:    (52, 48)
```

The sensor dummy is about `38 x 38 mm`, plus a cable-exit tab. The upper pad is `56 x 56 mm`.

That means:

- Sensor dummy Y range was about `-11..27 mm`.
- Upper pad Y range was about `20..76 mm`.
- The bodies overlapped by about `7 mm` in Y.
- Because both bodies were exported flat on the build plate, their Z ranges also overlapped.

This created real overlapping STL volume in the print-kit export.

## Was concept_v2 itself affected?

No.

In `concept_v2.py`, the real assembly stack is vertical:

```text
lower pad:   z 8..10 mm
sensor:      z 10..22 mm
upper pad:   z 22..25 mm
```

Those parts touch at the intended interfaces but do not overlap in volume.

The unlabeled `concept_v2_sensor_station` export is also not the source of the pad/sensor overlap. It is the station base coupon only. The overlap was in the labeled validation kit that includes the dummy pad and sensor pieces.

## Which body should move

The `UPPER PAD` should move.

Reason:

- The sensor dummy position is useful as a reference for the dummy sensor and cable-exit shape.
- The lower pad already had adequate clearance from the dummy sensor.
- Moving the upper pad is only a print-plate layout change.
- It does not change pad size, sensor dummy size, station geometry, clearances, or load path.

## Export strategy

For physical validation, these parts must be separate printable bodies:

- `LOWER PAD`
- `SENSOR DUMMY`
- `UPPER PAD`

The coupon STL should remain a print-kit layout, not a pre-assembled visualization.

A pre-assembled stack would be useful for visual review, but it would be wrong for first physical validation because it would:

- Fuse or overlap bodies if exported as one STL.
- Prevent measuring individual dummy parts.
- Prevent testing insertion/removal by hand.
- Hide whether the stack can be assembled in the intended service sequence.

Decision:

- Keep coupon exports as separated printable bodies.
- Move bodies farther apart on the print plate.
- Do not change the `concept_v2` architecture.

## CAD fix

Updated `cad/src/concept_v2_interface_coupons.py`.

Changes:

```text
sensor_station_coupon_v2:
  UPPER PAD moved from (52, 48) to (52, 82)

upper_lower_stack_coupon_v1:
  UPPER PAD moved from (58, 58) to (70, 58)
```

No functional dimensions changed.

No pad, sensor dummy, station, guide, stop, seam, or carrier geometry changed.

## Post-fix geometry check

`sensor_station_coupon_v2` body ranges:

```text
station:      x -92..4    y -48..48    z 0..21
lower pad:    x 30..74    y -56..-12   z 0..2
sensor dummy: x 33..87    y -11..27    z 0..12
upper pad:    x 24..80    y 54..110    z 0..3
```

There is now clear XY separation between the sensor dummy and upper pad.

`upper_lower_stack_coupon_v1` body ranges:

```text
lower station: x -100..-4  y -70..26   z 0..21
upper patch:   x 17..95    y -71..7    z 0..8
lower pad:     x -74..-30  y 36..80    z 0..2
sensor dummy:  x -19..35   y 39..77    z 0..12
upper pad:     x 42..98    y 30..86    z 0..3
```

The sensor dummy and upper pad now have about `7 mm` XY clearance.

## Recommendation

Use the labeled coupon exports as physical validation print kits:

```text
cad/exports/validation/stl/sensor_station_coupon_v2.stl
cad/exports/validation/stl/upper_lower_stack_coupon_v1.stl
```

Do not use a pre-assembled STL for first validation of the pad/sensor stack.
