# Concept v2 Interface Coupon Plan

Date: 2026-06-05

## Summary

`concept_v2_interface_coupons.py` adds small print-first coupons for the critical mechanical interfaces in `concept_v2`.

These coupons do not replace the full platform CAD. They are intended to validate the risky interfaces before printing full lower or upper ring segments.

Generated coupon exports:

| Coupon | Approximate envelope |
| --- | ---: |
| `sensor_station_coupon_v2` | 179.0 x 132.0 x 21.0 mm |
| `upper_lower_stack_coupon_v1` | 195.0 x 157.0 x 21.0 mm |
| `lower_seam_coupon_v1` | 84.0 x 120.0 x 8.0 mm |
| `upper_seam_coupon_v1` | 84.0 x 120.0 x 8.0 mm |
| `support_grate_fit_coupon_v1` | 160.0 x 52.0 x 8.0 mm |
| `centering_lip_coupon_v1` | 31.7 x 74.5 x 14.0 mm |

All coupons fit within the Prusa MK4 200 x 200 x 200 mm print envelope.

## General print notes

- Print in PETG.
- Use the same nozzle, layer height, perimeters, and hole compensation intended for the prototype.
- Print the coupons flat in their exported orientation.
- Multi-body STL files are intentional print kits. Keep the bodies separated on the bed; do not merge them into a single fused part.
- Deburr holes, pockets, guide edges, and pad contact faces before measurement.
- Record slicer material and print time estimates before printing full segments.

## 1. sensor_station_coupon_v2

Export files:

- `cad/exports/stl/sensor_station_coupon_v2.stl`
- `cad/exports/step/sensor_station_coupon_v2.step`

What it tests:

- Current fixed sensor station geometry.
- Dummy 38 x 38 x 12 mm sensor fit.
- Guide rail clearance.
- Lower pad seating on solid base material.
- Upper pad handling.
- Overload stop clearance.
- Open-side service access.

How to print it:

- Print flat in the exported orientation.
- No supports should be required.
- Print the included dummy sensor and pad pieces in the same job or separate them in the slicer if preferred.

Hardware or dummy parts needed:

- Included printed dummy sensor.
- Included printed lower pad.
- Included printed upper pad.
- Calipers.
- Paper strips or feeler gauges.

What to measure:

- Dummy sensor sliding clearance between guide rails.
- Dummy sensor removal path through the open outer side.
- Lower pad flatness and seating.
- Upper pad fit without binding on guides or stops.
- Vertical clearance from upper pad/upper carrier reference to overload stop tops.

Pass/fail criteria:

- Dummy sensor inserts and removes by hand without prying.
- Lower pad sits flat on solid base.
- Upper pad can be placed and removed without scraping guide walls.
- Guide walls start on solid printed base with no unsupported bottom bridges.
- Overload stops are not contacted in the nominal dummy stack.

Likely CAD change if it fails:

- Increase guide clearance.
- Move guide rails or overload stops outward.
- Add a non-trapping pad locator.
- Change overload stop height or make stop clearance adjustable.

## 2. upper_lower_stack_coupon_v1

Export files:

- `cad/exports/stl/upper_lower_stack_coupon_v1.stl`
- `cad/exports/step/upper_lower_stack_coupon_v1.step`

What it tests:

- Local upper-to-lower stack behavior.
- Floating upper carrier patch sitting on upper pad, dummy sensor, lower pad, and lower base.
- Clearance between upper carrier and lower guide/stops.
- Confirmation that no unintended upper-to-lower contact occurs outside the sensor stack.

How to print it:

- Print flat in the exported orientation.
- No supports should be required.
- Assemble the separate pieces after printing: lower station, lower pad, dummy sensor, upper pad, upper carrier patch.

Hardware or dummy parts needed:

- Included printed dummy sensor and pads.
- Included printed upper carrier patch.
- Paper strips or feeler gauges.
- Small household test weights if doing a light compression check.

What to measure:

- Clearance between upper carrier patch and guide walls.
- Clearance between upper carrier patch and overload stops.
- Whether paper strips slide freely around all non-load-path features.
- Whether the upper patch rocks on the dummy stack.

Pass/fail criteria:

- Upper patch contacts only the upper pad in the nominal stack.
- Paper strips show no normal contact at guide rails, stops, or lower-base features.
- Dummy stack remains removable after the upper patch is lifted.
- No upper-to-lower screw, dowel, or printed feature is needed to hold the stack together.

Likely CAD change if it fails:

- Increase vertical clearance around guides.
- Reduce upper carrier patch overhang near station features.
- Adjust pad size or station position.
- Lower overload stops or increase nominal stack height control.

## 3. lower_seam_coupon_v1

Export files:

- `cad/exports/stl/lower_seam_coupon_v1.stl`
- `cad/exports/step/lower_seam_coupon_v1.step`

What it tests:

- Two shortened lower-ring segment edges.
- Top-side M3 heat-set insert pockets.
- 4 mm dowel sockets.
- Separate lower seam bridge plate.
- Lower-to-lower joining without touching the upper structure.

How to print it:

- Print flat with insert pockets facing up.
- No supports should be required.
- Leave the bridge plate separate from the two segment-edge blocks.

Hardware or dummy parts needed:

- M3 heat-set inserts, if available.
- M3 screws matching the insert depth.
- 4 mm metal dowel, drill shank, or printed dowel stand-in.
- Soldering iron for insert installation.
- Calipers.

What to measure:

- Insert pocket diameter and depth after printing.
- Dowel socket diameter and depth after printing.
- Insert installation effort and whether bosses split.
- Bridge plate hole alignment.
- Seam gap and block alignment after installing bridge and dowel.

