# Concept v2 Assembly Review

Date: 2026-06-06

## Scope

This is an assembly review of the active `concept_v2` assembled/exploded STEP geometry, treating the currently validated decisions as correct:

- Four-sensor floating architecture.
- Captured M3 nut pockets.
- M3 bolts, standard M3 nuts, and printed bridge plates as default segment joining.
- No heat-set inserts or metal dowels as the default.
- `sensor_station_locator_v3` style sensor locator.
- `0.4 mm per side` as the current support-grate tab/slot clearance.

This document now includes the follow-up fix status after the targeted CAD repair.

Reviewed files:

- `cad/exports/active/step/concept_v2_assembly.step`
- `cad/exports/active/step/concept_v2_exploded_assembly.step`
- `cad/exports/active/step/concept_v2_one_quadrant_assembly.step`
- `cad/exports/active/step/concept_v2_one_quadrant_exploded.step`
- `cad/src/concept_v2.py`

## Summary

The major force-path architecture is still sound: the upper carrier, support grate, upper pad, sensor, lower pad, and lower base remain conceptually separated, and no direct upper-to-lower bridge was found in the reviewed geometry.

The original review found a real support-grate/upper-carrier interference. That has now been fixed with an upper-only full cross-arm receiver while preserving the validated `0.4 mm per side` clearance. The remaining serviceability caveat is upper seam bridge access: the upper bridge fasteners are underside fasteners, so upper-segment service requires lifting the upper carrier assembly first.

## Checks Performed

Bounding/z-position checks found:

- Lower segment: `z = 0..21 mm`, including locator/overload features.
- Upper segment: `z = 25..39 mm`.
- Lower bridge plates: `z = 8..12 mm`.
- Upper bridge plates: `z = 21..25 mm`.
- Lower pad: `z = 8..10 mm`.
- Sensor placeholder: `z = 10..22 mm`.
- Upper pad: `z = 22..25 mm`.
- Support grate: `z = 29..33 mm`.

Validated gaps/contacts:

- Upper pad top to upper carrier land bottom: `0.0 mm`, intended normal load contact.
- Overload stop top to upper pad bottom: `1.0 mm`, intended overload clearance.
- Upper/lower solid overlap check: no overlap between lower segment and upper segment.
- Lower segment/support grate overlap check: no overlap.
- Lower segment/upper bridge overlap check: no overlap.

Original problem found:

- Upper segment/support grate overlap volume before the fix: about `130.7 mm^3` in quadrant 0.
- Interference bounding box before the fix: approximately `x = 0.9..74.0 mm`, `y = 0.9..74.0 mm`, `z = 29..33 mm`.

Post-fix boolean checks:

- Support grate vs upper carrier: `0.0 mm^3` overlap.
- Support grate vs lower base: `0.0 mm^3` overlap.
- Upper bridge vs lower base: `0.0 mm^3` overlap.
- Upper carrier vs lower base: `0.0 mm^3` overlap.

## Issues

### 1. Support grate intersects the upper carrier

Severity: **Critical, fixed**

Location:

- `cad/src/concept_v2.py`
- `upper_segment()` support-grate receiver cuts
- `support_grate()` cross arms
- Seen in assembled STEP as support grate occupying volume that is still part of the upper segment.

Finding:

The previous active upper carrier included shallow receiver cuts using the validated `0.4 mm per side` clearance, but those receiver cuts did not clear the full support-grate geometry. A boolean intersection between `upper_segment(0)` and `support_grate()` found about `130.7 mm^3` of overlapping solid.

Fix applied:

The upper segment now uses full upper-only cross-arm receiver cuts for the support grate. The receiver keeps `0.4 mm per side` lateral clearance and does not touch or depend on the lower base. Post-fix boolean overlap is `0.0 mm^3`.

Future refinement, not required for installability:

- Keep `0.4 mm per side` as the default clearance.
- Consider self-centering or tapered upper-only locator geometry later if perceptible play remains objectionable.
- Do not loosen the validated `0.4 mm per side` clearance unless a later physical test proves it is necessary.

### 2. Support grate is not vertically seated in the modeled receiver

Severity: **Medium, fixed**

Location:

- `support_grate()` z-position: `z = 29..33 mm`.
- Receiver bottom: `z = 28.8 mm`.
- Receiver top cut: about `z = 33.2 mm`.

Finding:

The support grate was previously modeled about `0.2 mm` above the receiver bottom.

