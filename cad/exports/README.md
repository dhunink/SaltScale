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
cad/exports/active/stl/concept_v4_sensor_placeholder.stl
```

Active v4 includes:

- Four-sensor floating upper/lower architecture.
- Integrated M3 segment joining.
- Top-access upper M3 button-head screws.
- Captured standard M3 nuts.
- No heat-set inserts or dowels by default.
- Support grate clearance at `0.4 mm per side`.
- Round Cup removable upper-pad locator.

### `validated/`

Validation artifacts that represent accepted decisions.

Examples:

```text
cad/exports/validated/stl/test_m3_captured_nut_v1.stl
cad/exports/validated/stl/support_grate_fit_0p4mm_per_side.stl
cad/exports/validated/stl/sensor_station_locator_v3.stl
cad/exports/validated/stl/label_readability_coupon_v1.stl
cad/exports/validated/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl
```

### `experimental/`

Useful experiments that are not the active default.

Examples:

```text
cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl
cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl
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
