# Concept v4 Real Sensor Revision

Date: 2026-06-11

## Summary

This revision updates `concept_v4` around the measured Kiwi/SparkFun-style sensor while preserving the existing SaltScale architecture.

Preserved architecture:

- Four-sensor floating upper/lower platform.
- Upper and lower remain mechanically separate.
- Integrated M3 segment joining remains unchanged.
- No heat-set inserts or metal dowels as default.
- No upper-to-lower fasteners, clips, bridges, or locator features.
- Round Cup upper-carrier geometry is retired; the upper segment remains flat in the sensor area.
- Upper pad is now carrier-located by a `36 mm` upper locating lobe and an open-to-inner-edge upper-carrier socket.
- Upper integrated M3 lugs are same-plane with the main upper segment body for flat printing.

Main real-sensor changes:

- Sensor thickness is now treated as `6.84 mm` instead of the old `12.0 mm` placeholder stack.
- The upper pad now reaches the sensor with a smaller central contact boss.
- The lower pad is reduced to a `36 mm` rounded-square support.
- The sensor locator is tightened around the measured `34.07 mm` sensor body.
- Overload stop height is recalculated for the corrected stack.

## Corrected Stack Height

Measured sensor dimensions used:

| Feature | Value |
| --- | ---: |
| Sensor body width | `34.07 mm` |
| Sensor body thickness | `6.84 mm` |

Corrected stack:

| Feature | Z range |
| --- | ---: |
| Lower pad | `8.00..10.00 mm` |
| Kiwi sensor reference | `10.00..16.84 mm` |
| Upper pad total | `16.84..25.00 mm` |
| Upper pad contact boss | `16.84..22.00 mm` |
| Upper pad 40 mm body and inward key | `22.00..25.00 mm` |
| Upper carrier underside | `25.00 mm` |

The old `5.16 mm` vertical gap is removed. The upper pad now contacts the intended upper load-entry region of the Kiwi reference stack.

## Upper Pad Revision

The previous `56 mm` flat upper pad was oversized as a force-contact surface.

The new active upper pad has two functional zones:

| Zone | Geometry | Purpose |
| --- | --- | --- |
| Upper body | `40 mm` round body, `3 mm` thick | Bears against the flat upper carrier underside and remains easy to handle |
| Lower contact boss | `12 mm` round boss, `5.16 mm` tall | Introduces load into the sensor's central raised button/bridge region |

The Round Cup carrier locator was removed from the active upper segment because it created downward cup/rim geometry that compromised flat, support-free printing. The active validation coupon is one standalone upper pad only:

- `40 mm` upper pad body.
- `36 mm` upper locating lobe for carrier-relative positioning.
- `12 mm` round lower contact boss.
- No upper-carrier cup geometry.

Chosen default: **`12 mm` round boss**.

Rationale:

- Smaller and cleaner than the old `56 mm` flat contact.
- Large enough to print reliably in PETG.
- Small enough to avoid intentionally loading the full outer sensor frame from above.
- Good first default before any more specialized bridge-shaped contact is proven.

## Lower Pad Revision

The previous `44 x 44 mm` lower pad was oversized for the measured `34.07 mm` sensor body.

The new active lower pad is:

- `36 x 36 mm` rounded square.
- `2 mm` thick.
- `4 mm` corner radius.

The lower support coupon compares the current lower support direction against alternatives:

- Current-style `44 mm` square reference.
- `36 mm` rounded-square support.
- `36 mm` frame/ring support with central relief.

Chosen default: **`36 mm` rounded-square support**.

Rationale:

- Close to the measured sensor body size while leaving practical tolerance.
- Simpler and less fragile than the frame/ring support.
- More likely to support the real lower frame evenly than a very small pad.
- Still needs physical confirmation with the real sensor underside.

## Sensor Locator Revision

The old locator cavity was about `39 mm`, giving roughly `2.465 mm per side` clearance around the measured sensor body. That was too loose for a real sensor locator.

The new active sensor locator uses:

- Sensor body reference width: `34.07 mm`.
- Default body clearance: `0.4 mm per side`.
- Approximate target cavity: `34.87 mm`.
- Low v3-style broken locator features.
- Open cable side with relief so the sensor can still be removed outward.

Multi-variant locator testing has been retired. The project now uses one practical default.

