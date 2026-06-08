# Platform v5 — Segmentation Review

This document explains how the platform was split into four printable quarter segments and validates fit, seam placement, and risks.

Segment generation
- Each segment is a quarter-wedge derived from `_quarter_wedge` and contains one complete `sensor_module_v3` assembly placed at the quadrant center (sensor angles 45°, 135°, 225°, 315°).
- Alignment features: even-numbered segments have male alignment pins at both bounding seams; odd-numbered segments have mating receiver holes.
- M3 seam screw clearances are included using the same pattern as earlier platform versions; screw holes are placed near the outer perimeter and do not cross sensor force paths.

Segment dimensions (nominal)
- Outer radius: 160 mm (outer diameter 320 mm).
- Segment bounding box (XY): approximately 160 mm × 160 mm plus small margin for ribs and seam features — fits within 200 × 200 mm print bed.
- Max Z height: P.total_height_mm + top_plate_thickness_mm + centering_lip_height_mm (existing platform total height), which is 42 + 6 + 5 = 53 mm — fits within 200 mm build height.

How each segment fits on Prusa MK4
- Each segment's X and Y extents are under 200 mm (quarter wedge radius 160 mm), and the largest printed feature is the centering lip which is within the top surface thickness; segments therefore fit on a 200×200 bed when printed individually.

Seam strategy and sensor protection
- Segment boundaries align with 0°, 90°, 180°, 270° axes. Sensor modules are at 45°, 135°, 225°, 315° and therefore lie fully inside single segments (no sensor is split across a seam).
- Alignment pins/sockets are located near the outer perimeter and are intentionally small (pin radius 2 mm) to avoid interfering with the sensor pocket or creating a new load path.
- M3 joining holes are placed near the outer rim (reusing the existing seam hole pattern) and do not intrude into the sensor-supported regions.

Remaining risks
- Verify printing orientation and support: the module pocket and guide walls may require support depending on slicer settings. PETG bridging and retraction settings should be tuned.
- Tolerances and clearances: the sensor pocket clearance is nominally 0.4 mm; test prints are required to refine clearances for actual sensors and washers.
- Alignment peg strength: small pins (2 mm) may shear under high torque; consider metal dowels or larger pins if alignment accuracy under load is critical.

Files produced
- `cad/src/platform_v5.py` — segmentation implementation.
- `cad/exports/stl/platform_v5_segment_0.stl` .. `_3.stl` and corresponding `.step` files.
- `cad/exports/step/platform_v5_assembly.step` — combined assembly representation for visualization.
