# Bolted Captured-Nut Coupon Plan

Date: 2026-06-06

## Summary

The captured-nut bolted seam coupons validate the preferred default segment joining direction for `concept_v2`.

Physical validation on 2026-06-06 passed for the current captured M3 nut pocket geometry. The nut required a light press fit, did not rotate during tightening, did not fall out during assembly, and the M3 screw fit was correct. Keep the current nut pocket dimensions unchanged unless future larger seam or quadrant prints show assembly issues.

Generated coupon targets:

- `bolted_lower_seam_captured_nut_coupon_v1`
- `bolted_upper_seam_captured_nut_coupon_v1`

Each coupon is a small print-flat kit, not a full segment. It contains:

- Two segment-edge blocks.
- One removable printed bridge plate.
- Four M3 clearance holes.
- Four underside captured hex nut pockets for standard M3 nuts.

No heat-set inserts, dowels, supports, or upper-to-lower connections are used.

## Why Captured Nuts

The open-nut bolted coupon proves the basic M3 bolt, nut, and bridge plate strategy, but the nut must be held manually during assembly.

The captured-nut variant should allow one-screwdriver assembly:

```text
top side:    screwdriver + M3 bolt
printed:     bridge plate + segment blocks
underside:   captured standard M3 nut
```

The hex pocket prevents nut rotation. The smaller retaining lip should keep the nut from falling out while the builder places the bridge and starts the bolt.

## Nut Pocket Dimensions

Current CAD dimensions:

| Feature | Dimension |
| --- | ---: |
| M3 clearance hole | 3.4 mm diameter |
| Captured nut pocket | 5.9 mm across flats |
| Retaining lip opening | 5.35 mm across flats |
| Captured nut pocket depth | 3.0 mm |
| Retaining lip depth | 0.7 mm |
| Bridge plate thickness | 4.0 mm |
| Segment block thickness | 8.0 mm |

These dimensions assume common M3 hex nuts. Real M3 nuts vary by supplier, but the first physical test passed with the current dimensions. Treat these as the current accepted prototype dimensions.

## Hardware

For one coupon:

- 4x standard M3 hex nuts.
- 4x M3 bolts.
- Optional M3 washers under bolt heads.

Start with:

```text
M3x14
```

M3x12 may not have enough thread engagement through a 4 mm bridge plus 8 mm segment block. M3x16 should also work for testing, but may protrude below the nut depending on nut thickness.

## Assembly Steps

1. Print `bolted_lower_seam_captured_nut_coupon_v1.stl` flat.
2. Separate the two segment-edge blocks and bridge plate if the slicer imports them as one multi-body STL.
3. Remove stringing from the M3 holes and nut pockets.
4. Press one standard M3 nut into each underside captured pocket.
5. Confirm each nut is seated flat and does not fall out when the block is turned upright.
6. Put the two segment-edge blocks seam-to-seam.
7. Place the printed bridge plate over the seam.
8. Insert four M3 bolts from the top.
9. Tighten with one screwdriver, alternating bolts to avoid bending the bridge.
10. Stop when the seam is held closed. Do not crush PETG.

## Pass Criteria

The current pocket geometry has passed these criteria in the first physical test:

- Nuts press in by hand or with light plier pressure.
- Nuts do not rotate during tightening.
- Nuts do not fall out when the block is turned upright before bolt insertion.
- M3 bolts pass through the printed clearance holes after only light cleanup.

The full seam coupon should still be checked against the remaining criteria:

- The bridge plate pulls flat against both segment blocks.
- The seam stays closed under hand handling.
- The parts disassemble without tearing the retaining lip.
- No cracking appears around nut pockets after five assembly cycles.

## Fail Criteria

The coupon fails if:

- Nuts cannot be inserted without damaging PETG.
- Nuts spin in the pocket.
- Nuts fall out before assembly.
- Bolts bind badly in the clearance holes.
- The bridge rocks or cannot sit flat.
- The seam remains visibly open after tightening.
- The nut pocket cracks or delaminates.

## What To Measure

After printing, record:

- Actual nut across-flats dimension.
- Whether nuts seat flush.
- Whether each nut is retained when inverted.
- Bolt length used.
- Thread engagement with M3x12, M3x14, and M3x16 if available.
- Amount of cleanup required for M3 holes.
- Whether the bridge plate lies flat.
- Whether labels remain readable.
- Condition of retaining lips after five assembly cycles.

## Likely CAD Changes If It Fails

If nuts are too tight:

- Increase captured pocket across-flats dimension.
- Add a small lead-in chamfer or insertion relief.

If nuts fall out:

- Reduce retaining lip opening.
- Increase retaining lip depth slightly.

If nuts spin:

- Reduce captured pocket across-flats dimension.
- Increase pocket depth so more nut face is engaged.

If PETG cracks:

- Increase surrounding material.
- Reduce retention interference.
- Use the open-nut coupon as the safer baseline.

## Recommended First Print

The small captured-nut interface has passed. The next seam print should be:

```text
cad/exports/validation/stl/bolted_lower_seam_captured_nut_coupon_v1.stl
```

The lower seam coupon is the simpler next validation because it tests the default same-layer lower ring joining strategy without upper-carrier access questions.
