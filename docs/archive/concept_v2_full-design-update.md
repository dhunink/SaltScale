# Concept v2 Full Design Update

Date: 2026-06-06

## Summary

`concept_v2` now promotes the validated interface decisions from coupons into the active full design where it is safe to do so.

Applied now:

- Captured M3 nut pockets for same-layer segment joining.
- M3 bolts plus standard M3 nuts plus printed bridge plates as the default seam strategy.
- No heat-set inserts as the default.
- No metal dowels as the default.
- Low-profile `sensor_station_locator_v3` style locator geometry in the lower sensor station.
- Engraved labels only on non-contact functional surfaces, using the validated larger label standard.

Applied now:

- Support-grate tab/slot clearance default is `0.4 mm per side`, based on the 0.4/0.6/0.8 coupon result.

Not applied yet:

- More refined support-grate locator geometry. The active upper carrier now uses full upper-only cross-arm receivers with `0.4 mm per side` clearance and zero boolean overlap, but even the coupon had perceptible movement. Future work may test self-centering or tapered locator geometry.
- Real Kiwi/SparkFun sensor geometry beyond the current placeholder envelope.
- Electronics packaging, battery, firmware, and enclosure details.

## Physical Decisions Applied

### Captured M3 Nut Pocket

The active lower and upper segments now use the validated captured-nut dimensions:

- M3 clearance hole: `3.4 mm` diameter.
- Captured nut pocket: `5.9 mm` across flats.
- Retaining lip opening: `5.35 mm` across flats.
- Captured nut pocket depth: `3.0 mm`.
- Retaining lip depth: `0.7 mm`.

The lower segment captures nuts from the underside. The lower bridge plate sits on the top of the lower base, and M3 bolts enter from above.

The upper segment captures nuts from the top side of the upper carrier. The upper bridge plate sits on the underside of the floating upper carrier, and M3 bolts enter from below.

This keeps all fasteners same-layer only:

- lower-to-lower for lower seams
- upper-to-upper for upper seams

No fastener connects the lower base to the floating upper carrier.

### Segment Joining Strategy

The default segment joint is now:

```text
M3 bolt -> printed bridge plate -> segment edge -> captured standard M3 nut
```

The active full design no longer uses heat-set insert pockets or 4 mm dowel sockets as the default seam geometry.

Printed-only wedge, dovetail, and sliding-key joints remain experimental validation coupons only. They are not part of the active full platform.

### Sensor Station Locator

The lower sensor station now uses the v3-style locator direction:

- Low broken side tabs instead of long high rectangular rails.
- Inner stop features to limit inward sensor motion.
- Small rounded outer locator/cradle features while keeping the outer service side open.
- Four visually distinct overload stops.

The sensor still removes from the outer side after lifting the local upper carrier segment and upper pad.

The locator is lower than the upper pad and upper carrier contact height, so it is not intended to carry vertical load.

### Support-Grate Interface

The upper carrier now includes full upper-only support-grate cross-arm receiver cuts using `0.4 mm per side` clearance. This is the current validated default from the 0.4/0.6/0.8 coupon test.

The receiver is intentionally upper-only and cannot create an upper-to-lower load bypass. Boolean overlap checks after the fix show `0.0 mm^3` overlap between support grate and upper carrier, support grate and lower base, upper bridge and lower base, and upper carrier and lower base. It may still have perceptible play; future work may explore self-centering or tapered locators rather than loosening the clearance.

### Label Standard

The active model uses engraved labels only. Raised labels are not used on functional parts.

Current standard:

- text height: `7-8 mm` where space allows
- engraving depth: `0.8 mm`
- short labels only

Labels are placed only where they should not affect the force path or sliding/clamping interfaces. Contact pads are intentionally not labeled on their load-contact faces.

## Printed Parts

Active printable STLs:

