# Concept v2 Serviceability

Date: 2026-06-04

## Serviceability goal

A single failed sensor must be replaceable without reprinting the platform and without disassembling the lower base.

`concept_v2` supports that goal by keeping sensors accessible from above after removing the local floating upper carrier segment. The sensor is guided, not trapped.

## Replaceable parts

Per sensor station:

- 50 kg load sensor.
- Lower contact pad.
- Upper contact pad.
- Sensor wiring/connector, if used.

Shared parts:

- Upper carrier segment.
- Lower base segment.
- Upper seam bridge plates.
- Lower seam bridge plates.
- Removable support grate.

## Normal assembly sequence

1. Print and clean all lower base segments.
2. Install M3 heat-set inserts into the lower segment top-side pockets.
3. Assemble the lower ring using lower seam bridge plates, M3 screws, and 4 mm dowels.
4. Place lower contact pads into the four sensor stations.
5. Place one sensor in each station with its cable exiting outward.
6. Place upper contact pads on the sensors.
7. Print and clean all upper carrier segments.
8. Install M3 heat-set inserts into the upper segment underside pockets.
9. Assemble the upper carrier using underside upper seam bridge plates, M3 screws, and 4 mm dowels.
10. Attach or place the removable upper support grate on the floating upper carrier.
11. Lower the upper carrier assembly onto the four upper pads.
12. Confirm that the upper carrier contacts only the upper pads in normal unloaded condition.
13. Confirm overload stop clearance.
14. Install the salt container and calibrate.

## Single sensor replacement procedure

1. Remove the salt container.
2. Power down the electronics.
3. Remove the removable upper support grate if it blocks access to the target upper segment screws.
4. Loosen or remove the two upper seam bridge plates adjacent to the target upper segment.
5. Lift off the target upper carrier segment.
6. Remove the upper contact pad from the failed sensor.
7. Disconnect the failed sensor wiring.
8. Slide or lift the failed sensor out through the open outer side of the station.
9. Inspect the lower contact pad and pocket for salt debris or wear.
10. Replace the lower contact pad if worn or corroded.
11. Insert the replacement sensor with its cable exiting outward.
12. Reinstall the upper contact pad.
13. Reinstall the upper carrier segment.
14. Reinstall the upper seam bridge plates and dowels.
15. Reinstall the support grate.
16. Reconnect wiring.
17. Power on, tare, and recalibrate.

The lower base ring can remain assembled throughout this procedure.

## Why sensors are not trapped

The station uses:

- Two tangential guide rails.
- One inner radial stop.
- An open outer side.
- Removable upper pad.
- Removable upper carrier.

There is no printed cap over the sensor and no upper-to-lower fastener crossing the station. The sensor is held in place by gravity, lateral guides, and normal compression when the upper carrier is installed.

## Maintenance checks

At each sensor replacement or annual inspection:

- Check that guide rails are not worn or salt-crusted.
- Check that the lower contact pad is flat and clean.
- Check that the upper contact pad is flat and clean.
- Check that the overload stops are not polished or compressed from normal use.
- Check that dowels still slip into sockets without forcing.
- Check that M3 inserts are not loose.
- Check sensor wiring strain relief.

## Failure modes addressed

- Failed sensor: removable after lifting one upper segment.
- Worn contact pad: replaceable without reprinting ring segments.
- Loose upper seam: service upper-only seam plates.
- Loose lower seam: service lower-only seam plates without disturbing sensors.
- Damaged support grate: removable and replaceable as an upper-only part.

## Failure modes not fully addressed yet

- Cable strain relief is not finalized.
- Waterproofing is not designed.
- Salt dust sealing is not designed.
- Connector style is not selected.
- Long-term PETG creep around insert pockets is untested.

## Serviceability recommendation

Use connectors or a small terminal block for each sensor during the prototype phase. Direct soldering is cheaper, but it makes single-sensor replacement much worse and works against the serviceability goal.
