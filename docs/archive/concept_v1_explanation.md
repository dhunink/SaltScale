# Concept v1 Explanation

Date: 2026-06-04

## Purpose

`concept_v1` is a clean-sheet mechanical demonstrator for SaltScale. It does not continue from `platform_v6` and does not reuse previous CAD geometry.

The model demonstrates a four-sensor floating annular scale:

- Lower annular base segments sit on the floor.
- Upper annular carrier segments float above the lower base.
- Four load sensors sit between the two structures.
- Local guide rails constrain lateral movement without carrying vertical load.
- Overload stops protect sensors after about 1 mm of travel.
- A segmented centering lip helps place a 290 mm salt container but is part of the floating upper carrier only.

Generated source:

- `cad/src/concept_v1.py`

Generated exports:

- `cad/exports/step/concept_v1.step`
- `cad/exports/stl/concept_v1.stl`

## Load path

Normal load path:

```text
salt container
-> floating upper annular carrier
-> upper contact pad
-> load sensor
-> lower contact pad
-> lower annular base
-> floor
```

The lower base and upper carrier are separate structures. During normal operation, the only intended vertical load transfer between them is through the four sensor stacks.

The local guide rails are lower-base features. They sit beside each sensor station and are open on the outer radial side for service. They should prevent sensor shear and gross lateral motion, but their tops remain below the upper carrier/contact pad path so they are not normal-load supports.

The overload stops are intentional bypasses. They rise from the lower base and stop about 1 mm below the upper contact pad. If the upper carrier deflects too far, the upper pad contacts the stops and protects the sensor. Readings during stop contact should be considered invalid.

## Assembly sequence

Recommended prototype assembly sequence:

1. Print four lower base segments and four upper carrier segments.
2. Join the lower segments into a lower annular base.
3. Place lower contact pads into the four sensor stations.
4. Place one load sensor on each lower contact pad.
5. Place upper contact pads on the sensors.
6. Join the upper carrier segments separately.
7. Lower the upper carrier onto the four upper contact pads.
8. Confirm that guide rails do not touch the upper carrier or upper pads in the unloaded state.
9. Confirm about 1 mm overload-stop clearance.
10. Place the empty salt container, tare, then calibrate with a known mass.

The exported `concept_v1.stl` is a combined assembly visualization, not a final print plate. Production exports should later split fixed base parts, floating top parts, pads, and sensor placeholders into separate STL files.

## Sensor strategy

The recommended sensor strategy is four low-cost bathroom-scale style 50 kg sensors wired as a combined bridge into one HX711.

Why four sensors:

- Four support points give stable support to a round salt container.
- The summed reading is less sensitive to off-center salt distribution than a central PETG transfer structure.
- Commodity sensors are cheap and easy to replace.
- One HX711 can read the combined bridge, keeping electronics and firmware simple.
- Calibration can start with tare plus one known weight.

Why not one central loadcell:

- A good central single-point loadcell costs more.
- It requires exact vendor-specific mounting geometry.
- It asks the printed PETG structure to move all off-center load into one central sensor.
- It makes the first mechanical validation more expensive and less hobby-friendly.

Why not two or three sensors:

- Two sensors need a third support or hinge that risks bypassing the sensors.
- Three sensors are mechanically stable, but common low-cost bathroom-scale bridge wiring is naturally four-sensor.

## Why this concept is better than platform_v6

`platform_v6` should not be used as the basis for future CAD. It mixed useful four-sensor intent with unclear printable/serviceable geometry.

`concept_v1` improves on it in the following ways:

- It starts from a clean upper/lower separation.
- It makes the floating upper carrier explicit.
- It makes the lower floor reference explicit.
- It avoids a fused sensor-module assembly as the core model.
- It removes central-loadcell parameter inheritance.
- It uses an annular carrier instead of a heavy full disk.
- It keeps sensors near the container perimeter where they are mechanically useful.
- It leaves the center open for lower material use, inspection, and later wiring.
- It makes guide features lateral-only in intent.
- It treats overload stops as intentional, measurable bypasses.

The concept is also more honest: it does not pretend to be final. It is a mechanical architecture demonstrator that should be validated by printing one sensor station or one quarter stack before full-platform work.

## CAD dimensions

Assembled model envelope:

- 320.0 x 320.0 x 34.0 mm

Main printable segment envelopes from the current parametric model:

- Lower base segment: about 159.2 x 159.2 x 6.0 mm
- Upper carrier segment: about 153.0 x 153.0 x 12.0 mm

These fit within the Prusa MK4 200 x 200 x 200 mm constraint.

## Critical limitations

- The sensor placeholder is still generic: 38 x 38 x 12 mm.
- The contact pads are represented as simple rectangular pads; real metal pad geometry should be validated.
- No segment seam hardware is finalized.
- No electronics bay is included.
- No cable routing is included.
- No water/salt corrosion protection is included yet.
- The annular top support must be checked against the actual salt container bottom. If the container bottom is too flexible, add removable cross-spokes or a thin support disk only after testing.

## Recommended next validation

Print one lower sensor-station quadrant and one matching upper carrier quadrant. Install one real sensor and pads. Test:

- Sensor insertion/removal.
- Upper carrier seating.
- Guide clearance.
- Overload-stop gap.
- Repeatability under 5 kg, 10 kg, and 20 kg test loads.
- Off-center load response within that quadrant.

Only after that should the design move toward complete segmented exports or electronics packaging.