- `cad/exports/active/stl/concept_v2_lower_segment_0.stl`
- `cad/exports/active/stl/concept_v2_upper_segment_0.stl`
- `cad/exports/active/stl/concept_v2_support_grate.stl` using `0.4 mm per side` as the current target clearance for its tab/slot receiver
- `cad/exports/active/stl/concept_v2_lower_bridge_plate.stl`
- `cad/exports/active/stl/concept_v2_upper_bridge_plate.stl`
- `cad/exports/active/stl/concept_v2_upper_pad.stl`
- `cad/exports/active/stl/concept_v2_lower_pad.stl`
- `cad/exports/active/stl/concept_v2_sensor_placeholder.stl`

Print count for a full four-quadrant mechanical prototype, assuming the same quadrant design repeats:

- 4x lower segments
- 4x upper segments
- 4x lower bridge plates
- 4x upper bridge plates
- 4x lower pads
- 4x upper pads
- 4x sensors or placeholders
- 1x support grate using `0.4 mm per side` as the current target clearance, pending full-carrier confirmation

## Visualization Only

Assembly STEP exports are for inspection and human understanding:

- `cad/exports/active/step/concept_v2_assembly.step`
- `cad/exports/active/step/concept_v2_exploded_assembly.step`
- `cad/exports/active/step/concept_v2_one_quadrant_assembly.step`

The assembly STEP files are not print plates.

## Assembly Order

1. Print lower segments, upper segments, bridge plates, pads, and support grate.
2. Press standard M3 nuts into the underside captured pockets of the lower segments.
3. Place lower segments seam-to-seam.
4. Install lower bridge plates on top of lower seams using M3 bolts from above.
5. Place each lower pad into its sensor station.
6. Place each sensor or placeholder on its lower pad with cable exit outward.
7. Place each upper pad on its sensor.
8. Press standard M3 nuts into the top-side captured pockets of the upper segments.
9. Assemble the upper carrier separately using underside upper bridge plates and M3 bolts from below.
10. Place the support grate into the upper carrier using `0.4 mm per side` as the current target clearance; verify that the full upper carrier does not still feel too loose.
11. Lower the upper carrier assembly onto the four upper pads.
12. Confirm that the upper structure touches only the upper pads in normal unloaded condition.
13. Confirm overload stop clearance before adding real load.

## Why Upper And Lower Remain Separate

The measurement path is:

```text
container
-> support grate / upper carrier
-> upper pad
-> sensor
-> lower pad
-> lower base
-> floor
```

Any bridge, fastener, dowel, wall, tab, or locator that connects upper to lower would bypass the sensors and corrupt the reading.

`concept_v2` keeps seam hardware same-layer only. Lower bridge plates attach only to lower segments. Upper bridge plates attach only to upper segments.

## Pending Decisions

Do not apply these until physically validated:

- Whether the `0.4 mm per side` support-grate receiver feels controlled enough in the full upper carrier, or whether a later self-centering/tapered locator or `0.2 mm per side` coupon is needed.
- Final real-sensor locator adjustment after actual Kiwi/SparkFun sensor measurement.
- Contact pad material and whether printed pads are acceptable beyond validation.
- Full quadrant stiffness and seam behavior under load.


## Print-Sheet Efficiency

The main active parts remain comfortably within the Prusa MK4 envelope:

- Lower segment: about `159 x 159 x 21 mm`.
- Upper segment: about `153 x 153 x 14 mm`.
- Support grate: about `178 x 178 x 4 mm`.
- Bridge plates, pads, and sensor placeholder are small.

For fast prototype printing, do not print one tiny part per sheet. Recommended practical plating:

1. Lower-segment sheet: one lower segment plus lower bridge plates, lower pad, and sensor placeholder where the slicer can nest them in unused bed area.
2. Upper-segment sheet: one upper segment plus upper bridge plates and upper pad.
3. Support-grate sheet: support grate alone, or with very small loose parts if slicer placement remains clear.

Do not change functional dimensions just to save a print sheet until the one-quadrant assembly check passes. The safer efficiency win is slicer nesting, not shrinking validated interfaces.
