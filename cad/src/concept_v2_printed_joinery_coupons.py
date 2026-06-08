"""Printed-only seam joinery coupons for SaltScale concept_v2.

These coupons validate no-metal segment joining ideas. They do not modify the
concept_v2 platform. Each coupon is a print-flat kit containing two segment-edge
blocks and one separate removable printed key.
"""

from dataclasses import dataclass

import cadquery as cq

from concept_v2 import P, ConceptV2Params


LABEL_DEPTH_MM = 0.8
LABEL_SIZE_MM = 7.0


@dataclass(frozen=True)
class JoineryParams:
    block_len_mm: float = 96.0
    block_depth_mm: float = 34.0
    print_gap_mm: float = 8.0
    key_layout_y_mm: float = 84.0

    sliding_len_mm: float = 78.0
    sliding_slot_width_mm: float = 24.0
    sliding_slot_depth_mm: float = 4.8
    sliding_key_clearance_mm: float = 0.5

    dovetail_len_mm: float = 78.0
    dovetail_slot_depth_mm: float = 5.6
    dovetail_bottom_width_mm: float = 30.0
    dovetail_top_width_mm: float = 20.0
    dovetail_clearance_mm: float = 0.45

    wedge_len_mm: float = 78.0
    wedge_slot_depth_mm: float = 5.2
    wedge_slot_width_in_mm: float = 18.0
    wedge_slot_width_out_mm: float = 28.0
    wedge_key_clearance_mm: float = 0.6


JP = JoineryParams()


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _compound(parts: list[cq.Workplane]) -> cq.Compound:
    return cq.Compound.makeCompound([part.val() for part in parts])


def _engrave(part: cq.Workplane, label: str, x: float, y: float, z: float, size: float = LABEL_SIZE_MM) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    return part.cut(text.translate((x, y, 0.0)))


def _dovetail_prism(
    length: float,
    bottom_width: float,
    top_width: float,
    height: float,
    cx: float = 0.0,
    cy: float = 0.0,
    z0: float = 0.0,
) -> cq.Workplane:
    """Create a trapezoid in Y/Z extruded along X.

    The wider bottom and narrower top create a true sliding dovetail when the
    slot is cut into the top of the seam blocks.
    """

    points = [
        (-bottom_width / 2.0, 0.0),
        (bottom_width / 2.0, 0.0),
        (top_width / 2.0, height),
        (-top_width / 2.0, height),
    ]
    return cq.Workplane("YZ").polyline(points).close().extrude(length).translate((cx - length / 2.0, cy, z0))


def _tapered_plan(
    length: float,
    width_in: float,
    width_out: float,
    height: float,
    cx: float = 0.0,
    cy: float = 0.0,
    z0: float = 0.0,
) -> cq.Workplane:
    """Create a tapered plan-view prism. +X is OUT, -X is IN."""

    points = [
        (-length / 2.0, -width_in / 2.0),
        (length / 2.0, -width_out / 2.0),
        (length / 2.0, width_out / 2.0),
        (-length / 2.0, width_in / 2.0),
    ]
    return cq.Workplane("XY").polyline(points).close().extrude(height).translate((cx, cy, z0))


def _segment_blocks(part_label: str, strategy_label: str, thickness: float, jp: JoineryParams = JP) -> tuple[cq.Workplane, cq.Workplane]:
    lower_y = -(jp.block_depth_mm + jp.print_gap_mm) / 2.0
    upper_y = (jp.block_depth_mm + jp.print_gap_mm) / 2.0
    block_a = _box(jp.block_len_mm, jp.block_depth_mm, thickness, 0.0, lower_y)
    block_b = _box(jp.block_len_mm, jp.block_depth_mm, thickness, 0.0, upper_y)

    block_a = _engrave(block_a, part_label, 0.0, lower_y - 8.0, thickness)
    block_b = _engrave(block_b, strategy_label, 0.0, upper_y - 6.0, thickness)
    block_b = _engrave(block_b, "IN", -32.0, upper_y + 8.0, thickness)
    block_b = _engrave(block_b, "OUT", 31.0, upper_y + 8.0, thickness)
    return block_a, block_b


