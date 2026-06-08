"""Bolted seam joinery coupons for SaltScale concept_v2.

These coupons validate the default no-dowel, no-heat-set-insert segment
joining strategy: common M3 bolts, standard M3 nuts, and printed bridge plates.
They do not modify the full concept_v2 platform.
"""

from dataclasses import dataclass
import math

import cadquery as cq

from concept_v2 import P, ConceptV2Params


LABEL_DEPTH_MM = 0.8
LABEL_SIZE_MM = 7.0


@dataclass(frozen=True)
class BoltedJoineryParams:
    block_len_mm: float = 96.0
    block_depth_mm: float = 34.0
    print_gap_mm: float = 8.0
    bridge_layout_y_mm: float = 86.0

    bridge_len_mm: float = 86.0
    bridge_depth_mm: float = 42.0
    bridge_height_mm: float = 4.0

    hole_x_offset_mm: float = 28.0
    hole_from_seam_mm: float = 9.0
    m3_clearance_diameter_mm: float = 3.4

    nut_across_flats_mm: float = 6.1
    nut_pocket_depth_mm: float = 3.2

    captured_nut_across_flats_mm: float = 5.9
    captured_nut_lip_across_flats_mm: float = 5.35
    captured_nut_pocket_depth_mm: float = 3.0
    captured_nut_lip_depth_mm: float = 0.7


BJP = BoltedJoineryParams()


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _compound(parts: list[cq.Workplane]) -> cq.Compound:
    return cq.Compound.makeCompound([part.val() for part in parts])


def _engrave(part: cq.Workplane, label: str, x: float, y: float, z: float, size: float = LABEL_SIZE_MM) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    return part.cut(text.translate((x, y, 0.0)))


def _cylinder_cut(diameter: float, height: float, x: float, y: float, z0: float) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(height).translate((x, y, z0))


def _hex_nut_cut(across_flats: float, depth: float, x: float, y: float, z0: float) -> cq.Workplane:
    diameter = 2.0 * across_flats / math.sqrt(3.0)
    return (
        cq.Workplane("XY")
        .polygon(6, diameter)
        .extrude(depth)
        .rotate((0, 0, 0), (0, 0, 1), 30)
        .translate((x, y, z0))
    )


def _block_hole_centers(block_center_y: float, seam_side: int, p: BoltedJoineryParams = BJP) -> list[tuple[float, float]]:
    y = block_center_y + seam_side * (p.block_depth_mm / 2.0 - p.hole_from_seam_mm)
    return [(-p.hole_x_offset_mm, y), (p.hole_x_offset_mm, y)]


def _add_open_nut_features(
    block: cq.Workplane,
    block_center_y: float,
    seam_side: int,
    thickness: float,
    p: BoltedJoineryParams = BJP,
) -> cq.Workplane:
    for x, y in _block_hole_centers(block_center_y, seam_side, p):
        block = block.cut(_cylinder_cut(p.m3_clearance_diameter_mm, thickness + 0.4, x, y, -0.2))
        block = block.cut(_hex_nut_cut(p.nut_across_flats_mm, p.nut_pocket_depth_mm + 0.1, x, y, -0.05))
    return block


def _add_captured_nut_features(
    block: cq.Workplane,
    block_center_y: float,
    seam_side: int,
    thickness: float,
    p: BoltedJoineryParams = BJP,
) -> cq.Workplane:
    for x, y in _block_hole_centers(block_center_y, seam_side, p):
        block = block.cut(_cylinder_cut(p.m3_clearance_diameter_mm, thickness + 0.4, x, y, -0.2))
        block = block.cut(
            _hex_nut_cut(
                p.captured_nut_across_flats_mm,
                p.captured_nut_pocket_depth_mm,
                x,
                y,
                p.captured_nut_lip_depth_mm,
            )
        )
        block = block.cut(
            _hex_nut_cut(
                p.captured_nut_lip_across_flats_mm,
                p.captured_nut_lip_depth_mm + 0.15,
                x,
                y,
                -0.05,
            )
        )
    return block


