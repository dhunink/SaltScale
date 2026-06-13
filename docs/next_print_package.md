# Next Print Package

Date: 2026-06-08

## Summary

The current repository is clean enough to print from, but the next print should not be a full `concept_v4` segment yet.

The highest-value pre-Kiwi print package is the small `concept_v4` integrated seam validation set. It tests the riskiest current production assumption: whether the integrated M3 lug, captured nut, button-head recess, and printed locator can be assembled repeatedly in PETG without damage or awkwardness.

Do not print rejected, archived, or superseded concepts.

## Current Export Inventory

The current export tree is organized as:

- `cad/exports/active/`: current `concept_v4` printable parts and assembly STEP files.
- `cad/exports/validated/`: prints that validated accepted decisions.
- `cad/exports/experimental/`: useful experiments, including the current `concept_v4` seam validation coupons.
- `cad/exports/rejected/`: rejected alternatives kept for traceability.
- `cad/exports/archive/`: historical platform, concept, and obsolete coupon exports.

Relevant current active printable STLs:

- `cad/exports/active/stl/concept_v4_lower_segment_0.stl`
- `cad/exports/active/stl/concept_v4_upper_segment_0.stl`
- `cad/exports/active/stl/concept_v4_support_grate_bar_x.stl`
- `cad/exports/active/stl/concept_v4_support_grate_bar_y.stl`
- `cad/exports/active/stl/concept_v4_lower_pad.stl`
- `cad/exports/active/stl/concept_v4_upper_pad.stl`
- `cad/exports/active/stl/concept_v4_sensor_placeholder.stl`

Relevant current validation or experiment STLs:

- `cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_upper_lug_mating_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_lug_bolt_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_lug_nut_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p3_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p4_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p5_v1.stl`
- `cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl`
- `cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl`
- `cad/exports/validated/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl`
- `cad/exports/validated/stl/support_grate_fit_0p4mm_per_side.stl`
- `cad/exports/validated/stl/test_m3_captured_nut_v1.stl`
- `cad/exports/validated/stl/label_readability_coupon_v1.stl`
- `cad/exports/validated/stl/sensor_station_locator_v3.stl`

Rejected and archived STLs are not part of the next print package.

## Print Now

### `cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl`

Purpose: tests the upper seam M3 button-head recess in the integrated lug.

Estimated value: very high. This validates whether the top-access upper seam fastener strategy is physically realistic before printing a full upper segment.

Relevance: current and important.

### `cad/exports/experimental/stl/concept_v4_upper_lug_mating_block_v1.stl`

Purpose: mates with the upper lug recess block and tests the captured nut side of the upper seam.

Estimated value: very high. It confirms the nut pocket and bolt path work as a pair.

Relevance: current and important.

### `cad/exports/experimental/stl/concept_v4_lower_lug_bolt_block_v1.stl`

Purpose: tests the lower seam bolt-head side.

Estimated value: high. Lower seams are less risky than upper seams, but the integrated lug still needs physical checking.

Relevance: current.

### `cad/exports/experimental/stl/concept_v4_lower_lug_nut_block_v1.stl`

Purpose: tests the lower seam captured nut side.

Estimated value: high. Confirms the lower fastener stack still works in the new integrated geometry.

Relevance: current.

### `cad/exports/experimental/stl/concept_v4_locator_fit_0p3_v1.stl`

Purpose: validated printed tongue/socket seam locator clearance.

Estimated value: already validated. `0.3 mm per side` remained easy to assemble and gave the best alignment.

Relevance: current validated locator direction. Use this as the reference result; no tighter variant is currently required.

### `cad/exports/experimental/stl/concept_v4_locator_fit_0p4_v1.stl`

Purpose: comparison locator clearance.

Estimated value: completed. It showed unnecessary play compared with `0.3 mm`.

Relevance: superseded comparison result; do not print again unless diagnosing printer variation.

### `cad/exports/experimental/stl/concept_v4_locator_fit_0p5_v1.stl`

Purpose: comparison locator clearance.

Estimated value: completed. It showed unnecessary play compared with `0.3 mm`.

Relevance: superseded comparison result; do not print again unless diagnosing printer variation.

### `cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl`

Purpose: tests one minimal integrated seam with one M3 fastener stack, one captured nut, one locator, and one reinforced lug root.

Estimated value: very high. This is the closest small print to a real v4 seam assembly.

Relevance: current and important.

### `cad/exports/active/stl/concept_v4_upper_pad.stl`

Purpose: prints the current active removable round upper pressure pad.

Estimated value: medium. It is small and useful for checking surface quality and fit against the already validated Round Cup coupon or a future upper segment.

Relevance: current active part.

## Print Later

### `cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl`

Purpose: larger cropped real upper integrated seam coupon.

Estimated value: medium/high after micro coupons pass.

Relevance: current but not first. The micro coupons are the better next print because they are smaller and easier to interpret.

### `cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl`

Purpose: larger cropped real lower integrated seam coupon.

Estimated value: medium/high after micro coupons pass.

Relevance: current but not first.

### `cad/exports/active/stl/concept_v4_upper_segment_0.stl`

Purpose: first real active upper quadrant segment.

Estimated value: high after seam micro coupons pass.

Relevance: current active part, but too large for the first post-baseline print.

### `cad/exports/active/stl/concept_v4_support_grate_bar_x.stl`

Purpose: one active removable support grate bar.

Estimated value: medium after upper segment printing starts.

Relevance: current active part.

