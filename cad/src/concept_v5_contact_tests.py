"""Concept v5 contact test coupons for puck and upper-interface selection."""

import cadquery as cq

from concept_v5_cartridge_scale import ConceptV5Params, P, _engrave_top, _rounded_box


def _puck_body(bottom: cq.Workplane, label: str, p: ConceptV5Params = P) -> cq.Workplane:
    body = cq.Workplane("XY").circle(p.puck_body_diameter_mm / 2.0).extrude(p.puck_body_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm)
    )
    lobe = cq.Workplane("XY").circle(p.puck_lobe_diameter_mm / 2.0).extrude(p.puck_lobe_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm + p.puck_body_height_mm)
    )
    puck = bottom.union(body).union(lobe)
    return _engrave_top(
        puck,
        label,
        -7.0,
        -4.0,
        p.puck_boss_height_mm + p.puck_body_height_mm + p.puck_lobe_height_mm,
        size=4.0,
    )


def bridge_puck_12x24(p: ConceptV5Params = P) -> cq.Workplane:
    """Wide bridge contact matching the current v5 baseline."""
    boss = _rounded_box(12.0, 24.0, p.puck_boss_height_mm, 2.5)
    return _puck_body(boss, "12x24", p)


def bridge_puck_10x22(p: ConceptV5Params = P) -> cq.Workplane:
    """Narrower bridge contact to avoid touching rivets or frame edges."""
    boss = _rounded_box(10.0, 22.0, p.puck_boss_height_mm, 2.2)
    return _puck_body(boss, "10x22", p)


def oval_puck_9x18(p: ConceptV5Params = P) -> cq.Workplane:
    """Oval contact: directional like a bridge, but less sensitive to angle."""
    boss = cq.Workplane("XY").ellipse(4.5, 9.0).extrude(p.puck_boss_height_mm)
    return _puck_body(boss, "9x18", p)


def round_puck_10(p: ConceptV5Params = P) -> cq.Workplane:
    """Round point-ish contact for checking repeatability and centering."""
    boss = cq.Workplane("XY").circle(5.0).extrude(p.puck_boss_height_mm)
    return _puck_body(boss, "D10", p)


def upper_socket_coupon(clearance_mm: float = 0.6, p: ConceptV5Params = P) -> cq.Workplane:
    """Small upper-interface coupon with the same through-socket idea as v5."""
    plate_x = 50.0
    plate_y = 36.0
    plate_z = 6.0
    socket_d = p.puck_lobe_diameter_mm + clearance_mm
    throat_y = 16.0
    throat_x = plate_x / 2.0
    body = _rounded_box(plate_x, plate_y, plate_z, 3.0)
    socket = cq.Workplane("XY").circle(socket_d / 2.0).extrude(plate_z + 0.8).translate((0.0, 0.0, -0.4))
    throat = _rounded_box(throat_x + socket_d / 2.0, throat_y, plate_z + 0.8, 1.0).translate(
        (plate_x / 4.0, 0.0, -0.4)
    )
    body = body.cut(socket).cut(throat)
    label = f"SO {clearance_mm:.1f}".replace(".", "P")
    return _engrave_top(body, label, -18.0, -12.0, plate_z, size=4.0)


def printable_contact_tests(p: ConceptV5Params = P) -> dict[str, cq.Workplane]:
    return {
        "concept_v5_puck_bridge_12x24": bridge_puck_12x24(p),
        "concept_v5_puck_bridge_10x22": bridge_puck_10x22(p),
        "concept_v5_puck_oval_9x18": oval_puck_9x18(p),
        "concept_v5_puck_round_10": round_puck_10(p),
        "concept_v5_upper_socket_clearance_0p4": upper_socket_coupon(0.4, p),
        "concept_v5_upper_socket_clearance_0p8": upper_socket_coupon(0.8, p),
    }
