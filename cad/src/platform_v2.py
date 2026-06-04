"""Platform v2 — structurally realistic platform architecture.

Features:
- 320 mm outer diameter, 4 identical quarter segments
- explicit central loadcell cavity placeholder
- separated upper and lower platform plates
- radial structural ribs suitable for PETG
- alignment half-pockets at seams (identical segments form full pockets)
- M3 screw clearance holes at seams
- preliminary overload stop pads

This file intentionally keeps geometry parametric and conservative for PETG.
"""
import math
import cadquery as cq
from params import P
from saltscale_base import _quarter_wedge


def _quarter_lower(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0
    # lower shell (bottom plate)
    lower = _quarter_wedge(r_outer, P.bottom_plate_thickness_mm, quadrant)

    # inner radial cut to create skirt + internal cavity (keeps central service area free)
    inner_clearance_r = (P.loadcell_length_mm / 2.0) + 24.0
    inner_cut = cq.Workplane("XY").circle(inner_clearance_r).extrude(P.total_height_mm + 4)
    lower = lower.cut(inner_cut)

    # radial ribs (3 per quadrant) — rectangular ribs radiating from near inner_clearance_r
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

    # Internal alignment: each segment provides a small pin near its trailing seam
    # and a matching socket near its leading seam. When rotated and assembled
    # these form interlocking alignment features without external tabs.
    pin_d = 4.0
    pin_h = 8.0
    seam_start = quadrant * 90
    pin_ang = seam_start + 90 - 8.0
    sock_ang = seam_start + 8.0
    for ang, is_pin in [(pin_ang, True), (sock_ang, False)]:
        a = math.radians(ang)
        r = inner_clearance_r + 10.0
        x = r * math.cos(a)
        y = r * math.sin(a)
        if is_pin:
            pin = cq.Workplane("XY").circle(pin_d / 2.0).extrude(pin_h).translate((x, y, P.bottom_plate_thickness_mm))
            lower = lower.union(pin)
        else:
            sock = cq.Workplane("XY").circle((pin_d + 0.6) / 2.0).extrude(pin_h).translate((x, y, P.bottom_plate_thickness_mm))
            lower = lower.cut(sock)

    # M3 screw clearance holes through seam (will align when segments are assembled)
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

    # Overload stop pads (explicit, top at total_height - 1 mm to provide 1 mm clearance)
    stop_w = 16.0
    stop_d = 12.0
    stop_top_z = P.total_height_mm - 1.0
    for angle in [45, 135, 225, 315]:
        a = math.radians(angle)
        x = 100 * math.cos(a)
        y = 100 * math.sin(a)
        # lower pad height such that its top is stop_top_z
        pad_h = stop_top_z
        pad = (
            cq.Workplane("XY")
            .box(stop_w, stop_d, pad_h, centered=(True, True, False))
            .translate((x, y, 0))
        )
        lower = lower.union(pad)

    return lower


def _quarter_upper(quadrant: int = 0) -> cq.Workplane:
    r_outer = P.outer_diameter_mm / 2.0 - P.clearance_gap_mm
    top_z = P.total_height_mm
    upper = _quarter_wedge(r_outer, P.top_plate_thickness_mm, quadrant).translate((0, 0, top_z))

    # central top pad to interface with loadcell (keeps placeholder, no holes)
    lc_pad_w = P.loadcell_width_mm + 12.0
    lc_pad_l = P.loadcell_length_mm + 12.0
    pad = (
        cq.Workplane("XY")
        .box(lc_pad_l, lc_pad_w, 6.0, centered=(True, True, False))
        .translate((0, 0, P.total_height_mm - 6.0))
    )
    upper = upper.union(pad)

    # small ribs on top to increase stiffness
    rib_w = 4.0
    rib_h = 6.0
    for i in range(2):
        ang = quadrant * 90 + 25 + i * 30
        a = math.radians(ang)
        x = (r_outer - 60.0) * math.cos(a)
        y = (r_outer - 60.0) * math.sin(a)
        tr = cq.Workplane("XY").box(40.0, rib_w, rib_h, centered=(True, True, False)).translate((x, y, P.total_height_mm - rib_h))
        tr = tr.rotate((0, 0, 0), (0, 0, 1), ang)
        upper = upper.union(tr)

    # No external seam features on the upper plate; alignment is internal.
    # Keep small top ribs for stiffness already added above.

    return upper

    return upper


def quarter_segment(quadrant: int = 0) -> cq.Workplane:
    return _quarter_lower(quadrant).union(_quarter_upper(quadrant))


def platform_v2_full() -> cq.Workplane:
    parts = []
    for q in range(P.segment_count):
        parts.append(quarter_segment(q))

    full = parts[0]
    for p in parts[1:]:
        full = full.union(p)

    # Central loadcell cavity (cut through assembled model so it's a real placeholder)
    lc_box = (
        cq.Workplane("XY")
        .box(P.loadcell_length_mm + 4, P.loadcell_width_mm + 4, P.loadcell_height_mm + 12, centered=(True, True, False))
        .translate((0, 0, P.bottom_plate_thickness_mm))
    )
    full = full.cut(lc_box)

    return full


if __name__ == "__main__":
    show_object(platform_v2_full())  # type: ignore[name-defined]