### `cad/exports/active/stl/concept_v4_support_grate_bar_y.stl`

Purpose: the other active removable support grate bar.

Estimated value: medium after upper segment printing starts.

Relevance: current active part.

### `cad/exports/validated/stl/concept_v4_upper_pad_pocket_round_cup_v1.stl`

Purpose: validates the accepted Round Cup locator concept.

Estimated value: low if already physically accepted, medium if a new printer/material profile needs confirmation.

Relevance: validated reference, not active production geometry.

### `cad/exports/validated/stl/support_grate_fit_0p4mm_per_side.stl`

Purpose: validates the accepted `0.4 mm per side` support grate tab/slot clearance.

Estimated value: low if already printed and accepted.

Relevance: validated reference.

### `cad/exports/validated/stl/label_readability_coupon_v1.stl`

Purpose: validates label readability.

Estimated value: low because the label standard is already accepted.

Relevance: validated reference only.

### `cad/exports/validated/stl/test_m3_captured_nut_v1.stl`

Purpose: validates the captured M3 nut pocket.

Estimated value: low because the pocket is already accepted.

Relevance: validated reference only.

## Wait For Kiwi Hardware

### `cad/exports/active/stl/concept_v4_lower_segment_0.stl`

Purpose: active lower quadrant segment with sensor station and locator features.

Estimated value: high, but only after seam validation and real sensor arrival.

Relevance: current active part. Wait because the lower segment is large and the riskiest part of it is the real sensor fit.

### `cad/exports/active/stl/concept_v4_lower_pad.stl`

Purpose: active lower contact pad.

Estimated value: medium once real sensor contact geometry is known.

Relevance: current active part. Wait for real sensor fit and contact evaluation.

### `cad/exports/active/stl/concept_v4_sensor_placeholder.stl`

Purpose: visual/mechanical dummy for assembly planning.

Estimated value: low once real Kiwi hardware is on the way.

Relevance: active visualization helper, not a substitute for the real sensor.

### `cad/exports/validated/stl/sensor_station_locator_v3.stl`

Purpose: sensor locator validation coupon.

Estimated value: high with the real Kiwi/SparkFun sensor, lower without it.

Relevance: validated direction, but real sensor fit remains unvalidated.

### `cad/exports/validated/stl/test_sensor_locator_v3_fit_v1.stl`

Purpose: practical sensor locator fit test.

Estimated value: high with the real sensor, lower before hardware.

Relevance: validated direction, but best saved for real sensor arrival.

## Not Recommended

Do not print these for the current next session:

- Anything in `cad/exports/rejected/`.
- Anything in `cad/exports/archive/`.
- Printed-only wedge, dovetail, or sliding-key joinery coupons unless explicitly revisiting experimental no-metal joining.
- Old bolted bridge-plate seam coupons unless comparing against the rejected bridge-plate strategy.
- Full active upper or lower segments before the v4 integrated seam micro coupons pass.

## Integrated Seam Validation Status

Concept v4 integrated seam validation still exists.

Current small replacements:

- `cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_upper_lug_mating_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_lug_bolt_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_lug_nut_block_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p3_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p4_v1.stl`
- `cad/exports/experimental/stl/concept_v4_locator_fit_0p5_v1.stl`
- `cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl`

Larger cropped seam coupons also exist:

- `cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl`
- `cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl`

The small micro coupons should be treated as the current replacement test for first physical validation. The larger seam coupons remain useful later if the micro coupons pass.

## One Print Plate For Tonight

If printing one plate tonight, use this set:

```text
cad/exports/experimental/stl/concept_v4_upper_lug_recess_block_v1.stl
cad/exports/experimental/stl/concept_v4_upper_lug_mating_block_v1.stl
cad/exports/experimental/stl/concept_v4_lower_lug_bolt_block_v1.stl
cad/exports/experimental/stl/concept_v4_lower_lug_nut_block_v1.stl
cad/exports/experimental/stl/concept_v4_locator_fit_0p3_v1.stl
cad/exports/experimental/stl/concept_v4_integrated_mini_seam_test_v1.stl
cad/exports/active/stl/concept_v4_upper_pad.stl
```

Why this plate:

- It tests the integrated seam without printing a full segment.
- It checks both upper and lower M3 fastener stacks.
- It uses the now-validated `0.3 mm per side` seam locator clearance.
- It tests the mini real seam interaction between locator and fastener.
- It adds the active upper pad because it is small and useful.

Required hardware:

- M3 button-head screws matching the v4 assumption.
- Standard M3 hex nuts.
- Small screwdriver.
- Optional calipers for measuring fit and wear.

## What To Record

For each printed seam part:

- Does the nut press in lightly?
- Does the nut rotate during tightening?
- Does the nut fall out during handling?
- Does the M3 screw pass cleanly?
- Does the button head seat flush or below the intended surface?
- Does the locator assemble by hand?
- Does the validated `0.3 mm per side` locator still feel controlled in the integrated mini seam?
- Does the integrated mini seam clamp without rocking?
- Does the seam survive five assemble/disassemble cycles?
- Are labels readable enough to help assembly?

## Biggest Remaining Risk

The biggest pre-Kiwi risk is the integrated v4 seam.

Reason:

- It is new in concept v4.
- It replaces the earlier bridge-plate approach.
- It affects every upper and lower segment seam.
- If it is hard to assemble, weak, or poorly aligned, full segment prints would waste much more filament.

The biggest post-Kiwi risk is real sensor fit and load contact behavior in the sensor station.

