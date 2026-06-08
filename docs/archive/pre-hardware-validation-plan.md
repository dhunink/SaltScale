# Pre-Hardware Validation Plan

Date: 2026-06-05

## Summary

No load sensors have been purchased yet. Before buying them, SaltScale can still reduce meaningful risk by validating geometry, printability, installation constraints, and service motions.

The highest-impact pre-hardware work is not electronics and not full-platform printing. It is:

1. Measure the real salt container and installation space.
2. Print non-sensor fit coupons for the critical clearances.
3. Validate seam hardware geometry with cheap generic M3 inserts/screws/dowels or printed stand-ins.
4. Validate upper support/grate contact with the real container.

Important boundary:

Pre-hardware validation cannot prove sensor accuracy, bridge wiring, calibration stability, or true load-cell contact behavior. It can prevent buying sensors for a geometry that is obviously wrong.

## Ranked uncertainties

## 1. Real salt container bottom and support pattern

Impact: Highest.

Why it matters:

`concept_v2` added a removable upper support grate because the container bottom is unknown. If the container bottom only contacts a narrow rim, the grate may be unnecessary. If the bottom is flexible or has molded ribs/feet, the grate may be essential or may need a different shape. This affects the whole upper carrier before sensor hardware matters.

How to test without buying sensors:

- Measure the actual container bottom diameter, foot/rib pattern, and flat contact areas.
- Place the empty container on a flat table with paper strips under likely contact zones.
- Add safe ballast if available, such as water jugs or bagged salt, and repeat the paper-strip/contact test.
- Print the support grate only, or make a cardboard/MDF/foam-board mockup of the grate footprint, and check whether it improves stability.

Required method:

- Measurement.
- Low-cost mockup.
- Optional print: support grate.

Cost and effort:

- Cost: USD 0-2 for paper/cardboard mockup; about USD 1-3 filament if printing the grate.
- Effort: 30-90 minutes for measurement and contact mapping; 2-4 hours print time if printing the grate.

What becomes validated:

- Whether the annular carrier alone is plausible.
- Whether the support grate is needed.
- Whether the support grate should be cross-shaped, disk-like, wider, narrower, or removable.
- Whether the 300 mm centering lip clearance is reasonable for the actual container.

Decision gate:

- If the container rocks or sags without center support, keep the grate or redesign it before buying sensors.
- If the container bottom does not contact the modeled grate, revise the upper support geometry before buying sensors.

## 2. Installation envelope and service access

Impact: Very high.

Why it matters:

The platform is meant for a utility closet or meter cupboard. If the 320 mm footprint, 39 mm height, container removal path, or sensor service direction does not fit the real installation, sensor selection is premature.

How to test without buying sensors:

- Cut a 320 mm diameter paper/cardboard footprint.
- Place it in the intended installation location.
- Add a 39 mm height spacer or stack of cardboard to represent platform height.
- Test whether the salt container can be lifted out safely.
- Check whether a user can access the outer sensor station side for service.

Required method:

- Measurement.
- Cardboard/foam-board mockup.

Cost and effort:

- Cost: USD 0-5.
- Effort: 30-60 minutes.

What becomes validated:

- Platform footprint.
- Platform height tolerance.
- Clearance around walls, pipes, and cabinet edges.
- Whether the container can be removed for service.
- Whether outward sensor cable/service access is realistic.

Decision gate:

- If the container cannot be removed, the current serviceability concept fails and must be redesigned before buying sensors.
- If the 320 mm ring does not fit, reduce envelope or change architecture before buying sensors.

## 3. Sensor-station placeholder fit and service motion

Impact: Very high.

Why it matters:

Even without a real sensor, the station can be checked with a 38 x 38 x 12 mm dummy block. This tests whether the CAD’s assumed envelope is printable, removable, and serviceable. It does not prove the real sensor will fit, but it proves the design can accept the current placeholder cleanly.

How to test without buying sensors:

- Print `concept_v2_sensor_station.stl`.
- Print or make a 38 x 38 x 12 mm dummy block from scrap plastic, wood, acrylic, or stacked cardboard.
- Print or make the upper and lower pad stand-ins.
- Insert and remove the dummy block through the open outer side.
- Check guide clearances using paper strips or feeler gauges.
- Check that the upper pad can be placed and removed without binding.

Required method:

- Print.
- Measurement.

Cost and effort:

- Cost: about USD 1-3 filament.
- Effort: 4-7 hours print time; 30-60 minutes inspection.

