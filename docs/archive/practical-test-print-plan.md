# Practical Test Print Plan

Date: 2026-06-06

## Summary

These prints are compact validation parts for the next critical `concept_v2` interfaces. They are not scaled down. They keep real 1:1 functional geometry and only crop away surrounding ring area.

Generated targets:

- `test_label_readability_v1`
- `test_m3_captured_nut_v1`
- `test_support_grate_fit_v1`
- `test_sensor_locator_v3_fit_v1`
- `test_bolted_seam_slice_v1`

These complement the larger validation coupons. They do not replace or archive previous coupons.

## Recommended Print Order

1. `test_label_readability_v1`
2. `test_m3_captured_nut_v1`
3. `test_support_grate_fit_v1`
4. `test_sensor_locator_v3_fit_v1`
5. `test_bolted_seam_slice_v1`

Reason: validate labels first, because poor text affects every later coupon. Then validate the smallest hardware interface, then support-grate fit, then sensor locator, then a cropped seam assembly.

## Test 1: Label Readability

File:

```text
cad/exports/validation/stl/test_label_readability_v1.stl
```

Validates:

- Engraved and raised text.
- 5, 7, and 8 mm text heights.
- 0.6, 0.8, and 1.0 mm text depths/heights.
- Short labels: `IN`, `OUT`, `PAD`, `STOP`, `SENSOR`.

Why it is small but realistic:

- Text is printed at actual intended validation-label sizes.
- The surrounding plate is only there to hold the labels.

Pass criteria:

- `7 mm / 0.8 mm` engraved text is clearly readable.
- `8 mm / 1.0 mm` text is clean.
- `5 mm / 0.6 mm` is readable for short words.
- No slicer mesh repair problems appear.

Record:

- Which style is most readable.
- Whether raised text is worth using anywhere.
- Whether engraved text fills in.

## Test 2: M3 Captured Nut

File:

```text
cad/exports/validation/stl/test_m3_captured_nut_v1.stl
```

Validates:

- One real M3 clearance hole.
- One real captured M3 hex nut pocket.
- One small bridge-plate layer.
- Whether one-screwdriver assembly is possible.

Status:

- Passed first physical validation on 2026-06-06.
- Nut required a light press fit.
- Nut did not rotate.
- Nut did not fall out.
- M3 screw fit was correct.
- Keep current nut pocket dimensions unchanged unless larger seam prints show issues.

Why it is small but realistic:

- It keeps the same M3 hole, nut pocket, retaining lip, and bridge thickness as the captured-nut seam coupons.
- It removes the full seam and duplicate holes.

Pass criteria:

- A standard M3 nut presses in without heat. Passed.
- The nut does not rotate while tightening. Passed.
- The nut does not fall out when inverted. Passed.
- M3 screw fit is correct. Passed.
- PETG does not crack around the retaining lip.

Record:

- Nut across-flats measurement.
- Whether insertion required tools.
- Best screw length tested.
- Whether the retaining lip survives five cycles.

## Test 3: Support Grate Fit

File:

```text
cad/exports/validation/stl/test_support_grate_fit_v1.stl
```

Validates:

- Three real 1:1 support-grate slot/tab clearances.
- `0.4 mm`, `0.6 mm`, and `0.8 mm` clearance per side.
- Real tab width and thickness.

Why it is small but realistic:

- The tab and slot cross-sections are real.
- The slot length and surrounding block are cropped to save print time.

Pass criteria:

- All tabs and slots print as separate bodies.
- `0.6 mm` inserts by hand and has controlled play.
- `0.4 mm` is usable after light cleanup.
- `0.8 mm` is not as loose as the original coupon.

Record:

- Which clearance feels best.
- Whether the 0.4 mm slot binds.
- Whether 0.8 mm is too loose.
- Any rocking or vertical lift.

## Test 4: Sensor Locator v3 Fit

File:

```text
cad/exports/validation/stl/test_sensor_locator_v3_fit_v1.stl
```

Validates:

- Current real `sensor_station_locator_v3` locator geometry.
- Locator tabs.
- Overload stops.
- Dummy sensor.
- Lower pad and upper pad handling.
- Sensor insertion direction and service clearance.

Why it is small but realistic:

- The locator and stops use the same 1:1 v3 geometry.
- Only excess flat base around the station is cropped away.

Pass criteria:

- Dummy sensor installs and removes from the outside.
- Locator tabs prevent obvious sliding/rotation.
- Sensor is not pinched.
- Pads are easy to handle and understand.
- Stops remain visually distinct from locator features.

Record:

- Whether the locator feels too tight or too loose.
- Whether pad placement is intuitive.
- Whether labels are readable.
- Whether debris traps are obvious.

## Test 5: Bolted Seam Slice

File:

```text
cad/exports/validation/stl/test_bolted_seam_slice_v1.stl
```

Validates:

- Two cropped segment edges.
- One bridge plate.
- Two captured M3 nut features instead of four.
- Actual seam/bridge behavior with less print time than a full seam coupon.

Why it is small but realistic:

- M3 holes, nut traps, bridge thickness, seam gap, and same-layer bridge logic remain real.
- Only duplicate width and duplicate fastener pairs are removed.

Pass criteria:

- Nuts retain and do not spin.
- Bridge plate sits flat.
- Seam closes under light screw tightening.
- No upper-to-lower hardware concept is introduced.

Record:

- Screw length.
- Whether the seam closes flush.
- Whether the bridge bends.
- Whether the nut pockets survive repeated cycles.

## What These Replace Or Complement

They complement:

- `label_readability_coupon_v1`
- `support_grate_fit_0p4mm_per_side`
- `support_grate_fit_0p6mm_per_side`
- `support_grate_fit_0p8mm_per_side`
- `sensor_station_locator_v3`
- `bolted_lower_seam_captured_nut_coupon_v1`

They do not replace the larger coupons. Use the practical prints first when a fast, representative answer is enough. Use the larger coupons after the small slices pass.
