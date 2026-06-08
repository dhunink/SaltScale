"""Support-free upper-carrier pocket alternatives for concept_v4.

These are validation/display coupons only. They do not modify the active
concept_v4 assembly. Each option is carrier-relative, uses a removable upper
pad, avoids through-holes, avoids small locator tabs, and is arranged to print
with the pocket open upward without supports.
"""

import cadquery as cq

from concept_v2 import _engrave_top
from concept_v4_integrated_joining import P

PLATE_Z = 5.0
PAD_Z = P.upper_pad_height_mm
CLEARANCE = 0.45
ENGRAVE_Z = PLATE_Z


def _label(body: cq.Workplane, text: str, x: float, y: float, z: float, size: float = 7.0) -> cq.Workplane:
    return _engrave_top(body, text, x, y, z, size=size, p=P)


def _square_pad(size: float = 50.0) -> cq.Workplane:
    return cq.Workplane("XY").box(size, size, PAD_Z, centered=(True, True, False))


def _round_pad(diameter: float = 50.0) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(PAD_Z)


def chamfered_square_pocket_v1() -> cq.Workplane:
    """Broad square pocket with chamfer-like stepped lead-in."""
    plate = cq.Workplane("XY").box(78.0, 78.0, PLATE_Z, centered=(True, True, False))
    outer = cq.Workplane("XY").box(58.0, 58.0, 1.0, centered=(True, True, False)).translate((0, 0, PLATE_Z - 1.0))
    inner = cq.Workplane("XY").box(51.0, 51.0, 1.3, centered=(True, True, False)).translate((0, 0, PLATE_Z - 1.3))
    plate = plate.cut(outer).cut(inner)
    plate = _label(plate, "SQ", -26.0, 27.0, PLATE_Z, 8.0)
    plate = _label(plate, "0.45", 11.0, 27.0, PLATE_Z, 6.0)
    pad = _square_pad(50.0).translate((92.0, 0.0, 0.0))
    pad = _label(pad, "PAD", 82.0, -19.0, PAD_Z, 7.0)
    return plate.union(pad)


def round_cup_pocket_v1() -> cq.Workplane:
    """Round shallow cup, tolerant of rotation and easy to wipe clean."""
    plate = cq.Workplane("XY").box(78.0, 78.0, PLATE_Z, centered=(True, True, False))
    outer = cq.Workplane("XY").circle(30.0).extrude(1.0).translate((0, 0, PLATE_Z - 1.0))
    inner = cq.Workplane("XY").circle(25.45).extrude(1.3).translate((0, 0, PLATE_Z - 1.3))
    plate = plate.cut(outer).cut(inner)
    plate = _label(plate, "ROUND", -30.0, 27.0, PLATE_Z, 6.0)
    pad = _round_pad(50.0).translate((92.0, 0.0, 0.0))
    pad = _label(pad, "PAD", 82.0, -19.0, PAD_Z, 7.0)
    return plate.union(pad)


def side_entry_saddle_pocket_v1() -> cq.Workplane:
    """Open-sided saddle pocket, inserted from outside, no closed debris box."""
    plate = cq.Workplane("XY").box(92.0, 78.0, PLATE_Z, centered=(True, True, False))
    # Wide open slot from the outside edge. The retained three-sided pocket is
    # broad, not a cluster of small tabs.
    slot = cq.Workplane("XY").box(78.0, 53.0, 1.3, centered=(True, True, False)).translate((18.0, 0.0, PLATE_Z - 1.3))
    lead = cq.Workplane("XY").box(86.0, 59.0, 0.8, centered=(True, True, False)).translate((22.0, 0.0, PLATE_Z - 0.8))
    plate = plate.cut(lead).cut(slot)
    plate = _label(plate, "OPEN", -34.0, 27.0, PLATE_Z, 6.5)
    plate = _label(plate, "OUT", 20.0, 27.0, PLATE_Z, 7.0)
    pad = _square_pad(50.0).translate((106.0, 0.0, 0.0))
    pad = _label(pad, "PAD", 96.0, -19.0, PAD_Z, 7.0)
    return plate.union(pad)


def pocket_alternative_exports() -> dict[str, cq.Workplane]:
    return {
        "concept_v4_upper_pad_pocket_chamfer_square_v1": chamfered_square_pocket_v1(),
        "concept_v4_upper_pad_pocket_round_cup_v1": round_cup_pocket_v1(),
        "concept_v4_upper_pad_pocket_side_entry_v1": side_entry_saddle_pocket_v1(),
    }
