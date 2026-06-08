"""Small practical validation coupons for concept_v4 integrated M3 seams.

These coupons keep the real v4 seam interface geometry but remove surrounding
ring material. They are intended for quick PETG validation before printing full
concept_v4 segments.
"""

import math

import cadquery as cq

from concept_v2 import _engrave_top
from concept_v4_integrated_joining import (
    LUG_HEIGHT_MM,
    LUG_RADIAL_LEN_MM,
    LUG_RECEIVER_TANGENT_OFFSET_MM,
    LUG_ROOT_SHOULDER_RADIAL_MM,
    LUG_ROOT_SHOULDER_TANGENT_MM,
    LUG_TANGENT_LEN_MM,
    LOCATOR_RADIAL_LEN_MM,
    LOCATOR_SOCKET_TANGENT_MM,
    LOCATOR_TONGUE_TANGENT_MM,
    LOWER_HEAD_SEAT_DEPTH_MM,
    M3_BUTTON_HEAD_DIAMETER_MM,
    M3_BUTTON_HEAD_HEIGHT_MM,
    M3_HEAD_RECESS_DEPTH_MM,
    M3_HEAD_RECESS_DIAMETER_MM,
    P,
)

BLOCK_THICKNESS_MM = 8.0
GAP_MM = 8.0


def _hex_cut(across_flats: float, height: float, z: float) -> cq.Workplane:
    diameter = 2.0 * across_flats / math.sqrt(3.0)
    return (
        cq.Workplane("XY")
        .polygon(6, diameter)
        .extrude(height)
        .rotate((0, 0, 0), (0, 0, 1), 30)
        .translate((0, 0, z))
    )


def _m3_clearance(height: float, z: float = -0.2) -> cq.Workplane:
    return cq.Workplane("XY").circle(P.m3_clearance_diameter_mm / 2.0).extrude(height).translate((0, 0, z))


def _engrave(body: cq.Workplane, label: str, x: float, y: float, z: float, size: float = 7.0) -> cq.Workplane:
    return _engrave_top(body, label, x, y, z, size=size, p=P)


def _nut_block(label: str, nut_from_top: bool) -> cq.Workplane:
    body = cq.Workplane("XY").box(36.0, 30.0, BLOCK_THICKNESS_MM, centered=(True, True, False))
    body = body.cut(_m3_clearance(BLOCK_THICKNESS_MM + 0.4))
    if nut_from_top:
        lip_z = BLOCK_THICKNESS_MM - P.captured_nut_lip_depth_mm
        pocket_z = lip_z - P.captured_nut_pocket_depth_mm
    else:
        lip_z = -0.05
        pocket_z = P.captured_nut_lip_depth_mm
    body = body.cut(_hex_cut(P.captured_nut_lip_across_flats_mm, P.captured_nut_lip_depth_mm + 0.15, lip_z))
    body = body.cut(_hex_cut(P.captured_nut_across_flats_mm, P.captured_nut_pocket_depth_mm, pocket_z))
    body = _engrave(body, label, -9.0, 8.0, BLOCK_THICKNESS_MM, size=6.5)
    body = _engrave(body, "NUT", 10.0, -8.0, BLOCK_THICKNESS_MM, size=6.5)
    return body


def _lug_block(label: str, upper: bool) -> cq.Workplane:
    lug = cq.Workplane("XY").box(LUG_RADIAL_LEN_MM, LUG_TANGENT_LEN_MM, LUG_HEIGHT_MM, centered=(True, True, False))
    shoulder = (
        cq.Workplane("XY")
        .box(LUG_ROOT_SHOULDER_RADIAL_MM, LUG_ROOT_SHOULDER_TANGENT_MM, LUG_HEIGHT_MM, centered=(True, True, False))
        .translate((-8.0, -LUG_TANGENT_LEN_MM / 2.0 + LUG_ROOT_SHOULDER_TANGENT_MM / 2.0, 0))
    )
    body = lug.union(shoulder)
    body = body.cut(_m3_clearance(LUG_HEIGHT_MM + 0.6, -0.3))
    if upper:
        body = body.cut(
            cq.Workplane("XY")
            .circle(M3_HEAD_RECESS_DIAMETER_MM / 2.0)
            .extrude(M3_HEAD_RECESS_DEPTH_MM + 0.2)
            .translate((0, 0, -0.1))
        )
    else:
        body = body.cut(
            cq.Workplane("XY")
            .circle(M3_HEAD_RECESS_DIAMETER_MM / 2.0)
            .extrude(LOWER_HEAD_SEAT_DEPTH_MM + 0.2)
            .translate((0, 0, LUG_HEIGHT_MM - LOWER_HEAD_SEAT_DEPTH_MM))
        )
    body = _engrave(body, label, -15.0, 10.0, LUG_HEIGHT_MM, size=6.5)
    body = _engrave(body, "M3", 11.0, -9.0, LUG_HEIGHT_MM, size=6.5)
    return body


