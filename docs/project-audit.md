# SaltScale Project Audit

Date: 2026-06-04

## Executive summary

SaltScale has a clear validated direction in the recent project context: four Kiwi/SparkFun-style 50 kg sensors, `sensor_module_v3` as the reference force-path module, and `platform_v6` as the current platform architecture to validate mechanically before electronics or firmware work.

The repository itself is not yet cleanly aligned with that direction. The strongest mechanical concept is `sensor_module_v3`: it has a clear lower pad -> sensor -> upper pad stack, guide walls that stop below the upper pad, and 1 mm overload-stop clearance. `platform_v6` does reuse that module, and the segment bounding boxes fit a Prusa MK4, but the current CAD appears to be an assembly/visualization compound rather than a clean printable/serviceable platform part. In particular, `platform_v6_segment()` unions the whole `sensor_module_v3` assembly, including the sensor placeholder and upper pad, into the segment body, and it does not model the user-facing top plate/centering lip described by the v6 assembly docs.

The largest project risk is stale source-of-truth material. `README.md`, `docs/mechanical-spec-v1.md`, `hardware/bom.md`, `docs/cad-task-001-platform.md`, `docs/codex_prompt.md`, `cad/src/saltscale_base.py`, and older platform files still describe or implement a central single-point loadcell architecture. `hardware/loadcell-spec.md` and the newer sensor/platform docs describe the current four-sensor direction. This contradiction can easily cause future agents or contributors to revert to the wrong architecture.

The single highest-value next action is to print and measure `test_coupon_v1` plus the separate `sensor_module_v3` pads/placeholders, then use those measurements to decide the first minimal CAD correction for serviceable `platform_v6` exports. Do not proceed to electronics, firmware, battery bays, or a full four-segment print yet.

## Critical issues

1. `platform_v6` is not a complete printable/serviceable platform model yet.

   `cad/src/platform_v6.py` creates a lower quarter wedge and ribs, then unions a full `sensor_module_v3` assembly into it (`platform_v6.py` lines 18-34 and 70-73). There is no equivalent of the upper wedge, centering lip, or top contact bosses that `docs/saltscale-v6-assembly-review.md` says should contact the module upper pads (`saltscale-v6-assembly-review.md` lines 21 and 43-47). This means the current v6 CAD does not yet show how tank load enters the sensors.

2. The exported `platform_v6_segment_*.stl` likely traps/fuses parts that are supposed to be serviceable.

   `sensor_module_v3()` returns separate base, lower pad, sensor placeholder, upper pad, and assembly bodies, but its assembly is created by boolean union (`sensor_module_v3.py` lines 63-72). `platform_v6_segment()` inserts that unioned assembly into each segment (`platform_v6.py` lines 70-73). As an STL, this likely becomes one fused solid containing the placeholder sensor and pads, conflicting with the intended service sequence in `docs/saltscale-v6-assembly-review.md` lines 31-39 and 85-91.

3. The repository source of truth contradicts the validated four-sensor architecture.

   Current architecture: `hardware/loadcell-spec.md` states the project changed to four distributed half-bridge sensors (`hardware/loadcell-spec.md` lines 1-15). Contradictory stale docs: `README.md` still says the target hardware is a central 50 kg single-point loadcell and central load path (`README.md` lines 5-9 and 36-42); `docs/mechanical-spec-v1.md` says single-point, centrally mounted (`mechanical-spec-v1.md` lines 32-37); `hardware/bom.md` says not to use SparkFun/Kiwi sensors and recommends LA360-C (`hardware/bom.md` lines 3-15). This is a high-risk drift path.

4. `AGENTS.md` in the repo does not contain the project instructions.

   The actual file contains only three git commands (`AGENTS.md` lines 1-3). It does not contain the mechanical architecture, serviceability, load-path, validation, and workflow constraints supplied in the IDE context. Future agents reading the repo will miss the rules that protect the validated design.

5. The active build exports too many historical and potentially misleading models.

   `cad/build.py` exports v1 through v6, legacy bottom/top segments, sensor modules v1-v3, and test coupons in one run (`cad/build.py` lines 25-116). This preserves history, but a contributor can easily pick obsolete central-loadcell exports as current. The build does not mark `platform_v6` and `test_coupon_v1` as the active validation targets.

