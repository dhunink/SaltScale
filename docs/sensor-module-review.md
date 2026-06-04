# Sensor Module v1 — Design Review

This review describes how `cad/src/sensor_module_v1.py` positions and protects a single Kiwi/SparkFun-style 38×38×12 mm sensor placeholder, the intended force path, lateral restraint, overload stops, and serviceability.

1) Where the sensor is expected to sit
- The sensor placeholder is centered on the 100×100 mm test base. It occupies the rectangular pocket located at the base center.
- Intended seating: the sensor rests on a lower support boss (a small solid pad) that raises the sensor above the base plate. The upper contact pad (a separate part) sits on top of the sensor when assembled, creating a sandwich.

2) Which surfaces transfer force
- Primary compressive force path (intended):
  - Upper platform / test jig → upper contact pad bottom face → sensor top face → sensor body → sensor bottom face → lower support boss top face → base/lower fixture → floor.
- The upper pad provides a distributed, flat contact surface to avoid point loading on the sensor flexure.
- The lower boss provides a stiff reaction surface; it should be broad enough to distribute load across the sensor bottom face.

3) Which surfaces prevent lateral movement
- Guide walls surrounding the pocket (left, right, front and back walls) constrain the sensor laterally and protect it from side impacts.
- The pocket sidewalls (and any small clearance between the sensor and pocket) limit lateral motion; the 0.5 mm clearance in the CAD is intended to give slight play while still guiding the sensor.
- When compressed between upper pad and lower boss, friction and the guide walls together prevent the sensor from sliding under normal use.

4) Which parts are intended as overload stops
- Four small square posts placed around the pocket (at ~45°, 135°, 225°, 315°) act as preload/overload stops. Their height is set to limit additional compression beyond the nominal sensor stack by about 1 mm.
- When the platform is overloaded, the upper pad will contact these stops instead of further compressing the sensor, protecting the sensor from overstress.

5) Why the wall height was chosen
- The wall height in the module equals the lower boss height + pocket height + a safety margin (CAD uses `wall_h = boss_h + pocket_h + 6.0`). Rationale:
  - Extend above the sensor so the sensor is enclosed and protected from lateral impacts and tipping during insertion/removal.
  - Provide a guide that prevents shear loads on the sensor while still allowing top-down assembly.
  - The extra margin (6 mm) gives room for the upper pad and any assembly tolerance.

6) Serviceability — insertion and removal
- Intended assembly flow: place the sensor into the pocket from above so it sits on the lower boss, then place the upper contact pad on top (or lower the upper plate) to compress the sensor.
- The CAD uses a 0.5 mm radial clearance (sensor footprint 38 mm vs pocket 38.5 mm) so parts should be slidable by hand on a well-calibrated printer. Slightly tighter/looser fits depending on printer and PETG will occur.
- Removal: remove or lift the upper pad and lift the sensor out vertically; the guide walls protect the sensor and keep it aligned while removing.

7) Implementation note and verification
- Observation: the intended lower boss must remain as a solid support. Verify in the rendered model that the boss top remains after the pocket cut (the order of boolean unions/cuts in code can affect this). If the boss is removed by the pocket operation, the sensor would not have a defined lower support.

8) Minor recommendations (non-blocking)
- Add a shallow chamfer (1–2 mm × 15°) to the pocket upper entry to aid insertion and prevent catching.
- Add a small ledge or chamfer on the upper pad corners to ease alignment when placing it by hand.
- Add small fillets at wall-to-base and boss-to-base transitions to reduce stress concentrations in PETG.
- Consider exporting the `upper_pad` as a separate STL (currently returned by the module) so you can print it as a second part and test assembly.

9) Summary
- The module models the desired sandwich load path and includes lateral guide walls and 1 mm overload stops. With the current clearances and wall height, the sensor should be insertable and removable by hand on a calibrated Prusa MK4 using PETG. Verify in the viewer that the lower boss survives the pocket cut and perform a quick test-print to validate fit and assembly motions.
