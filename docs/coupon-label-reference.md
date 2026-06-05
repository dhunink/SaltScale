# Coupon Label Reference

Date: 2026-06-05

## Summary

The `concept_v2` interface coupons now include engraved identification labels on top-facing surfaces.

The labels are for physical validation only. They do not change the intended mechanical dimensions, clearances, load paths, or assembly concept.

Engraving note:

- Implemented engraving depth: `0.6 mm`.
- Text height: about `3.6-4.5 mm`, depending on available part area.
- A literal `6 mm` engraving would cut through the 2 mm lower pad, 3 mm seam bridge plates, and 4 mm grate tab, so it would alter or destroy validation geometry. The shallow engraving keeps the labels readable in PETG while preserving the coupon interfaces.

## sensor_station_coupon_v2

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Sensor station base | `LOWER BASE`, `OVERLOAD STOP`, `INSIDE`, `OUTSIDE` | Identifies the lower structure, shows which side is inward/outward, and calls out the stop features during clearance checks. |
| Lower pad dummy | `LOWER PAD` | Prevents mixing the lower pad with the larger upper pad during stack tests. |
| Sensor dummy | `SENSOR DUMMY` | Makes the dummy sensor easy to identify when testing insertion and cable-exit orientation. |
| Upper pad dummy | `UPPER PAD` | Prevents pad mixups during overload-gap and stack-height checks. |

## upper_lower_stack_coupon_v1

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Sensor station base | `LOWER BASE`, `OVERLOAD STOP`, `INSIDE`, `OUTSIDE` | Keeps orientation clear while checking upper-to-lower non-contact. |
| Upper carrier patch | `UPPER CARRIER`, `FRONT` | Identifies the floating upper piece and gives a repeatable orientation during paper-strip clearance tests. |
| Lower pad dummy | `LOWER PAD` | Confirms the first pad in the stack. |
| Sensor dummy | `SENSOR DUMMY` | Confirms the dummy sensor block and cable-tab side. |
| Upper pad dummy | `UPPER PAD` | Confirms the top pad in the stack. |

## lower_seam_coupon_v1

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Lower seam block A | `LOWER`, `M3 INSERT`, `DOWEL TEST` | Identifies the lower-ring coupon body and separates insert-pocket checks from dowel-fit checks. |
| Lower seam block B | `LOWER`, `M3 INSERT`, `DOWEL TEST` | Mirrors the other lower seam edge for alignment and clamp tests. |
| Lower seam bridge plate | `LOWER BRIDGE`, `M3 + DOWEL` | Identifies the separate lower-only bridge plate and the combined screw/dowel interface. |

## upper_seam_coupon_v1

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Upper seam block A | `UPPER`, `M3 INSERT`, `DOWEL TEST` | Identifies the upper-ring underside coupon body and shows the insert/dowel test regions. |
| Upper seam block B | `UPPER`, `M3 INSERT`, `DOWEL TEST` | Mirrors the other upper seam edge for repeatability checks. |
| Upper seam bridge plate | `UPPER BRIDGE`, `M3 + DOWEL` | Identifies the separate upper-only bridge plate and avoids confusing it with the lower bridge coupon. |

## support_grate_fit_coupon_v1

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Upper carrier grate receiver | `UPPER CARRIER`, `SLOT` | Identifies the upper-only carrier section and the removable grate interface under test. |
| Grate tab | `TAB` | Makes the removable grate piece obvious during fit and removal trials. |

## centering_lip_coupon_v1

Printed parts:

| Part | Labels | Why useful |
| --- | --- | --- |
| Centering lip coupon | `CENTERING LIP`, `INSIDE`, `OUTSIDE` | Identifies the curved lip and shows which face should be checked against the salt container wall. |

## Validation use

During physical testing:

- Keep the labels visible when laying out parts.
- Use `INSIDE` and `OUTSIDE` markers to keep sensor-station and lip orientation consistent.
- Use `M3 INSERT` and `DOWEL TEST` labels to record measurements against the correct feature.
- Use pad and sensor labels to avoid assembling the dummy stack in the wrong order.
