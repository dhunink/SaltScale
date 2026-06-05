# Prototype Strategy

Date: 2026-06-05

## Summary

Do not print the full `concept_v2` platform next.

The smallest physical prototype with the highest engineering value is:

```text
A) sensor station only
```

Recommended next print:

- `cad/exports/stl/concept_v2_sensor_station.stl`

This print attacks the most dangerous unknowns first: real sensor fit, replaceability, guide clearance, contact pad seating, and overload-stop clearance. If any of those fail, every larger print is premature.

## Estimate basis

Print time and material estimates are rough. They are based on current CAD solid volumes, then translated into practical PETG print ranges. A slicer estimate should be used before committing printer time.

Assumptions:

- PETG at roughly USD 20-30 per kg.
- 0.4 mm nozzle.
- 0.2-0.28 mm layers.
- 3-4 perimeters.
- 20-35% infill.
- Filament-only material cost, excluding sensors, pads, inserts, dowels, screws, electronics, and failed prints.

Current CAD solid-volume reference:

| Part | Solid mass equivalent |
| --- | ---: |
| Sensor station coupon | about 101 g |
| One lower segment | about 167 g |
| One upper segment | about 152 g |
| Support grate | about 39 g |
| One seam bridge | about 7 g |
| Full assembly, all modeled bodies | about 1524 g solid equivalent |

Actual sliced PETG use will usually be lower than solid equivalent, but the ranking is still useful.

## Option A: sensor station only

Print:

- `concept_v2_sensor_station.stl`

Estimated print time:

- About 4-7 hours.

Estimated material cost:

- About 45-80 g practical PETG.
- About USD 1-3 filament.

Engineering value:

- Very high for first validation.
- Directly tests the riskiest geometry in the design.
- Small enough to iterate quickly if sensor clearance is wrong.

Risk reduction:

- Highest risk reduction per gram of plastic.
- Validates the assumptions most likely to force CAD changes.

Assumptions validated:

- Real 50 kg sensor fits the station.
- Sensor can be inserted and removed without prying.
- Outer-side service access works.
- Guide rails do not pinch the sensor.
- Lower pad seats flat.
- Upper pad can sit on the sensor without binding.
- Overload stops have measurable clearance.
- Salt/debris traps around the station are visible.
- A single sensor can be loaded for rough repeatability tests.

Assumptions not validated:

- Upper segment seating.
- Lower/upper segment seam hardware.
- Annular carrier stiffness.
- Support grate usefulness.
- Four-sensor summed calibration.
- Full container stability.

Verdict:

- Best next print.

## Option B: one lower segment

Print:

- `concept_v2_lower_segment_0.stl`

Estimated print time:

- About 7-12 hours.

Estimated material cost:

- About 80-130 g practical PETG.
- About USD 2-4 filament.

Engineering value:

- Medium.
- Useful after the sensor station coupon proves the station geometry.
- Tests whether the full lower segment prints flat and whether seam features survive.

Risk reduction:

- Reduces lower-ring printability risk.
- Reduces heat-set insert and dowel socket risk.
- Confirms the sensor station still works inside the full segment footprint.

Assumptions validated:

- Lower segment fits the Prusa MK4.
- Lower segment warping is manageable.
- M3 insert pockets are printable.
- 4 mm dowel sockets are printable.
- Lower ring seam bosses are strong enough for handling.
- Sensor station features survive the larger print.

Assumptions not validated:

- Upper carrier contact.
- Upper seam bridge design.
- Full stack load path.
- Service procedure requiring upper segment removal.
- Support grate behavior.

Verdict:

- Good second print, not first.

## Option C: one upper segment

Print:

- `concept_v2_upper_segment_0.stl`

Estimated print time:

- About 6-10 hours.

Estimated material cost:

- About 75-120 g practical PETG.
- About USD 2-4 filament.

Engineering value:

- Medium-low as a first print.
- It validates a large printable upper part, but it does not test the sensor station.

Risk reduction:

- Reduces upper-carrier printability risk.
- Tests centering lip print quality.
- Tests underside insert pockets and upper-only seam hardware access.

Assumptions validated:

- Upper segment fits the Prusa MK4.
- Centering lip prints cleanly.
- Underside M3 insert pockets are accessible.
- Upper segment is stiff enough for handling.

Assumptions not validated:

- Real sensor fit.
- Sensor replacement.
- Pad seating.
- Overload stop clearance.
- Lower-to-upper load path.
- Whether the salt container bottom needs the support grate.

