# SaltScale v6 — Assembly Review

This document describes how all parts of SaltScale v6 fit together, the exploded arrangement, a cross-section through one sensor module, the recommended assembly order, and notes on trapped parts or impossible sequences.

See the exploded/annotated diagram: [docs/saltscale-v6-exploded-assembly.svg](docs/saltscale-v6-exploded-assembly.svg)

Parts (names map to CAD/exports):
- `platform_v6_segment_0..3` — four printable quarter segments (each contains lower plate geometry and one `sensor_module_v3` assembly).
- `sensor_module_v3` (module parts inside each segment):
  - `module_base` — module base pocket integrated into the segment lower plate.
  - `lower_pad` — lower reaction pad (z = 6..8 mm).
  - `sensor_placeholder` — sensor body placeholder (z = 8..20 mm).
  - `upper_pad` — removable upper contact pad (z = 20..24 mm).
  - `module_stops` — distinct cylindrical overload stops (top at z = 19 mm).
- Joining/locating hardware (not modelled as separate parts):
  - metal dowel pins (4 mm recommended; holes are 4.2 mm clearance in CAD)
  - M3 screws into blind pockets near rim

Exploded view (summary)
- The platform is assembled from the four quarter segments. Each segment already contains a complete `sensor_module_v3` assembly placed at its quadrant center (45°, 135°, 225°, 315°).
- When exploded, the sequence shows (top → bottom): upper platform/top plate (per segment), `upper_pad` (module), `sensor_placeholder` (or real sensor), `lower_pad`, module base integrated into the segment lower plate, and finally the assembled full platform skirt/perimeter when all segments are joined.

Cross-section through one sensor module (Z heights, all mm, top-of-base = z 6.0):
- Upper plate boss / upper platform: contacts `upper_pad` at z = 20..24.
- `upper_pad`: 20..24 mm — transmits load to the sensor.
- `sensor_placeholder` (sensor): 8..20 mm — sensing element flexes in this range.
- `lower_pad`: 6..8 mm — reaction pad that transfers load into the segment lower plate.
- Segment lower plate / ribs: z = 0..6 mm — carries load outward to perimeter.
- Module stops top at z = 19.0 mm — provide 1 mm clearance to `upper_pad` underside (protective limit).

Assembly order (recommended, by step):
1. Place one segment flat on the work surface (segment 0). The `sensor_module_v3` parts intended to be removable are already modelled as separate bodies in the segment; ensure `lower_pad` and module base are present in the segment.
2. Insert the real sensor (or `sensor_placeholder` test part) into the pocket from above so it seats on the `lower_pad` (sensor should be removable upward).
3. Place the `upper_pad` onto the sensor from above (upper pad sits into the pocket and is removable). Do not compress beyond the 1 mm gap to the module stops.
4. Repeat steps 1–3 for the other three segments.
5. Bring two adjacent segments together and insert alignment dowels through matching holes near the rim.
6. Fit the remaining segments using dowels to align all seams.
7. Install M3 screws into the blind pockets near the rim to secure the seam (screw depth is limited to lower plate area — they do not create top→bottom though-holes consistent with v6 design).
8. Optionally install metal dowels permanently (press-fit) or add caps over M3 screws.

Per-part details

- `Upper platform / top plate` (per segment top wedge)
  - What it does: provides the user-facing surface and top bosses that contact module upper pads.
  - What it touches: `upper_pad` when assembled; ribs and top plate material elsewhere.
  - Carries load? Yes — during normal operation load transfers from top plate boss → upper_pad → sensor.
  - Alignment only? No.

- `Upper_pad` (module part)
  - What it does: distributes contact pressure into the sensor and provides defined contact geometry.
  - What it touches: top plate boss (above) and sensor placeholder (below); may contact module stops under overload.
  - Carries load? Yes (primary vertical load path when within travel range).
  - Alignment only? No, but it is removable for service.

- `Sensor_placeholder` / sensor (module part)
  - What it does: the sensing element inside the module; flexes under load to produce readable strain.
  - What it touches: `upper_pad` (top) and `lower_pad` (bottom).
  - Carries load? Yes (primary sensing element).
  - Alignment only? No.

- `Lower_pad` (module part)
  - What it does: reaction surface that transmits sensor output into the segment lower plate.
  - What it touches: sensor bottom and segment lower plate.
  - Carries load? Yes.
  - Alignment only? No.

- `Module_base` (module base integrated into segment lower plate)
  - What it does: houses pocket, guide walls, and stops; provides lateral guidance and overload stop support.
  - What it touches: `lower_pad`, sensor (when installed), module stops (if engaged), surrounding ribs.
  - Carries load? Yes (receives load from lower_pad and spreads to lower plate).
  - Alignment only? Partly: guide walls help locate the sensor, but module base also carries load.

- `Dowel pins` (hardware, not modelled)
  - What they do: provide accurate alignment between segments under assembly and load.
  - What they touch: reinforced dowel bosses in each segment.
  - Carry load? Primarily alignment; if sized/pressed they may carry some shear between segments but not intended to be primary vertical load path.
  - Alignment only? Primarily yes.

- `M3 screws` (into blind pockets)
  - What they do: clamp segments together and hold seams closed.
  - What they touch: lower-plate blind pockets and local boss material; do not pass into top plate region.
  - Carry load? They clamp; not part of sensor load path and intentionally do not form a top→bottom stiffener across sensor zones.
  - Alignment only? No — they secure the seam.

Assembly sequencing hazards
- Impossible or trapped components:
  - No trapped `upper_pad`/`sensor_placeholder` parts: sensors and pads are designed to be removable from above before segments are joined; therefore no part is trapped if assembled in recommended order.
  - If segments are joined before sensors/upper pads are installed, you will not be able to insert sensors from above into a fully assembled platform — therefore sensors must be installed into each segment prior to final seam joining.

- Parts that cannot be installed after another part:
  - Sensors and `upper_pad` must be installed into their segment pockets before adjoining that segment to neighbors; installing them after full assembly may be impossible without disassembly.

Checks to perform before final assembly
- Print and validate one segment with `sensor_module_v3` placeholder to check pocket clearance and dowel fit.
- Verify dowel diameter and fit (4.2 mm hole; choose dowel size accordingly, e.g., 4.0 mm dowel).
- Verify M3 screw length and head clearance so screws do not bottom out or deform the lower plate excessively.

Conclusion
- The v6 design supports a clear, serviceable assembly sequence: build and populate each segment individually (sensor + upper_pad), then join segments with dowels and blind M3 screws. No trapped parts if the recommended order is followed. Sensor force paths remain preserved and protected by module stops and platform-level overload pads.
