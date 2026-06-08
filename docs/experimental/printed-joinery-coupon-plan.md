# Printed Joinery Coupon Plan

Date: 2026-06-05

## Summary

This document is now historical for default strategy selection.

The current default segment joining strategy is documented in `docs/segment-joining-strategy.md`: M3 bolts, standard M3 nuts, and printed bridge plates. Printed-only joints remain experimental validation coupons.

SaltScale should not require metal dowels or heat-set inserts for the default open-source assembly. Earlier work explored whether the default path could be fully printed, low-cost, removable, and hobby-friendly.

This plan defines printed-only seam coupons for `concept_v2`. They do not modify the full platform geometry. They are small validation prints for upper-to-upper and lower-to-lower segment joining only.

Current coupon targets:

- `printed_lower_seam_sliding_key_coupon_v1`
- `printed_upper_seam_sliding_key_coupon_v1`
- `printed_lower_seam_true_dovetail_coupon_v1`
- `printed_upper_seam_true_dovetail_coupon_v1`
- `printed_lower_seam_wedge_coupon_v2`
- `printed_upper_seam_wedge_coupon_v2`

Archived/misleading names:

- `printed_lower_seam_dovetail_coupon_v1`
- `printed_upper_seam_dovetail_coupon_v1`

Those v1 dovetail exports were reclassified because the printed geometry behaved more like a straight sliding key than a true mechanically captured dovetail.

Each current coupon is a print-flat kit containing:

- Two segment-edge blocks.
- One separate removable printed key.
- Short engraved labels: `LOWER`, `UPPER`, `KEY`, `OUT`, `IN`, `SLIDE`, `DOVE`, or `WEDGE`.

## Why no-metal joinery was explored

Printed-only joinery was explored because it:

- Reduces hardware cost.
- Avoids heat-set insert tools.
- Avoids 4 mm dowel sourcing.
- Avoids corrosion-prone alignment hardware near salt.
- Makes the design easier to reproduce from only filament and common hand tools.
- Could keep M3 inserts and metal dowels as optional upgrades rather than default requirements.

The printed joinery remains same-layer only. It must never connect the floating upper carrier to the lower base.

After wedge analysis, printed-only joinery is no longer recommended as the default. The wedge key mainly prevents separation after manual seam closure; it does not actively pull the seam closed. These coupons remain useful experiments.

## Strategy 1: sliding key

Files:

- `cad/exports/validation/stl/printed_lower_seam_sliding_key_coupon_v1.stl`
- `cad/exports/validation/step/printed_lower_seam_sliding_key_coupon_v1.step`
- `cad/exports/validation/stl/printed_upper_seam_sliding_key_coupon_v1.stl`
- `cad/exports/validation/step/printed_upper_seam_sliding_key_coupon_v1.step`

What it tests:

- A straight printed key sliding into a top-open slot across the seam.
- Simple printed alignment and basic seam separation resistance.
- Removability with minimum geometry and no hardware.

Important limitation:

- This is not a dovetail.
- It is not mechanically captured against vertical pull-out.
- It is useful as a simple printed key, but it should not be treated as the strongest no-metal option.

Expected fit:

- Easiest to print and clean.
- Should slide by hand after light deburring.
- May have more rattle or lift than the dovetail or wedge.

Pass criteria:

- Key inserts fully by hand.
- Key removes by hand.
- Blocks do not separate under light hand pulling while the key is seated.
- No key or slot cracking after five insert/remove cycles.

## Strategy 2: true dovetail

Files:

- `cad/exports/validation/stl/printed_lower_seam_true_dovetail_coupon_v1.stl`
- `cad/exports/validation/step/printed_lower_seam_true_dovetail_coupon_v1.step`
- `cad/exports/validation/stl/printed_upper_seam_true_dovetail_coupon_v1.stl`
- `cad/exports/validation/step/printed_upper_seam_true_dovetail_coupon_v1.step`

What it tests:

