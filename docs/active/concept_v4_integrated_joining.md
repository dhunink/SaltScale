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
bolt head above, recessed -> upper segment/same-plane lug -> captured nut below
```

The upper seam remains top-access for serviceability. The M3 button head sits in a top-side recess from `z = 31.2..33.0 mm`, flush with the upper carrier top surface. The integrated upper lug now starts at the same `z = 25.0 mm` lower plane as the main upper segment body, so the printable upper segment no longer rests on a lower protruding lug. The shaft points downward into a captured nut pocket that opens from the underside of the same-plane lug/body region.

Visual M3 nuts include center holes so the bolt shaft and nut are represented as compatible physical hardware instead of overlapping solid placeholders.

## Upper Pad Locator

Decision: retire the Round Cup as active upper-segment geometry.

The Round Cup carrier-relative locator was selected earlier, but the integrated full assembly showed a practical printability problem: the cup/rim became downward geometry attached to the upper segment near the sensor stack. That made the upper segment harder to print flat and introduced confusing disk/ring bodies around the upper pad area.

Rejected or inactive concepts:

- Through-hole boss/socket through the upper carrier.
- Sensor-relative upper pad locator.
- Small underside locator tabs.
- Round Cup underside cup/rim on the upper carrier.

Current active method:

- The upper segment has no sensor-area underside cup or circular land disk.
- The upper segment has an open inner-edge notch at each sensor station. The notch is cut to the inner edge, not a blind underside pocket, so it remains support-free.
- The upper pad remains a separate removable printed part.
- Upper pad body: `40 mm` round body, `3 mm` thick.
- Upper pad lower contact boss: `12 mm` round boss that contacts the Kiwi sensor's central load-entry region.
- The pad has a `36 mm` upper locating lobe that drops into a matching open-to-inner-edge socket in the upper segment. This carrier-relative feature keeps the pad centered during handling while remaining removable by hand.
- No text is placed on pad contact faces.
- The assembly STEP shows the pad in installed orientation, with the boss downward.
- The printable upper-pad STL is flipped so the broad body/key side prints flat on the bed and the `12 mm` boss prints upward without supports.

The vertical load path remains:

```text
upper carrier -> removable upper pad body -> 12 mm contact boss -> Kiwi sensor -> lower pad -> lower base
```

Open validation note: the lobe/socket system should be checked physically for hand removability, pad centering, and whether it stays put during normal upper-carrier handling.

## Locator Geometry

Concept v4 now uses a printed tongue-and-socket locator separate from the M3 bolts.

Current locator parameters:

- Locator radius: `134 mm`.
- Tongue radial length: `22 mm`.
- Tongue tangential width: `10 mm`.
- Socket tangential width: `11 mm`.
- Validated clearance: `0.3 mm per side`. Physical testing showed `0.4 mm` and `0.5 mm` had unnecessary play, while `0.3 mm` remained easy to assemble and gave the best alignment.

The locator is same-layer only:

- Lower locator connects lower segment to lower segment.
- Upper locator connects upper segment to upper segment.
- No locator connects upper to lower.

## Lug Reinforcement

The integrated lugs now include broad flat XY shoulders near the lug roots. These are intended to reduce PETG stress concentration while remaining support-free when printed flat.

## Validation Coupons

Generated seam validation coupons:

```text
cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl
cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl
```

The coupons use cropped real v4 seam geometry and include:

- Integrated same-plane lugs.
- M3 clearance holes.
- Captured nut pockets.
- Printed seam locator.
- Upper counterbore on the upper coupon.
- Short engraved labels.

## CAD Verification

Sample checks after removing active Round Cup geometry:

- Upper segment 0 vs round upper pad: `0.0 mm^3` overlap.
- Upper segment 0 vs sensor placeholder: `0.0 mm^3` overlap.
- Upper segment 0 vs lower pad: `0.0 mm^3` overlap.
- Upper segment 0 vs lower segment 0: `0.0 mm^3` overlap.
- Full upper carrier vs full lower base: `0.0 mm^3` overlap.
- Upper segment material below main body plane: `0.0 mm^3`.
- Upper fastener visuals vs full lower base: `0.0 mm^3` overlap.
- Lower fastener visuals vs full upper carrier: `0.0 mm^3` overlap.
- Support grate bars vs full upper carrier: `0.0 mm^3` overlap.
- Support grate bars vs full lower base: `0.0 mm^3` overlap.

The upper fastener visual bounding box is now `z = 25.0..33.0 mm`. The upper button head portion is `z = 31.2..33.0 mm`, recessed from the top side. The captured nut visual sits in the same-plane lug/body underside pocket at about `z = 25.85..28.25 mm`.

## Service Note

Upper ring service is improved because upper seam bolts are now top-access. Remove the salt container and support grate first, then loosen the recessed upper seam bolts from above. The upper ring still remains mechanically separate from the lower base.

## Recommended First Print

Print first:

```text
cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl
```

Reason: it validates the integrated upper seam fastener and captured-nut details before full platform printing.

Print second:

```text
cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl
```