Verdict:

- Useful, but lower priority than A and B.

## Option D: one complete quadrant

Print:

- One lower segment.
- One upper segment.
- One sensor station stack with real sensor and contact pads.
- Optional local seam bridge samples.

Estimated print time:

- About 14-24 hours.

Estimated material cost:

- About 160-250 g practical PETG.
- About USD 4-8 filament.
- Plus one real sensor, pads, and representative hardware.

Engineering value:

- High.
- This is the first prototype that can test the actual local load stack with upper and lower parts together.

Risk reduction:

- High, but only after the sensor station geometry is known good.
- If printed before A, it risks wasting a large print on a small sensor clearance error.

Assumptions validated:

- Upper carrier contacts the upper pad as intended.
- Upper carrier does not contact guide rails or overload stops during normal unloaded setup.
- One-station service procedure is realistic.
- Upper segment can be removed and reinstalled without disturbing the lower base.
- Local load path can carry test weights.
- One sensor gives repeatable readings after remove/reinstall cycles.
- Local PETG deflection is acceptable over short tests.

Assumptions not validated:

- Full annular support.
- Full platform flatness.
- Four-sensor summed readings.
- Real container stability.
- Cross-platform off-center response.

Verdict:

- Best second-stage prototype after A passes.

## Option E: full platform

Print:

- Four lower segments.
- Four upper segments.
- Support grate.
- Seam bridge plates.
- Four complete sensor stations.
- All inserts, dowels, screws, pads, and sensors.

Estimated print time:

- About 45-80 hours total across multiple prints.

Estimated material cost:

- About 600-900 g practical PETG.
- About USD 15-30 filament.
- Plus four sensors, pads, inserts, dowels, screws, wiring, and electronics.

Engineering value:

- Highest final-system value, but poor first-prototype value.
- Too many variables change at once.

Risk reduction:

- Validates full assembly only if everything works.
- If it fails, diagnosis will be slower because sensor fit, seams, upper/lower contact, support grate, and four-sensor wiring are all entangled.

Assumptions validated:

- Full ring assembly.
- Full support grate behavior.
- Four-sensor summed calibration.
- Off-center load response.
- Real salt container fit.
- Segment joining under full geometry.
- Installation footprint.

Assumptions not validated efficiently:

- Which small feature caused a failure.
- Whether sensor station geometry alone was correct.
- Whether a smaller simpler change would solve the issue.

Verdict:

- Do not print next.

## Comparison table

| Option | Print time | Material cost | Engineering value | Risk reduction | First-print suitability |
| --- | ---: | ---: | --- | --- | --- |
| A) Sensor station only | 4-7 h | USD 1-3 | Very high for sensor fit/load path | Very high per gram | Best |
| B) One lower segment | 7-12 h | USD 2-4 | Medium | Medium | Good second print |
| C) One upper segment | 6-10 h | USD 2-4 | Medium-low first | Medium-low first | Later |
| D) One complete quadrant | 14-24 h | USD 4-8 | High | High after A passes | Second stage |
| E) Full platform | 45-80 h | USD 15-30 | Highest system value | Poor first-step efficiency | Not next |

## Recommended next print

Print `concept_v2_sensor_station.stl` first.

Use it with:

- One real 50 kg sensor.
- One lower contact pad.
- One upper contact pad.
- Temporary wiring or connector.
- Known test weights.

Test sequence:

1. Print the station in PETG.
2. Clean stringing and inspect guide rails.
3. Insert the real sensor by hand.
4. Confirm it can be removed without tools.
5. Add lower and upper contact pads.
6. Measure overload stop clearance.
7. Apply 5 kg, 10 kg, and 20 kg loads.
8. Remove and reinstall the sensor three times.
9. Repeat the same loads.
10. Record whether readings shift after reinstalling.

Go to a one-complete-quadrant print only after this passes.

## Why this is the best next print

The sensor station is where the project can fail fastest:

- Wrong sensor dimensions.
- Bad contact pad geometry.
- Binding guide rails.
- Overload stops touching too early.
- Sensor impossible to remove.
- Side loading from the pocket.

Those failures would invalidate the lower segment, upper segment, complete quadrant, and full platform. A small station coupon finds them with the least plastic and time.

## Do not print yet

- Do not print the full platform.
- Do not print all four lower segments.
- Do not print all four upper segments.
- Do not commit to final seam hardware.
- Do not design electronics packaging around unvalidated mechanical geometry.
