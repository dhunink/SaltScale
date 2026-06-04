"""Platform v5 — segmented printable platform using sensor_module_v3.

Splits the round platform into four printable quarter segments. Each segment
contains exactly one `sensor_module_v3` assembly positioned wholly inside the
segment. Adds alignment pins/sockets and M3 seam screw clearances while
preserving sensor force paths and overload stops.
"""
import math
import cadquery as cq
from params import P
from saltscale_base import _quarter_wedge
from sensor_module_v3 import sensor_module_v3


def platform_v5_segment(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0
    lower = _quarter_wedge(r_outer, P.bottom_plate_thickness_mm, quadrant)

    # Keep stiffness ribs similar to earlier versions
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

    # seam screw clearances (reuse the same pattern as base)
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

    # Add alignment features on the two seams bounding this quadrant.
    # Even quadrants get male pins; odd quadrants get mating sockets.
    pin_r = 2.0
    pin_h = 8.0
    # seam angles for this quadrant: start and end
    start_ang = quadrant * 90
    end_ang = start_ang + 90
    for seam_ang, is_start in ((start_ang, True), (end_ang, False)):
        a = math.radians(seam_ang)
        r_pos = r_outer - 8.0
        x = r_pos * math.cos(a)
        y = r_pos * math.sin(a)
        if quadrant % 2 == 0:
            # make a peg on even quadrants
            peg = cq.Workplane("XY").circle(pin_r).extrude(pin_h).translate((x, y, P.bottom_plate_thickness_mm))
            lower = lower.union(peg)
        else:
            # make a receiving hole (slightly larger) on odd quadrants
            hole = cq.Workplane("XY").circle(pin_r * 1.2).extrude(P.bottom_plate_thickness_mm + 2).translate((x, y, 0))
            lower = lower.cut(hole)

    # Do not create sensor-support bosses here; insert full sensor_module_v3 inside this segment
    # Determine the sensor angle that belongs to this quadrant (center of quadrant)
    sensor_angle = quadrant * 90 + 45
    a = math.radians(sensor_angle)
    r_sensor = 100.0
    sx = r_sensor * math.cos(a)
    sy = r_sensor * math.sin(a)

    # sensor_module_v3 returns: base_with_cut, lower_pad, sensor_placeholder, upper_pad, assembly
    base_mod, lower_pad, sensor_ph, upper_pad, assembly = sensor_module_v3()

    # translate the module assembly into the segment so it sits wholly inside this quadrant
    placed_module = assembly.translate((sx, sy, 0))

    # Ensure we do not create any new top->bottom bridges: module design contains overload stops
    seg = lower.union(placed_module)

    return seg


def platform_v5_assembly() -> cq.Workplane:
    parts = []
    for q in range(P.segment_count):
        parts.append(platform_v5_segment(q))

    full = parts[0]
    for p in parts[1:]:
        full = full.union(p)

    return full


if __name__ == "__main__":
    show_object(platform_v5_assembly())  # type: ignore[name-defined]
