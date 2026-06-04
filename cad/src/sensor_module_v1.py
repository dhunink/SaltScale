"""Standalone sensor module for Kiwi/SparkFun-style 50kg sensor validation.

Creates a small printable fixture containing:
- sensor pocket (38x38x12 placeholder)
- lower support pad
- upper contact pad (removable as a separate body)
- guide walls and 1 mm overload stop
"""
import math
import cadquery as cq
from params import P


def sensor_module() -> cq.Workplane:
    # Base plate sized for Prusa MK4 printable test (100x100 mm)
    base = cq.Workplane("XY").box(100.0, 100.0, 6.0, centered=(True, True, False))

    # Sensor pocket location centered on base
    pocket_size = 38.0
    pocket_h = 12.0
    # lower support boss (solid) raises sensor slightly above base
    boss_h = 4.0
    boss = cq.Workplane("XY").box(pocket_size, pocket_size, boss_h, centered=(True, True, False)).translate((0, 0, 6.0))
    base = base.union(boss)

    # Create pocket cut for sensor body (clearance)
    clearance = 0.5
    pocket = cq.Workplane("XY").box(pocket_size + clearance, pocket_size + clearance, pocket_h, centered=(True, True, False)).translate((0, 0, 6.0))
    base = base.cut(pocket)

    # Guide walls around pocket (for lateral protection)
    wall_thickness = 3.0
    wall_h = boss_h + pocket_h + 6.0
    left = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((-50.0 + wall_thickness / 2.0, 0, 6.0))
    right = cq.Workplane("XY").box(wall_thickness, pocket_size + 20.0, wall_h, centered=(False, True, False)).translate((50.0 - wall_thickness / 2.0, 0, 6.0))
    front = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, -50.0 + wall_thickness / 2.0, 6.0))
    back = cq.Workplane("XY").box(pocket_size + 20.0, wall_thickness, wall_h, centered=(True, False, False)).translate((0, 50.0 - wall_thickness / 2.0, 6.0))
    base = base.union(left).union(right).union(front).union(back)

    # Upper contact pad (separate body) — placed above boss, not fused so it can be printed separately
    upper_pad_h = 4.0
    upper_pad = cq.Workplane("XY").box(pocket_size, pocket_size, upper_pad_h, centered=(True, True, False)).translate((0, 0, 6.0 + boss_h + pocket_h))

    # Overload stop: small posts around pocket that limit compression to 1 mm clearance
    stop_h = 1.0
    stop_w = 6.0
    stops = cq.Workplane("XY")
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = (pocket_size / 2.0 + 12.0) * math.cos(a)
        y = (pocket_size / 2.0 + 12.0) * math.sin(a)
        stops = stops.union(cq.Workplane("XY").box(stop_w, stop_w, stop_h, centered=(True, True, False)).translate((x, y, 6.0 + boss_h + pocket_h - stop_h)))
    base = base.union(stops)

    # Combine base and leave upper_pad separate (return both)
    return base, upper_pad


if __name__ == "__main__":
    b, u = sensor_module()
    show_object(b)  # type: ignore[name-defined]
    show_object(u)  # type: ignore[name-defined]
