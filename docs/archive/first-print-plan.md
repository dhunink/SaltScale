# First Print Plan — SaltScale v6 (PETG)

This short plan recommends the minimum prints and checks before committing to full-platform prints. It assumes PETG on a Prusa MK4 (200×200×200 build volume).

1) Which part to print first
- Print one complete `platform_v6_segment_0` (one quarter segment) including its integrated `sensor_module_v3` pocket. Also print a spare `sensor_module_v3_sensor_placeholder.stl`, `sensor_module_v3_upper_pad.stl`, and `sensor_module_v3_lower_pad.stl` separately for fit tests.

2) Expected print time (approximate)
- `sensor_module_v3` small parts (placeholder, upper/lower pads): 1–3 hours combined.
- One full segment (`platform_v6_segment_0`): 6–12 hours depending on layer height and infill.
- Full 4-segment platform (for planning): ~24–48 hours total (sum of segments).

3) Expected PETG usage (approximate)
- `sensor_module_v3` small parts: 15–40 g.
- One full segment: 80–160 g.
- Full platform (4 segments): 320–640 g.

4) Recommended orientation
- Segment: flat on the build plate with the lower plate face down (native orientation in CAD). This keeps the sensor pocket vertical and preserves dimensional accuracy for dowel holes and blind pockets.
- Sensor placeholder / pads: print upright (flat faces horizontal) so mating faces are printed smooth and dimensional.

5) Expected support requirements
- Segment: minimal global supports if printed flat; small supports may be needed for top-plate boss underside if geometry creates overhangs. Use sparse, breakaway supports for pocket interiors if your slicer requires them.
- Sensor upper pad and lower pad: normally support-free when printed flat.

6) Most likely print failures
- Warping/edge lift on large thin plates (PETG benefits from an enclosure and brim).
- Pocket bridging sag or poor surface finish inside the sensor pocket (affects fit).
- Undersized/oversized dowel holes and blind pocket tolerances causing tight/loose fits.

7) Most likely assembly failures
- Dowel mismatch (holes too tight or too loose) — dowel boss failure under press-fit.
- M3 screw length/clearance mistakes — screws bottoming out or head colliding with features.
- Upper pad binding or being too loose in the pocket (affects load transmission and repeatability).

8) What to physically test before printing the full platform
- Print a small test coupon set: `sensor_module_v3_sensor_placeholder.stl`, `sensor_module_v3_lower_pad.stl`, `sensor_module_v3_upper_pad.stl`, and one cropped section of the segment that includes a dowel boss and blind M3 pocket (a ~60×60×10 mm test block).
- Check clearances: sensor pocket fit, dowel hole fit with chosen dowel, M3 screw length and fit in blind pocket, and upper_pad seating/removal force.
- Print orientation test: try one segment with and without brim/enclosure to confirm no warping.

Practical slicer settings (starting point for PETG)
- Nozzle temp: 240–250 °C. Bed: 80–90 °C. Enclosure recommended when available.
- Layer height: 0.2–0.28 mm for segments (0.2 mm for sensor-fit parts if tighter tolerances needed).
- Infill: 20–30% for segments; 50–100% (or solid) for small pads if desired.
- Perimeter walls: 3–4 perimeters for strength near dowel bosses and pocket walls.
- Brim: 8–12 mm for segments to mitigate warping.

Final note
- Start conservative: validate one populated segment and test coupons, adjust clearances and fastener lengths, then print remaining segments. This minimizes wasted PETG and time while ensuring fit and assembly reliability.
