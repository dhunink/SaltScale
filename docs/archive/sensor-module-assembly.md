# Sensor Module v2 — Assembly & Force Path

This document explains the parts produced by `sensor_module_v2` and exactly where loads travel and where constraints occur.

Generated files
- `cad/exports/stl/sensor_module_base.stl` — base fixture (pocketed plate and guide walls, with overload stops).
- `cad/exports/stl/sensor_module_lower_pad.stl` — lower reaction pad (solid boss the sensor sits on).
- `cad/exports/stl/sensor_module_upper_pad.stl` — removable upper contact pad that presses on the sensor.
- `cad/exports/stl/sensor_module_sensor_placeholder.stl` — sensor placeholder body (38×38×12) for fit checks.
- `cad/exports/step/sensor_module_v2_assembly.step` — full assembly compound (base + lower pad + sensor placeholder + upper pad).

Exact locations and roles

- Where force enters:
  - The user/applied load presses onto the `upper_pad` (the top face of `sensor_module_upper_pad.stl`). This is the primary external contact.

- Where force leaves (reaction path):
  - The load transmits through the `upper_pad` into the sensor placeholder (or real sensor) and then into the `lower_pad` (the solid boss exported as `sensor_module_lower_pad.stl`). From the lower pad the load is carried into the `base` plate and into the test rig or fixture.

- Where lateral guidance occurs:
  - Lateral guidance is provided by the guide walls on the `base` (in `sensor_module_base.stl`). These surround the pocket and prevent lateral/shear motion of the sensor and upper pad relative to the base.
  - The sensor placeholder itself is dimensioned with a small clearance; guide walls and pocket faces react any sideways loads before they reach the sensing element.

- Where the overload stop engages:
  - Overload stops are short posts located around the pocket on the top of the `base`. When the `upper_pad` is pressed beyond the intended travel, these posts physically contact the underside of the `upper_pad` and limit further compression — protecting the sensor from excessive compression or mechanical damage.

Updated wall-height rule (v3)
- Guide walls in `sensor_module_v3` end at or below z = 19.0 mm (base top is z = 6.0 mm). This guarantees the guide walls cannot make vertical contact with the `upper_pad` (which has its underside at z = 20.0 mm) and therefore cannot bypass the sensor by carrying vertical load.

Exact overload stop behavior (v3)
- Overload stops are distinct cylindrical posts in `sensor_module_v3_base.stl` and reach up to z = 19.0 mm. They create a 1.0 mm clearance below the `upper_pad` underside (z = 20.0 mm). When the `upper_pad` is depressed more than 1.0 mm relative to the base, the pad contacts these stops and further compression is prevented.

Design notes
- The `lower_pad` is a purposefully separate body so you can print or machine a hardened pad (washer/metal plate) and assemble it into the base to reduce wear and improve repeatability.
- The `upper_pad` is removable so you can iterate on contact-face materials (PTFE, metal washer, printed pad) and try different clearances.
- The `sensor_placeholder` is provided so you can validate fit and verify that the pocket, guide walls, and boss align correctly before installing real sensors.

Recommended next steps
- Print `sensor_module_sensor_placeholder.stl` and `sensor_module_base.stl` with the planned wall/clearance settings to verify fit on your Prusa MK4.
- Try lower-pad variants (metal washer glued to `sensor_module_lower_pad`) to test wear and repeatability.
