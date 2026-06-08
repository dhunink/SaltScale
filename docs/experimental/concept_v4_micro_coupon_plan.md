# Concept v4 Micro Coupon Plan

Date: 2026-06-07

## Summary

The first concept v4 integrated seam coupons used cropped real segment geometry. They were useful for CAD review, but too large and awkward for fast physical validation. They also exported as combined bodies that were not convenient to split into the exact functional pieces a builder needs to test.

The new micro coupons keep real 1:1 interface geometry while removing almost all surrounding ring material. They are intended to answer the risky questions before printing full `concept_v4` segments.

## What Stayed Real

The micro coupons preserve:

- M3 clearance diameter.
- Captured M3 nut pocket geometry.
- Upper M3 button-head counterbore geometry.
- Lug thickness.
- Lug root shoulder geometry.
- Tongue/socket locator proportions and tested clearance variants.
- Engraved short labels only.

## Why The Older Coupons Were Too Large

The older coupons were cropped from full segment pairs. That preserved context, but it also included too much ring material. In practice they were less convenient because:

- They used more filament than needed for first seam checks.
- They took longer to print.
- Their functional test pieces were not exported as separate STLs.
- They were harder to orient and reason about in PrusaSlicer.

Those older coupons can remain available, but the micro coupons should be used first.

## Generated Micro Coupons

### Upper lug recess test

Files:

```text
cad/exports/validation/stl/concept_v4_upper_lug_recess_block_v1.stl
cad/exports/validation/stl/concept_v4_upper_lug_mating_block_v1.stl
```

Approximate dimensions:

- Upper lug recess block: `43 x 34 x 4 mm`.
- Mating upper nut block: `36 x 30 x 8 mm`.

Validates:

- M3 button-head recess diameter and depth.
- Bolt insertion from underside.
- Captured nut from top side.
- Tightening stack feel.

Pass criteria:

- M3 button head seats flush or below the lower lug face.
- Bolt passes through without drilling.
- Nut presses in with light force.
- Nut does not rotate while tightening.
- Parts clamp without visible cracking or crushing.

Fail criteria:

- Bolt head protrudes below the lug face.
- Counterbore is too tight or ragged.
- Nut spins.
- Lug cracks or bows under normal hand tightening.

Likely CAD response if it fails:

- Adjust button-head counterbore diameter/depth.
- Increase lug thickness only if counterbore depth cannot be made safe.

### Lower lug/nut test

Files:

```text
cad/exports/validation/stl/concept_v4_lower_lug_bolt_block_v1.stl
cad/exports/validation/stl/concept_v4_lower_lug_nut_block_v1.stl
```

Approximate dimensions:

- Lower lug bolt block: `43 x 34 x 4 mm`.
- Lower nut block: `36 x 30 x 8 mm`.

Validates:

- Lower bolt head seat.
- Lower captured nut from underside.
- Lower seam fastener stack.

Pass criteria:

- Bolt inserts from above.
- Nut presses from underside and remains retained.
- Tightening does not crush the lug.

Likely CAD response if it fails:

- Adjust lower head seat or nut pocket access.

### Locator fit test

Files:

```text
cad/exports/validation/stl/concept_v4_locator_fit_0p3_v1.stl
cad/exports/validation/stl/concept_v4_locator_fit_0p4_v1.stl
cad/exports/validation/stl/concept_v4_locator_fit_0p5_v1.stl
```

Approximate dimensions:

- Each variant: about `88 x 31 x 6 mm`.

Validates:

- Tongue/socket fit independent of fasteners.
- PETG clearance choice for same-layer seam alignment.

Expected feel:

- `0.3 mm`: snug, may need cleanup on over-extruded PETG.
- `0.4 mm`: likely best default if it slides without wobble.
- `0.5 mm`: safer for many printers, but may allow more seam play.

Pass criteria:

- Tongue starts by hand.
- No hammering required.
- Parts seat fully after normal deburring.
- No obvious side play once seated.

Likely CAD response if it fails:

- Choose the smallest clearance that remains hand-assemblable and repeatable.

### Integrated mini seam test

File:

```text
cad/exports/validation/stl/concept_v4_integrated_mini_seam_test_v1.stl
```

Approximate dimensions:

- About `99 x 49 x 8 mm`.

Validates:

- One M3 fastener stack.
- One captured nut.
- One tongue/socket locator.
- One reinforced lug-root layout.
- Minimal same-layer seam assembly behavior.

Pass criteria:

- Both sides print cleanly without supports.
- Nut and bolt fit correctly.
- Locator seats without fighting the bolt.
- Seam clamps without visible rocking.
- Five assemble/disassemble cycles do not damage the lug or locator.

Likely CAD response if it fails:

- Tune locator clearance before changing the full segment.
- Increase lug-root shoulder only if visible cracking occurs.

## Recommended Print Order

1. `concept_v4_upper_lug_recess_block_v1.stl` and `concept_v4_upper_lug_mating_block_v1.stl`
2. `concept_v4_locator_fit_0p4_v1.stl`
3. `concept_v4_locator_fit_0p3_v1.stl` and `concept_v4_locator_fit_0p5_v1.stl` if 0.4 is not clearly right
4. `concept_v4_lower_lug_bolt_block_v1.stl` and `concept_v4_lower_lug_nut_block_v1.stl`
5. `concept_v4_integrated_mini_seam_test_v1.stl`

## How Results Affect Full Concept v4

Do not print full `concept_v4` segments until these checks pass:

- Upper M3 button-head recess is confirmed flush/recessed.
- Captured nut fit remains good in the new blocks.
- Locator clearance is chosen.
- Mini seam assembles, clamps, and disassembles cleanly.

If all pass, the next print should be one full `concept_v4_lower_segment_0` or a larger two-segment partial assembly, not the full platform.
