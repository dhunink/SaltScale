# Upper Pad Pocket Alternatives

Date: 2026-06-07

## Purpose

These are three support-free, carrier-relative upper pressure pad pocket alternatives for `concept_v4`.

They intentionally avoid:

- Through-holes in the upper carrier.
- Small underside locator tabs.
- Sensor-relative pad positioning.
- Screws or clips for the upper pad.

They are validation/display coupons only. They do not modify the active `concept_v4` assembly.

## Common Rules

All three concepts keep:

- Removable upper pad.
- PETG-friendly clearance target around `0.4-0.5 mm per side`.
- Broad locating geometry instead of small fragile features.
- Carrier-relative location only.
- No upper-to-lower bypass.

For the coupons, the pocket face is oriented upward so the feature prints support-free on a Prusa MK4/MK4S/Core One. A full upper-segment integration would still need a print-orientation review before replacing the current boss/socket fallback.

## Alternative 1: Chamfered Square Pocket

Files:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_chamfer_square_v1.stl
cad/exports/validation/step/concept_v4_upper_pad_pocket_chamfer_square_v1.step
```

Approximate size:

```text
156 x 78 x 5 mm
```

Intent:

- Keep the current square pad style.
- Use a broad stepped/chamfer-like pocket instead of small locator tabs.
- Locate the pad with flat sides and a shallow lead-in.

Strengths:

- Familiar square pad shape.
- Easy to measure with calipers.
- Least change from the existing square upper pad.

Risks:

- Corners can trap salt dust.
- Square alignment may bind if PETG corners are slightly over-extruded.

## Alternative 2: Round Cup Pocket

Files:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl
cad/exports/validation/step/concept_v4_upper_pad_pocket_round_cup_v1.step
```

Approximate size:

```text
156 x 78 x 5 mm
```

Intent:

- Use a round removable pad in a shallow round cup.
- Avoid rotational alignment concerns.
- Make wiping debris easier than a square pocket.

Strengths:

- Cleanest visually.
- No corner binding.
- Rotation does not matter.
- Likely easiest to clean.

Risks:

- Changes the upper pad footprint from square to round.
- Contact area and pad stiffness should be checked before full integration.

## Alternative 3: Side-Entry Open Saddle

Files:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_side_entry_v1.stl
cad/exports/validation/step/concept_v4_upper_pad_pocket_side_entry_v1.step
```

Approximate size:

```text
177 x 78 x 5 mm
```

Intent:

- Use a broad open-sided pocket that the pad slides into from the outside.
- Avoid a closed debris box.
- Keep the pad removable without lifting straight out.

Strengths:

- Best debris escape path.
- Strong visual service direction: slide in/out from outside.
- No closed pocket around the pad.

Risks:

- Larger footprint.
- May allow pad drift toward the open side unless the upper assembly constrains it.
- Side insertion path could conflict with nearby sensor-station geometry in the full ring.

## Recommendation

Inspect first:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl
```

Reason: it is the cleanest carrier-relative alternative. It avoids through-holes, small tabs, sharp square-corner binding, and sensor-relative uncertainty.

Print second:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_chamfer_square_v1.stl
```

Reason: it preserves the current square pad philosophy and is the most direct comparison against the existing concept.

Print third only if service direction becomes important:

```text
cad/exports/validation/stl/concept_v4_upper_pad_pocket_side_entry_v1.stl
```

Reason: it may be useful for serviceability, but it is larger and less obviously self-retaining.

## Pass Criteria

A pocket alternative passes if:

- Pad inserts/removes by hand.
- No support is needed in the coupon orientation.
- Pad does not rattle enough to drift away from the intended load point.
- Pocket can be cleaned easily.
- Feature looks simpler than the current boss/socket through-hole.

## Full Concept Impact If One Passes

If one of these passes and is chosen for full `concept_v4`:

- Remove the current upper pad through-socket from the upper carrier.
- Remove the central boss from the active upper pad.
- Replace them with the selected carrier-relative pocket/pad pair.
- Re-check support-free print orientation for the full upper segment.
- Re-run upper/lower overlap, support-grate overlap, pad drift, and serviceability checks.