Fix applied:

- Receiver floor: `z = 29.0 mm`.
- Support grate bottom: `z = 29.0 mm`.
- The assembled view now shows the grate seated on the upper-only receiver floor without an ambiguous vertical near-gap.

### 3. Upper seam fasteners are not accessible in installed orientation

Severity: **Medium**

Location:

- Upper bridge plates at `z = 21..25 mm`, underneath the upper segment.
- Upper captured nuts open from the top side of the upper segment.
- M3 bolts insert from below through the upper bridge plates.

Finding:

The upper bridge plates are underside parts. Once the upper carrier is resting on the sensor stack, the underside bridge bolts are not practically accessible. That makes the documented “remove one upper segment” service idea harder than the assembly text suggests.

A failed sensor can still be replaced without disassembling the lower base, but the realistic sequence is likely:

1. Remove the salt container.
2. Remove/lift the support grate.
3. Lift the full upper carrier assembly off the sensor stack.
4. Access upper bridge fasteners from below, or flip the upper carrier on the bench.
5. Remove the target upper segment if needed.

This is serviceable, but not as convenient as loosening one upper segment in place.

Decision / proposed fix:

- Use Option A: keep the underside upper bridge because it is mechanically simple and keeps the upper surface clear for the support grate and salt container.
- Document that upper segment removal requires lifting the upper carrier assembly first.
- If later usability demands true in-place upper-segment removal, explore a top-access upper bridge strategy that still remains upper-only and cannot touch the lower base.
- Do not add any upper-to-lower fastener to solve this.

### 4. Lower captured nuts must be installed before the lower ring is placed on the floor

Severity: **Minor**

Location:

- Lower segment captured nut pockets open from the underside.
- Lower bridge plates install from above.

Finding:

The lower captured nuts are retained and validated, but they are inserted from the underside. Once the lower ring is assembled and placed on the floor, those nuts are not conveniently accessible.

This is not an impossible assembly, but it is an assembly-order dependency.

Proposed fix:

- Keep the current geometry.
- Document the lower ring assembly order clearly: preload lower captured nuts before placing the lower ring in its final location.
- During future full-platform validation, confirm that nuts stay retained during handling and ring placement.

### 5. Support grate may interfere with upper segment removal during service

Severity: **Minor**

Location:

- Support grate spans the upper carrier.
- Support grate receiver is upper-only.

Finding:

The support grate belongs to the upper assembly, which is correct for the load path. But because it spans multiple quadrants, it may block direct removal of one upper segment unless the grate is removed first.

This is acceptable if the grate remains removable by hand, but it should be part of the service sequence.

Proposed fix:

- Keep support grate removable.
- Document “remove support grate first” before loosening or lifting upper carrier segments.
- After receiver geometry is fixed, validate that the grate can still be removed without disturbing sensors or lower parts.

## Non-Issues / Confirmed Good

### No direct upper-to-lower solid bridge found

Severity: **None**

Finding:

The reviewed geometry does not show a direct structural connection between the upper carrier/support grate and lower base. Boolean checks found no solid overlap between:

- lower segment and upper segment
- lower segment and support grate
- lower segment and upper bridge plates

The support-grate collision is upper-only and does not itself bypass sensors.

### Sensor stack order is physically understandable

Severity: **None**

Finding:

The intended stack is clear:

```text
upper carrier land
upper pad
sensor
lower pad
lower base
```

The upper pad contacts the upper carrier land at the intended height. The overload stops remain `1.0 mm` below the upper pad underside in nominal assembly.

### Sensor is not permanently trapped by lower locator geometry

Severity: **None**

Finding:

The v3-style lower locator remains low and broken rather than a tall closed wall. Once the upper carrier and upper pad are removed, the sensor can be lifted or moved out through the outer side.

## Recommended Next Action

The support-grate receiver overlap has been fixed in CAD. The next action is a one-quadrant physical assembly check:

1. Lower segment.
2. Lower pad.
3. Sensor placeholder or real sensor.
4. Upper pad.
5. Upper segment.
6. Upper and lower bridge plates with M3 bolts/nuts.
7. Support grate.

Acceptance criteria for that check:

- Support grate installs and removes by hand.
- No visible grate rocking beyond acceptable play.
- Upper carrier touches only the upper pad in normal assembly.
- Overload stops have visible clearance.
- Upper and lower bridge hardware remain same-layer only.
- Sensor can be replaced without disassembling the lower ring.
