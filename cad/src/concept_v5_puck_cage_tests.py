"""Puck-capture coupons for the concept v5 upper ring.

The upper cage coupon is modeled in print orientation: the functional underside
faces upward while printing. After printing, flip it over for the mechanical
test. This keeps the captive counterbore support-free.

Physical test note, 2026-06-15:
- 0.20 mm radial clearance was the best hand-tight keyhole variant tested.
- 0.35 mm and 0.50 mm were too loose.
- 0.20 mm did not fall out when inverted, but the puck was still removable by
  hand without meaningful force.
- PETG did not flex enough for the intended side-slide insertion, so this family
  is not yet a validated captive puck interface.
"""

import cadquery as cq

from concept_v5_cartridge_scale import ConceptV5Params, P, _engrave_top, _rounded_box


def loose_captive_puck(p: ConceptV5Params = P) -> cq.Workplane:
    """Puck with separate load shoulder and loose captive head."""
    contact = _rounded_box(10.0, 22.0, 4.8, 2.2)
    shoulder = cq.Workplane("XY").circle(15.0).extrude(2.2).translate((0.0, 0.0, 4.8))
    neck = cq.Workplane("XY").circle(7.0).extrude(2.6).translate((0.0, 0.0, 7.0))
    head = cq.Workplane("XY").circle(11.0).extrude(2.0).translate((0.0, 0.0, 9.6))
    body = contact.union(shoulder).union(neck).union(head)
    return _engrave_top(body, "FLOAT", -7.5, -4.0, 11.6, size=3.3)


def upper_loose_cage_coupon(clearance_mm: float = 1.2, p: ConceptV5Params = P) -> cq.Workplane:
    """Support-free side-entry cage with a loose capture pocket.

    Print orientation:
    - engraved/counterbore side up,
    - flip the part after printing for the actual upper-ring orientation.
    """
    plate_x = 76.0
    plate_y = 52.0
    plate_z = 8.0
    head_d = 22.0
    neck_d = 14.0
    shoulder_d = 30.0
    head_pocket_depth = 2.65
    head_slot_w = head_d + clearance_mm
    neck_slot_w = neck_d + clearance_mm
    entry_x = plate_x / 2.0 + 1.0

    body = _rounded_box(plate_x, plate_y, plate_z, 3.0)

    # Through-slot for the neck. This is deliberately loose; it should locate
    # against the puck shoulder under load, not against the captive head.
    neck_center = cq.Workplane("XY").circle(neck_slot_w / 2.0).extrude(plate_z + 0.8).translate((0.0, 0.0, -0.4))
    neck_entry = _rounded_box(entry_x, neck_slot_w, plate_z + 0.8, 1.0).translate((entry_x / 2.0, 0.0, -0.4))

    # Counterbore for the head, open upward in print orientation.
    head_center = cq.Workplane("XY").circle(head_slot_w / 2.0).extrude(head_pocket_depth + 0.4).translate(
        (0.0, 0.0, plate_z - head_pocket_depth - 0.2)
    )
    head_entry = _rounded_box(entry_x, head_slot_w, head_pocket_depth + 0.4, 1.0).translate(
        (entry_x / 2.0, 0.0, plate_z - head_pocket_depth - 0.2)
    )

    # Shoulder clearance pocket on the functional underside. It prevents the
    # cage lips from taking load before the intended shoulder face does.
    shoulder_relief = cq.Workplane("XY").circle((shoulder_d + 0.8) / 2.0).extrude(0.7).translate(
        (0.0, 0.0, plate_z - 0.6)
    )

    body = body.cut(neck_center).cut(neck_entry).cut(head_center).cut(head_entry).cut(shoulder_relief)

    # A shallow keeper groove at the mouth shows where the non-load-bearing
    # keeper closes the side entry.
    keeper_groove = _rounded_box(3.2, head_slot_w + 3.2, head_pocket_depth + 0.3, 0.6).translate(
        (plate_x / 2.0 - 4.8, 0.0, plate_z - head_pocket_depth - 0.15)
    )
    body = body.cut(keeper_groove)

    rail_y = plate_y / 2.0 - 3.2
    rail = _rounded_box(plate_x - 8.0, 2.6, 1.6, 0.8).translate((0.0, rail_y, plate_z))
    body = body.union(rail).union(_rounded_box(plate_x - 8.0, 2.6, 1.6, 0.8).translate((0.0, -rail_y, plate_z)))

    label = f"CAGE {clearance_mm:.1f}".replace(".", "P")
    return _engrave_top(body, label, -30.0, -19.0, plate_z + 1.6, size=3.8)


def side_entry_keeper(clearance_mm: float = 1.2) -> cq.Workplane:
    """Simple friction keeper for the cage mouth; it is not a load path."""
    head_slot_w = 22.0 + clearance_mm
    keeper = _rounded_box(10.0, head_slot_w + 2.4, 2.35, 0.7)
    keeper = keeper.union(_rounded_box(3.0, head_slot_w + 5.0, 1.2, 0.6).translate((-3.5, 0.0, 2.35)))
    return _engrave_top(keeper, "KEEP", -4.5, -5.0, 3.55, size=2.5)


