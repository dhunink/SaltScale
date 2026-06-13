# Concept v4 Upper Carrier Cleanup

Date: 2026-06-11

## Summary

This cleanup resolves the upper-pad / upper-carrier integration issues in `concept_v4`.

The active design now uses:

- A support-free upper segment with no lower protruding upper seam lugs.
- A removable one-piece upper pad.
- A `40 mm` upper pad body.
- A `12 mm` lower contact boss for the Kiwi sensor load-entry region.
- A `36 mm` upper locating lobe on the pad.
- A matching open-to-inner-edge socket/notch in the upper carrier.

The Round Cup remains rejected as active geometry. There is no underside cup, no through-hole boss, no sensor-relative locator, no fragile tabs, and no separate retainer plug in the active design.

## What Was Removed

The cleanup removes the overlapping upper-pad concepts from the active assembly:

- Round Cup underside cup/rim geometry.
- Circular upper-pad land disk geometry.
- The earlier key-only notch that looked like a locator but did not positively engage the carrier.
- The separate upper-pad retainer plug experiment.
- Any floating disk-like construction bodies near the sensor stack.

No sensor-station, lower-pad, lower-base, support-grate, or integrated M3 seam architecture was redesigned.

## Final Retention Method

The upper pad is located by a drop-in open socket:

1. The upper pad has a `36 mm` upper locating lobe above the `40 mm` pad body.
2. The upper carrier has a matching open-to-inner-edge socket at each sensor station.
3. The socket is larger than the lobe by `0.6 mm per side`.
4. A `22 mm` throat connects the socket to the inner edge.

The lobe drops into the socket when the upper carrier is lowered onto the pad. The socket side walls constrain the pad laterally, so the pad cannot drift sideways during normal handling. The narrowed throat prevents the lobe from sliding out through the inner edge. The pad remains removable by lifting the upper carrier and taking the pad out by hand.

This is carrier-relative retention. It does not depend on the sensor for locating and does not create an upper-to-lower bypass.

## Assembly Explanation

Normal assembly order for one sensor stack:

1. Place the lower pad into the lower sensor station.
2. Place the Kiwi sensor on the lower pad with the cable exiting outward.
3. Place the upper pad on the sensor, with the `12 mm` boss facing downward.
4. Align the pad's `36 mm` upper lobe with the upper carrier's open socket.
5. Lower the upper carrier onto the upper pad.
6. Confirm the lobe is seated in the socket and the `40 mm` pad body bears against the flat underside of the upper carrier.

The measurement load path remains:

```text
upper carrier
-> 40 mm upper pad body/shoulder
-> 12 mm lower contact boss
-> Kiwi sensor central load region
-> lower pad
-> lower base
-> floor
```

The locating lobe is not intended as the primary force-contact surface; it is a lateral positioning feature.

## Why It Is Support-Free

Upper segment:

- The upper integrated M3 lugs are same-plane with the main upper segment body.
- There is no material below the main upper body plane.
- The pad locator is an open-to-inner-edge socket, not a blind underside pocket.
- The socket and throat are through-cuts, so they do not create hidden bridges.

Upper pad:

- The active STL is exported in print orientation with the upper locating lobe on the bed.
- The `40 mm` body overhangs the `36 mm` lobe by about `2 mm per side`, which is intended to print as a short support-free PETG shoulder.
- The `12 mm` contact boss prints upward.

## Why It Is Mechanically Robust

The socket avoids thin fragile tabs. The estimated material around the risky areas is:

| Feature | Value |
| --- | ---: |
| Socket diameter | `37.2 mm` |
| Throat width | `22.0 mm` |
| Throat-to-socket shoulder per side | `7.6 mm` |
| Outer radial web beyond socket | `23.4 mm` |

The socket is open to the inner edge, so there is no isolated thin wall at the inside of the ring. The outer radial web remains broad, and the M3 nut pockets are not near the pad socket.

If physical testing shows the pad is too loose, adjust socket clearance first. The load path should remain unchanged.

## Verification

CAD checks after cleanup:

| Check | Result |
| --- | ---: |
| Upper segment material below main body plane | `0.0 mm^3` |
| Upper pad vs upper segment overlap | `0.0 mm^3` |
| Upper/lower segment overlap | `0.0 mm^3` |
| Support grate vs upper segment overlap | `0.0 mm^3` |
| Support grate vs lower segment overlap | `0.0 mm^3` |
| Sensor top / upper pad bottom | `16.84 mm / 16.84 mm` |

Printable envelopes:

| Part | Approximate print envelope |
| --- | ---: |
| Upper segment 0 | `178.99 x 158.11 x 14.00 mm` |
| Upper pad | `40.00 x 40.00 x 11.16 mm` |

## Next Inspection

Inspect these files first:

```text
cad/exports/active/stl/concept_v4_upper_segment_0.stl
cad/exports/active/stl/concept_v4_upper_pad.stl
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Physical validation should confirm:

- The upper segment lies flat in PrusaSlicer.
- The upper pad prints without supports.
- The pad drops into the carrier socket by hand.
- The pad cannot slide out through the inner-edge throat during normal handling.
- The `12 mm` boss still lands on the intended Kiwi sensor load-entry region.