def concept_v4_upper_lug_recess_block_v1() -> cq.Workplane:
    return _lug_block("UPPER", upper=True)


def concept_v4_upper_lug_mating_block_v1() -> cq.Workplane:
    return _nut_block("UPPER", nut_from_top=True)


def concept_v4_lower_lug_bolt_block_v1() -> cq.Workplane:
    return _lug_block("LOWER", upper=False)


def concept_v4_lower_lug_nut_block_v1() -> cq.Workplane:
    return _nut_block("LOWER", nut_from_top=False)


def _locator_tongue_block() -> cq.Workplane:
    body = cq.Workplane("XY").box(36.0, 24.0, 6.0, centered=(True, True, False))
    tongue = (
        cq.Workplane("XY")
        .box(LOCATOR_RADIAL_LEN_MM, LOCATOR_TONGUE_TANGENT_MM, 6.0, centered=(True, True, False))
        .translate((0, 12.0, 0))
    )
    return body.union(tongue)


def _locator_socket_block(clearance_per_side: float) -> cq.Workplane:
    body = cq.Workplane("XY").box(36.0, 28.0, 6.0, centered=(True, True, False))
    socket = (
        cq.Workplane("XY")
        .box(
            LOCATOR_RADIAL_LEN_MM + 2.0 * clearance_per_side,
            LOCATOR_TONGUE_TANGENT_MM + 2.0 * clearance_per_side,
            6.6,
            centered=(True, True, False),
        )
        .translate((0, -14.0, -0.3))
    )
    return body.cut(socket)


def concept_v4_locator_fit_variant(clearance_per_side: float, label: str) -> cq.Workplane:
    tongue = _locator_tongue_block().translate((-24.0, 0, 0))
    socket = _locator_socket_block(clearance_per_side).translate((28.0, 0, 0))
    body = tongue.union(socket)
    body = _engrave(body, label, -6.0, 4.0, 6.0, size=7.0)
    body = _engrave(body, "KEY", -36.0, -8.0, 6.0, size=6.5)
    body = _engrave(body, "SLOT", 20.0, -8.0, 6.0, size=6.5)
    return body


def concept_v4_locator_fit_0p3_v1() -> cq.Workplane:
    return concept_v4_locator_fit_variant(0.3, "0.3")


def concept_v4_locator_fit_0p4_v1() -> cq.Workplane:
    return concept_v4_locator_fit_variant(0.4, "0.4")


def concept_v4_locator_fit_0p5_v1() -> cq.Workplane:
    return concept_v4_locator_fit_variant(0.5, "0.5")


def concept_v4_integrated_mini_seam_test_v1() -> cq.Workplane:
    lug = _lug_block("LUG", upper=False).translate((-24.0, 0, 0))
    nut = _nut_block("NUT", nut_from_top=False).translate((28.0, 0, 0))

    tongue = (
        cq.Workplane("XY")
        .box(LOCATOR_RADIAL_LEN_MM, LOCATOR_TONGUE_TANGENT_MM, 6.0, centered=(True, True, False))
        .translate((-24.0, -24.0, 0))
    )
    socket_cut = (
        cq.Workplane("XY")
        .box(
            LOCATOR_RADIAL_LEN_MM + 2.0 * 0.5,
            LOCATOR_TONGUE_TANGENT_MM + 2.0 * 0.5,
            8.6,
            centered=(True, True, False),
        )
        .translate((28.0, -24.0, -0.3))
    )
    nut = nut.union(cq.Workplane("XY").box(36.0, 16.0, BLOCK_THICKNESS_MM, centered=(True, True, False)).translate((28.0, -24.0, 0))).cut(socket_cut)
    lug = lug.union(tongue)
    body = lug.union(nut)
    body = _engrave(body, "SEAM", 2.0, 19.0, BLOCK_THICKNESS_MM, size=7.0)
    return body


def micro_coupon_exports() -> dict[str, cq.Workplane]:
    return {
        "concept_v4_upper_lug_recess_block_v1": concept_v4_upper_lug_recess_block_v1(),
        "concept_v4_upper_lug_mating_block_v1": concept_v4_upper_lug_mating_block_v1(),
        "concept_v4_lower_lug_bolt_block_v1": concept_v4_lower_lug_bolt_block_v1(),
        "concept_v4_lower_lug_nut_block_v1": concept_v4_lower_lug_nut_block_v1(),
        "concept_v4_locator_fit_0p3_v1": concept_v4_locator_fit_0p3_v1(),
        "concept_v4_locator_fit_0p4_v1": concept_v4_locator_fit_0p4_v1(),
        "concept_v4_locator_fit_0p5_v1": concept_v4_locator_fit_0p5_v1(),
        "concept_v4_integrated_mini_seam_test_v1": concept_v4_integrated_mini_seam_test_v1(),
    }
