"""Compact 1:1 practical validation prints for SaltScale concept_v2.

These are not scaled-down parts. They crop away surrounding ring geometry while
keeping real interface dimensions, clearances, M3 holes, nut pockets, grate-tab
fits, and sensor-locator geometry.
"""

from dataclasses import dataclass

import cadquery as cq

from concept_v2 import P, ConceptV2Params
from concept_v2_bolted_joinery_coupons import BJP, BoltedJoineryParams
from concept_v2_sensor_station_v3 import _locator_features, _overload_stops
from label_readability_coupon import label_readability_coupon_v1


LABEL_DEPTH_MM = 0.8
LABEL_SIZE_MM = 7.0


@dataclass(frozen=True)
class PracticalParams:
    sensor_base_size_mm: float = 86.0
    support_slot_len_mm: float = 44.0
    support_slot_block_len_mm: float = 58.0
    support_slot_block_width_mm: float = 32.0
    support_slot_depth_mm: float = 4.2
    support_tab_len_mm: float = 44.0


PP = PracticalParams()


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _cylinder_cut(diameter: float, height: float, x: float, y: float, z0: float) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(height).translate((x, y, z0))


def _hex_cut(across_flats: float, depth: float, x: float, y: float, z0: float) -> cq.Workplane:
    import math

    diameter = 2.0 * across_flats / math.sqrt(3.0)
    return (
        cq.Workplane("XY")
        .polygon(6, diameter)
        .extrude(depth)
        .rotate((0, 0, 0), (0, 0, 1), 30)
        .translate((x, y, z0))
    )


def _compound(parts: list[cq.Workplane]) -> cq.Compound:
    return cq.Compound.makeCompound([part.val() for part in parts])


def _engrave(part: cq.Workplane, label: str, x: float, y: float, z: float, size: float = LABEL_SIZE_MM) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    return part.cut(text.translate((x, y, 0.0)))


def test_label_readability_v1() -> cq.Workplane:
    return label_readability_coupon_v1()


def _captured_nut_block(
    block_x: float,
    block_y: float,
    label: str,
    thickness: float = 8.0,
    b: BoltedJoineryParams = BJP,
) -> cq.Workplane:
    block = _box(block_x, block_y, thickness)
    block = block.cut(_cylinder_cut(b.m3_clearance_diameter_mm, thickness + 0.4, 0.0, 0.0, -0.2))
    block = block.cut(
        _hex_cut(
            b.captured_nut_across_flats_mm,
            b.captured_nut_pocket_depth_mm,
            0.0,
            0.0,
            b.captured_nut_lip_depth_mm,
        )
    )
    block = block.cut(
        _hex_cut(
            b.captured_nut_lip_across_flats_mm,
            b.captured_nut_lip_depth_mm + 0.15,
            0.0,
            0.0,
            -0.05,
        )
    )
    return _engrave(block, label, 0.0, block_y / 2.0 - 7.0, thickness)


def _single_bridge_plate(width: float, depth: float, hole_ys: tuple[float, ...], z: float = 0.0) -> cq.Workplane:
    plate = _box(width, depth, BJP.bridge_height_mm, z0=z)
    for y in hole_ys:
        plate = plate.cut(_cylinder_cut(BJP.m3_clearance_diameter_mm, BJP.bridge_height_mm + 0.4, 0.0, y, z - 0.2))
    plate = _engrave(plate, "BRIDGE", 0.0, depth / 2.0 - 8.0, z + BJP.bridge_height_mm, size=6.4)
    plate = _engrave(plate, "M3", 0.0, -depth / 2.0 + 8.0, z + BJP.bridge_height_mm)
    return plate


def test_m3_captured_nut_v1() -> cq.Compound:
    nut_block = _captured_nut_block(34.0, 28.0, "NUT").translate((-24.0, 0.0, 0.0))
    bridge = _single_bridge_plate(34.0, 24.0, (0.0,)).translate((24.0, 0.0, 0.0))
    return _compound([nut_block, bridge])


def _support_slot_pair(clearance: float, x: float, y: float, p: ConceptV2Params = P, pp: PracticalParams = PP) -> list[cq.Workplane]:
    slot_width = p.grate_arm_width_mm + 2.0 * clearance
    slot = _box(pp.support_slot_block_len_mm, pp.support_slot_block_width_mm, p.upper_thickness_mm, x, y)
    cut = _box(
        pp.support_slot_len_mm,
        slot_width,
        pp.support_slot_depth_mm + 0.3,
        x - 4.0,
        y,
        p.upper_thickness_mm - pp.support_slot_depth_mm,
    )
    slot = slot.cut(cut)
    slot = _engrave(slot, "SLOT", x - 15.0, y + 10.0, p.upper_thickness_mm, size=5.8)
    slot = _engrave(slot, f"{clearance:.1f}", x + 16.0, y + 10.0, p.upper_thickness_mm, size=6.6)

    tab = _box(pp.support_tab_len_mm, p.grate_arm_width_mm, p.grate_thickness_mm, x + 66.0, y)
    tab = _engrave(tab, "TAB", x + 66.0, y + 5.5, p.grate_thickness_mm, size=6.6)
    tab = _engrave(tab, f"{clearance:.1f}", x + 66.0, y - 7.0, p.grate_thickness_mm, size=6.6)
    return [slot, tab]