What becomes validated:

- The station prints without supports.
- Guide rails are printable and robust.
- The current 0.7 mm placeholder clearance is plausible.
- Sensor service motion is physically possible.
- The open outer side is usable.
- Pad handling is realistic.

Decision gate:

- If the dummy block binds, increase clearance or change guide geometry before buying sensors.
- If the block can fall out too easily, add a non-trapping retention feature before buying sensors.

## 4. Overload stop and pad-stack Z tolerance

Impact: High.

Why it matters:

The overload stop target is about 1 mm clearance. Real printed Z tolerance, pad thickness, and placeholder height can consume that margin. If the stops touch during normal unloaded assembly, the scale will bypass sensors.

How to test without buying sensors:

- Use the printed sensor station.
- Use a 12 mm dummy sensor block.
- Use pad stand-ins matching the modeled lower and upper pad thickness.
- Measure the gap from upper pad underside to overload stop tops.
- Repeat with intentionally varied dummy thicknesses, such as 11.5 mm, 12.0 mm, and 12.5 mm.

Required method:

- Print.
- Measurement.

Cost and effort:

- Cost: USD 0-3 after the sensor-station print.
- Effort: 30-60 minutes.

What becomes validated:

- Whether 1 mm stop clearance survives real print tolerances.
- Whether pad thickness needs adjustment.
- Whether overload stops need to be lower, adjustable, or separate.

Decision gate:

- If measured clearance is under about 0.5 mm with nominal dummy parts, revise before buying sensors.
- If clearance is over about 1.5-2.0 mm, sensor protection may be weak and should be reconsidered.

## 5. Seam hardware geometry

Impact: High.

Why it matters:

`concept_v2` relies on upper-only and lower-only seam bridge plates, M3 heat-set inserts, and 4 mm dowel sockets. If these are hard to install, split PETG, or misalign, the segmented architecture becomes unpleasant even if the sensor idea is good.

How to test without buying sensors:

- Print a small seam coupon or one lower segment corner region.
- If generic M3 inserts, M3 screws, and 4 mm dowels are already available, test them.
- If not, use printed or drill-bit stand-ins for dowel sizing and measure the pockets.
- Heat-set one insert and inspect for splitting, pullout, and tilt.
- Screw on a bridge plate and check whether it clamps without bending.

Required method:

- Print.
- Measurement.
- Optional cheap generic hardware, not sensor-specific hardware.

Cost and effort:

- Cost: USD 1-5 filament for a coupon; USD 5-15 if buying generic inserts/screws/dowels.
- Effort: 2-5 hours including print and installation checks.

What becomes validated:

- Insert pocket diameter/depth.
- Heat-set installation access.
- Dowel socket fit.
- Seam bridge plate screw access.
- Whether upper-only/lower-only joining is practical.

Decision gate:

- If inserts split bosses, enlarge bosses or change insert dimensions.
- If dowels are too tight after printing, increase socket diameter before buying sensors.

## 6. Upper carrier to lower base non-contact

Impact: High.

Why it matters:

The design depends on no upper-to-lower load bypass except overload stops. This can be checked with dummy blocks before sensors exist.

How to test without buying sensors:

- Print one lower segment and one upper segment, or use partial coupons if created.
- Use dummy blocks and pads to represent the sensor stack.
- Assemble the local stack.
- Use paper strips around guide rails, stops, and nearby base features to confirm no unintended contact.
- Add a small load and check whether contact occurs anywhere except the pad stack or intended overload stops.

Required method:

- Print.
- Measurement.
- Simple load test with household weights.

Cost and effort:

- Cost: about USD 4-8 filament for one quadrant-scale test if using full segment prints.
- Effort: 14-24 hours print time; 1-2 hours inspection.

What becomes validated:

- Local upper/lower spacing.
- Guide rail vertical clearance.
- Upper pad alignment.
- Whether the serviceable stack height is plausible.

Decision gate:

- If paper strips show normal contact outside the dummy sensor stack, revise geometry before buying sensors.

## 7. PETG warping and flatness of large segments

Impact: Medium-high.

Why it matters:

Sensor readings will be sensitive to uneven seating. Large flat PETG segments can warp, and a warped lower or upper ring can create preload differences.

How to test without buying sensors:

- Print one lower segment.
- Print one upper segment.
- Place each on a known flat surface.
- Check rocking, corner lift, and seam flatness.
- Measure flatness with feeler gauges or paper strips.

