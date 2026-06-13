# SaltScale Project State Summary

Date: 2026-06-07

## Current Active Architecture

The active mechanical direction is `concept_v4_integrated_joining`.

Current architecture:

- Four Kiwi/SparkFun-style 50 kg load sensors.
- Floating upper carrier over a lower base.
- One sensor station per quadrant.
- Upper and lower structures remain mechanically separate.
- No upper-to-lower fasteners, clips, bridges, ribs, spacers, or locator features.
- Integrated same-layer M3 segment joining.
- Standard M3 bolts and standard captured M3 nuts.
- No heat-set inserts or metal dowels by default.
- Removable support grate with `0.4 mm per side` clearance.
- Removable round upper pressure pad located by a broad Round Cup carrier locator.

Start with:

```text
cad/src/concept_v4_integrated_joining.py
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
cad/exports/active/step/concept_v4_assembly.step
```

## Validated Decisions

Validated or accepted decisions:

- Captured M3 nut pocket dimensions work: light press fit, no nut rotation, nut does not fall out.
- Label standard: engraved text, `7-8 mm` height, `0.8 mm` depth, short labels.
- Support grate default clearance: `0.4 mm per side`.
- Low-profile sensor locator v3 direction is preferred over tall rectangular rails.
- Default segment joining uses common M3 bolts and standard captured nuts.
- Concept v4 seam locator clearance is validated at `0.3 mm per side`; M3 fasteners clamp and locators position.
- Round Cup upper-pad locator is the accepted upper-pad positioning concept.

Validated exports are in:

```text
cad/exports/validated/
docs/validated/
```

## Open Questions

Open questions before full platform printing:

- Real Kiwi/SparkFun sensor dimensions and tolerance.
- Sensor wiring strain relief and connector choice.
- Real sensor fit in the locator station.
- Whether integrated v4 seams tolerate repeated assembly cycles.
- Whether full-size upper/lower segment seams preserve the validated `0.3 mm per side` locator feel over repeated assembly cycles.
- Whether the full upper support grate still feels acceptable with `0.4 mm per side` clearance.
- Long-term PETG creep under a 20-35 kg salt container.

## Rejected Approaches

Rejected or superseded approaches:

- Central single-point loadcell architecture.
- `platform_v1` through `platform_v6` as active paths.
- `concept_v1`, `concept_v2`, and `concept_v3` as active paths.
- Upper pad through-hole boss/socket locator.
- Upper pad sensor-relative locator.
- Small underside-tab upper pad locator.
- Support grate `0.6 mm` and `0.8 mm` per-side clearances as defaults.
- Heat-set inserts and metal dowels as default segment joining hardware.
- Printed-only wedge/dovetail/sliding-key joinery as the default connection method.

Rejected exports are in:

```text
cad/exports/rejected/
docs/rejected/
```

## What Should Be Printed Next

Inspect first:

```text
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Print next for mechanical fit validation:

```text
cad/exports/active/stl/concept_v4_upper_pad.stl
cad/exports/active/stl/concept_v4_upper_segment_0.stl
```

Purpose:

- Validate the Round Cup pad fit in the real upper segment.
- Confirm the pad is removable by hand.
- Confirm the cup is clean and not fragile.
- Inspect top-access upper M3 holes and support-grate receivers in the same real segment.

If avoiding a large segment print, print current experimental seam coupons first:

```text
cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl
cad/exports/experimental/stl/concept_v4_lower_lug_nut_block_v1.stl
```

## Waiting For Kiwi Hardware

Do not finalize these until real hardware arrives:

- Sensor pocket dimensions.
- Upper/lower pad final contact geometry.
- Cable exit and strain relief.
- Sensor replacement procedure with real cable stiffness.
- Load repeatability and calibration behavior.
- Any electronics packaging.

## Recommended Starting Files For New Contributors

Read in this order:

```text
AGENTS.md
docs/project_state_summary.md
docs/active/concept_v4_integrated_joining.md
docs/validated/design-decisions-validated.md
docs/validated/segment-joining-strategy.md
cad/exports/README.md
```

Then inspect:

```text
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
cad/exports/active/stl/concept_v4_upper_segment_0.stl
cad/exports/active/stl/concept_v4_upper_pad.stl
```
