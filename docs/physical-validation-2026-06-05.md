# Physical Validation 2026-06-05

## Summary

First physical validation prints for the `concept_v2` coupon set were successful enough to prove the basic coupon workflow, but they exposed several usability and design-direction issues.

Most important outcome:

- The printed sensor-station coupon validates that the earlier unsupported-wall issue is fixed.
- The large rectangular guide-wall station is printable, but it now looks mechanically oversized.
- The newer `sensor_station_locator_v3` direction is a better next locator test.
- The support-grate fit coupon is too loose.
- The seam/dowel coupons are no longer aligned with the preferred low-hardware open-source assembly direction.

No CAD changes are made by this note.

## What Printed Well

### Sensor station coupon

`sensor_station_coupon_v2` printed successfully after the earlier unsupported-wall issue was fixed.

Observed positives:

- Guide walls start on supported base geometry.
- No obvious bottom-wall bridging issue remains.
- The station base, stops, and dummy parts are physically printable in PETG.
- The coupon format is useful for handling and visual inspection.
- The separate dummy sensor and pad pieces are helpful for assembly thinking.

### General coupon workflow

The multi-body validation-coupon approach is useful.

It allows quick checking of:

- Sensor station printability.
- Dummy stack handling.
- Support-grate fit.
- Seam hardware concepts.
- Label readability.

This is better than jumping directly to full ring segments.

### Labels

The labels are useful.

They make it easier to identify:

- Upper vs lower pads.
- Sensor dummy.
- Outside direction.
- Stops and locator areas.
- Seam coupon test features.

The idea is good; the current execution needs improvement.

## What Failed Or Felt Wrong

### Labels are too small or too shallow

Some engraved/negative text is hard to read after PETG printing.

Observed issue:

- Small engraved labels lose detail.
- Some text becomes fuzzy or partially filled.
- The labels are useful but not robust enough for repeated open-source printing.

Recommended future label style:

- Text height: `6-8 mm` where part area allows.
- Engraving depth: about `0.8 mm` where geometry thickness allows.
- Use shorter labels where possible.
- Avoid long text on small/thin parts.

Current labels around `3.6-4.5 mm` high and `0.5-0.6 mm` deep are marginal.

### Support grate fit is too loose

`support_grate_fit_coupon_v1` printed and the tab slides very freely in the upper-carrier slot.

Estimated clearance:

```text
about 1.0-1.5 mm per side
```

This is too loose for the normal removable support-grate interface.

Target fit:

```text
normal removable PETG fit: about 0.4-0.6 mm per side
salt/dust-tolerant variant: about 0.8 mm per side
```

The current support-grate interface is better as a proof of removability than as a final fit target.

### Current guide-wall sensor station is oversized

The printed `sensor_station_coupon_v2` confirms that the current long rectangular rails are printable, but they look too large for their purpose.

Issues:

- The rails are visually dominant.
- The station feels more like a large guide pocket than a precise sensor locator.
- Clearance is more generous than needed for the assumed 38 x 38 mm sensor placeholder.
- The geometry may create more salt/debris collection area than necessary.

Design direction:

- Prefer the newer `sensor_station_locator_v3` concept for the next print.
- Use lower-profile, broken locator features.
- Keep overload stops visually and mechanically distinct.

### Dowel-test coupons no longer match preferred assembly strategy

The lower and upper seam coupons include 4 mm dowel sockets and M3 heat-set insert tests.

The current project direction is shifting away from metal connector dependency as the default open-source assembly method.

Implication:

- Dowel-test coupons are now partly obsolete.
- They are still useful as historical fit checks if metal alignment is reconsidered.
- They should not drive the next assembly design by default.

### M3 heat-set inserts should be optional, not default

M3 heat-set inserts remain useful for durable service prototypes, but they increase required tooling and hardware assumptions.

Open-source default should prefer:

- Printable alignment features.
- Printed keys/tabs/bridges where practical.
- Simple screws only if needed.
- Metal inserts as an optional upgrade path.

## Design Implications

### Sensor station

The current v2 station is printable but should not be treated as final.

Implications:

- Replace long rails with lower locator tabs in the next design pass.
- Use `sensor_station_locator_v3` as the next physical test direction.
- Keep the outer side open for sensor removal.
- Keep locator height low enough that it cannot touch the upper pad or carrier.
- Preserve solid lower-pad support.

