# Concept v2 Quadrant Walkthrough

Date: 2026-06-06

## Purpose

This walkthrough shows one complete `concept_v2` quadrant as a human builder should think about it.

One quadrant contains:

- One lower base segment.
- One floating upper carrier segment.
- One sensor station.
- One lower pad.
- One 50 kg load sensor.
- One upper pad.
- The local portion of the removable upper support grate.
- Same-layer seam hardware at the two radial edges.

The important rule: the upper carrier and lower base are never bolted together. Seam hardware joins lower-to-lower or upper-to-upper only.

## Orientation

The full SaltScale has four quadrants. Each quadrant covers about 90 degrees of the annular platform. The sensor station sits near the middle of the quadrant, roughly halfway between the two radial seams.

```text
Top view, one quadrant, not to scale

                         OUTSIDE
                 outer diameter about 320 mm

          left seam edge             right seam edge
              |                            |
              v                            v
        +----------------------------------------+
        |  lower/upper annular quadrant sector   |
        |                                        |
        |          [ sensor station ]            |
        |                at mid-angle            |
        |                                        |
        |     support grate arm passes above     |
        +-------------------    -----------------+
                            inner opening

                          INSIDE
```

The lower base rests on the floor. The upper carrier floats above it and is supported only through the sensor stack during normal weighing.

## Exploded Quadrant View

This is the vertical assembly order. It is shown exploded so each part is visible.

```text
Exploded vertical view, not to scale

        salt container
             ||
             vv
   +---------------------+
   | upper support grate |     removable, upper-only
   +---------------------+
             ||
             vv
   +---------------------+
   | upper carrier seg.  |     floating upper quadrant
   +---------------------+
             ||
             vv
   +---------------------+
   | upper contact pad   |     loose/replaceable
   +---------------------+
             ||
             vv
   +---------------------+
   | 50 kg load sensor   |     cable exits outward
   +---------------------+
             ||
             vv
   +---------------------+
   | lower contact pad   |     loose/replaceable
   +---------------------+
             ||
             vv
   +---------------------+
   | lower base segment  |     floor-supported quadrant
   +---------------------+
             ||
             vv
            floor
```

Normal load path:

```text
container
-> support grate and/or upper carrier
-> upper pad
-> sensor
-> lower pad
-> lower base
-> floor
```

Nothing in the seam hardware is part of the weighing stack.

## Sensor Station Section View

This section cuts through the sensor station from outside to inside.

```text
Section through sensor station, not to scale

OUTSIDE / cable exit                                      INSIDE

      floating upper system
   +-------------------------+      upper carrier segment
   |                         |
   +-----------+-------------+
               |
          +----v----+
          | upper   |              upper pad, replaceable
          | pad     |
          +----+----+
               |
          +----v----+
          | sensor  |              50 kg Kiwi/SparkFun-style sensor
          +----+----+
               |
          +----v----+
          | lower   |              lower pad, replaceable
          | pad     |
          +----+----+
               |
   +-----------v-------------+
   | lower base segment      |
   +-------------------------+

   local overload stops sit nearby with clearance;
   they must not touch during normal unloaded assembly.
```

The sensor is vertically compressed by the upper pad and lower pad. It is not glued, screwed, or trapped.

## Sensor Service View

The sensor is meant to come out from the outer side after the upper segment is removed.

```text
Top view of local station, not to scale

                       INSIDE
                         ^
                         |
              inner locator / stop
                         |
        +--------------------------------+
        |                                |
        |       lower pad pocket         |
        |       sensor sits here         |
        |                                |
        +--------------------------------+
          side locator        side locator

                         |
                         v
                OUTSIDE / cable exit
             sensor slides/lifts out here
```

The upper pad is removed first, then the sensor can be lifted or slid out toward the outside. The lower base ring does not need to be disassembled for one-sensor service.

## Seam Hardware Top View

Each quadrant has two radial seam edges. Each seam is shared with the neighboring quadrant. The current default active direction is M3 bolts, captured standard M3 nuts, and printed bridge plates.

```text
Top view of one seam, not to scale

lower segment A       seam       lower segment B
+--------------+      ||      +--------------+
|              |      ||      |              |
|   M3   M3    |======||======|   M3   M3    |  printed lower bridge plate
|              |      ||      |              |
+--------------+      ||      +--------------+

upper segment A       seam       upper segment B
+--------------+      ||      +--------------+
|              |      ||      |              |
|   M3   M3    |======||======|   M3   M3    |  printed upper bridge plate
|              |      ||      |              |
+--------------+      ||      +--------------+
```

The lower bridge plate touches only lower parts. The upper bridge plate touches only upper parts.

## Seam Section View

This section shows why upper and lower seam hardware must stay separate.

```text
Section through a radial seam, not to scale

        upper-to-upper bridge only
        +---------------------+
        | M3 bolt + bridge    |
   +----+---------------------+----+
   | upper segment A   upper segment B |
   +-----------------------------------+

             air gap / no fastener
             no bridge, screw, dowel,
             spacer, wall, or clip here

   +-----------------------------------+
   | lower segment A   lower segment B |
   +----+---------------------+----+
        | M3 bolt + bridge    |
        +---------------------+
        lower-to-lower bridge only
```

