"""Sensor module v2: explicit force-path parts and separate exports.

Creates:
- base (fixture body without removable pads)
- lower_pad (reaction pad that the sensor sits on)
- upper_pad (removable contact pad)
- sensor_placeholder (38x38x12 placeholder body)
- assembly (compound of all parts for STEP export)
"""
import math
import cadquery as cq
from params import P


def sensor_module_v2():
    # Base plate
    base = cq.Workplane("XY").box(100.0, 100.0, 6.0, centered=(True, True, False))

    # Pocket geometry
    pocket_size = 38.0
    pocket_h = 12.0

    # Lower pad (separate body) — solid boss that supports the sensor
    lower_pad_h = 2.0
    lower_pad = cq.Workplane("XY").box(pocket_size, pocket_size, lower_pad_h, centered=(True, True, False)).translate((0, 0, 6.0))

    # Attach lower pad to base as separate body (do not fuse) by union on base copy
    base_with_cut = base

    # Create pocket cut that leaves room above the lower pad
    clearance = 0.4
    pocket_cut = cq.Workplane("XY").box(pocket_size + clearance, pocket_size + clearance, pocket_h, centered=(True, True, False)).translate((0, 0, 6.0 + lower_pad_h))
    base_with_cut = base.cut(pocket_cut)

    # Guide walls around pocket (lateral guidance)
    wall_thickness = 3.0
    wall_h = lower_pad_h + pocket_h + 6.0
    left = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((-50.0 + wall_thickness / 2.0, 0, 6.0))
    right = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((50.0 - wall_thickness / 2.0, 0, 6.0))
    front = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, -50.0 + wall_thickness / 2.0, 6.0))
    back = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, 50.0 - wall_thickness / 2.0, 6.0))
    base_with_cut = base_with_cut.union(left).union(right).union(front).union(back)

    # Overload stops: small posts that engage the upper pad to limit compression
    stop_h = 1.0
    stop_w = 6.0
    stops = cq.Workplane("XY")
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = (pocket_size / 2.0 + 12.0) * math.cos(a)
        y = (pocket_size / 2.0 + 12.0) * math.sin(a)
        stops = stops.union(cq.Workplane("XY").box(stop_w, stop_w, stop_h, centered=(True, True, False)).translate((x, y, 6.0 + lower_pad_h + pocket_h - stop_h)))
    base_with_cut = base_with_cut.union(stops)

    # Upper contact pad (removable) — sits above pocket and transmits force to sensor
    upper_pad_h = 4.0
    upper_pad = cq.Workplane("XY").box(pocket_size, pocket_size, upper_pad_h, centered=(True, True, False)).translate((0, 0, 6.0 + lower_pad_h + pocket_h))

    # Sensor placeholder (separate body) — used for fit checks and assembly view
    sensor_placeholder = cq.Workplane("XY").box(pocket_size, pocket_size, pocket_h, centered=(True, True, False)).translate((0, 0, 6.0 + lower_pad_h))

    # Assembly: compound of base, lower pad, sensor placeholder, upper pad
    assembly = base_with_cut.union(lower_pad).union(sensor_placeholder).union(upper_pad)

    # Return all bodies so caller can export individually
    return base_with_cut, lower_pad, upper_pad, sensor_placeholder, assembly


if __name__ == "__main__":
    b, l, u, s, a = sensor_module_v2()
    show_object(b)  # type: ignore[name-defined]
    show_object(l)  # type: ignore[name-defined]
    show_object(u)  # type: ignore[name-defined]
    show_object(s)  # type: ignore[name-defined]
    show_object(a)  # type: ignore[name-defined]
