"""Concept v4 upper pad positioning validation coupons.

These coupons compare cleaner alternatives to the current concept_v4 upper-pad
boss/socket through the upper carrier. They do not modify the full concept_v4
assembly.
"""

import cadquery as cq

from concept_v2 import ConceptV2Params, _engrave_top, lower_pad, sensor_placeholder
from concept_v4_integrated_joining import P

PAD_SIZE_MM = P.upper_pad_size_mm
PAD_HEIGHT_MM = P.upper_pad_height_mm
SENSOR_SIZE_MM = P.sensor_size_mm
SENSOR_HEIGHT_MM = P.sensor_height_mm
SENSOR_RELATIVE_CLEARANCE_PER_SIDE_MM = 0.5
CARRIER_POCKET_CLEARANCE_PER_SIDE_MM = 0.4
LOCATOR_HEIGHT_MM = 1.2
LOCATOR_WALL_MM = 2.2
POCKET_RIM_HEIGHT_MM = 1.2
PLATE_THICKNESS_MM = 4.0


def _label(body: cq.Workplane, text: str, x: float, y: float, z: float, size: float = 7.0) -> cq.Workplane:
    return _engrave_top(body, text, x, y, z, size=size, p=P)


def _sensor_dummy_print() -> cq.Workplane:
    body = sensor_placeholder(P)
    body = _label(body, "SENSOR", -6.0, 0.0, SENSOR_HEIGHT_MM, 5.5)
    return body


def _upper_pad_base() -> cq.Workplane:
    return cq.Workplane("XY").box(PAD_SIZE_MM, PAD_SIZE_MM, PAD_HEIGHT_MM, centered=(True, True, False))


def _sensor_relative_upper_pad_print() -> cq.Workplane:
    """Upper pad printed with underside locator features facing upward.

    The four broken locator tabs represent shallow underside features that would
    surround the top of the sensor after the printed pad is flipped for use.
    """
    pad = _upper_pad_base()
    cavity = SENSOR_SIZE_MM + 2.0 * SENSOR_RELATIVE_CLEARANCE_PER_SIDE_MM
    offset = cavity / 2.0 + LOCATOR_WALL_MM / 2.0
    tab_len = 18.0
    z = PAD_HEIGHT_MM
    tabs = [
        cq.Workplane("XY").box(LOCATOR_WALL_MM, tab_len, LOCATOR_HEIGHT_MM, centered=(True, True, False)).translate((offset, 0.0, z)),
        cq.Workplane("XY").box(LOCATOR_WALL_MM, tab_len, LOCATOR_HEIGHT_MM, centered=(True, True, False)).translate((-offset, 0.0, z)),
        cq.Workplane("XY").box(tab_len, LOCATOR_WALL_MM, LOCATOR_HEIGHT_MM, centered=(True, True, False)).translate((0.0, offset, z)),
        cq.Workplane("XY").box(tab_len, LOCATOR_WALL_MM, LOCATOR_HEIGHT_MM, centered=(True, True, False)).translate((0.0, -offset, z)),
    ]
    for tab in tabs:
        pad = pad.union(tab)
    pad = _label(pad, "PAD", -15.0, -20.0, PAD_HEIGHT_MM + LOCATOR_HEIGHT_MM, 7.0)
    pad = _label(pad, "0.5", 13.0, -20.0, PAD_HEIGHT_MM + LOCATOR_HEIGHT_MM, 6.0)
    return pad


def concept_v4_upper_pad_sensor_relative_test_v1(p: ConceptV2Params = P) -> cq.Workplane:
    base = cq.Workplane("XY").box(122.0, 70.0, 1.6, centered=(True, True, False))
    base = _label(base, "SENSOR REL", -44.0, 20.0, 1.6, 6.0)
    sensor = _sensor_dummy_print().translate((-32.0, 0.0, 1.6))
    pad = _sensor_relative_upper_pad_print().translate((36.0, 0.0, 1.6))
    return base.union(sensor).union(pad)


def _carrier_pocket_reference() -> cq.Workplane:
    """Small carrier reference with one open underside-pocket concept.

    This prints pocket-side-up as a validation coupon. It deliberately avoids a
    through-hole, but the raised rim represents the carrier-side locating walls.
    """
    plate = cq.Workplane("XY").box(74.0, 74.0, PLATE_THICKNESS_MM, centered=(True, True, False))
    pocket = PAD_SIZE_MM + 2.0 * CARRIER_POCKET_CLEARANCE_PER_SIDE_MM
    offset = pocket / 2.0 + LOCATOR_WALL_MM / 2.0
    tab_len = 28.0
    z = PLATE_THICKNESS_MM
    rims = [
        cq.Workplane("XY").box(LOCATOR_WALL_MM, tab_len, POCKET_RIM_HEIGHT_MM, centered=(True, True, False)).translate((offset, 0.0, z)),
        cq.Workplane("XY").box(LOCATOR_WALL_MM, tab_len, POCKET_RIM_HEIGHT_MM, centered=(True, True, False)).translate((-offset, 0.0, z)),
        cq.Workplane("XY").box(tab_len, LOCATOR_WALL_MM, POCKET_RIM_HEIGHT_MM, centered=(True, True, False)).translate((0.0, offset, z)),
        cq.Workplane("XY").box(tab_len, LOCATOR_WALL_MM, POCKET_RIM_HEIGHT_MM, centered=(True, True, False)).translate((0.0, -offset, z)),
    ]
    for rim in rims:
        plate = plate.union(rim)
    plate = _label(plate, "CARR", -18.0, 23.0, PLATE_THICKNESS_MM + POCKET_RIM_HEIGHT_MM, 6.0)
    plate = _label(plate, "0.4", 18.0, 23.0, PLATE_THICKNESS_MM + POCKET_RIM_HEIGHT_MM, 6.0)
    return plate


def _plain_upper_pad_print() -> cq.Workplane:
    pad = _upper_pad_base()
    pad = _label(pad, "PAD", -10.0, 0.0, PAD_HEIGHT_MM, 7.0)
    return pad


def concept_v4_upper_pad_carrier_pocket_test_v1(p: ConceptV2Params = P) -> cq.Workplane:
    base = cq.Workplane("XY").box(152.0, 82.0, 1.6, centered=(True, True, False))
    base = _label(base, "CARRIER", -58.0, 28.0, 1.6, 6.0)
    carrier = _carrier_pocket_reference().translate((-38.0, 0.0, 1.6))
    pad = _plain_upper_pad_print().translate((42.0, 0.0, 1.6))
    sensor = _sensor_dummy_print().translate((42.0, 0.0, 1.6 + PAD_HEIGHT_MM + 6.0))
    return base.union(carrier).union(pad).union(sensor)


def upper_pad_positioning_coupon_exports() -> dict[str, cq.Workplane]:
    return {
        "concept_v4_upper_pad_sensor_relative_test_v1": concept_v4_upper_pad_sensor_relative_test_v1(),
        "concept_v4_upper_pad_carrier_pocket_test_v1": concept_v4_upper_pad_carrier_pocket_test_v1(),
    }
