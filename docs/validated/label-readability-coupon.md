# Label Readability Coupon

Date: 2026-06-06

## Summary

`label_readability_coupon_v1` is a small PETG text test for Prusa MK4/Core One style printing.

It compares engraved and raised text using the label sizes that have come up during SaltScale validation:

- `5 mm` text height with `0.6 mm` depth/height.
- `7 mm` text height with `0.8 mm` depth/height.
- `8 mm` text height with `1.0 mm` depth/height.

Generated exports:

- `cad/exports/validation/stl/label_readability_coupon_v1.stl`
- `cad/exports/validation/step/label_readability_coupon_v1.step`

## Coupon Layout

The coupon is about `80 x 50 mm` and prints flat without supports.

Layout:

```text
left side:  engraved text
right side: raised text
center:     shallow divider line
```

Rows:

| Row | Engraved | Raised | Text height | Depth / raised height |
| --- | --- | --- | ---: | ---: |
| 1 | `IN` | `OUT` | 5 mm | 0.6 mm |
| 2 | `PAD` | `STOP` | 7 mm | 0.8 mm |
| 3 | `STOP` | `SENSOR` | 8 mm | 1.0 mm |

## Expected Result

Expected best overall setting:

```text
7 mm text height, 0.8 mm engraved depth
```

Reason:

- It should be much more readable than the earlier 3.6-4.5 mm labels.
- It is not as space-hungry as 8 mm text.
- A 0.8 mm engraved depth should survive PETG surface texture better than 0.6 mm.

Expected ranking:

- Best general engraved label: `7 mm / 0.8 mm`.
- Best large high-confidence engraved label: `8 mm / 1.0 mm`.
- Smallest likely acceptable label: `5 mm / 0.6 mm`, only for very short words like `IN` and `OUT`.
- Raised text may be more readable but is less suitable on functional contact surfaces because it protrudes.

## Print Guidance

Use normal prototype PETG settings:

- 0.4 mm nozzle.
- 0.2 mm layer height preferred for text evaluation.
- No supports.
- Flat on the build plate.
- Same filament and slicer settings as future validation coupons.

## What To Inspect

After printing, check:

- Whether `IN` and `OUT` are readable at 5 mm.
- Whether engraved `PAD` at 7 mm is clearly readable.
- Whether engraved `STOP` at 8 mm has clean internal corners.
- Whether raised `SENSOR` at 8 mm is clean or stringy.
- Whether engraved text fills in with PETG gloss/stringing.
- Whether raised text causes rough top surfaces or fragile edges.

## Pass Criteria

A setting passes if:

- It is readable at arm's length under normal room light.
- Letters remain distinct after light cleanup.
- Internal spaces do not fill in completely.
- The slicer reports no mesh repair problems.
- The text does not create fragile islands or lifted edges.

## Recommendation

Use `7 mm` text height and `0.8 mm` engraved depth as the default validation-coupon label setting if this coupon prints cleanly.

Use `8 mm / 1.0 mm` for critical orientation labels where space allows.

Avoid `5 mm / 0.6 mm` except for very short labels.