Chosen default: **`0.4 mm per side`**.

Rationale:

- The real Kiwi sensor is available for direct fit testing.
- Very loose fits are already known to be undesirable.
- `0.4 mm per side` is the active decision point: tight enough to locate, still PETG-realistic.
- Locator features position the sensor only; they must not carry vertical load.

## Overload Stop Revision

The overload stop height has been recalculated for the corrected real-sensor stack.

Current values:

| Feature | Value |
| --- | ---: |
| Upper carrier underside | `25.00 mm` |
| Overload stop top | `24.00 mm` |
| Nominal unloaded clearance | `1.00 mm` |
| Expected overload travel before engagement | `1.00 mm` |

The stops are lower-base-only features. They should not touch the upper carrier during normal unloaded assembly. Under overload, the floating upper structure can travel about `1 mm` before the stops engage.

## Validation Exports

New compact validation prints:

```text
cad/exports/experimental/stl/concept_v4_upper_pad_12mm_boss_test_v2.stl
cad/exports/experimental/stl/concept_v4_lower_support_test_v1.stl
cad/exports/experimental/stl/concept_v4_real_sensor_locator_test_v2.stl
```

Corresponding STEP files are exported in:

```text
cad/exports/experimental/step/
```

Active updated printable parts include:

```text
cad/exports/active/stl/concept_v4_upper_pad.stl
cad/exports/active/stl/concept_v4_lower_pad.stl
cad/exports/active/stl/concept_v4_lower_segment_0.stl
cad/exports/active/stl/concept_v4_upper_segment_0.stl
cad/exports/active/stl/concept_v4_kiwi_sensor_reference_v1.stl
```

Updated assembly STEP files:

```text
cad/exports/active/step/concept_v4_assembly.step
cad/exports/active/step/concept_v4_exploded_assembly.step
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

## Recommended Print Order

Print first as one practical plate:

```text
cad/exports/experimental/stl/concept_v4_real_sensor_locator_test_v2.stl
cad/exports/experimental/stl/concept_v4_upper_pad_12mm_boss_test_v2.stl
```

Reason:

- Upper force introduction is the highest-risk real-sensor geometry.
- The `12 mm` round boss is now the active default; this print validates the single chosen pad rather than comparing alternatives.

Print second:

```text
cad/exports/experimental/stl/concept_v4_real_sensor_locator_test_v2.stl
```

Reason:

- The sensor must remain removable but not rattle around.

Print third:

```text
cad/exports/experimental/stl/concept_v4_lower_support_test_v1.stl
```

Reason:

- Lower support is important, but the current `36 mm` rounded-square default is less risky than the upper load-entry surface.

## Inspection Recommendation

Inspect first:

```text
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Check specifically:

- Upper pad boss contacts the central Kiwi load region.
- Upper pad body bears against the flat upper carrier underside while the `36 mm` upper lobe seats in the open-to-inner-edge socket; no Round Cup geometry remains active.
- Lower pad supports the sensor body without obvious cable/glue conflict.
- Sensor locator remains lower-only and does not touch the upper pad or carrier.
- Overload stops remain clear during normal assembly.

## Remaining Risks

- The exact load sensitivity of the central bridge/button must be tested physically.
- The underside support behavior of the real stamped metal sensor is still partly inferred from photos.
- The active `0.4 mm` sensor-locator clearance has already felt loose in one physical test; the separate `0.2 mm` v3 locator coupon is the next validation print.
- Overload stop behavior should be checked after the upper contact boss and locator are validated.
- PETG creep around the contact boss and pads remains untested.

## Sensor Retention Update

The next concept_v4 validation direction uses `0.2 mm` per-side sensor locator clearance and separate quarter-turn clips on the two front round posts. The clips are retention-only: they prevent accidental lift-out during handling, but they must not preload the Kiwi sensor or carry vertical measuring force. The sensor still rests on the lower pad and is loaded by the upper pad's 12 mm boss.

Print `cad/exports/experimental/stl/concept_v4_sensor_clip_station_coupon_v2.stl` with two copies of `cad/exports/active/stl/concept_v4_sensor_quarter_turn_clip.stl` before printing a full lower segment. Coupon v2 uses a larger cropped base so all fixed pillars and stops grow from solid printed geometry.