### Labels

Labels should remain in validation coupons, but the label parameters need to change.

Implications:

- Increase label size on future coupons.
- Use fewer, shorter labels.
- Avoid detailed labels on thin or tiny parts.
- Keep text out of load/contact surfaces.
- Re-check STL watertightness after text changes, because text booleans have already caused mesh issues once.

### Support grate

The support-grate interface needs a tighter fit coupon before integration.

Implications:

- Current support-grate slot clearance is too loose.
- A second grate-fit coupon should test at least two clearances.
- Consider a normal-fit version and a salt/dust-tolerant version.
- Do not finalize the grate locator until the real container bottom is checked.

### Seam strategy

The seam strategy should be reconsidered before more seam coupons are printed.

Implications:

- Do not continue optimizing 4 mm metal dowel coupons as the default path.
- Keep M3 inserts optional.
- Create a low-hardware seam concept before printing more seam validation parts.

## Recommended CAD Parameter Changes

Do not apply these yet; use them as the next CAD-change list.

### Label parameters

Recommended:

```text
label_text_height_mm: 6.0-8.0
label_engrave_depth_mm: 0.8 where wall/part thickness allows
minimum practical label depth on thin parts: 0.5-0.6
```

Also recommended:

- Use short labels like `PAD`, `SENSOR`, `STOP`, `OUTSIDE`, `SLOT`, `TAB`.
- Avoid long text like `SENSOR DUMMY` on small pieces unless the piece has enough area.

### Support grate fit

Current coupon logic uses a loose channel around the grate tab.

Recommended target clearances:

```text
standard removable fit: 0.4-0.6 mm per side
salt/dust tolerant fit: about 0.8 mm per side
current observed fit: about 1.0-1.5 mm per side, too loose
```

Create a new support-grate clearance coupon with multiple slots if possible.

### Sensor station locator

For the next sensor-station validation:

```text
sensor placeholder: 38 x 38 x 12 mm
locator target clearance: about 0.8-1.2 mm total
locator height: about half current wall height or less
outer side: open/removable
```

Use `sensor_station_locator_v3` as the next test coupon rather than continuing the long-rail station.

### Seam and connector strategy

Recommended next parameter direction:

- De-emphasize 4 mm dowels as default.
- Treat heat-set inserts as optional.
- Explore printed alignment keys or screw-light joining before committing to metal hardware.

## Old Coupons Now Obsolete Or Lower Priority

### Obsolete as default next prints

`lower_seam_coupon_v1`

Reason:

- It validates metal dowels and M3 inserts, but that is no longer the preferred default assembly strategy.

`upper_seam_coupon_v1`

Reason:

- Same as lower seam coupon; useful historically but no longer the first-choice direction.

### Superseded for sensor-station development

`sensor_station_coupon_v2`

Reason:

- Printed successfully and proved the station is printable.
- Long rectangular rails are now judged oversized.
- Future testing should move to `sensor_station_locator_v3`.

`concept_v2_sensor_station`

Reason:

- Useful as the unlabeled station-only reference.
- Less useful than the labeled v2 coupon and the newer v3 locator coupon.

### Still useful but needs revision

`support_grate_fit_coupon_v1`

Reason:

- It proved the removable concept.
- Fit is too loose.
- Needs a new tighter-clearance coupon.

### Still useful

`centering_lip_coupon_v1`

Reason:

- Still relevant to real salt-container fit.
- Should be tested against the actual container.

`upper_lower_stack_coupon_v1`

Reason:

- Still useful for checking upper/lower non-contact, but should eventually be updated with the refined sensor locator and larger labels.

## What Should Be Tested Next

Recommended next physical tests:

1. Print `sensor_station_locator_v3.stl`.
2. Test dummy sensor insertion/removal in the lower-profile locator.
3. Check whether the tighter locator feels too tight, too loose, or debris-prone.
4. Create and print a revised support-grate fit coupon with tighter clearances.
5. Test the centering lip against the real salt container.
6. Measure the real salt container bottom contact pattern.
7. Decide on the no-metal/default seam strategy before printing more seam coupons.

Do not print full ring segments yet.

Do not buy all four sensors yet.

One real sensor may be purchased after the v3 locator and revised grate fit pass basic print/fit checks.
