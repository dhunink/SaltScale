# Concept v2 Sensor Station Printability Review

Date: 2026-06-05

## Summary

PrusaSlicer reported unsupported bridge lines at the bottom of the `concept_v2_sensor_station` guide walls.

The guide walls were not fully floating bodies, but the model did create small unsupported wall-bottom spans. The cause was a shallow lower-pad locator cut applied after the guide walls were unioned into the base. That cut removed the top 1 mm of base material under parts of the guide-wall footprints.

Fix applied:

- Moved guide rails and the inner stop outward so they sit outside the lower-pad footprint.
- Removed the lower-pad locator cut from both `sensor_station_coupon()` and `lower_segment()`.
- Kept the lower contact pad on solid base material.
- Re-exported `cad/exports/stl/concept_v2_sensor_station.stl`.

## Investigation

Relevant CAD source:

- `cad/src/concept_v2.py`
- `_sensor_station_lower_features()`
- `lower_segment()`
- `sensor_station_coupon()`

Original geometry sequence:

1. Create base plate.
2. Union guide rails, inner stop, and overload stops at `z = lower_thickness_mm`.
3. Cut a shallow lower-pad locator pocket from `z = 7..8 mm`.

The guide walls also began at `z = 8 mm`, exactly at the top of the base plate. That is correct only if the base is still solid underneath the wall footprint.

## What created the unsupported spans

The shallow locator cut was larger than the clear area inside the guide walls.

Before the fix:

- Lower-pad locator cut size: `45.2 x 45.2 x 1.0 mm`.
- Locator half-width: `22.6 mm`.
- Guide rail inner faces were inside that envelope.
- The cut was applied after guide-wall union.

Result:

- The guide walls still started at `z = 8 mm`.
- But part of the base directly under the first guide-wall layer had been cut down to `z = 7 mm`.
- PrusaSlicer saw the first wall layer crossing over a shallow void and marked bridge lines.

This was a slicer artifact caused by real CAD geometry, not a PrusaSlicer false positive.

## Were guide walls floating?

Not as whole bodies.

The walls were unioned into the station body and nominally started at the base top. However, because the later pocket cut removed support below part of the footprint, some bottom wall lines became locally unsupported.

After the fix:

- Guide walls still start at the top of the base plate.
- No locator cut removes material under them.
- They sit on continuous solid printed geometry.

## Did a pocket cut remove support below the walls?

Yes.

The lower-pad locator pocket cut was the direct cause. It overlapped the wall footprints because it was sized around the larger lower contact pad, while the guide-wall spacing had originally been based on the smaller sensor placeholder.

A second issue came from the same cut: the lower contact pad was modeled at the top of the base while the locator pocket removed material below it. That meant the pad was not clearly supported by solid base material in the assembly model.

After the fix:

- The locator cut is no longer applied.
- The lower contact pad rests on solid base material.
- Guide walls provide lateral location without cutting a recess below the pad.

## Were bodies not fully unioned?

No.

The guide walls were unioned into the station body. The issue was not missing boolean union. The issue was boolean order and footprint overlap:

```text
base + guide walls -> cut locator pocket
```

The cut happened after the walls existed, so it could remove material under the wall bottoms.

## CAD fix

Changes in `cad/src/concept_v2.py`:

- Replaced the old guide-wall spacing based on sensor span with spacing based on the lower-pad locator envelope.
- Added an explicit `0.8 mm` clearance beyond the former locator footprint.
- Moved the inner radial stop outward by the same rule.
- Moved overload stops outward so they remain distinct and do not merge into the guide rails.
- Removed the lower-pad locator cut in `lower_segment()`.
- Removed the lower-pad locator cut in `sensor_station_coupon()`.

Current geometry check:

- Former locator half-width: `22.6 mm`.
- Guide rail inner face: `23.4 mm` from station center.
- Inner stop outer face: `23.4 mm` from station center on the inward side.
- Clearance beyond former pocket footprint: `0.8 mm`.

Because the locator cut is no longer applied, this clearance is conservative rather than merely exact.

## Serviceability impact

Serviceability is preserved.

The sensor station remains:

- Open on the outer side.
- Accessible after removing the upper carrier.
- Free of upper-to-lower fasteners.
- Free of a printed sensor cap.

The lower contact pad is no longer recessed, but it remains removable. Lateral location is provided by the surrounding guide geometry instead of a shallow pocket.

## Force path impact

The force path is improved.

Before:

```text
lower contact pad -> partly over shallow locator recess -> base
```

After:

```text
lower contact pad -> solid base top -> lower base
```

The normal load path remains:

```text
upper carrier -> upper pad -> sensor -> lower pad -> lower base
```

No upper-to-lower bypass was introduced.

## Export and build status

Updated export:

- `cad/exports/stl/concept_v2_sensor_station.stl`

Build/checks run:

- `python -m py_compile cad/src/concept_v2.py`
- Targeted CadQuery export for `concept_v2_sensor_station.stl`
- `python cad/build.py`

The existing `cad/build.py` completed successfully. It does not currently export `concept_v2`; the updated v2 sensor station STL was exported separately from `concept_v2.py`.

## Recommendation

Re-slice the updated `concept_v2_sensor_station.stl` in PrusaSlicer.

Expected result:

- No unsupported bridge lines at the bottom of the guide walls.
- Guide walls should start on solid base geometry.
- Lower contact pad should be treated as sitting on solid support in the physical prototype.

If PrusaSlicer still reports bridging, inspect for slicer settings around thin walls/perimeters rather than the old locator-pocket issue.