def test_support_grate_fit_v1() -> cq.Compound:
    parts: list[cq.Workplane] = []
    for clearance, y in ((0.4, 43.0), (0.6, 0.0), (0.8, -43.0)):
        parts.extend(_support_slot_pair(clearance, -38.0, y))
    return _compound(parts)


def _sensor_dummy(p: ConceptV2Params = P) -> cq.Workplane:
    body = _box(p.sensor_size_mm, p.sensor_size_mm, p.sensor_height_mm)
    cable = _box(16.0, 4.0, 2.0, p.sensor_size_mm / 2.0 + 8.0, 0.0, 4.0)
    sensor = body.union(cable)
    return _engrave(sensor, "SENSOR", 0.0, 0.0, p.sensor_height_mm, size=5.8)


def _pad(size: float, height: float, label: str) -> cq.Workplane:
    return _engrave(_box(size, size, height), label, 0.0, 0.0, height, size=5.6)


def test_sensor_locator_v3_fit_v1(p: ConceptV2Params = P, pp: PracticalParams = PP) -> cq.Compound:
    base = _box(pp.sensor_base_size_mm, pp.sensor_base_size_mm, p.lower_thickness_mm)
    base = base.union(_locator_features(p)).union(_overload_stops(p))
    base = _engrave(base, "OUT", 26.0, -34.0, p.lower_thickness_mm, size=6.0)
    base = _engrave(base, "STOP", -22.0, -34.0, p.lower_thickness_mm, size=6.0)

    lower_pad = _pad(p.lower_pad_size_mm, p.lower_pad_height_mm, "PAD").translate((72.0, -44.0, 0.0))
    sensor = _sensor_dummy(p).translate((72.0, 4.0, 0.0))
    upper_pad = _pad(p.upper_pad_size_mm, p.upper_pad_height_mm, "UPPER").translate((72.0, 62.0, 0.0))
    return _compound([base, lower_pad, sensor, upper_pad])


def _seam_block(center_y: float, seam_side: int, label: str) -> cq.Workplane:
    block = _box(54.0, 24.0, 8.0, 0.0, center_y)
    hole_y = center_y + seam_side * (12.0 - BJP.hole_from_seam_mm)
    block = block.cut(_cylinder_cut(BJP.m3_clearance_diameter_mm, 8.4, 0.0, hole_y, -0.2))
    block = block.cut(
        _hex_cut(
            BJP.captured_nut_across_flats_mm,
            BJP.captured_nut_pocket_depth_mm,
            0.0,
            hole_y,
            BJP.captured_nut_lip_depth_mm,
        )
    )
    block = block.cut(
        _hex_cut(
            BJP.captured_nut_lip_across_flats_mm,
            BJP.captured_nut_lip_depth_mm + 0.15,
            0.0,
            hole_y,
            -0.05,
        )
    )
    return _engrave(block, label, 0.0, center_y + seam_side * 6.0, 8.0, size=5.8)


def test_bolted_seam_slice_v1() -> cq.Compound:
    gap = BJP.print_gap_mm
    lower_y = -(24.0 + gap) / 2.0
    upper_y = (24.0 + gap) / 2.0
    block_a = _seam_block(lower_y, 1, "NUT")
    block_b = _seam_block(upper_y, -1, "NUT")

    hole_offset = 24.0 / 2.0 - BJP.hole_from_seam_mm
    bridge = _single_bridge_plate(54.0, 34.0, (-hole_offset, hole_offset)).translate((0.0, 62.0, 0.0))
    return _compound([block_a, block_b, bridge])


def practical_test_prints() -> dict[str, cq.Workplane | cq.Compound]:
    return {
        "test_label_readability_v1": test_label_readability_v1(),
        "test_m3_captured_nut_v1": test_m3_captured_nut_v1(),
        "test_support_grate_fit_v1": test_support_grate_fit_v1(),
        "test_sensor_locator_v3_fit_v1": test_sensor_locator_v3_fit_v1(),
        "test_bolted_seam_slice_v1": test_bolted_seam_slice_v1(),
    }