def _seam_centers(jp: JoineryParams = JP) -> tuple[float, float]:
    return -jp.print_gap_mm / 2.0, jp.print_gap_mm / 2.0


def _cut_rect_slot_halves(block_a: cq.Workplane, block_b: cq.Workplane, thickness: float, jp: JoineryParams = JP) -> tuple[cq.Workplane, cq.Workplane]:
    z0 = thickness - jp.sliding_slot_depth_mm
    lower_seam_y, upper_seam_y = _seam_centers(jp)
    cut_h = jp.sliding_slot_depth_mm + 0.2
    lower_cut = _box(jp.sliding_len_mm, jp.sliding_slot_width_mm, cut_h, 0.0, lower_seam_y, z0)
    upper_cut = _box(jp.sliding_len_mm, jp.sliding_slot_width_mm, cut_h, 0.0, upper_seam_y, z0)
    return block_a.cut(lower_cut), block_b.cut(upper_cut)


def _sliding_key(thickness: float, jp: JoineryParams = JP) -> cq.Workplane:
    key_h = min(jp.sliding_slot_depth_mm - 0.25, thickness - 0.8)
    key_w = jp.sliding_slot_width_mm - 2.0 * jp.sliding_key_clearance_mm
    key = _box(jp.sliding_len_mm - 1.0, key_w, key_h, 0.0, jp.key_layout_y_mm)
    return _engrave(key, "KEY", 0.0, jp.key_layout_y_mm, key_h)


def _cut_true_dovetail_halves(block_a: cq.Workplane, block_b: cq.Workplane, thickness: float, jp: JoineryParams = JP) -> tuple[cq.Workplane, cq.Workplane]:
    z0 = thickness - jp.dovetail_slot_depth_mm
    lower_seam_y, upper_seam_y = _seam_centers(jp)
    cut_h = jp.dovetail_slot_depth_mm + 0.2
    lower_cut = _dovetail_prism(
        jp.dovetail_len_mm,
        jp.dovetail_bottom_width_mm,
        jp.dovetail_top_width_mm,
        cut_h,
        cy=lower_seam_y,
        z0=z0,
    )
    upper_cut = _dovetail_prism(
        jp.dovetail_len_mm,
        jp.dovetail_bottom_width_mm,
        jp.dovetail_top_width_mm,
        cut_h,
        cy=upper_seam_y,
        z0=z0,
    )
    return block_a.cut(lower_cut), block_b.cut(upper_cut)


def _true_dovetail_key(thickness: float, jp: JoineryParams = JP) -> cq.Workplane:
    key_h = min(jp.dovetail_slot_depth_mm - 0.3, thickness - 0.8)
    key = _dovetail_prism(
        jp.dovetail_len_mm - 1.0,
        jp.dovetail_bottom_width_mm - 2.0 * jp.dovetail_clearance_mm,
        jp.dovetail_top_width_mm - 2.0 * jp.dovetail_clearance_mm,
        key_h,
        cy=jp.key_layout_y_mm,
    )
    return _engrave(key, "KEY", 0.0, jp.key_layout_y_mm, key_h, size=6.6)


def _cut_wedge_halves(block_a: cq.Workplane, block_b: cq.Workplane, thickness: float, jp: JoineryParams = JP) -> tuple[cq.Workplane, cq.Workplane]:
    z0 = thickness - jp.wedge_slot_depth_mm
    lower_seam_y, upper_seam_y = _seam_centers(jp)
    cut_h = jp.wedge_slot_depth_mm + 0.2
    lower_cut = _tapered_plan(
        jp.wedge_len_mm,
        jp.wedge_slot_width_in_mm,
        jp.wedge_slot_width_out_mm,
        cut_h,
        cy=lower_seam_y,
        z0=z0,
    )
    upper_cut = _tapered_plan(
        jp.wedge_len_mm,
        jp.wedge_slot_width_in_mm,
        jp.wedge_slot_width_out_mm,
        cut_h,
        cy=upper_seam_y,
        z0=z0,
    )
    return block_a.cut(lower_cut), block_b.cut(upper_cut)


