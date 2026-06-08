# Concept v4 Integrated Joining

Date: 2026-06-07

## Summary

`concept_v4_integrated_joining` is the current assembly-simplification candidate. It keeps the SaltScale four-sensor floating architecture but removes separate printed bridge plates. Same-layer M3 lugs are integrated directly into the upper and lower ring segments.

This is not a release baseline until the integrated seam coupons are physically tested.

## Architecture Preserved

Concept v4 keeps:

- Four load sensors.
- Floating upper carrier over lower base.
- Upper and lower mechanically separate.
- No upper-to-lower fasteners, ribs, locators, clips, or bridges.
- Standard M3 bolts and captured standard M3 nuts.
- No heat-set inserts.
- No metal dowels.
- Support-grate clearance at `0.4 mm per side`.
- Sensor locator v3 direction.
- Engraved labels only.

## Integrated Seam Strategy

Each segment has two seam roles:

- The outgoing seam has integrated M3 lap lugs.
- The receiving seam has M3 clearance holes and captured nut pockets.
- The receiving seam also has a printed socket for the neighboring locator tongue.

The M3 bolts clamp the seam. They are no longer intended to locate the segment position.

## Fastener Assumption

The current v4 seam assumes M3 button-head screws, similar to ISO 7380 geometry.

Modeled assumption:

- Button-head diameter: `5.7 mm`.
- Button-head height: `1.8 mm`.
- Counterbore/recess diameter: `6.4 mm`.
- Upper recess depth: `2.0 mm`.

Reason:

- A button-head screw is shorter than a socket-head cap screw.
- It can be recessed into the upper carrier top side without interfering with the support grate or salt container contact area.

## Fastener Orientation

Lower ring:

```text
bolt head above -> lower integrated lug -> neighboring lower segment -> captured nut below
```

The lower visual bolt shaft points downward from the top-side head seat into the underside captured nut. The lower captured nut visual sits in the underside nut pocket.

Upper ring:

```text
bolt head above, recessed -> upper segment -> integrated underside lug -> captured nut below
```

The upper seam is now top-access for serviceability. The M3 button head sits in a top-side recess from `z = 31.2..33.0 mm`, flush with the upper carrier top surface. The shaft points downward into a captured nut in the underside lug at about `z = 21.85..24.25 mm`.

Visual M3 nuts include center holes so the bolt shaft and nut are represented as compatible physical hardware instead of overlapping solid placeholders.

## Upper Pad Locator

Decision: use the accepted Round Cup carrier-relative upper-pad locator.

The rejected concepts have been removed from active v4:

- Through-hole boss/socket through the upper carrier.
- Sensor-relative upper pad locator.
- Small underside locator tabs.

Current active method:

- The upper pad is a separate removable round printed part.
- Upper pad diameter: `56.0 mm`.
- The upper carrier has one broad circular underside cup/rim around the pad.
- Cup clearance target: `0.45 mm per side`.
- The cup/rim is upper-only and never touches the lower base, lower pad, sensor, or overload stops.
- The cup/rim prints as broad bottom-starting geometry in the current upper segment orientation; it is not a through-hole and does not use small tabs.
- No fasteners retain the pad.
- No text is placed on pad contact faces.

The vertical load path remains:

```text
upper carrier -> removable round upper pad -> sensor -> lower pad -> lower base
```

## Locator Geometry

Concept v4 now uses a printed tongue-and-socket locator separate from the M3 bolts.

Current locator parameters:

- Locator radius: `134 mm`.
- Tongue radial length: `22 mm`.
- Tongue tangential width: `10 mm`.
- Socket tangential width: `11 mm`.
- Clearance target: about `0.5 mm per side`.

The locator is same-layer only:

- Lower locator connects lower segment to lower segment.
- Upper locator connects upper segment to upper segment.
- No locator connects upper to lower.

## Lug Reinforcement

The integrated lugs now include broad flat XY shoulders near the lug roots. These are intended to reduce PETG stress concentration while remaining support-free when printed flat.

## Validation Coupons

Generated seam validation coupons:

```text
cad/exports/validation/stl/concept_v4_lower_integrated_seam_coupon_v1.stl
cad/exports/validation/stl/concept_v4_upper_integrated_seam_coupon_v1.stl
```

The coupons use cropped real v4 seam geometry and include:

- Integrated lugs.
- M3 clearance holes.
- Captured nut pockets.
- Printed seam locator.
- Upper counterbore on the upper coupon.
- Short engraved labels.

## CAD Verification

Sample checks after Round Cup integration:

- Upper segment 0 vs round upper pad: `0.0 mm^3` overlap.
- Upper segment 0 vs sensor placeholder: `0.0 mm^3` overlap.
- Upper segment 0 vs lower pad: `0.0 mm^3` overlap.
- Upper segment 0 vs lower segment 0: `0.0 mm^3` overlap.
- Full upper carrier vs full lower base: `0.0 mm^3` overlap.
- Upper fastener visuals vs full lower base: `0.0 mm^3` overlap.
- Lower fastener visuals vs full upper carrier: `0.0 mm^3` overlap.
- Support grate bars vs full upper carrier: `0.0 mm^3` overlap.
- Support grate bars vs full lower base: `0.0 mm^3` overlap.

The upper fastener visual bounding box is `z = 21.0..33.0 mm`. The upper button head portion is `z = 31.2..33.0 mm`, recessed from the top side. The captured nut visual sits below in the underside lug at about `z = 21.85..24.25 mm`.

## Service Note

Upper ring service is improved because upper seam bolts are now top-access. Remove the salt container and support grate first, then loosen the recessed upper seam bolts from above. The upper ring still remains mechanically separate from the lower base.

## Recommended First Print

Print first:

```text
cad/exports/validation/stl/concept_v4_upper_integrated_seam_coupon_v1.stl
```

Reason: it validates the integrated upper seam fastener and captured-nut details before full platform printing.

Print second:

```text
cad/exports/validation/stl/concept_v4_lower_integrated_seam_coupon_v1.stl
```
