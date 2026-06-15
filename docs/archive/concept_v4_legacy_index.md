# Concept V4 Legacy Index

Updated: 2026-06-15

This project has moved from `concept_v4_integrated_joining` to
`concept_v5_cartridge_scale`.

The v4 work is still valuable prior art, but it should no longer be treated as
the active build path. Use it mainly for historical decisions and print-test
lessons.

## Current Starting Point

Use these files first:

```text
docs/project_state_summary.md
docs/concept_v5_cartridge_scale.md
docs/concept_v5_system_architecture.md
cad/src/concept_v5_cartridge_scale.py
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
```

## Legacy V4 References

The previous active design was:

```text
docs/active/concept_v4_integrated_joining.md
cad/src/concept_v4_integrated_joining.py
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Useful retained v4 lessons:

- Four-sensor architecture is still preferred.
- Integrated segment joining and M3 captured-nut tests remain useful.
- Support-free printing constraints remain central.
- Earlier sensor locators and quarter-turn clips are superseded by the v5
  removable cartridge.
- Round-cup upper pad locating is not the current active puck strategy.

## Export Folder Meaning

```text
cad/exports/concept_v5_cartridge/   current validated cartridge baseline
cad/exports/active/                 legacy v4 active exports
cad/exports/validated/              v4-era accepted coupons and tests
cad/exports/experimental/           v4-era experiments
cad/exports/rejected/               rejected or superseded tests
cad/exports/archive/                older v1-v3/platform history
```

## Puck Status

The upper-ring puck capture is still open. The latest keyhole tests showed:

- `0.20 mm` radial clearance is the best tested variant.
- `0.35 mm` and `0.50 mm` are too loose.
- `0.20 mm` does not fall out when inverted, but it is still removable by hand.
- PETG did not flex enough for side-slide insertion; the puck currently installs
  only by pressing it from above.

So the next puck design should not assume the current side-entry keyhole is a
validated captive interface.
