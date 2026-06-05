# SaltScale CAD Exports

These generated CAD exports are intentionally kept in the repository for GitHub visibility. They let builders inspect and slice the current design without installing CadQuery first.

## Folder Structure

### `active/`

Current design direction: `concept_v2`.

Use this folder for the latest inspectable SaltScale concept_v2 architecture files:

- `active/step/concept_v2_assembly.step`
- `active/stl/concept_v2_lower_segment_0.stl`
- `active/stl/concept_v2_upper_segment_0.stl`
- `active/stl/concept_v2_support_grate.stl`

These are active architecture exports, not a release-ready print set. Do not print the full platform before the validation coupons pass.

### `validation/`

Current test prints and coupons that are useful before printing full ring segments.

Recommended first print:

```text
validation/stl/sensor_station_locator_v3.stl
```

Also still relevant:

- `validation/stl/centering_lip_coupon_v1.stl`

Future support-grate fit variants and printed-only joinery coupons should also be exported here when their source modules exist.

### `archive/`

Historical exports retained for traceability.

This includes:

- `platform_v1` through `platform_v6`
- `concept_v1`
- old `sensor_module_v1` through `sensor_module_v3` exports
- old `test_coupon_v1` files
- old `saltscale_v1` top/bottom segment exports
- superseded concept_v2 coupons such as `sensor_station_coupon_v2` and the M3/dowel seam coupons

Archive files are useful for design history, but they are not recommended as current print targets.

## Build Behavior

Run:

```text
python3 cad/build.py
```

The build script writes future exports into:

- `active/` for current concept_v2 main files
- `validation/` for current test prints and coupons
- `archive/` for historical exports

The legacy flat folders `cad/exports/stl/` and `cad/exports/step/` are ignored and should remain unused.

Accidental generated PNG files are ignored by Git unless explicitly requested later.