Required method:

- Print.
- Measurement.

Cost and effort:

- Cost: about USD 4-8 filament combined.
- Effort: 13-22 hours print time; 30-60 minutes inspection.

What becomes validated:

- PETG settings for large annular segments.
- Need for brim/enclosure.
- Whether segment thickness is adequate.
- Whether seam features distort during cooling.

Decision gate:

- If segments warp enough to rock, tune print settings or revise geometry before buying sensors.

## 8. Contact pad material and shape options, without sensors

Impact: Medium.

Why it matters:

The real sensor will need repeatable contact surfaces. Printed PETG pads may creep. Metal pads are preferred, but their size and handling can be evaluated before buying sensors.

How to test without buying sensors:

- Prepare candidate pad stand-ins: printed PETG, washers, small metal plates, acrylic squares.
- Place them in the printed station with dummy blocks.
- Check seating, rocking, handling, and removal.
- Leave a weighted dummy stack overnight and inspect visible denting in printed pads.

Required method:

- Print or simple fabrication.
- Measurement.

Cost and effort:

- Cost: USD 0-10 depending on scrap material.
- Effort: 1-2 hours plus optional overnight compression test.

What becomes validated:

- Pad size handling.
- Whether metal pads fit the station.
- Whether printed pads are obviously unsuitable.
- Whether pad retention is needed.

Decision gate:

- If pads slide or rotate easily, add a shallow non-trapping locator before buying sensors.

## 9. Salt/debris exposure paths

Impact: Medium.

Why it matters:

Salt dust and damp debris can fall into the sensor station, increase friction, corrode pads, or bridge guide clearances.

How to test without buying sensors:

- Inspect printed station and segment geometry.
- Sprinkle table salt or similar dry granules near the ring and observe where debris collects.
- Vacuum/brush the station and inspect whether debris is easy to remove.

Required method:

- Print.
- Observation.

Cost and effort:

- Cost: negligible after station print.
- Effort: 15-30 minutes.

What becomes validated:

- Whether pocket geometry traps debris.
- Whether cleaning access is adequate.
- Whether drain/relief gaps are needed before release.

Decision gate:

- If salt collects around guides or pad seats, add debris relief before buying sensors.

## 10. CAD/export and slicer workflow

Impact: Medium.

Why it matters:

Bad exports or awkward slicer orientation can waste time before hardware arrives.

How to test without buying sensors:

- Open/slice `concept_v2_sensor_station.stl`, `concept_v2_lower_segment_0.stl`, and `concept_v2_upper_segment_0.stl`.
- Check orientation, support requirements, estimated time, and wall behavior around pockets.
- Confirm units are correct.

Required method:

- Slicer review.
- Optional print preview screenshots or notes.

Cost and effort:

- Cost: USD 0.
- Effort: 30-60 minutes.

What becomes validated:

- Export sanity.
- Support-free assumptions.
- Actual slicer material estimates.
- Whether part naming and workflow are understandable.

Decision gate:

- If slicer requires supports inside functional pockets, revise geometry before buying sensors.

## What cannot be answered before buying sensors

These remain blocked until at least one real sensor is purchased:

- Actual sensor body fit.
- Actual cable exit location.
- Correct contact faces.
- Safe load region.
- Electrical wiring behavior.
- HX711 noise and stability.
- Calibration repeatability.
- Off-center measurement error.
- Long-term sensor drift.
- Sensor corrosion resistance.

## Recommended pre-hardware sequence

1. Measure installation space and salt container.
2. Map the salt container bottom contact pattern.
3. Slice the current v2 exports and check support/time assumptions.
4. Print `concept_v2_sensor_station.stl`.
5. Make a 38 x 38 x 12 mm dummy sensor block.
6. Test dummy insertion/removal, pad seating, and overload stop gap.
7. Test candidate pad materials with the dummy block.
8. Print or mock the support grate and test it against the real container bottom.
9. Print a small seam hardware coupon or one seam region if generic hardware is already available.
10. Only then purchase one sensor for real fit/load/electrical testing.

## Recommendation

Before buying any load sensors, the single highest-value validation is:

```text
Measure the real salt container bottom and installation envelope, then print the sensor station with a dummy 38 x 38 x 12 mm block.
```

If only one physical print is allowed before hardware purchase, print:

```text
concept_v2_sensor_station.stl
```

Do not buy all four sensors until one real sensor has later passed fit, service, load, and repeatability tests in the station.
