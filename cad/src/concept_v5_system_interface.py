"""Concept v5 whole-system interface coupons.

These coupons focus on the contract between upper ring, captive puck, and lower
sensor station. They are intentionally smaller than a full quadrant assembly.

Physical test note, 2026-06-15: the side-entry keyhole puck concept is not
validated. The best tested fit was 0.20 mm radial clearance, which stayed in
place when inverted but was still easy to remove by hand; PETG did not flex
enough for the intended slide-in behavior.
"""

import cadquery as cq

from concept_v5_cartridge_scale import ConceptV5Params, P, _engrave_top, _rounded_box


def captive_bridge_puck_10x22(p: ConceptV5Params = P) -> cq.Workplane:
    """Puck intended to be lightly captive in a support-free upper T-slot."""
    contact = _rounded_box(10.0, 22.0, p.puck_boss_height_mm, 2.2)
    shoulder_h = 2.6
    neck_d = 14.0
    neck_h = 2.2
    head_d = 22.0
    head_h = 2.0
    shoulder = cq.Workplane("XY").circle(15.0).extrude(shoulder_h).translate((0.0, 0.0, p.puck_boss_height_mm))
    neck = cq.Workplane("XY").circle(neck_d / 2.0).extrude(neck_h).translate(
        (0.0, 0.0, p.puck_boss_height_mm + shoulder_h)
    )
    head = cq.Workplane("XY").circle(head_d / 2.0).extrude(head_h).translate(
        (0.0, 0.0, p.puck_boss_height_mm + shoulder_h + neck_h)
    )
    puck = contact.union(shoulder).union(neck).union(head)
    return _engrave_top(puck, "CAPT", -7.0, -4.0, p.puck_boss_height_mm + shoulder_h + neck_h + head_h, size=4.0)


def upper_captive_keyhole_coupon(clearance_mm: float = 0.5, p: ConceptV5Params = P) -> cq.Workplane:
    """Upper-ring T-slot coupon: side-entry, support-free, lightly captive.

    Print with the engraved side up. The wide pocket is open upward during
    printing; the narrower through-slot captures the puck head during use.
    """
    plate_x = 70.0
    plate_y = 46.0
    plate_z = 8.0
    entry_side_x = plate_x / 2.0 + 1.0
    neck_d = 14.0
    head_d = 22.0
    head_h = 2.0
    head_pocket_depth = head_h + 0.45
    neck_slot_w = neck_d + clearance_mm
    head_slot_w = head_d + clearance_mm

    body = _rounded_box(plate_x, plate_y, plate_z, 3.0)

    neck_center = cq.Workplane("XY").circle(neck_slot_w / 2.0).extrude(plate_z + 0.8).translate((0.0, 0.0, -0.4))
    neck_entry = _rounded_box(entry_side_x, neck_slot_w, plate_z + 0.8, 1.0).translate((entry_side_x / 2.0, 0.0, -0.4))

    head_center = cq.Workplane("XY").circle(head_slot_w / 2.0).extrude(head_pocket_depth + 0.4).translate(
        (0.0, 0.0, plate_z - head_pocket_depth - 0.2)
    )
    head_entry = _rounded_box(entry_side_x, head_slot_w, head_pocket_depth + 0.4, 1.0).translate(
        (entry_side_x / 2.0, 0.0, plate_z - head_pocket_depth - 0.2)
    )

    body = body.cut(neck_center).cut(neck_entry).cut(head_center).cut(head_entry)

    # Small side rails make the coupon feel more like the future upper ring:
    # it is a stiff load path, not a loose washer around the puck.
    rail_y = plate_y / 2.0 - 3.5
    rail = _rounded_box(plate_x - 8.0, 3.0, 2.0, 1.0).translate((0.0, rail_y, plate_z))
    body = body.union(rail).union(_rounded_box(plate_x - 8.0, 3.0, 2.0, 1.0).translate((0.0, -rail_y, plate_z)))

    label = f"KEY {clearance_mm:.1f}".replace(".", "P")
    return _engrave_top(body, label, -26.0, -17.0, plate_z + 2.0, size=4.0)


def upper_lower_interface_preview(p: ConceptV5Params = P) -> cq.Assembly:
    """Small visual stack showing upper coupon and captive puck relation."""
    assembly = cq.Assembly(name="concept_v5_upper_puck_interface")
    upper = upper_captive_keyhole_coupon(0.5, p)
    puck = captive_bridge_puck_10x22(p).translate((0.0, 0.0, -p.puck_boss_height_mm - 2.6))
    assembly.add(upper, name="upper_keyhole_coupon")
    assembly.add(puck, name="captive_puck")
    return assembly


def printable_system_interface_tests(p: ConceptV5Params = P) -> dict[str, cq.Workplane]:
    return {
        "concept_v5_captive_puck_bridge_10x22": captive_bridge_puck_10x22(p),
        "concept_v5_upper_keyhole_clearance_0p4": upper_captive_keyhole_coupon(0.4, p),
        "concept_v5_upper_keyhole_clearance_0p8": upper_captive_keyhole_coupon(0.8, p),
    }
