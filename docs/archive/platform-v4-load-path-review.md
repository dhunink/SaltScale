# Platform v4 — Structural Load-Path Review

Purpose
- Review all load paths in `platform_v4` and highlight any geometry that allows load to travel from the upper plate to the lower plate without passing through a `sensor_module_v3` sensor element.

Summary (short)
- Primary load path: top plate bosses → module `upper_pad` → sensor (placeholder) → module `lower_pad` → platform lower plate → radial ribs → perimeter.
- Intended bypass (protective): platform-level overload pads (bottom) can contact the top in extreme compression and carry load directly from upper to lower, bypassing sensors — this is a designed safety stop.

1) All load paths (detailed)

- Per-module (canonical) load path — normal operation
  - External force on platform top is applied to the local top boss (part of the top plate) at each sensor location.
  - The top boss contacts the `upper_pad` (module component, z = 20..24 mm).
  - Load transmits through the `upper_pad` into the sensor body (sensor placeholder, z = 8..20 mm).
  - Load flows into the `lower_pad` (module component, z = 6..8 mm) which bears on the platform base.
  - From the `lower_pad`, load spreads into the platform lower plate and radial ribs and is carried outwards to the centering lip and perimeter.

- Module-local protective path (module overload stops)
  - Each `sensor_module_v3` contains distinct cylindrical overload stops whose tops are at z = 19.0 mm (1 mm below `upper_pad` underside). When compression exceeds 1 mm, the `upper_pad` bottoms onto these stops and further travel is prevented; load is then routed into the module base and into the lower plate.

- Platform-level protective path (global overload pads)
  - `bottom_segment` defines platform-level overload stop pads (radius ≈ 112 mm) that are tall enough to reach the top under extreme compression (their nominal top is intentionally set near the top plate with a gap `P.overload_stop_gap_mm`). When these pads engage, they provide a direct upper→lower load path that bypasses the sensor modules.

2) Direct upper-to-lower connections (explicit)

- Intended/direct (module): top boss ↔ upper_pad ↔ sensor ↔ lower_pad ↔ base — this is the designed sensor force path.
- Protective bypasses (intentional):
  - Module overload stops (local) — restrict travel and route excessive load into the module/base (still local to module, but bypasses the sensing element once engaged).
  - Platform-level overload pads (global) — when engaged they form a direct load bridge from the upper plate to the lower plate outside of the sensor footprints.

3) Sensor-supported regions (where applied load will reliably be read by sensors)

- The top bosses / contact bosses added in `_quarter_upper` at angles 45/135/225/315 are the primary sensor-supported regions; any load centered on those bosses will travel through the matched module upper/lower pads and be read by the sensor.
- The `sensor_module_v3` pocket area (38×38 mm) and immediate surrounding guide walls are part of the supported region for that sensor.

4) Geometry that bypasses sensors (areas of concern)

- Platform-level overload pads (bottom): these pads at radius ≈ 112 mm are explicitly designed to contact the top plate under extreme compression and thus transfer load without passing through the sensors. This is intentional (hardware safety stop), but it is the principal region where bypass occurs.

- Any direct top-to-bottom contact created by future changes: currently there are no other solid geometries that bridge top→bottom at the sensor radii, but modifications (adding thicker bosses, welding fused inserts, or changing pad heights) could create unintended bypasses.

5) Impact & recommendations

- Impact:
  - Normal operation: loads at sensor boss positions will be captured by sensors as designed.
  - Overloads: both module-level stops and platform-level pads will bypass sensors to protect them; readings during/after such events are not representative and sensors may see non-linear loading.

- Recommendations:
  - Keep `sensor_module_v3` guide walls capped at or below z = 19.0 mm (already enforced in v3) so walls cannot carry vertical load.
  - Verify platform-level overload-pad gap (`P.overload_stop_gap_mm`) is sized intentionally — if you want no global bypass, increase the gap (or reduce pad height) so the global pads never contact the top in expected loading ranges.
  - When adding inserts or stiffeners, ensure their top/bottom heights do not create new direct upper→lower bridges at or near sensor radii.

Files referenced
- `cad/src/platform_v4.py` — platform placement and top/bottom geometry.
- `cad/src/sensor_module_v3.py` — canonical sensor architecture (pads, pocket, guide walls, stops).
- `docs/sensor-module-assembly.md` — description of module-level force path and stop behavior.

Annotated schematic
- See the top-down schematic showing sensor positions, load zones, and bypass annulus: [docs/platform-v4-load-path-review.svg](docs/platform-v4-load-path-review.svg)

Conclusion
- Platform v4 implements the required per-sensor force paths correctly via `sensor_module_v3`. The only designed bypasses are the module overload stops (local, protective) and the platform-level overload pads (global protective stops). No other direct top-to-bottom load bridges are present in the current CAD.
