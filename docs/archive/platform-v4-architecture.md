# Platform v4 — Architecture and Notes

This document describes the v4 platform which integrates four `sensor_module_v3` modules as the canonical sensor architecture.

Overview
- Outer diameter: 320 mm (driven by `params.P.outer_diameter_mm`).
- Centering lip inner diameter: 300 mm.
- Four sensor modules placed at 45°, 135°, 225°, 315° at radius 100 mm from center.
- Uses the exact force-path parts from `cad/src/sensor_module_v3.py` (base, lower pad, sensor placeholder, upper pad, stops).

Load path
- External load enters at the top face of the `upper_pad` (module upper contact pad).
- Load transmits through the `upper_pad` into the sensor body (sensor placeholder / real sensor), then into the `lower_pad` which bears on the platform base.
- From the `lower_pad` the load spreads into the platform lower plate and radial ribs and is carried to the platform perimeter and centering lip.

Overload stop strategy
- Overload stops are implemented in each sensor module as separate cylindrical posts with tops at z = 19.0 mm, creating a 1.0 mm clearance below the `upper_pad` underside (z = 20.0 mm). When excessive compression occurs, the `upper_pad` will contact these stops and further travel is prevented, protecting the sensor.

Sensor placement rationale
- Modules are placed at 45/135/225/315° on a 100 mm radius to mimic typical four-sensor scale architectures (corner loading) while keeping them well inside the centering lip.
- Using complete `sensor_module_v3` assemblies ensures the validated force-path (lower pad → sensor → upper pad → overload stops) is preserved and repeatable across all four sensors.

Remaining assumptions and next steps
- Sensor mechanical/dimensional assumptions: the design uses a 38×38×12 mm placeholder for the sensor body. Obtain vendor datasheet to model screw holes or precise locating features.
- Electronics: no electronics, battery, button, or LED are included in this CAD (per requirements).
- Validation: print `sensor_module_v3` parts and `platform_v4.stl` to verify fit and clearances on a Prusa MK4.