def _segment_blocks(
    part_label: str,
    thickness: float,
    captured_nuts: bool,
    p: BoltedJoineryParams = BJP,
) -> tuple[cq.Workplane, cq.Workplane]:
    lower_y = -(p.block_depth_mm + p.print_gap_mm) / 2.0
    upper_y = (p.block_depth_mm + p.print_gap_mm) / 2.0

    block_a = _box(p.block_len_mm, p.block_depth_mm, thickness, 0.0, lower_y)
    block_b = _box(p.block_len_mm, p.block_depth_mm, thickness, 0.0, upper_y)

    feature_fn = _add_captured_nut_features if captured_nuts else _add_open_nut_features
    block_a = feature_fn(block_a, lower_y, 1, thickness, p)
    block_b = feature_fn(block_b, upper_y, -1, thickness, p)

    block_a = _engrave(block_a, part_label, 0.0, lower_y - 8.0, thickness)
    block_b = _engrave(block_b, "NUT", 0.0, upper_y - 7.5, thickness)
    block_b = _engrave(block_b, "IN", -32.0, upper_y + 8.0, thickness)
    block_b = _engrave(block_b, "OUT", 31.0, upper_y + 8.0, thickness)
    return block_a, block_b


def _bridge_plate(p: BoltedJoineryParams = BJP) -> cq.Workplane:
    bridge = _box(p.bridge_len_mm, p.bridge_depth_mm, p.bridge_height_mm, 0.0, p.bridge_layout_y_mm)
    for x in (-p.hole_x_offset_mm, p.hole_x_offset_mm):
        for y in (-p.hole_from_seam_mm, p.hole_from_seam_mm):
            bridge = bridge.cut(
                _cylinder_cut(p.m3_clearance_diameter_mm, p.bridge_height_mm + 0.4, x, p.bridge_layout_y_mm + y, -0.2)
            )

    bridge = _engrave(bridge, "BRIDGE", 0.0, p.bridge_layout_y_mm + 8.0, p.bridge_height_mm, size=6.4)
    bridge = _engrave(bridge, "M3", 0.0, p.bridge_layout_y_mm - 9.0, p.bridge_height_mm)
    return bridge


def _bolted_coupon(part_label: str, thickness: float, captured_nuts: bool, p: BoltedJoineryParams = BJP) -> cq.Compound:
    block_a, block_b = _segment_blocks(part_label, thickness, captured_nuts, p)
    return _compound([block_a, block_b, _bridge_plate(p)])


def bolted_lower_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _bolted_coupon("LOWER", p.lower_thickness_mm, captured_nuts=False)


def bolted_upper_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _bolted_coupon("UPPER", p.upper_thickness_mm, captured_nuts=False)


def bolted_lower_seam_coupon_v2(p: ConceptV2Params = P) -> cq.Compound:
    return _bolted_coupon("LOWER", p.lower_thickness_mm, captured_nuts=True)


def bolted_upper_seam_coupon_v2(p: ConceptV2Params = P) -> cq.Compound:
    return _bolted_coupon("UPPER", p.upper_thickness_mm, captured_nuts=True)


def bolted_lower_seam_captured_nut_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return bolted_lower_seam_coupon_v2(p)


def bolted_upper_seam_captured_nut_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return bolted_upper_seam_coupon_v2(p)


def bolted_joinery_coupons(p: ConceptV2Params = P) -> dict[str, cq.Compound]:
    return {
        "bolted_lower_seam_coupon_v1": bolted_lower_seam_coupon_v1(p),
        "bolted_upper_seam_coupon_v1": bolted_upper_seam_coupon_v1(p),
        "bolted_lower_seam_coupon_v2": bolted_lower_seam_coupon_v2(p),
        "bolted_upper_seam_coupon_v2": bolted_upper_seam_coupon_v2(p),
        "bolted_lower_seam_captured_nut_coupon_v1": bolted_lower_seam_captured_nut_coupon_v1(p),
        "bolted_upper_seam_captured_nut_coupon_v1": bolted_upper_seam_captured_nut_coupon_v1(p),
    }
