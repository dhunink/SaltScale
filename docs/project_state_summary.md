# SaltScale Project State Summary

Date: 2026-06-15

## Current Active Architecture

The active mechanical direction is now `concept_v5_cartridge_scale`.

Current architecture:

- Four Kiwi/SparkFun-style 50 kg load sensors.
- Floating upper carrier over a lower base.
- One removable sensor cartridge per quadrant.
- Support-free over-wall cartridge retainer.
- Validated cartridge locator walls: `7.1 mm` above the cartridge floor.
- Upper and lower structures remain mechanically separate.
- No normal upper-to-lower fasteners or force-shunting contacts.
- Captive load puck concept in the upper ring remains experimental.
- Minimal metal fasteners remain preferred; use screws only where the print tests show they earn their keep.

Start with:

```text
cad/src/concept_v5_cartridge_scale.py
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
docs/concept_v5_cartridge_scale.md
docs/concept_v5_system_architecture.md
```

## Validated Decisions

Validated or accepted decisions:

- Captured M3 nut pocket dimensions work: light press fit, no nut rotation, nut does not fall out.
- Label standard: engraved text, `7-8 mm` height, `0.8 mm` depth, short labels.
- Support grate default clearance: `0.4 mm per side`.
- Low-profile sensor locator v3 direction is preferred over tall rectangular rails.
- Default segment joining uses common M3 bolts and standard captured nuts.
- Concept v4 seam locator clearance is validated at `0.3 mm per side`; M3 fasteners clamp and locators position.
- Round Cup upper-pad locator is retired from active geometry; the current pad uses a removable lobe/socket locator.
- Measured Kiwi sensor dimensions are `34.07 mm` wide and `6.84 mm` thick.
- Concept-v5 sensor cartridge with `7.1 mm` raised locator walls is physically validated: the sensor fit is snug with only minimal movement.
- Concept-v5 over-wall retainer direction is the accepted cartridge baseline.
- Hand-tight keyhole puck tests: `0.20 mm` is the best tested retention fit; `0.35 mm` and `0.50 mm` are too loose.

Validated exports are in:

```text
cad/exports/validated/
docs/validated/
```

## Open Questions

Open questions before full platform printing:

- Final captive puck architecture in the upper ring.
- Whether puck retention should use top-down insertion plus keeper, a compliant latch, or a two-piece printed capture.
- Long-term repeatability of the validated cartridge/retainer after repeated sensor service.
- Sensor wiring strain relief and connector choice.
- Segment joining strategy for the concept-v5 full ring.
- Upper/lower lift retention with free play, without normal weighing contact.
- Long-term PETG creep under a 20-35 kg salt container.

## Rejected Approaches

Rejected or superseded approaches:

- Central single-point loadcell architecture.
- `platform_v1` through `platform_v6` as active paths.
- `concept_v1`, `concept_v2`, and `concept_v3` as active paths.
- `concept_v4_integrated_joining` as the current active path; it remains useful prior art, but concept v5 supersedes it.
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
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
```

Print next for mechanical fit validation only if the generated files changed:

```text
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_cartridge.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_retainer_clip.stl
```

Purpose:

- Confirm the default exported cartridge is the validated `7.1 mm` wall version.
- Confirm retainer fit still matches the physical test result.
- Then continue with full upper/lower ring integration and the still-open puck capture design.

## Recommended Starting Files For New Contributors

Read in this order:

```text
AGENTS.md
docs/project_state_summary.md
docs/concept_v5_cartridge_scale.md
docs/concept_v5_system_architecture.md
cad/exports/README.md
```

Then inspect:

```text
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_cartridge.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_retainer_clip.stl
```