def _wedge_key_v2(thickness: float, jp: JoineryParams = JP) -> cq.Workplane:
    key_h = min(jp.wedge_slot_depth_mm - 0.25, thickness - 0.8)
    # The key is shorter than the pocket. Pushing it farther toward IN makes the
    # taper engage progressively, while the initial fit remains forgiving.
    key = _tapered_plan(
        jp.wedge_len_mm - 8.0,
        jp.wedge_slot_width_in_mm - 2.0 * jp.wedge_key_clearance_mm,
        jp.wedge_slot_width_out_mm - 2.0 * jp.wedge_key_clearance_mm,
        key_h,
        cy=jp.key_layout_y_mm,
    )
    return _engrave(key, "KEY", 0.0, jp.key_layout_y_mm, key_h)


def _sliding_key_coupon(part_label: str, thickness: float, jp: JoineryParams = JP) -> cq.Compound:
    block_a, block_b = _segment_blocks(part_label, "SLIDE", thickness, jp)
    block_a, block_b = _cut_rect_slot_halves(block_a, block_b, thickness, jp)
    return _compound([block_a, block_b, _sliding_key(thickness, jp)])


def _true_dovetail_coupon(part_label: str, thickness: float, jp: JoineryParams = JP) -> cq.Compound:
    block_a, block_b = _segment_blocks(part_label, "DOVE", thickness, jp)
    block_a, block_b = _cut_true_dovetail_halves(block_a, block_b, thickness, jp)
    return _compound([block_a, block_b, _true_dovetail_key(thickness, jp)])


def _wedge_coupon_v2(part_label: str, thickness: float, jp: JoineryParams = JP) -> cq.Compound:
    block_a, block_b = _segment_blocks(part_label, "WEDGE", thickness, jp)
    block_a, block_b = _cut_wedge_halves(block_a, block_b, thickness, jp)
    return _compound([block_a, block_b, _wedge_key_v2(thickness, jp)])


def printed_lower_seam_sliding_key_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _sliding_key_coupon("LOWER", p.lower_thickness_mm)


def printed_upper_seam_sliding_key_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _sliding_key_coupon("UPPER", p.upper_thickness_mm)


def printed_lower_seam_true_dovetail_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _true_dovetail_coupon("LOWER", p.lower_thickness_mm)


def printed_upper_seam_true_dovetail_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    return _true_dovetail_coupon("UPPER", p.upper_thickness_mm)


def printed_lower_seam_wedge_coupon_v2(p: ConceptV2Params = P) -> cq.Compound:
    return _wedge_coupon_v2("LOWER", p.lower_thickness_mm)


def printed_upper_seam_wedge_coupon_v2(p: ConceptV2Params = P) -> cq.Compound:
    return _wedge_coupon_v2("UPPER", p.upper_thickness_mm)


def printed_joinery_coupons(p: ConceptV2Params = P) -> dict[str, cq.Compound]:
    return {
        "printed_lower_seam_sliding_key_coupon_v1": printed_lower_seam_sliding_key_coupon_v1(p),
        "printed_upper_seam_sliding_key_coupon_v1": printed_upper_seam_sliding_key_coupon_v1(p),
        "printed_lower_seam_true_dovetail_coupon_v1": printed_lower_seam_true_dovetail_coupon_v1(p),
        "printed_upper_seam_true_dovetail_coupon_v1": printed_upper_seam_true_dovetail_coupon_v1(p),
        "printed_lower_seam_wedge_coupon_v2": printed_lower_seam_wedge_coupon_v2(p),
        "printed_upper_seam_wedge_coupon_v2": printed_upper_seam_wedge_coupon_v2(p),
    }


if __name__ == "__main__":
    show_object(printed_lower_seam_wedge_coupon_v2())  # type: ignore[name-defined]
