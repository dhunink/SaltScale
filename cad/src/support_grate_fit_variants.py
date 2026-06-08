"""Support-grate fit clearance coupons for SaltScale concept_v2.

These are validation coupons only. They test upper support-grate tab clearance
without changing the full concept_v2 platform or introducing lower-base
geometry.
"""

from dataclasses import dataclass

import cadquery as cq

from concept_v2 import P, ConceptV2Params


LABEL_DEPTH_MM = 0.8
LABEL_SIZE_MM = 7.0


@dataclass(frozen=True)
class SupportGrateFitParams:
    slot_block_len_mm: float = 92.0
    slot_block_width_mm: float = 54.0
    slot_block_height_mm: float = 8.0

    slot_len_mm: float = 72.0
    slot_depth_mm: float = 4.2

    tab_len_mm: float = 68.0
    tab_layout_x_mm: float = 86.0


SGP = SupportGrateFitParams()


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _compound(parts: list[cq.Workplane]) -> cq.Compound:
    return cq.Compound.makeCompound([part.val() for part in parts])


def _engrave(part: cq.Workplane, label: str, x: float, y: float, z: float, size: float = LABEL_SIZE_MM) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    return part.cut(text.translate((x, y, 0.0)))


def _slot_body(clearance_per_side_mm: float, p: ConceptV2Params = P, s: SupportGrateFitParams = SGP) -> cq.Workplane:
    slot_width = p.grate_arm_width_mm + 2.0 * clearance_per_side_mm
    body = _box(s.slot_block_len_mm, s.slot_block_width_mm, s.slot_block_height_mm)

    slot_cut = _box(
        s.slot_len_mm,
        slot_width,
        s.slot_depth_mm + 0.3,
        -6.0,
        0.0,
        s.slot_block_height_mm - s.slot_depth_mm,
    )
    body = body.cut(slot_cut)

    body = _engrave(body, "SLOT", -27.0, 19.0, s.slot_block_height_mm)
    body = _engrave(body, f"{clearance_per_side_mm:.1f}", 26.0, 19.0, s.slot_block_height_mm)
    return body


def _tab_body(clearance_per_side_mm: float, p: ConceptV2Params = P, s: SupportGrateFitParams = SGP) -> cq.Workplane:
    tab = _box(s.tab_len_mm, p.grate_arm_width_mm, p.grate_thickness_mm, s.tab_layout_x_mm, 0.0)
    tab = _engrave(tab, "TAB", s.tab_layout_x_mm, 5.5, p.grate_thickness_mm)
    tab = _engrave(tab, f"{clearance_per_side_mm:.1f}", s.tab_layout_x_mm, -7.5, p.grate_thickness_mm)
    return tab


def _coupon(clearance_per_side_mm: float, p: ConceptV2Params = P) -> cq.Compound:
    return _compound([_slot_body(clearance_per_side_mm, p), _tab_body(clearance_per_side_mm, p)])


def support_grate_fit_0p4mm_per_side(p: ConceptV2Params = P) -> cq.Compound:
    return _coupon(0.4, p)


def support_grate_fit_0p6mm_per_side(p: ConceptV2Params = P) -> cq.Compound:
    return _coupon(0.6, p)


def support_grate_fit_0p8mm_per_side(p: ConceptV2Params = P) -> cq.Compound:
    return _coupon(0.8, p)


def support_grate_fit_variants(p: ConceptV2Params = P) -> dict[str, cq.Compound]:
    return {
        "support_grate_fit_0p4mm_per_side": support_grate_fit_0p4mm_per_side(p),
        "support_grate_fit_0p6mm_per_side": support_grate_fit_0p6mm_per_side(p),
        "support_grate_fit_0p8mm_per_side": support_grate_fit_0p8mm_per_side(p),
    }
