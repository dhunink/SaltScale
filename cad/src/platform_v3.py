"""Platform v3 — four-sensor architecture (four 38x38x12 placeholders).

Replaces central single-point loadcell with four corner sensors placed at
45/135/225/315 degrees. Keeps platform outer diameter and centering lip.
Focuses on structural architecture; no exact mounting holes.
"""
import math
import cadquery as cq
from params import P
from saltscale_base import _quarter_wedge


def _quarter_lower(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0
    lower = _quarter_wedge(r_outer, P.bottom_plate_thickness_mm, quadrant)

    # inner clearance: keep central area solid (no central cavity for v3)
    inner_clearance_r = (P.loadcell_length_mm / 2.0) + 24.0

    # radial ribs (similar to v2)
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

    # small support boss under each sensor location (will meet sensor bottom)
    sensor_h = 12.0
    sensor_foot = 38.0
    support_h = 4.0
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        r = 100.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        boss = cq.Workplane("XY").box(sensor_foot, sensor_foot, support_h, centered=(True, True, False)).translate((x, y, 0))
        lower = lower.union(boss)

    # M3 seam screw clearances (same as v2)
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

    # Overload stop pads (matching v2 locations)
    stop_h = P.total_height_mm - P.overload_stop_gap_mm - 1.0
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = 100 * math.cos(a)
        y = 100 * math.sin(a)
        pad = cq.Workplane("XY").box(18, 12, stop_h, centered=(True, True, False)).translate((x, y, 0))
        lower = lower.union(pad)

    return lower


def _quarter_upper(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0 - P.clearance_gap_mm
    top_z = P.total_height_mm
    upper = _quarter_wedge(r_outer, P.top_plate_thickness_mm, quadrant).translate((0, 0, top_z))

    # top contact bosses under upper plate for each sensor (will meet sensor top)
    sensor_foot = 38.0
    support_h = 6.0
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        r = 100.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        boss = cq.Workplane("XY").box(sensor_foot, sensor_foot, support_h, centered=(True, True, False)).translate((x, y, P.total_height_mm - support_h))
        upper = upper.union(boss)

    # small top ribs for stiffness
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


def platform_v3_full() -> cq.Workplane:
    parts = []
    for q in range(P.segment_count):
        parts.append(quarter_segment(q))

    full = parts[0]
    for p in parts[1:]:
        full = full.union(p)

    # Create sensor placeholder solids between upper and lower plates for visualization
    sensor_h = 12.0
    sensor_foot = 38.0
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        r = 100.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        # place sensor block sitting on lower boss and contacting upper boss
        z = P.bottom_plate_thickness_mm + 2.0
        sensor = cq.Workplane("XY").box(sensor_foot, sensor_foot, sensor_h, centered=(True, True, False)).translate((x, y, z))
        full = full.union(sensor)

    return full


if __name__ == "__main__":
    show_object(platform_v3_full())  # type: ignore[name-defined]
