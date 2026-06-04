"""Platform v1 parametric CAD model for SaltScale.

Creates a circular platform split into 4 quarter segments, with
alignment features and M3 fastening holes. Builds on utilities in
`saltscale_base.py` and `params.py` to remain parametric.
"""
import math
import cadquery as cq
from params import P
from saltscale_base import bottom_segment, top_segment


def platform_compound() -> cq.Workplane:
    """Return a single compound Workplane containing all four segments
    assembled into a full circular platform, with alignment pins and
    M3 fastening holes added on the segment seams.
    """
    # Start with the base segment geometry from saltscale_base
    parts = []
    for q in range(P.segment_count):
        b = bottom_segment(q)
        t = top_segment(q)
        parts.append(b)
        parts.append(t)

    # Union all segment solids into one compound
    full = parts[0]
    for p in parts[1:]:
        full = full.union(p)

    # Add seam fastening holes: two M3 clearance holes per seam near outer rim
    r = P.outer_diameter_mm / 2.0
    hole_d = 3.5  # clearance for M3
    hole_depth = P.total_height_mm + P.top_plate_thickness_mm + 4

    # For each seam (at angles 0,90,180,270) place two holes symmetric across seam
    seams = [0, 90, 180, 270]
    for ang in seams:
        for offset in (-12.0, 12.0):
            a = math.radians(ang + offset)
            x = (r - 18.0) * math.cos(a)
            y = (r - 18.0) * math.sin(a)
            hole = cq.Workplane("XY").circle(hole_d / 2.0).extrude(hole_depth).translate((x, y, 0))
            full = full.cut(hole)

    # Alignment dowel holes (non-through, small pockets) placed at 45,135,225,315
    dowel_d = 4.0
    dowel_depth = 6.0
    for ang in [45, 135, 225, 315]:
        a = math.radians(ang)
        x = (r - 28.0) * math.cos(a)
        y = (r - 28.0) * math.sin(a)
        pocket = cq.Workplane("XY").circle(dowel_d / 2.0).extrude(dowel_depth).translate((x, y, P.bottom_plate_thickness_mm))
        full = full.cut(pocket)

    return full


if __name__ == "__main__":
    show_object(platform_compound())  # type: ignore[name-defined]
