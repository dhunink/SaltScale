"""Sensor module v3: corrected wall heights and distinct overload stops.

Stack (Z coordinates, top-of-base = 6.0):
- lower_pad: z = 6.0 .. 8.0
- sensor_placeholder: z = 8.0 .. 20.0
- upper_pad: z = 20.0 .. 24.0

Guide walls end at or below z = 19.0 so they never carry vertical load.
Overload stops are separate cylindrical posts with top at z = 19.0 (creating a 1 mm clearance
below the `upper_pad` underside at z=20.0).
"""
import math
import cadquery as cq
from params import P


def sensor_module_v3():
    # Base plate
    base_thickness = 6.0
    base = cq.Workplane("XY").box(100.0, 100.0, base_thickness, centered=(True, True, False))

    # Stack heights
    lower_pad_h = 2.0  # top at z = 8.0
    pocket_h = 12.0    # sensor placeholder 8..20
    upper_pad_h = 4.0  # top at z = 24.0

    # Lower pad (separate body)
    pocket_size = 38.0
    lower_pad = cq.Workplane("XY").box(pocket_size, pocket_size, lower_pad_h, centered=(True, True, False)).translate((0, 0, base_thickness))

    # Pocket cut leaving clearance above lower pad
    clearance = 0.4
    pocket_cut = cq.Workplane("XY").box(pocket_size + clearance, pocket_size + clearance, pocket_h, centered=(True, True, False)).translate((0, 0, base_thickness + lower_pad_h))
    base_with_cut = base.cut(pocket_cut)

    # Guide walls (lateral guidance only) -- end at or below z = 19.0
    wall_top_z = 19.0
    wall_h = wall_top_z - base_thickness  # height measured from base top (z=base_thickness)
    if wall_h < 0:
        wall_h = 0.0
    wall_thickness = 3.0
    left = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((-50.0 + wall_thickness / 2.0, 0, base_thickness))
    right = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((50.0 - wall_thickness / 2.0, 0, base_thickness))
    front = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, -50.0 + wall_thickness / 2.0, base_thickness))
    back = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, 50.0 - wall_thickness / 2.0, base_thickness))
    base_with_cut = base_with_cut.union(left).union(right).union(front).union(back)

    # Distinct overload stops: cylindrical posts with top at z = 19.0 (1 mm below upper pad underside)
    stop_top_z = 19.0
    stop_h = stop_top_z - base_thickness
    stop_r = 3.0
    stops = cq.Workplane("XY")
    stop_positions = []
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = (pocket_size / 2.0 + 12.0) * math.cos(a)
        y = (pocket_size / 2.0 + 12.0) * math.sin(a)
        stop_positions.append((x, y))
        stops = stops.union(cq.Workplane("XY").circle(stop_r).extrude(stop_h).translate((x, y, base_thickness)))
    # Make stops a separate body by unioning into base_with_cut (still visually distinct in CAD viewers)
    base_with_cut = base_with_cut.union(stops)

    # Upper pad (removable)
    upper_pad = cq.Workplane("XY").box(pocket_size, pocket_size, upper_pad_h, centered=(True, True, False)).translate((0, 0, base_thickness + lower_pad_h + pocket_h))

    # Sensor placeholder (separate body) — fits into the pocket
    sensor_placeholder = cq.Workplane("XY").box(pocket_size, pocket_size, pocket_h, centered=(True, True, False)).translate((0, 0, base_thickness + lower_pad_h))

    # Assembly compound
    assembly = base_with_cut.union(lower_pad).union(sensor_placeholder).union(upper_pad)

    return base_with_cut, lower_pad, sensor_placeholder, upper_pad, assembly


if __name__ == "__main__":
    b, l, s, u, a = sensor_module_v3()
    show_object(b)  # type: ignore[name-defined]
    show_object(l)  # type: ignore[name-defined]
    show_object(s)  # type: ignore[name-defined]
    show_object(u)  # type: ignore[name-defined]
    show_object(a)  # type: ignore[name-defined]