## Medium issues

1. The v6 seam and M3 pocket geometry is plausible but not physically specified enough.

   M3 "blind pockets" are 3.5 mm diameter vertical cuts from z=0 to z=8 (`platform_v6.py` lines 36-48). They do not yet define screw head clearance, insert/nut strategy, screw length, or assembly direction. They are safe from a top-to-bottom bridge only because v6 currently lacks a top plate; once a top plate is added, this must be rechecked.

2. Dowel alignment is plausible but needs coupon validation before segment printing.

   The 4.2 mm dowel holes and surrounding bosses are reasonable for 4.0 mm metal dowels (`platform_v6.py` lines 50-62), and the docs correctly call this out as a fit risk. PETG hole shrink and press-fit cracking should be validated on `test_coupon_v1` before relying on it for four large segments.

3. PETG support/bridging risk is concentrated around the sensor pocket and module assembly.

   `sensor_module_v3` has vertical guide walls and overhang-free simple pads, so small parts should print cleanly. The risk is the combined segment export: if the placeholder, lower pad, and upper pad are fused into one STL, slicer behavior and internal surfaces may not represent real assembly or fit.

4. Sensor serviceability is conceptually good, but not yet true in the current v6 segment export.

   The intended sequence is good: install sensor and upper pad from above per segment, then join segments. But the actual v6 segment export does not provide separate segment base, lower pad, upper pad, and sensor placeholder bodies for a serviceable print.

5. `params.py` still carries central loadcell dimensions.

   `platform_v6.py` uses `P.loadcell_length_mm` to set rib clearance (`platform_v6.py` line 21), even though the active architecture uses 38 x 38 x 12 mm sensor placeholders. This is not necessarily harmful yet, but it is stale coupling and makes future edits harder to reason about.

6. Export hygiene is incomplete for generated render attempts.

   `.gitignore` ignores `cad/exports/stl/*.stl` and `cad/exports/step/*.step` (`.gitignore` lines 4-5), but `cad/build.py` attempts PNG exports into `cad/exports/step` (`cad/build.py` lines 46-53). Generated `.png` files are not ignored.

## Minor issues

1. `README.md` build paths are stale or ambiguous.

   The README says `python build.py` and `exports/stl/`, `exports/step/`, but the file is `cad/build.py` and exports land under `cad/exports/...`.

2. `docs/open-questions.md` mixes old and new architecture.

   It includes a note that the design changed to four sensors, but much of the document still discusses central LA360-C dimensions and updates to `platform_v2.py`. It should be marked historical or split into "historical central-loadcell assumptions" and "current four-sensor unknowns."

3. `docs/sensor-module-review.md` is for v1 while the active module is v3.

   It is useful history, but the title makes it easy to read as current. Mark historical or rename the active sensor-module doc around v3.

4. `docs/platform-v4-*` and `docs/platform-v5-*` are useful lineage but need status labels.

   These documents should remain as historical design reviews, not active implementation guidance.

5. `firmware/` exists but is empty.

   That is fine for the current mechanical-validation stage, but it should stay explicitly out of scope until the mechanical coupon and first segment are validated.

## Mechanical architecture assessment

- `sensor_module_v3` is consistent with the intended force path. The lower pad is z=6..8, sensor placeholder z=8..20, upper pad z=20..24, guide walls stop at z=19, and overload stops also stop at z=19. This correctly prevents guide-wall vertical load bypass during normal operation.
- `platform_v6` references and places `sensor_module_v3` at one sensor per quadrant, centered at 45/135/225/315 degrees on a 100 mm radius. That is consistent with the current architecture at the placement level.
- Accidental load bypass is not fully assessable in v6 because the top platform/load-entry geometry is missing. The current lower ribs run to z=42, so any future top plate added at or below that level could create direct top-to-bottom bridges unless carefully separated from ribs and sensor pads.
- Sensors are intended to be serviceable from above before segment joining, but current v6 STL exports do not preserve that separability.
- Segment seams, dowels, and M3 pockets are plausible as first coupon targets, not yet validated as final assembly features.

## Printability assessment