- A trapezoidal/dovetail key sliding into a matching undercut slot.
- Mechanical capture against seam pull-out perpendicular to the seam.
- Whether PETG can print the shallow dovetail lips cleanly without supports.
- Whether the captured key remains removable.

Expected fit:

- Strongest mechanical capture if the print is accurate.
- More tolerance-sensitive than sliding key or wedge.
- May need careful elephant-foot cleanup before insertion.

Pass criteria:

- Key starts from the end and slides fully into the dovetail slot.
- Blocks resist seam separation better than the sliding key.
- Key can still be removed without damaging the lips.
- Dovetail lips do not crack or delaminate.

Fail criteria:

- Key cannot start after normal cleanup.
- Key jams partway through.
- Dovetail lips split.
- Print variation makes the fit unreliable.

## Strategy 3: wedge key v2

Files:

- `cad/exports/validation/stl/printed_lower_seam_wedge_coupon_v2.stl`
- `cad/exports/validation/step/printed_lower_seam_wedge_coupon_v2.step`
- `cad/exports/validation/stl/printed_upper_seam_wedge_coupon_v2.stl`
- `cad/exports/validation/step/printed_upper_seam_wedge_coupon_v2.step`

What it tests:

- A tapered printed key in a matching tapered top-open pocket.
- Progressive self-tightening as the wedge is pushed from `OUT` toward `IN`.
- A more forgiving printed-only seam than the true dovetail.
- Removability with light hand-tool assistance.

Expected fit:

- Easier to start than the true dovetail.
- More clamping action than the sliding key.
- Likely best beginner-friendly no-metal option if it seats repeatably.

Pass criteria:

- Wedge starts easily.
- Wedge seats with thumb pressure or light tool pressure.
- Blocks resist light to moderate seam pulling.
- Wedge can be removed without damaging the pocket.
- No visible wear problem after five insert/remove cycles.

Fail criteria:

- Wedge bottoms out while the seam remains loose.
- Wedge requires hammering.
- Wedge chews up the pocket.
- Blocks separate easily while the wedge is installed.

## Strategy considered but not generated: tongue-and-groove only

A tongue-and-groove-only seam was considered, but it mainly improves alignment, not retention. It may be combined with one of the generated strategies later, but by itself it is not enough for the default seam connection.

## Recommended printed-only experiment

If testing printed-only joinery anyway, print first:

```text
cad/exports/validation/stl/printed_lower_seam_wedge_coupon_v2.stl
```

Reason:

- It is the most beginner-friendly no-metal candidate.
- It should be less tolerance-sensitive than the true dovetail.
- It may reduce play better than the simple sliding key.
- The lower seam is the simpler same-layer first test.

For the current default segment-joining strategy, print this instead:

```text
cad/exports/validation/stl/bolted_lower_seam_coupon_v1.stl
```

Print second:

```text
cad/exports/validation/stl/printed_lower_seam_true_dovetail_coupon_v1.stl
```

Reason:

- It tests the strongest mechanically captured no-metal option.
- It is worth validating after the easier wedge fit is understood.

Print third only if needed:

```text
cad/exports/validation/stl/printed_lower_seam_sliding_key_coupon_v1.stl
```

Reason:

- It is simple and may still be useful, but it is not mechanically locked like a dovetail and should not be the preferred default unless the other designs fail.

## What to measure

For each coupon:

- Whether the key starts by hand.
- Whether the key seats fully.
- Whether the seam closes flush.
- How much force is needed to remove the key.
- Whether visible wear appears after five insert/remove cycles.
- Whether the blocks separate under hand pulling.
- Whether labels remain readable after printing.

## Design recommendation after testing

Experimental printed-only candidate if it passes:

- Wedge key v2.

Stronger optional printed-only candidate:

- True dovetail.

Simplest printed-only fallback:

- Sliding key.

Use M3 bolts, standard M3 nuts, and printed bridge plates as the current default. Keep heat-set inserts as optional. Keep metal dowels out of the default unless future testing proves they are necessary.
