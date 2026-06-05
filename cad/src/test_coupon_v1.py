"""Test coupon v1: small printable block to validate sensor pocket, pads, stops, dowel, and M3 blind pocket.

Exports separate bodies: coupon (with module base), upper_pad, lower_pad, sensor_placeholder.
"""
import cadquery as cq
import math
from sensor_module_v3 import sensor_module_v3
from params import P


def test_coupon_v1():
    # coupon platform: 140 x 140 mm, base thickness matching module base top at z=6
    coupon_size = 140.0
    base_thickness = 6.0
    coupon = cq.Workplane("XY").box(coupon_size, coupon_size, base_thickness, centered=(True, True, False))

    # pull module components from sensor_module_v3
    base_mod, lower_pad, sensor_ph, upper_pad, assembly = sensor_module_v3()

    # place module at coupon center
    placed_module = assembly.translate((0, 0, 0))
    coupon = coupon.union(placed_module)

    # Add a reinforced dowel boss near +X edge for testing (4.2 mm clearance hole)
    dowel_x = coupon_size / 2.0 - 12.0
    dowel_y = 0
    dowel_d = 4.2
    boss_r = dowel_d * 2.0
    boss_h = base_thickness
    boss = cq.Workplane("XY").circle(boss_r).extrude(boss_h).translate((dowel_x, dowel_y, 0))
    coupon = coupon.union(boss)
    # hole
    hole = cq.Workplane("XY").circle(dowel_d / 2.0).extrude(base_thickness + 2.0).translate((dowel_x, dowel_y, 0))
    coupon = coupon.cut(hole)

    # Add one M3 blind pocket representative: 3.5 mm dia, pocket depth = base_thickness + 2 mm
    pocket_x = -coupon_size / 2.0 + 20.0
    pocket_y = 0
    pocket_d = 3.5
    pocket_depth = base_thickness + 2.0
    pocket = cq.Workplane("XY").circle(pocket_d / 2.0).extrude(pocket_depth).translate((pocket_x, pocket_y, 0))
    coupon = coupon.cut(pocket)

    # Return coupon and separate module parts for printing
    return coupon, upper_pad, lower_pad, sensor_ph


if __name__ == "__main__":
    c, u, l, s = test_coupon_v1()
    show_object(c)  # type: ignore[name-defined]
    show_object(u)  # type: ignore[name-defined]
    show_object(l)  # type: ignore[name-defined]
    show_object(s)  # type: ignore[name-defined]