If a screw, dowel, or bridge connects upper to lower, load can bypass the sensors and the scale reading becomes unreliable.

## Support Grate Relationship

The support grate belongs to the floating upper system.

```text
Top view, simplified

       upper annular quadrant
   +-----------------------------+
   |                             |
   |       grate arm/tab         |  removable support grate
   |            ====             |
   |                             |
   +-----------------------------+

The grate may touch the upper carrier.
The grate must not touch the lower base.
```

The support grate helps uncertain salt-container bottoms. It should be installed only into the upper carrier or placed on upper-only supports. It must not create a lower-base contact point.

## Assembly Sequence For One Quadrant

1. Place the lower segment on the bench with the sensor station facing up.
2. If testing seam hardware, join this lower segment to neighboring lower segments using lower-only bridge plates.
3. Press standard M3 nuts into the captured nut pockets. Lower nuts press in from the underside; upper nuts press in from the top side.
4. Install lower bridge plates on top of the lower seams and tighten the M3 bolts lightly and evenly.
5. Place the lower contact pad in the sensor station.
6. Place the sensor on the lower pad with its cable exiting outward.
7. Place the upper contact pad on the sensor.
8. Assemble the upper segment to neighboring upper segments using underside upper-only bridge plates and M3 bolts from below.
9. Place or attach the local support grate portion to the upper carrier.
10. Lower the upper carrier segment onto the upper pad.
11. Confirm the upper carrier contacts the upper pad, not the locator walls or overload stops.
12. Confirm there is visible clearance between upper and lower structures everywhere except the sensor stack.
13. Add the salt container only after all four quadrants pass the same checks.

## What To Inspect Before Loading

Check these items before putting weight on the scale:

- Lower pad sits flat.
- Sensor sits flat and is not pinched by locator geometry.
- Upper pad sits centered on the sensor.
- Sensor cable exits outward without being crushed.
- Upper carrier is floating and not touching lower base features.
- Overload stops have clearance.
- Lower seam bridge touches only lower parts.
- Upper seam bridge touches only upper parts.
- Support grate touches only the upper carrier.
- No bolt, nut, dowel, bridge, clip, or printed wall crosses from upper to lower.

## One-Sensor Replacement Sequence

1. Remove the salt container.
2. Remove or lift the support grate if it blocks the target upper segment.
3. Lift the upper carrier assembly off the sensor stack, then access the underside upper-only seam hardware around the target quadrant.
4. Lift off the local upper segment.
5. Remove the upper pad.
6. Disconnect the sensor wiring.
7. Lift or slide the sensor out toward the outside.
8. Inspect and clean the lower pad and station.
9. Install the replacement sensor with the cable exiting outward.
10. Reinstall the upper pad, upper segment, support grate, and upper seam hardware.
11. Tare and recalibrate.

The lower ring can remain assembled throughout this procedure.

## Builder Mental Model

Think of the quadrant as two separate machines stacked together:

```text
upper machine:
support grate + upper carrier + upper bridge plates

measurement stack:
upper pad + sensor + lower pad

lower machine:
lower base + lower bridge plates
```

The measurement stack is the only normal connection between the upper machine and lower machine.



## Active Printable Files

The current active printable files are:

- `cad/exports/active/stl/concept_v2_lower_segment_0.stl`
- `cad/exports/active/stl/concept_v2_upper_segment_0.stl`
- `cad/exports/active/stl/concept_v2_support_grate.stl`
- `cad/exports/active/stl/concept_v2_lower_bridge_plate.stl`
- `cad/exports/active/stl/concept_v2_upper_bridge_plate.stl`
- `cad/exports/active/stl/concept_v2_lower_pad.stl`
- `cad/exports/active/stl/concept_v2_upper_pad.stl`
- `cad/exports/active/stl/concept_v2_sensor_placeholder.stl`

Assembly STEP files are visual references, not print plates:

- `cad/exports/active/step/concept_v2_assembly.step`
- `cad/exports/active/step/concept_v2_exploded_assembly.step`
- `cad/exports/active/step/concept_v2_one_quadrant_assembly.step`

Support-grate clearance is now set to `0.4 mm per side` as the current default; verify it again in the full upper carrier.

## Support-Grate Fit Status

The current default support-grate clearance is `0.4 mm per side`. It was the least-loose tested removable option. Because even 0.4 mm had perceptible movement, future work may explore self-centering or tapered upper-only locator geometry. Do not loosen the default unless a later physical test proves it is necessary.


## Upper Seam Service Note

The active design keeps underside upper bridge plates. This is the mechanically safer/simple choice for now because it keeps upper seam hardware upper-only and leaves the top surface available for the support grate and salt container.

A single upper segment is not meant to be loosened while the upper carrier is sitting on the sensor stack. For upper-segment service, remove the container and support grate, lift the upper carrier assembly, then access the underside bridge bolts on the bench.