def _tapered_entry_cut(
    start_x: float,
    end_x: float,
    start_width: float,
    end_width: float,
    height: float,
    z: float,
) -> cq.Workplane:
    points = [
        (start_x, -start_width / 2.0),
        (end_x, -end_width / 2.0),
        (end_x, end_width / 2.0),
        (start_x, start_width / 2.0),
    ]
    return cq.Workplane("XY").polyline(points).close().extrude(height).translate((0.0, 0.0, z))


def upper_hand_tight_keyhole_coupon(
    radial_clearance_mm: float = 0.35,
    vertical_clearance_mm: float = 0.3,
    mouth_clearance_mm: float = 2.2,
    p: ConceptV5Params = P,
) -> cq.Workplane:
    """Side-entry keyhole with a hand-tight captive head pocket.

    The mouth is intentionally wider than the final head pocket. The last part
    of the path is close-fitting so the puck head is retained by light friction
    instead of floating freely in an oversized counterbore.
    """
    plate_x = 78.0
    plate_y = 52.0
    plate_z = 8.0
    neck_d = 14.0
    head_d = 22.0
    head_h = 2.0
    shoulder_d = 30.0
    head_slot_w = head_d + radial_clearance_mm
    neck_slot_w = neck_d + 0.55
    mouth_w = head_d + mouth_clearance_mm
    head_pocket_depth = head_h + vertical_clearance_mm

    body = _rounded_box(plate_x, plate_y, plate_z, 3.0)

    # Through-slot for the neck stays loose; the hand-tight behavior is only in
    # the captive head pocket.
    neck_center = cq.Workplane("XY").circle(neck_slot_w / 2.0).extrude(plate_z + 0.8).translate((0.0, 0.0, -0.4))
    neck_entry = _tapered_entry_cut(0.0, plate_x / 2.0 + 1.0, neck_slot_w, neck_slot_w + 1.8, plate_z + 0.8, -0.4)

    pocket_z = plate_z - head_pocket_depth - 0.1
    pocket_h = head_pocket_depth + 0.5
    head_center = cq.Workplane("XY").circle(head_slot_w / 2.0).extrude(pocket_h).translate((0.0, 0.0, pocket_z))
    straight_start = head_d / 2.0 - 1.4
    taper_start = straight_start + 10.0
    entry_end = plate_x / 2.0 + 1.0
    head_straight = _rounded_box(taper_start - straight_start, head_slot_w, pocket_h, 0.8).translate(
        ((taper_start + straight_start) / 2.0, 0.0, pocket_z)
    )
    head_lead_in = _tapered_entry_cut(taper_start, entry_end, head_slot_w, mouth_w, pocket_h, pocket_z)

    # Functional underside relief for the puck shoulder, so the captured head
    # does not become the load path.
    shoulder_relief = cq.Workplane("XY").circle((shoulder_d + 0.9) / 2.0).extrude(0.75).translate(
        (0.0, 0.0, plate_z - 0.7)
    )

    body = body.cut(neck_center).cut(neck_entry).cut(head_center).cut(head_straight).cut(head_lead_in).cut(shoulder_relief)

    rail_y = plate_y / 2.0 - 3.2
    rail = _rounded_box(plate_x - 8.0, 2.6, 1.6, 0.8).translate((0.0, rail_y, plate_z))
    body = body.union(rail).union(_rounded_box(plate_x - 8.0, 2.6, 1.6, 0.8).translate((0.0, -rail_y, plate_z)))

    label = f"HT {radial_clearance_mm:.2f}".replace(".", "P")
    return _engrave_top(body, label, -33.0, -19.0, plate_z + 1.6, size=3.5)


def printable_hand_tight_keyhole_tests(p: ConceptV5Params = P) -> dict[str, cq.Workplane]:
    return {
        "concept_v5_hand_tight_puck": loose_captive_puck(p),
        "concept_v5_upper_keyhole_handtight_0p20": upper_hand_tight_keyhole_coupon(0.20, 0.30, 2.2, p),
        "concept_v5_upper_keyhole_handtight_0p35": upper_hand_tight_keyhole_coupon(0.35, 0.30, 2.2, p),
        "concept_v5_upper_keyhole_handtight_0p50": upper_hand_tight_keyhole_coupon(0.50, 0.30, 2.2, p),
    }


def printable_puck_cage_tests(p: ConceptV5Params = P) -> dict[str, cq.Workplane]:
    return {
        "concept_v5_loose_captive_puck": loose_captive_puck(p),
        "concept_v5_upper_loose_cage_1p2": upper_loose_cage_coupon(1.2, p),
        "concept_v5_side_entry_keeper_1p2": side_entry_keeper(1.2),
    }
