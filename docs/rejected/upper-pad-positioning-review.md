# Upper Pad Positioning Review

Date: 2026-06-07

## Summary

The current `concept_v4` upper pad boss/socket works mechanically, but the through-hole in the upper carrier is visually undesirable and adds a feature to a clean upper ring surface.

Recommended positioning philosophy for the next validation step:

```text
Prefer C: sensor-relative upper pad location.
```

Reason: the upper pad is part of the measurement stack, not a structural ring alignment part. Locating it from the sensor/station geometry keeps the upper carrier cleaner and avoids putting pad-specific holes or pockets in every upper segment.

This is not yet a full-design change. The current boss/socket method remains in `concept_v4` until a physical coupon proves a cleaner alternative.

## Option A: Current Boss/Socket Through Upper Carrier

Description:

- Upper pad has a central boss.
- Upper carrier has a matching through-socket.
- Pad is located relative to the upper carrier.

Strengths:

- Simple to understand.
- Positive lateral location.
- No underside tabs or hidden carrier clutter.
- Current CAD has zero overlap with upper/lower/support-grate bodies.

Weaknesses:

- Puts a through-hole in the upper carrier at every sensor station.
- Makes the upper ring visually busier.
- Couples pad location to the upper carrier rather than to the sensor stack.
- Could collect salt dust from above unless covered by the container/grate area.

Risk:

- Low mechanical risk, medium design-cleanliness concern.

Verdict:

- Keep as the current working fallback, but do not assume it is the final best answer.

## Option B: Upper-Carrier Underside Pocket

Description:

- Upper pad remains removable.
- Upper carrier has a shallow underside pocket or open locator feature.
- No through-hole in the upper carrier.

Strengths:

- Keeps pad location tied to the upper carrier.
- Avoids top-side holes.
- Can be simple if implemented as a broad open pocket.

Weaknesses:

- Underside pockets are difficult to make support-free when the upper carrier is printed flat in its normal orientation.
- Small underside features quickly become visual and mechanical clutter.
- Hidden underside pockets can trap salt debris.
- If the pocket is too shallow, it may not locate the pad well; if too deep, printability gets worse.

Risk:

- Medium printability risk and medium debris risk.

Verdict:

- Worth validating as a fallback, but only if the feature stays broad, open, and support-free. Avoid small tabs.

## Option C: Sensor-Relative Pad Location

Description:

- Upper pad is located by the sensor/station geometry instead of the upper carrier.
- No boss or hole through the upper carrier.
- No screws.
- Pad sits on/around the sensor with shallow locating features that limit drift.

Strengths:

- Keeps the upper carrier clean.
- Locates the pad relative to the part it actually loads: the sensor.
- Does not add upper-to-lower fasteners or bridges.
- Can make the whole sensor stack a removable/serviceable subassembly.
- Avoids a through-hole in the upper ring.

Weaknesses:

- Depends more strongly on the real Kiwi/SparkFun sensor dimensions.
- Badly sized features could side-load the sensor.
- Features around the sensor can trap salt unless broken/open.
- Must preserve easy outside sensor removal.

Risk:

- Medium until real sensors are available.

Verdict:

- Best design philosophy to test next. It is cleaner if the fit can be made loose enough to avoid side-loading while still preventing pad drift.

## Comparison

| Criterion | A: Current boss/socket | B: Carrier pocket | C: Sensor-relative |
| --- | --- | --- | --- |
| Printability | Good, but through-hole | Risky if underside pocket is blind | Good if pad prints with features upward |
| Serviceability | Good | Good if pocket is open | Good if sensor can still slide out |
| Sensor replacement | Good | Good | Must be validated carefully |
| Pad drift risk | Low | Low-medium | Low if fit works |
| Sensor side-load risk | Low | Low | Medium if too tight |
| Salt/debris trapping | Medium at through-hole | Medium-high in pocket | Medium, reduced by broken features |
| Real sensor uncertainty | Low | Low | Higher |
| Clean upper carrier | Poorer | Good | Best |

## Validation Coupons Created

Generated validation exports:

```text
cad/exports/validation/stl/concept_v4_upper_pad_sensor_relative_test_v1.stl
cad/exports/validation/step/concept_v4_upper_pad_sensor_relative_test_v1.step
cad/exports/validation/stl/concept_v4_upper_pad_carrier_pocket_test_v1.stl
cad/exports/validation/step/concept_v4_upper_pad_carrier_pocket_test_v1.step
```

### Sensor-Relative Coupon

Approximate size:

```text
125 x 70 x 13.6 mm
```

What it tests:

- Upper pad with shallow broken sensor-relative locating tabs.
- Sensor placeholder fit inside those tabs.
- Whether shallow features prevent drift without pinching.
- Whether the pad can be lifted off by hand.

Important note:

- The pad is arranged for easy printing in the coupon. The locator features represent the pad underside after the part is flipped for use.

Pass criteria:

- Sensor placeholder fits without forcing.
- Pad does not visibly rock on the sensor placeholder.
- Pad can be removed by hand.
- Locator tabs do not scrape hard enough to suggest sensor side-loading.
- Open corners look cleanable.

Fail criteria:

- Fit is tight or requires force.
- Tabs feel fragile.
- Pad can rotate or slide enough to leave the intended sensor contact area.
- Debris traps look unavoidable.

### Carrier Pocket Coupon

Approximate size:

```text
153 x 82 x 22.6 mm
```

What it tests:

- A broad open carrier-side locator concept with `0.4 mm` per-side clearance.
- A plain removable upper pad.
- Whether a carrier-located pad can be clean without a through-hole.

Pass criteria:

- Pad fits by hand.
- Pad can be removed without prying.
- Locator is visibly simpler than the rejected small underside-tab design.
- Feature appears printable without supports in the intended orientation.

Fail criteria:

- Pocket/rim feels cluttered.
- Pad rattles too much.
- Feature would require supports in a real upper segment orientation.
- Debris trapping looks worse than the current boss/socket.

## Recommended Print Order

Print first:

```text
cad/exports/validation/stl/concept_v4_upper_pad_sensor_relative_test_v1.stl
```

Reason: it tests the cleaner philosophy that could remove pad-specific features from the upper carrier entirely.

Print second only if needed:

```text
cad/exports/validation/stl/concept_v4_upper_pad_carrier_pocket_test_v1.stl
```

Reason: it is the fallback if sensor-relative location proves too sensor-specific or too likely to side-load the sensor.

## Full Concept v4 Change If Sensor-Relative Test Passes

If the sensor-relative coupon passes:

- Remove the upper carrier through-socket.
- Remove the central boss from the current active upper pad.
- Replace it with a sensor-relative removable upper pad locator.
- Keep the upper carrier as a clean flat load-entry surface above the pad.
- Re-run checks for pad/sensor fit, sensor removal from outside, upper/lower overlap, support-grate overlap, and side-load risk.

Do not apply this to the full concept until either a real sensor or a dimensionally accurate dummy proves that the locator does not pinch or side-load the sensor.
