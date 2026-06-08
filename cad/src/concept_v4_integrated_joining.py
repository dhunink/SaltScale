"""Concept v4 integrated M3 joining candidate.

This candidate keeps the concept_v2 four-sensor floating architecture but
removes separate printed bridge plates. Each same-layer ring segment has
integrated lap lugs at one seam edge and captured M3 nut pockets at the other
seam edge. A segment bolts directly to its neighbor with standard M3 bolts and
standard captured M3 nuts.

The joining remains lower-to-lower or upper-to-upper only. There are no
upper-to-lower fasteners, dowels, heat-set inserts, or bridge plates.
"""

from dataclasses import replace
import math

import cadquery as cq

from concept_v2 import (
    ConceptV2Params,
    _add_support_grate_receivers,
    _annular_sector,
    _engrave_local,
    _engrave_top,
    _hex_cut,
    _local_box,
    _local_cylinder,
    _sensor_stack_heights,
    _sensor_station_lower_features,
    lower_pad,
    sensor_placeholder,
)
from concept_v3_print_optimized import support_grate_bar_x, support_grate_bar_y


P = replace(
    ConceptV2Params(),
    segment_count=4,
    seam_gap_deg=1.4,
    seam_feature_inset_deg=0.0,
    seam_bolt_radii_mm=(122.0, 145.0),
)

LUG_RADIAL_LEN_MM = 28.0
LUG_TANGENT_LEN_MM = 34.0
LUG_HEIGHT_MM = 4.0
LUG_RECEIVER_TANGENT_OFFSET_MM = 8.0
LUG_ROOT_SHOULDER_TANGENT_MM = 13.0
LUG_ROOT_SHOULDER_RADIAL_MM = 42.0

LOCATOR_RADIUS_MM = 134.0
LOCATOR_RADIAL_LEN_MM = 22.0
LOCATOR_TONGUE_TANGENT_MM = 10.0
LOCATOR_SOCKET_TANGENT_MM = 11.0
LOCATOR_TANGENT_OFFSET_MM = 4.0
LOCATOR_CLEARANCE_PER_SIDE_MM = 0.5

# Default fastener assumption for integrated v4 seams.
# ISO 7380 style M3 button-head screws keep top-access upper fasteners low
# enough to recess flush with the upper carrier top surface.
M3_BUTTON_HEAD_DIAMETER_MM = 5.7
M3_BUTTON_HEAD_HEIGHT_MM = 1.8
M3_HEAD_RECESS_DIAMETER_MM = 6.4
M3_HEAD_RECESS_DEPTH_MM = 2.0
LOWER_HEAD_SEAT_DEPTH_MM = 1.0

UPPER_PAD_ROUND_DIAMETER_MM = 56.0
UPPER_PAD_CUP_CLEARANCE_PER_SIDE_MM = 0.45
UPPER_PAD_CUP_WALL_MM = 4.0
UPPER_PAD_CUP_HEIGHT_MM = LUG_HEIGHT_MM


def _segment_angles(index: int, p: ConceptV2Params = P) -> tuple[float, float]:
    span = 360.0 / p.segment_count
    start = index * span + p.seam_gap_deg / 2.0
    end = (index + 1) * span - p.seam_gap_deg / 2.0
    return start, end


def _segment_mid_angle(index: int, p: ConceptV2Params = P) -> float:
    start, end = _segment_angles(index, p)
    return (start + end) / 2.0