Pass/fail criteria:

- Inserts install straight without splitting the PETG.
- Screws engage inserts without bottoming out.
- Dowel is a controlled slip fit, not a forced press fit.
- Bridge plate clamps both segment edges without visible bending.
- Joined blocks remain flat on the table.

Likely CAD change if it fails:

- Adjust insert pocket diameter/depth.
- Increase boss diameter.
- Increase dowel socket clearance.
- Increase bridge plate thickness or width.
- Move seam hardware away from edges.

## 4. upper_seam_coupon_v1

Export files:

- `cad/exports/stl/upper_seam_coupon_v1.stl`
- `cad/exports/step/upper_seam_coupon_v1.step`

What it tests:

- Two shortened upper-ring segment underside edges.
- Underside M3 heat-set insert pockets.
- 4 mm dowel sockets.
- Separate upper seam bridge plate.
- Upper-to-upper joining without any lower-base connection.

How to print it:

- Print flat with the underside pocket face upward.
- Treat the upward-facing pocket face as the underside of the real upper carrier.
- No supports should be required.

Hardware or dummy parts needed:

- M3 heat-set inserts, if available.
- M3 screws.
- 4 mm metal dowel, drill shank, or printed dowel stand-in.
- Soldering iron for insert installation.
- Calipers.

What to measure:

- Insert pocket access from the underside face.
- Insert seating depth and straightness.
- Dowel socket fit.
- Bridge plate screw access.
- Whether the bridge plate can be removed and reinstalled repeatedly.

Pass/fail criteria:

- Inserts can be installed from the underside face without damaging the coupon.
- Bridge plate attaches and detaches cleanly.
- Dowel alignment is repeatable.
- The coupon validates an upper-only joint; no lower-base part is needed.

Likely CAD change if it fails:

- Revise underside insert pocket access.
- Change bridge plate screw layout.
- Increase local material around insert pockets.
- Add chamfers or lead-ins to dowel sockets.

## 5. support_grate_fit_coupon_v1

Export files:

- `cad/exports/stl/support_grate_fit_coupon_v1.stl`
- `cad/exports/step/support_grate_fit_coupon_v1.step`

What it tests:

- A small upper-carrier section with a removable support-grate channel.
- A representative support-grate arm tab.
- Whether a top-side removable grate interface can locate cleanly while remaining serviceable.

How to print it:

- Print flat in the exported orientation.
- No supports should be required because the channel is open from the top and one side.
- Insert the grate tab by hand after printing.

Hardware or dummy parts needed:

- Included printed grate tab.
- Calipers.
- Actual salt container, if available.

What to measure:

- Grate tab sliding clearance.
- Whether the tab seats flat in the channel.
- Whether the tab rattles, jams, or rocks.
- Whether the channel would trap salt debris.
- Whether the interface is easy to remove by hand.

Pass/fail criteria:

- Grate tab inserts and removes by hand.
- Grate tab sits flush enough that the container cannot catch on an edge.
- Interface remains upper-only and does not imply any lower-base contact.
- Channel does not create an obvious salt trap that cannot be cleaned.

Likely CAD change if it fails:

- Increase channel clearance.
- Change grate arm width or thickness.
- Add a lead-in chamfer.
- Replace the channel with a simpler loose/removable grate feature.
- Add debris relief before integrating this interface into the full upper carrier.

## 6. centering_lip_coupon_v1

Export files:

- `cad/exports/stl/centering_lip_coupon_v1.stl`
- `cad/exports/step/centering_lip_coupon_v1.step`

What it tests:

- Curved section of the 300 mm centering lip.
- Upper carrier/lip print quality.
- Contact feel against the real salt container wall.
- Whether the lip height and wall thickness are practical in PETG.

How to print it:

- Print flat in the exported orientation.
- No supports should be required.
- Use the same perimeter settings intended for the upper carrier.

Hardware or dummy parts needed:

- Actual salt container, if available.
- Calipers.
- Paper strips for contact checks.

What to measure:

- Lip thickness after printing.
- Lip height after printing.
- Curved inner face quality.
- Clearance against the container wall.
- Whether the lip scuffs, jams, or leaves too much play.

Pass/fail criteria:

- Lip prints cleanly without supports.
- Inner curved face contacts or clears the real container as intended.
- Container can be lifted away without snagging.
- Lip is stiff enough for handling and not sharp enough to scrape the container.

Likely CAD change if it fails:

- Increase inner diameter clearance.
- Reduce lip height.
- Add a chamfer or roundover.
- Increase wall thickness if PETG feels fragile.
- Replace continuous lip with shorter centering tabs.

## Recommended print order

1. `sensor_station_coupon_v2`
2. `upper_lower_stack_coupon_v1`
3. `lower_seam_coupon_v1`
4. `upper_seam_coupon_v1`
5. `support_grate_fit_coupon_v1`
6. `centering_lip_coupon_v1`

First print:

```text
sensor_station_coupon_v2
```

Reason:

The sensor station is still the highest-risk local interface. If dummy sensor fit, guide clearance, pad seating, or overload stop clearance is wrong, full lower segments and full quadrants should not be printed yet.

## Do not validate with full ring segments yet

Do not print full `concept_v2` lower or upper ring segments until these coupons have answered the local interface questions. A full segment print should come only after:

- Dummy sensor insertion/removal passes.
- Upper-to-lower stack clearance passes.
- Seam hardware geometry is plausible.
- Support grate and centering lip assumptions are checked against the real container.
