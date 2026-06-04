"""Platform v4 — full platform using sensor_module_v3 at four positions.

Uses sensor_module_v3 as the canonical sensor architecture and places four
identical modules at 45/135/225/315 degrees on a round platform.

Outer diameter and centering lip are taken from `params.P`.
"""
import math
import cadquery as cq
from params import P
from saltscale_base import _quarter_wedge
from sensor_module_v3 import sensor_module_v3


def _quarter_lower(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0
    lower = _quarter_wedge(r_outer, P.bottom_plate_thickness_mm, quadrant)

    # radial ribs for stiffness (same pattern as v3)
    inner_clearance_r = (P.loadcell_length_mm / 2.0) + 24.0
    rib_width = 5.0
    rib_height = P.total_height_mm - P.bottom_plate_thickness_mm - 2.0
    rib_count = 3
    for i in range(rib_count):
        ang = quadrant * 90 + 15 + i * (60 / max(1, rib_count - 1))
        inner_r = inner_clearance_r + 6.0
        rib_len = r_outer - inner_r - 16.0
        rib = (
            cq.Workplane("XY")
            .box(rib_len, rib_width, rib_height, centered=(False, True, False))
            .translate((inner_r + rib_len / 2.0, 0, P.bottom_plate_thickness_mm + 2.0))
        )
        rib = rib.rotate((0, 0, 0), (0, 0, 1), ang)
        lower = lower.union(rib)

    # retain M3 seam screw clearances
    screw_d = 3.5
    seam_angles = [0, 90, 180, 270]
    for ang in seam_angles:
        a = math.radians(ang)
        for along in (-14.0, 14.0):
            aa = a + math.radians(along)
            x = (r_outer - 20.0) * math.cos(aa)
            y = (r_outer - 20.0) * math.sin(aa)
            hole = cq.Workplane("XY").circle(screw_d / 2.0).extrude(P.total_height_mm + 8).translate((x, y, 0))
            lower = lower.cut(hole)

    # NOTE: do NOT add sensor support bosses or overload pads here; sensor_module_v3
    # provides its own lower pad and overload stops and must be the canonical force path.

    return lower


def _quarter_upper(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0 - P.clearance_gap_mm
    top_z = P.total_height_mm
    upper = _quarter_wedge(r_outer, P.top_plate_thickness_mm, quadrant).translate((0, 0, top_z))

    # Top contact bosses sized to meet sensor_module_v3 upper pad (which occupies z=20..24)
    sensor_foot = 38.0
    # Create bosses whose bottom is at z=20.0 so they contact the module's upper pad
    boss_bottom_z = 20.0
    boss_h = P.total_height_mm - boss_bottom_z
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        r = 100.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        boss = cq.Workplane("XY").box(sensor_foot, sensor_foot, boss_h, centered=(True, True, False)).translate((x, y, boss_bottom_z))
        upper = upper.union(boss)

    # small top ribs for stiffness (keep same pattern as v3)
    rib_w = 4.0
    rib_h = 6.0
    for i in range(2):
        ang = quadrant * 90 + 25 + i * 30
        x = (r_outer - 60.0) * math.cos(math.radians(ang))
        y = (r_outer - 60.0) * math.sin(math.radians(ang))
        tr = cq.Workplane("XY").box(40.0, rib_w, rib_h, centered=(True, True, False)).translate((x, y, P.total_height_mm - rib_h))
        tr = tr.rotate((0, 0, 0), (0, 0, 1), ang)
        upper = upper.union(tr)

    return upper


def quarter_segment(quadrant: int = 0) -> cq.Workplane:
    return _quarter_lower(quadrant).union(_quarter_upper(quadrant))


def platform_v4_full() -> cq.Workplane:
    parts = []
    for q in range(P.segment_count):
        parts.append(quarter_segment(q))

    full = parts[0]
    for p in parts[1:]:
        full = full.union(p)

    # Place four sensor_module_v3 assemblies at 45/135/225/315 and union them into the platform
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        r = 100.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        # sensor_module_v3 returns (base_with_cut, lower_pad, sensor_placeholder, upper_pad, assembly)
        _, _, _, _, assembly = sensor_module_v3()
        placed = assembly.translate((x, y, 0))
        full = full.union(placed)

    return full


if __name__ == "__main__":
    show_object(platform_v4_full())  # type: ignore[name-defined]