def _lug_body(
    seam_angle: float,
    z: float,
    label: str,
    upper_lug: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    lug = None
    for radius in p.seam_bolt_radii_mm:
        pad = _local_box(
            LUG_RADIAL_LEN_MM,
            LUG_TANGENT_LEN_MM,
            LUG_HEIGHT_MM,
            radius,
            seam_angle,
            z,
            tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
        )
        pad = pad.cut(
            _local_cylinder(
                p.m3_clearance_diameter_mm,
                LUG_HEIGHT_MM + 0.8,
                radius,
                seam_angle,
                z - 0.4,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )
        if upper_lug:
            # Upper bolts now install from the top of the neighboring segment.
            # The integrated underside lug carries the captured M3 nut.
            pad = pad.cut(
                _hex_cut(
                    p.captured_nut_lip_across_flats_mm,
                    p.captured_nut_lip_depth_mm + 0.15,
                    radius,
                    seam_angle,
                    z - 0.05,
                    tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
                )
            )
            pad = pad.cut(
                _hex_cut(
                    p.captured_nut_across_flats_mm,
                    p.captured_nut_pocket_depth_mm,
                    radius,
                    seam_angle,
                    z + p.captured_nut_lip_depth_mm,
                    tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
                )
            )
        else:
            # Shallow top-side seat. Lower heads may protrude slightly upward;
            # this is away from the normal measuring path.
            pad = pad.cut(
                _local_cylinder(
                    M3_HEAD_RECESS_DIAMETER_MM,
                    LOWER_HEAD_SEAT_DEPTH_MM + 0.2,
                    radius,
                    seam_angle,
                    z + LUG_HEIGHT_MM - LOWER_HEAD_SEAT_DEPTH_MM,
                    tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
                )
            )
        lug = pad if lug is None else lug.union(pad)

    # Broad flat XY shoulders increase lug root area while remaining support-free.
    shoulder = _local_box(
        LUG_ROOT_SHOULDER_RADIAL_MM,
        LUG_ROOT_SHOULDER_TANGENT_MM,
        LUG_HEIGHT_MM,
        sum(p.seam_bolt_radii_mm) / 2.0,
        seam_angle,
        z,
        tangent_offset=-1.5,
    )
    lug = lug.union(shoulder)

    # One short label on the outer lug only, away from screw holes.
    lug = _engrave_local(
        lug,
        label,
        p.seam_bolt_radii_mm[1],
        seam_angle,
        z + LUG_HEIGHT_MM,
        tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM + 9.0,
        size=6.5,
        p=p,
    )
    return lug


def _add_receiving_nut_features(
    body: cq.Workplane,
    seam_angle: float,
    z_base: float,
    thickness: float,
    nut_from_top: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    for radius in p.seam_bolt_radii_mm:
        body = body.cut(
            _local_cylinder(
                p.m3_clearance_diameter_mm,
                thickness + 0.6,
                radius,
                seam_angle,
                z_base - 0.3,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )

        if nut_from_top:
            lip_z = z_base + thickness - p.captured_nut_lip_depth_mm
            pocket_z = lip_z - p.captured_nut_pocket_depth_mm
        else:
            lip_z = z_base - 0.05
            pocket_z = z_base + p.captured_nut_lip_depth_mm

        body = body.cut(
            _hex_cut(
                p.captured_nut_lip_across_flats_mm,
                p.captured_nut_lip_depth_mm + 0.15,
                radius,
                seam_angle,
                lip_z,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )
        body = body.cut(
            _hex_cut(
                p.captured_nut_across_flats_mm,
                p.captured_nut_pocket_depth_mm,
                radius,
                seam_angle,
                pocket_z,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )
    return body


def _add_seam_locator_features(
    body: cq.Workplane,
    receive_seam: float,
    outgoing_seam: float,
    z_base: float,
    height: float,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    tongue = _local_box(
        LOCATOR_RADIAL_LEN_MM,
        LOCATOR_TONGUE_TANGENT_MM,
        height,
        LOCATOR_RADIUS_MM,
        outgoing_seam,
        z_base,
        tangent_offset=LOCATOR_TANGENT_OFFSET_MM,
    )
    socket = _local_box(
        LOCATOR_RADIAL_LEN_MM + 2.0 * LOCATOR_CLEARANCE_PER_SIDE_MM,
        LOCATOR_SOCKET_TANGENT_MM + 2.0 * LOCATOR_CLEARANCE_PER_SIDE_MM,
        height + 0.6,
        LOCATOR_RADIUS_MM,
        receive_seam,
        z_base - 0.3,
        tangent_offset=LOCATOR_TANGENT_OFFSET_MM,
    )
    return body.union(tongue).cut(socket)


def _add_upper_top_bolt_features(
    body: cq.Workplane,
    seam_angle: float,
    z_base: float,
    thickness: float,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    for radius in p.seam_bolt_radii_mm:
        body = body.cut(
            _local_cylinder(
                p.m3_clearance_diameter_mm,
                thickness + 0.8,
                radius,
                seam_angle,
                z_base - 0.4,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )
        body = body.cut(
            _local_cylinder(
                M3_HEAD_RECESS_DIAMETER_MM,
                M3_HEAD_RECESS_DEPTH_MM + 0.2,
                radius,
                seam_angle,
                z_base + thickness - M3_HEAD_RECESS_DEPTH_MM,
                tangent_offset=LUG_RECEIVER_TANGENT_OFFSET_MM,
            )
        )
    return body


def _local_annular_ring(
    outer_diameter: float,
    inner_diameter: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
) -> cq.Workplane:
    ring = (
        cq.Workplane("XY")
        .circle(outer_diameter / 2.0)
        .extrude(height)
        .cut(cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(height + 0.4).translate((0.0, 0.0, -0.2)))
        .translate((radius, 0.0, z))
    )
    return ring.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def _upper_pad_round_cup(angle_deg: float, p: ConceptV2Params = P) -> cq.Workplane:
    inner_diameter = UPPER_PAD_ROUND_DIAMETER_MM + 2.0 * UPPER_PAD_CUP_CLEARANCE_PER_SIDE_MM
    outer_diameter = inner_diameter + 2.0 * UPPER_PAD_CUP_WALL_MM
    return _local_annular_ring(
        outer_diameter,
        inner_diameter,
        UPPER_PAD_CUP_HEIGHT_MM,
        p.sensor_radius_mm,
        angle_deg,
        p.upper_z_mm - UPPER_PAD_CUP_HEIGHT_MM,
    )


def upper_pad(p: ConceptV2Params = P) -> cq.Workplane:
    return cq.Workplane("XY").circle(UPPER_PAD_ROUND_DIAMETER_MM / 2.0).extrude(p.upper_pad_height_mm)


def lower_segment(index: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    segment = _annular_sector(
        p.lower_outer_diameter_mm / 2.0,
        p.lower_inner_diameter_mm / 2.0,
        p.lower_thickness_mm,
        start,
        end,
    )
    mid = _segment_mid_angle(index, p)
    segment = segment.union(_sensor_station_lower_features(mid, p))

    receive_seam = index * (360.0 / p.segment_count)
    outgoing_seam = (index + 1) * (360.0 / p.segment_count)
    segment = _add_receiving_nut_features(segment, receive_seam, 0.0, p.lower_thickness_mm, False, p)
    segment = _add_seam_locator_features(segment, receive_seam, outgoing_seam, 0.0, p.lower_thickness_mm, p)
    segment = segment.union(_lug_body(outgoing_seam, p.lower_thickness_mm, "M3", upper_lug=False, p=p))
    segment = _engrave_local(segment, "LOWER", 126.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "OUT", 151.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    return segment


def upper_segment(index: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.upper_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segment = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
    segment = _add_support_grate_receivers(segment, index, inner_r, p)
    segment = segment.union(_annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, start, end, p.upper_z_mm + p.upper_thickness_mm))

    mid = _segment_mid_angle(index, p)
    land = _local_cylinder(UPPER_PAD_ROUND_DIAMETER_MM + 8.0, 1.0, p.sensor_radius_mm, mid, p.upper_z_mm)
    segment = segment.union(land).union(_upper_pad_round_cup(mid, p))

    receive_seam = index * (360.0 / p.segment_count)
    outgoing_seam = (index + 1) * (360.0 / p.segment_count)
    segment = _add_upper_top_bolt_features(segment, receive_seam, p.upper_z_mm, p.upper_thickness_mm, p)
    segment = _add_seam_locator_features(segment, receive_seam, outgoing_seam, p.upper_z_mm, p.upper_thickness_mm, p)
    segment = segment.union(_lug_body(outgoing_seam, p.upper_z_mm - LUG_HEIGHT_MM, "M3", upper_lug=True, p=p))
    segment = _engrave_local(segment, "UPPER", 124.0, mid, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    return segment


def _m3_nut_visual(z: float, p: ConceptV2Params = P) -> cq.Workplane:
    diameter = 2.0 * p.captured_nut_across_flats_mm / math.sqrt(3.0)
    nut = cq.Workplane("XY").polygon(6, diameter).extrude(2.4).rotate((0, 0, 0), (0, 0, 1), 30)
    through_hole = cq.Workplane("XY").circle(1.6).extrude(3.0).translate((0, 0, -0.3))
    return nut.cut(through_hole).translate((0, 0, z))


def _m3_button_bolt_visual(lower: bool, p: ConceptV2Params = P) -> cq.Workplane:
    if lower:
        # Lower bolts install from above. The head sits in the shallow top-side
        # seat and the shaft points downward into the underside captured nut.
        head_z = p.lower_thickness_mm + LUG_HEIGHT_MM - LOWER_HEAD_SEAT_DEPTH_MM
        shaft_z = 1.0
        shaft_h = head_z - shaft_z
    else:
        # Upper bolts install from above. The head is recessed into the top
        # counterbore and the shaft points downward to the underside nut.
        head_z = p.upper_z_mm + p.upper_thickness_mm - M3_BUTTON_HEAD_HEIGHT_MM
        shaft_z = p.upper_z_mm - LUG_HEIGHT_MM
        shaft_h = head_z - shaft_z

    head = cq.Workplane("XY").circle(M3_BUTTON_HEAD_DIAMETER_MM / 2.0).extrude(M3_BUTTON_HEAD_HEIGHT_MM).translate((0, 0, head_z))
    shaft = cq.Workplane("XY").circle(1.5).extrude(shaft_h).translate((0, 0, shaft_z))
    return head.union(shaft)


def seam_fastener_visuals(lower: bool, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    bodies = []
    nut_z = 0.85 if lower else p.upper_z_mm - LUG_HEIGHT_MM + 0.85
    for i in range(p.segment_count):
        seam_angle = (i + 1) * (360.0 / p.segment_count)
        for j, radius in enumerate(p.seam_bolt_radii_mm):
            bolt = _m3_button_bolt_visual(lower, p)
            nut = _m3_nut_visual(nut_z, p)
            bolt = bolt.translate((radius, LUG_RECEIVER_TANGENT_OFFSET_MM, 0)).rotate((0, 0, 0), (0, 0, 1), seam_angle)
            nut = nut.translate((radius, LUG_RECEIVER_TANGENT_OFFSET_MM, 0)).rotate((0, 0, 0), (0, 0, 1), seam_angle)
            layer = "lower" if lower else "upper"
            bodies.append((f"{layer}_m3_button_bolt_{i}_{j}", bolt))
            bodies.append((f"{layer}_captured_m3_nut_{i}_{j}", nut))
    return bodies


def seam_bolt_head_visuals(lower: bool, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    # Backward-compatible alias for older callers; now returns complete fastener
    # visuals, not just heads.
    return seam_fastener_visuals(lower, p)


def sensor_stack_parts(index: int, angle_deg: float, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    h = _sensor_stack_heights(p)
    lower_p = lower_pad(p).translate((p.sensor_radius_mm, 0, h["lower_pad_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    sensor = sensor_placeholder(p).translate((p.sensor_radius_mm, 0, h["sensor_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    upper_p = upper_pad(p).translate((p.sensor_radius_mm, 0, h["upper_pad_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return [
        (f"sensor_{index}_lower_pad", lower_p),
        (f"sensor_{index}_placeholder", sensor),
        (f"sensor_{index}_upper_pad", upper_p),
    ]


def concept_v4_parts(p: ConceptV2Params = P, include_fastener_visuals: bool = True) -> list[tuple[str, cq.Workplane]]:
    parts: list[tuple[str, cq.Workplane]] = []
    for i in range(p.segment_count):
        parts.append((f"lower_segment_{i}", lower_segment(i, p)))
    for i in range(p.segment_count):
        parts.append((f"upper_segment_{i}", upper_segment(i, p)))
    for i in range(p.segment_count):
        parts.extend(sensor_stack_parts(i, _segment_mid_angle(i, p), p))
    parts.append(("support_grate_bar_x", support_grate_bar_x(p)))
    parts.append(("support_grate_bar_y", support_grate_bar_y(p)))
    if include_fastener_visuals:
        parts.extend(seam_fastener_visuals(lower=True, p=p))
        parts.extend(seam_fastener_visuals(lower=False, p=p))
    return parts


def concept_v4_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v4 integrated joining")
    for name, body in concept_v4_parts(p, include_fastener_visuals=True):
        assembly.add(body, name=name)
    return assembly


def concept_v4_exploded_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v4 exploded")
    for i in range(p.segment_count):
        assembly.add(lower_segment(i, p), name=f"lower_segment_{i}")
        assembly.add(upper_segment(i, p).translate((0, 0, 30.0)), name=f"upper_segment_{i}_raised")
    for i in range(p.segment_count):
        for name, body in sensor_stack_parts(i, _segment_mid_angle(i, p), p):
            lift = 0.0
            if "upper_pad" in name:
                lift = 20.0
            elif "placeholder" in name:
                lift = 12.0
            assembly.add(body.translate((0, 0, lift)), name=name)
    assembly.add(support_grate_bar_x(p).translate((0, 0, 45.0)), name="support_grate_bar_x_raised")
    assembly.add(support_grate_bar_y(p).translate((0, 0, 51.0)), name="support_grate_bar_y_raised")
    for name, body in seam_fastener_visuals(lower=True, p=p):
        assembly.add(body.translate((0, 0, 8.0)), name=f"{name}_raised")
    for name, body in seam_fastener_visuals(lower=False, p=p):
        assembly.add(body.translate((0, 0, 52.0)), name=f"{name}_raised")
    return assembly


def concept_v4_one_quadrant_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v4 one quadrant")
    assembly.add(lower_segment(0, p), name="lower_segment_0_integrated_lugs")
    assembly.add(upper_segment(0, p), name="upper_segment_0_integrated_lugs")
    for name, body in sensor_stack_parts(0, _segment_mid_angle(0, p), p):
        assembly.add(body, name=name)
    for name, body in seam_fastener_visuals(lower=True, p=p):
        if name.startswith("lower_m3_button_bolt_0") or name.startswith("lower_captured_m3_nut_0") or name.startswith("lower_m3_button_bolt_3") or name.startswith("lower_captured_m3_nut_3"):
            assembly.add(body, name=name)
    for name, body in seam_fastener_visuals(lower=False, p=p):
        if name.startswith("upper_m3_button_bolt_0") or name.startswith("upper_captured_m3_nut_0") or name.startswith("upper_m3_button_bolt_3") or name.startswith("upper_captured_m3_nut_3"):
            assembly.add(body, name=name)
    assembly.add(support_grate_bar_x(p), name="support_grate_bar_x")
    assembly.add(support_grate_bar_y(p), name="support_grate_bar_y")
    return assembly


def _crop_to_printable_coupon(body: cq.Workplane, seam_angle: float, z_min: float, height: float) -> cq.Workplane:
    crop = _local_box(96.0, 86.0, height, 134.0, seam_angle, z_min, tangent_offset=2.0)
    coupon = body.intersect(crop)
    bb = coupon.val().BoundingBox()
    return coupon.translate((-(bb.xmin + bb.xmax) / 2.0, -(bb.ymin + bb.ymax) / 2.0, -bb.zmin))


def concept_v4_lower_integrated_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Workplane:
    seam_angle = 90.0
    pair = lower_segment(0, p).union(lower_segment(1, p))
    coupon = _crop_to_printable_coupon(pair, seam_angle, 0.0, p.lower_thickness_mm + LUG_HEIGHT_MM)
    bb = coupon.val().BoundingBox()
    coupon = _engrave_top(coupon, "LOWER", -28.0, 24.0, bb.zmax, size=7.0, p=p)
    coupon = _engrave_top(coupon, "M3", 18.0, 24.0, bb.zmax, size=7.0, p=p)
    coupon = _engrave_top(coupon, "KEY", -4.0, -24.0, bb.zmax, size=7.0, p=p)
    return coupon


def concept_v4_upper_integrated_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Workplane:
    seam_angle = 90.0
    pair = upper_segment(0, p).union(upper_segment(1, p))
    coupon = _crop_to_printable_coupon(pair, seam_angle, p.upper_z_mm - LUG_HEIGHT_MM, p.upper_thickness_mm + LUG_HEIGHT_MM + p.lip_height_mm)
    bb = coupon.val().BoundingBox()
    coupon = _engrave_top(coupon, "UPPER", -28.0, 24.0, bb.zmax, size=7.0, p=p)
    coupon = _engrave_top(coupon, "M3", 18.0, 24.0, bb.zmax, size=7.0, p=p)
    coupon = _engrave_top(coupon, "KEY", -4.0, -24.0, bb.zmax, size=7.0, p=p)
    return coupon