- Computed bounding boxes from the CAD:
  - `platform_v6_segment_0..3`: about 171.8 x 171.8 x 42.0 mm each.
  - `test_coupon_v1`: 140.0 x 140.0 x 24.0 mm.
  - `sensor_module_v3` upper pad: 38.0 x 38.0 x 4.0 mm.
  - `sensor_module_v3` lower pad: 38.0 x 38.0 x 2.0 mm.
  - sensor placeholder: 38.0 x 38.0 x 12.0 mm.
- These fit within the Prusa MK4 200 x 200 x 200 mm constraint.
- The first print should be `test_coupon_v1` plus the separate upper pad, lower pad, and sensor placeholder. Do not print a full v6 segment until the coupon validates pocket fit, 1 mm stop clearance, dowel fit, and M3 pocket behavior.
- PETG tolerances are realistic as starting points: 0.4 mm sensor pocket clearance and 4.2 mm dowel clearance for a 4.0 mm dowel are plausible, but they are not safe to freeze without measurement.

## Documentation quality assessment

Update as current:
- `README.md`: make it four-sensor, mechanical-validation-first, and point to `cad/build.py` and `cad/exports`.
- `AGENTS.md`: replace command-only content with the project rules from the current IDE context.
- `hardware/loadcell-spec.md`: keep as the active sensor architecture, adding chosen vendor details when known.
- `docs/first-print-plan.md` and `docs/test-coupon-v1.md`: keep active, after aligning with the corrected v6 printable/export strategy.

Mark historical or archive:
- `docs/mechanical-spec-v1.md`
- `docs/cad-task-001-platform.md`
- `docs/codex_prompt.md`
- `docs/platform-v4-architecture.md`
- `docs/platform-v4-load-path-review.md`
- `docs/platform-v5-segmentation-review.md`
- `docs/sensor-module-review.md`

Update or split:
- `docs/open-questions.md`: separate stale LA360-C central-loadcell assumptions from current four-sensor unknowns.
- `hardware/bom.md`: replace the central-loadcell shortlist with the current 4x sensor, HX711, ESP32-C3 direction, or mark it historical.
- `docs/saltscale-v6-assembly-review.md`: revise after CAD separates printable/serviceable bodies and adds/defines the real top platform.

## Repository hygiene assessment

- Generated STL/STEP exports are ignored, which is good.
- Generated PNG exports are not ignored.
- `cad/exports/` contains many generated files from historical versions. They are ignored but can confuse local inspection.
- `cad/build.py` is currently modified, and several current docs/CAD files are untracked according to `git status`. This is acceptable during active work, but the next commit should group source/docs logically after review.
- Historical source files (`platform_v1.py` through `platform_v5.py`, `sensor_module_v1.py`, `sensor_module_v2.py`, `saltscale_base.py`) are useful for lineage but should be clearly labeled historical in docs or moved under an archive path later.

## Recommended next actions

1. Print and measure `test_coupon_v1` plus separate `sensor_module_v3` upper pad, lower pad, and sensor placeholder.
2. Record pocket dimensions, insertion/removal force, upper-pad stop clearance, dowel fit, and M3 pocket fit.
3. Based on the coupon, correct `platform_v6` so printable exports separate fixed segment structure from serviceable sensor/pad/placeholder parts.
4. Add or define the actual v6 load-entry/top platform geometry while preserving the `sensor_module_v3` force path and avoiding direct upper-to-lower rib bridges.
5. Update `AGENTS.md`, `README.md`, and `hardware/bom.md` so the repository itself reflects the current four-sensor architecture.
6. Mark central-loadcell docs and older platform docs historical before asking another agent to continue CAD.

## Do not do yet

- Do not create electronics bays, battery doors, button holes, LED holes, or cable routing.
- Do not write firmware.
- Do not choose final HX711 wiring or calibration workflow.
- Do not buy or model final sensor mounting holes until the actual sensor package is confirmed.
- Do not print all four `platform_v6_segment_*` parts yet.
- Do not treat current `platform_v6_segment_*.stl` as a final serviceable printable part.
- Do not revive the central single-point loadcell architecture unless explicitly requested.
- Do not commit generated exports.
