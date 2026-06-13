# SaltScale CAD Exports

Generated CAD exports are intentionally kept in the repository so builders can inspect and slice the current design without installing CadQuery first.

## Folder Map

### `active/`

Current active design only.

Active architecture: `concept_v4_integrated_joining`.

Recommended first STEP to inspect:

```text
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Active printable STLs:

```text
cad/exports/active/stl/concept_v4_lower_segment_0.stl
cad/exports/active/stl/concept_v4_upper_segment_0.stl
cad/exports/active/stl/concept_v4_support_grate_bar_x.stl
cad/exports/active/stl/concept_v4_support_grate_bar_y.stl
cad/exports/active/stl/concept_v4_lower_pad.stl
cad/exports/active/stl/concept_v4_upper_pad.stl
cad/exports/active/stl/concept_v4_sensor_quarter_turn_clip.stl
cad/exports/active/stl/concept_v4_sensor_placeholder.stl
cad/exports/active/stl/concept_v4_kiwi_sensor_reference_v1.stl
```

Active v4 includes:

- Four-sensor floating upper/lower architecture.
- Integrated M3 segment joining.
- Top-access upper M3 button-head screws.
- Captured standard M3 nuts.
- No heat-set inserts or dowels by default.
- Support grate clearance at `0.4 mm per side`.
- Round Cup upper-carrier locator retired from active geometry; the upper segment is flat in the sensor area.
- Upper integrated M3 lugs are same-plane with the main upper segment body for flat printing.
- Dimensionally representative `kiwi_sensor_reference_v1` in concept_v4 assemblies.
- Real-sensor stack using `6.84 mm` sensor thickness.
- Removable upper pad with `40 mm` body, `36 mm` upper locating lobe, and `12 mm` contact boss; the pad STL is print-oriented for support-free printing.
- Lower pad revised to `36 mm` rounded-square support.
- Sensor locator revised around the measured `34.07 mm` body with `0.2 mm per side` current test clearance.
- Front sensor locator posts now act as pivots for separate quarter-turn retention clips; clips are anti-lift/handling retention only and are not part of the weighing load path.
- Integrated seam locator clearance validated at `0.3 mm per side`.

### `validated/`

Validation artifacts that represent accepted decisions.

Examples:

```text
cad/exports/validated/stl/test_m3_captured_nut_v1.stl
cad/exports/validated/stl/support_grate_fit_0p4mm_per_side.stl
cad/exports/validated/stl/sensor_station_locator_v3.stl
cad/exports/validated/stl/label_readability_coupon_v1.stl
```

### `experimental/`

Useful experiments that are not the active default.

Examples:

```text
cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl
cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl
cad/exports/experimental/stl/concept_v4_upper_pad_12mm_boss_test_v2.stl
cad/exports/experimental/stl/concept_v4_lower_support_test_v1.stl
cad/exports/experimental/stl/concept_v4_real_sensor_locator_test_v2.stl
cad/exports/experimental/stl/concept_v4_sensor_clip_station_coupon_v2.stl
cad/exports/experimental/stl/printed_lower_seam_wedge_coupon_v2.stl
```

### `rejected/`

Rejected or superseded validation concepts kept for traceability.

Examples:

```text
cad/exports/rejected/stl/concept_v4_upper_pad_sensor_relative_test_v1.stl
cad/exports/rejected/stl/concept_v4_upper_pad_carrier_pocket_test_v1.stl
cad/exports/rejected/stl/concept_v4_upper_pad_pocket_chamfer_square_v1.stl
cad/exports/rejected/stl/concept_v4_upper_pad_pocket_side_entry_v1.stl
cad/exports/rejected/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl
cad/exports/rejected/stl/support_grate_fit_0p6mm_per_side.stl
cad/exports/rejected/stl/support_grate_fit_0p8mm_per_side.stl
```

### `archive/`

Historical exports retained for traceability.

This includes:

- `platform_v1` through `platform_v6`.
- `concept_v1`, `concept_v2`, and `concept_v3` exports.
- Old sensor module exports.
- Old test coupons and duplicate migrated exports.

## Build Behavior

Run:

```text
python3 cad/build.py
```

The build writes future exports into:

```text
cad/exports/active/
cad/exports/validated/
cad/exports/experimental/
cad/exports/rejected/
cad/exports/archive/
```

The old `cad/exports/validation/` folder is superseded by the clearer `validated/`, `experimental/`, and `rejected/` folders.
