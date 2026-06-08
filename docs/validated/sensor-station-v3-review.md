# Sensor Station v3 Review

Date: 2026-06-05

## Summary

`sensor_station_locator_v3` is a focused validation coupon for a refined `concept_v2` sensor station locator.

It does not change the overall `concept_v2` architecture:

```text
upper carrier -> upper pad -> sensor -> lower pad -> lower base
```

It also does not change the floating upper/lower platform logic. The v3 coupon only explores a better local sensor locator shape before any full platform integration.

Generated files:

- `cad/exports/validation/stl/sensor_station_locator_v3.stl`
- `cad/exports/validation/step/sensor_station_locator_v3.step`

## What changed compared to current concept_v2 station

Current `concept_v2_sensor_station` uses long, tall rectangular guide rails and an inner stop. Those rails were useful as a conservative first print, but the physical print showed they are visually and mechanically oversized for a 38 x 38 mm sensor placeholder.

`sensor_station_locator_v3` changes the station coupon by replacing those long rails with:

- Short low tangential locator tabs.
- Rounded inner locator posts.
- A short inner stop.
- Two rounded outer cradle tabs.
- Distinct taller overload stops.
- A separate printed sensor dummy for fit testing.

The locator height is about `5 mm` above the lower base top. The current concept_v2 guide walls were about `12 mm` tall. This keeps the locator well below the upper pad and upper carrier.

## How the sensor is located

The sensor placeholder is still treated as a nominal `38 x 38 x 12 mm` body.

The locator targets a cavity of about `39 x 39 mm`:

```text
sensor placeholder: 38 x 38 mm
locator cavity:     about 39 x 39 mm
nominal clearance:  about 1.0 mm total, about 0.5 mm per side
```

The features work together:

- The short side tabs constrain tangential sliding.
- The inner stop and inner rounded posts constrain inward radial motion.
- The outer rounded cradle tabs reduce rotation and gross outward wandering while leaving the center of the outer side open.
- The overload stops are separate tall cylinders outside the locator envelope.

The locator is meant to prevent sensor sliding and rotation. It is not meant to guide the upper pad.

## How the sensor is removed

The outer side remains serviceable.

The center of the outer side is open, so after removing the upper structure and upper pad, the sensor can be lifted or slid outward from the station. The outer rounded tabs are low locator/cradle features, not a cap.

The coupon includes a separate printed sensor dummy so this insertion/removal motion can be tested before buying a real sensor.

## Expected clearance

Nominal target:

- About `0.8-1.2 mm` total XY clearance around the assumed sensor envelope.
- The CAD target is about `1.0 mm` total clearance.

This is intentionally tighter than the current oversized concept_v2 guide spacing. It should reduce sensor wander while still leaving PETG print tolerance and small sensor variation allowance.

Important caveat:

The existing `concept_v2` lower contact pad is wider than the assumed sensor body. A tight sensor-shaped locator cannot be fully integrated into the full platform until the real sensor and real contact pad choice are confirmed. This v3 coupon validates the locator concept first; it does not finalize the lower pad geometry.

## Why the locator does not create a load bypass

The v3 locator does not connect the upper carrier to the lower base.

The locator features are lower-base-only geometry. They rise from the lower base and stop far below the upper pad and upper carrier:

- Lower base top: about `z = 8 mm`.
- Locator top: about `z = 13 mm`.
- Nominal upper pad bottom in current concept_v2 stack: about `z = 22 mm`.
- Upper carrier begins above the upper pad.

Because the locator does not touch the upper pad or upper carrier, it does not provide a vertical bypass around the sensor.

The overload stops remain distinct. Their purpose is still protective bypass only after excessive compression, not normal load support.

## Printability

The coupon remains support-free in the intended orientation:

- Flat lower base on the print bed.
- Locator tabs grow vertically from the base.
- Rounded locator posts are vertical cylinders.
- Overload stops are vertical cylinders.
- No trapped components.
- No underside pockets.

Estimated envelope:

```text
about 169 x 104 x 21 mm
```

This fits easily on a Prusa MK4.

## What to inspect in PrusaSlicer

Check:

- No open edges or repair warning.
- No generated supports.
- Locator tabs print as separate low features, not merged into overload stops.
- The outer side remains visibly open.
- The sensor dummy is separate from the station body on the print plate.
- Text labels do not create mesh warnings.
- First layer around rounded posts and stops is continuous.

## Remaining risk until a real sensor is purchased

The v3 coupon still assumes a generic Kiwi/SparkFun-style sensor envelope.

Unknowns:

- Actual sensor body dimensions.
- Actual cable exit shape.
- Actual contact faces and safe load area.
- Whether the final lower contact pad should be smaller, notched, metal, or otherwise shaped to fit with the tighter locator.
- Whether 1.0 mm total clearance is enough for the purchased sensor and PETG print variation.
- Whether salt debris accumulates around the rounded locator tabs.

Recommendation:

Print `sensor_station_locator_v3.stl` only as a locator validation coupon. Do not integrate it into the full platform until one real sensor and candidate contact pads have been tested.
