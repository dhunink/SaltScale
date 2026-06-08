# Support Grate Fit Variant Plan

Date: 2026-06-06

## Summary

The first printed `support_grate_fit_coupon_v1` was too loose. The grate tab moved freely with roughly `1.0-1.5 mm` clearance per side.

These variants test tighter clearances for the upper-only support-grate interface. They do not modify the full `concept_v2` platform and do not include lower-base geometry.

Generated coupon targets:

- `support_grate_fit_0p4mm_per_side`
- `support_grate_fit_0p6mm_per_side`
- `support_grate_fit_0p8mm_per_side`

Each coupon is a small print-flat kit with two separate printable bodies:

- A labeled upper slot block.
- A labeled support-grate tab.

## Geometry

The tab uses the current `concept_v2` support-grate arm dimensions:

- Tab width: `22.0 mm`.
- Tab thickness: `4.0 mm`.

Slot width is calculated as:

```text
slot width = tab width + 2 * clearance_per_side
```

| Coupon | Clearance per side | Slot width |
| --- | ---: | ---: |
| `0p4` | 0.4 mm | 22.8 mm |
| `0p6` | 0.6 mm | 23.2 mm |
| `0p8` | 0.8 mm | 23.6 mm |

The slot is a top-open upper-carrier-style channel, so it should print flat without supports.

## Expected Fit

### 0.4 mm per side

Expected feel:

- Snug PETG fit.
- Likely best if the printer is well tuned.
- May need light cleanup if there is elephant foot, stringing, or over-extrusion.

Risk:

- Could bind with rough PETG or salt dust.

### 0.6 mm per side

Expected feel:

- Preferred starting point.
- Removable by hand.
- Should reduce visible side-to-side rattle compared with the original coupon.
- More tolerant than 0.4 mm while still feeling controlled.

Risk:

- Could still feel slightly loose on a very accurate print.

### 0.8 mm per side

Expected feel:

- Dust-tolerant removable fit.
- Should slide easily.
- May be acceptable if salt dust or moisture makes the tighter versions bind.

Risk:

- May still feel too loose for the default clean-interface design.

## Which To Print First

The clearance test has completed. For reprints or confirmation, print the current default:

```text
cad/exports/validation/stl/support_grate_fit_0p4mm_per_side.stl
```

Reason:

- It had the least play among the tested removable variants.
- `0.6` and `0.8 mm` remained removable but felt looser than desired.

## Pass Criteria

A variant passes if:

- The tab and slot print as separate bodies.
- Both bodies print flat without supports.
- Labels remain readable.
- The tab inserts and removes by hand.
- The tab does not visibly rock in all directions.
- The tab does not jam after light PETG cleanup.
- The slot walls do not crack or curl.

## Fail Criteria

A variant fails if:

- The tab cannot be inserted by hand after normal cleanup.
- The tab rattles almost as freely as the old coupon.
- The tab rocks enough to make the support grate feel uncontrolled.
- The slot wall deforms, cracks, or delaminates.
- The labels or text booleans create slicer mesh errors.

## What To Measure

After printing, record:

- Actual tab width.
- Actual slot width.
- Side-to-side play by feel or caliper.
- Whether insertion is smooth.
- Whether removal is possible without tools.
- Whether PETG stringing or elephant foot affects fit.
- Which clearance feels best for clean conditions.
- Which clearance seems best for salt/dust tolerance.

## Physical Test Result

All three variants, `0.4`, `0.6`, and `0.8 mm` per side, remained removable and none fell out. All still allowed visible/playable movement.

`0.4 mm per side` had the least play and is the best tested option.

## Recommendation After Testing

Use `0.4 mm per side` as the current default support-grate tab/slot clearance. Do not make the default looser.

If a future full upper-carrier test still feels too loose, create and test a `0.2 mm per side` variant before changing the active design. Future work may also explore self-centering or tapered locator geometry, but the current default should not be loosened.
