"""Parametric SaltScale mechanical prototype.

This is intentionally a first solid CAD target, not a cosmetic final model.
The geometry focuses on:
- round four-piece printable base/top segments
- central loadcell cavity and screw-hole references
- electronics bay placeholders
- tank-centering lip

All exact loadcell dimensions must be verified against the purchased datasheet.
"""
import math
import cadquery as cq
from params import P


def _quarter_wedge(radius: float, height: float, quadrant: int) -> cq.Workplane:
    """Create one 90-degree wedge as a prism on XY, extruded in Z."""
    start = quadrant * 90
    end = start + 90
    pts = [(0, 0)]
    steps = 24
    for i in range(steps + 1):
        a = math.radians(start + (end - start) * i / steps)
        pts.append((radius * math.cos(a), radius * math.sin(a)))
    return cq.Workplane("XY").polyline(pts).close().extrude(height)


def bottom_segment(quadrant: int = 0) -> cq.Workplane:
    r = P.outer_diameter_mm / 2
    body = _quarter_wedge(r, P.bottom_plate_thickness_mm, quadrant)

    # Raise outer wall as protective skirt, leaving center clear for loadcell hardware.
    outer_wall = _quarter_wedge(r, P.total_height_mm, quadrant)
    inner_cut = cq.Workplane("XY").circle(r - P.wall_thickness_mm).extrude(P.total_height_mm + 2)
    wall = outer_wall.cut(inner_cut)
    body = body.union(wall)

    # Central loadcell clearance pocket reference, kept in each segment to support export/alignment.
    # This cut intentionally crosses segment boundaries; final assembly uses all quadrants.
    pocket = (
        cq.Workplane("XY")
        .box(P.loadcell_length_mm + 18, P.loadcell_width_mm + 18, P.loadcell_height_mm + 8, centered=(True, True, False))
        .translate((0, 0, P.bottom_plate_thickness_mm))
    )
    body = body.cut(pocket)

    # Overload stop pads: present in base, with nominal 1 mm gap to top platform.
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = 112 * math.cos(a)
        y = 112 * math.sin(a)
        pad = (
            cq.Workplane("XY")
            .box(14, 14, P.total_height_mm - P.overload_stop_gap_mm, centered=(True, True, False))
            .translate((x, y, 0))
        )
        body = body.union(pad)

    # Side electronics bay placeholder only on quadrant 0.
    if quadrant == 0:
        bay = (
            cq.Workplane("XY")
            .box(P.electronics_bay_width_mm, P.electronics_bay_depth_mm, P.electronics_bay_height_mm, centered=(True, True, False))
            .translate((92, 92, P.bottom_plate_thickness_mm))
        )
        body = body.cut(bay)

        # Button and LED holes on the arc-facing side, approximate placeholders.
        button = cq.Workplane("YZ").circle(P.button_hole_diameter_mm / 2).extrude(20).translate((150, 92, 22))
        led = cq.Workplane("YZ").circle(P.led_hole_diameter_mm / 2).extrude(20).translate((150, 116, 22))
        body = body.cut(button).cut(led)

    return body


def top_segment(quadrant: int = 0) -> cq.Workplane:
    r = P.outer_diameter_mm / 2 - P.clearance_gap_mm
    body = _quarter_wedge(r, P.top_plate_thickness_mm, quadrant).translate((0, 0, P.total_height_mm))

    # Centering lip on top surface.
    lip_outer_r = (P.centering_lip_inner_diameter_mm / 2) + P.wall_thickness_mm
    lip_inner_r = P.centering_lip_inner_diameter_mm / 2
    lip = _quarter_wedge(lip_outer_r, P.centering_lip_height_mm, quadrant).translate((0, 0, P.total_height_mm + P.top_plate_thickness_mm))
    lip_cut = cq.Workplane("XY").circle(lip_inner_r).extrude(P.centering_lip_height_mm + 2).translate((0, 0, P.total_height_mm + P.top_plate_thickness_mm - 1))
    body = body.union(lip.cut(lip_cut))

    # Central loadcell top mount pad/reference.
    pad = (
        cq.Workplane("XY")
        .box(70, 48, 8, centered=(True, True, False))
        .translate((0, 0, P.total_height_mm - 8))
    )
    body = body.union(pad)

    return body


def assembly_preview() -> cq.Assembly:
    assy = cq.Assembly(name="SaltScale v1 round base")
    for q in range(P.segment_count):
        assy.add(bottom_segment(q), name=f"bottom_segment_{q}")
        assy.add(top_segment(q), name=f"top_segment_{q}")
    # Loadcell reference block
    lc = cq.Workplane("XY").box(P.loadcell_length_mm, P.loadcell_width_mm, P.loadcell_height_mm, centered=(True, True, False)).translate((0, 0, P.bottom_plate_thickness_mm))
    assy.add(lc, name=P.loadcell_model)
    return assy


if __name__ == "__main__":
    show_object(assembly_preview())  # type: ignore[name-defined]
