"""Concept v3 print-optimized SaltScale candidate.

This is a print-efficiency variant of concept_v2. It preserves the validated
four-sensor floating architecture, captured M3 nut pockets, bolted bridge
plates, v3-style sensor locator, engraved label standard, and 0.4 mm per-side
support-grate clearance.

Main change from concept_v2: the upper and lower rings are split into eight
45-degree sectors instead of four 90-degree quadrants. Four alternating sectors
carry sensor stations; four are plain filler/alignment sectors. The support
grate is split into two interlocking half-lap bars so it can be nested with
other plates instead of requiring one large square-ish print by itself.
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
    upper_pad,
)


P = replace(
    ConceptV2Params(),
    segment_count=8,
    seam_gap_deg=1.2,
    seam_feature_inset_deg=3.5,
    seam_bridge_tangent_len_mm=30.0,
)


def _segment_angles(index: int, p: ConceptV2Params = P) -> tuple[float, float]:
    span = 360.0 / p.segment_count
    start = index * span + p.seam_gap_deg / 2.0
    end = (index + 1) * span - p.seam_gap_deg / 2.0
    return start, end


def _segment_mid_angle(index: int, p: ConceptV2Params = P) -> float:
    start, end = _segment_angles(index, p)
    return (start + end) / 2.0


def _add_captured_nut_seam_features_v3(
    body: cq.Workplane,
    index: int,
    z_base: float,
    thickness: float,
    nut_from_top: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    feature_angles = (start + p.seam_feature_inset_deg, end - p.seam_feature_inset_deg)

    for angle in feature_angles:
        for radius in p.seam_bolt_radii_mm:
            body = body.union(_local_cylinder(p.seam_boss_diameter_mm, thickness, radius, angle, z_base))
            body = body.cut(_local_cylinder(p.m3_clearance_diameter_mm, thickness + 0.6, radius, angle, z_base - 0.3))

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
                    angle,
                    lip_z,
                )
            )
            body = body.cut(
                _hex_cut(
                    p.captured_nut_across_flats_mm,
                    p.captured_nut_pocket_depth_mm,
                    radius,
                    angle,
                    pocket_z,
                )
            )
    return body


def lower_sensor_segment(index: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
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
    segment = _add_captured_nut_seam_features_v3(segment, index, 0.0, p.lower_thickness_mm, False, p)
    segment = _engrave_local(segment, "LOWER", 127.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "SENSOR", 101.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    return segment


def lower_plain_segment(index: int = 1, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    segment = _annular_sector(
        p.lower_outer_diameter_mm / 2.0,
        p.lower_inner_diameter_mm / 2.0,
        p.lower_thickness_mm,
        start,
        end,
    )
    segment = _add_captured_nut_seam_features_v3(segment, index, 0.0, p.lower_thickness_mm, False, p)
    mid = _segment_mid_angle(index, p)
    segment = _engrave_local(segment, "LOWER", 127.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "PLAIN", 101.0, mid, p.lower_thickness_mm, size=7.0, p=p)
    return segment


def upper_sensor_segment(index: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.upper_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segment = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
    segment = _add_support_grate_receivers(segment, index, inner_r, p)
    segment = segment.union(_annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, start, end, p.upper_z_mm + p.upper_thickness_mm))

    mid = _segment_mid_angle(index, p)
    land = _local_box(p.upper_pad_size_mm + 4.0, p.upper_pad_size_mm + 4.0, 1.0, p.sensor_radius_mm, mid, p.upper_z_mm)
    segment = segment.union(land)
    segment = _add_captured_nut_seam_features_v3(segment, index, p.upper_z_mm, p.upper_thickness_mm, True, p)
    segment = _engrave_local(segment, "UPPER", 126.0, mid, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "SENSOR", 101.0, mid, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    return segment


def upper_plain_segment(index: int = 1, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.upper_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segment = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
    segment = _add_support_grate_receivers(segment, index, inner_r, p)
    segment = segment.union(_annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, start, end, p.upper_z_mm + p.upper_thickness_mm))
    segment = _add_captured_nut_seam_features_v3(segment, index, p.upper_z_mm, p.upper_thickness_mm, True, p)
    mid = _segment_mid_angle(index, p)
    segment = _engrave_local(segment, "UPPER", 126.0, mid, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "PLAIN", 101.0, mid, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    return segment


def _bridge_plate_local(label: str, p: ConceptV2Params = P) -> cq.Workplane:
    bridge = cq.Workplane("XY").box(
        p.seam_bridge_radial_len_mm,
        p.seam_bridge_tangent_len_mm,
        p.seam_bridge_height_mm,
        centered=(True, True, False),
    )
    for delta in (-p.seam_feature_inset_deg, p.seam_feature_inset_deg):
        for radius in p.seam_bolt_radii_mm:
            x = radius * math.cos(math.radians(delta)) - p.seam_bridge_radius_mm
            y = radius * math.sin(math.radians(delta))
            cut = cq.Workplane("XY").circle(p.m3_clearance_diameter_mm / 2.0).extrude(p.seam_bridge_height_mm + 0.6).translate((x, y, -0.3))
            bridge = bridge.cut(cut)
    bridge = _engrave_top(bridge, label, -17.0, 8.0, p.seam_bridge_height_mm, size=6.8, p=p)
    bridge = _engrave_top(bridge, "M3", 16.0, -8.0, p.seam_bridge_height_mm, p=p)
    return bridge


def lower_bridge_plate(p: ConceptV2Params = P) -> cq.Workplane:
    return _bridge_plate_local("LOWER", p)


def upper_bridge_plate(p: ConceptV2Params = P) -> cq.Workplane:
    return _bridge_plate_local("UPPER", p)


def _place_bridge_plate(bridge: cq.Workplane, seam_angle: float, z: float, p: ConceptV2Params = P) -> cq.Workplane:
    return bridge.translate((p.seam_bridge_radius_mm, 0.0, z)).rotate((0, 0, 0), (0, 0, 1), seam_angle)


def lower_seam_bridge(seam_angle: float, p: ConceptV2Params = P) -> cq.Workplane:
    return _place_bridge_plate(lower_bridge_plate(p), seam_angle, p.lower_thickness_mm, p)


def upper_seam_bridge(seam_angle: float, p: ConceptV2Params = P) -> cq.Workplane:
    return _place_bridge_plate(upper_bridge_plate(p), seam_angle, p.upper_z_mm - p.seam_bridge_height_mm, p)


def support_grate_bar_x(p: ConceptV2Params = P) -> cq.Workplane:
    bar = cq.Workplane("XY").box(p.grate_arm_length_mm, p.grate_arm_width_mm, p.grate_thickness_mm, centered=(True, True, False))
    # Half-lap removes the top half at the center. Bar Y drops into this notch.
    notch = cq.Workplane("XY").box(p.grate_arm_width_mm + 0.8, p.grate_arm_width_mm + 0.8, p.grate_thickness_mm / 2.0 + 0.1, centered=(True, True, False)).translate((0, 0, p.grate_thickness_mm / 2.0))
    bar = bar.cut(notch)
    bar = _engrave_top(bar, "GRATE", -30.0, 0.0, p.grate_thickness_mm, size=7.0, p=p)
    bar = _engrave_top(bar, "X", 35.0, 0.0, p.grate_thickness_mm, size=7.0, p=p)
    return bar.translate((0, 0, p.grate_z_mm))


def support_grate_bar_y(p: ConceptV2Params = P) -> cq.Workplane:
    bar = cq.Workplane("XY").box(p.grate_arm_width_mm, p.grate_arm_length_mm, p.grate_thickness_mm, centered=(True, True, False))
    # Half-lap removes the bottom half at the center.
    notch = cq.Workplane("XY").box(p.grate_arm_width_mm + 0.8, p.grate_arm_width_mm + 0.8, p.grate_thickness_mm / 2.0 + 0.1, centered=(True, True, False)).translate((0, 0, -0.1))
    bar = bar.cut(notch)
    bar = _engrave_top(bar, "GRATE", 0.0, -30.0, p.grate_thickness_mm, size=7.0, p=p)
    bar = _engrave_top(bar, "Y", 0.0, 35.0, p.grate_thickness_mm, size=7.0, p=p)
    return bar.translate((0, 0, p.grate_z_mm))


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


def concept_v3_parts(p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    parts: list[tuple[str, cq.Workplane]] = []
    for i in range(p.segment_count):
        if i % 2 == 0:
            parts.append((f"lower_sensor_segment_{i}", lower_sensor_segment(i, p)))
            parts.append((f"upper_sensor_segment_{i}", upper_sensor_segment(i, p)))
        else:
            parts.append((f"lower_plain_segment_{i}", lower_plain_segment(i, p)))
            parts.append((f"upper_plain_segment_{i}", upper_plain_segment(i, p)))

    for sensor_i, seg_i in enumerate((0, 2, 4, 6)):
        parts.extend(sensor_stack_parts(sensor_i, _segment_mid_angle(seg_i, p), p))

    for i in range(p.segment_count):
        seam_angle = i * (360.0 / p.segment_count)
        parts.append((f"lower_bridge_{i}", lower_seam_bridge(seam_angle, p)))
        parts.append((f"upper_bridge_{i}", upper_seam_bridge(seam_angle, p)))

    parts.append(("support_grate_bar_x", support_grate_bar_x(p)))
    parts.append(("support_grate_bar_y", support_grate_bar_y(p)))
    return parts


def concept_v3_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v3 print optimized")
    for name, body in concept_v3_parts(p):
        assembly.add(body, name=name)
    return assembly


def concept_v3_exploded_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v3 exploded")
    for i in range(p.segment_count):
        if i % 2 == 0:
            assembly.add(lower_sensor_segment(i, p), name=f"lower_sensor_segment_{i}")
            assembly.add(upper_sensor_segment(i, p).translate((0, 0, 30.0)), name=f"upper_sensor_segment_{i}_raised")
        else:
            assembly.add(lower_plain_segment(i, p), name=f"lower_plain_segment_{i}")
            assembly.add(upper_plain_segment(i, p).translate((0, 0, 30.0)), name=f"upper_plain_segment_{i}_raised")

    for sensor_i, seg_i in enumerate((0, 2, 4, 6)):
        for name, body in sensor_stack_parts(sensor_i, _segment_mid_angle(seg_i, p), p):
            lift = 0.0
            if "upper_pad" in name:
                lift = 20.0
            elif "placeholder" in name:
                lift = 12.0
            assembly.add(body.translate((0, 0, lift)), name=name)

    for i in range(p.segment_count):
        seam_angle = i * (360.0 / p.segment_count)
        assembly.add(lower_seam_bridge(seam_angle, p).translate((0, 0, 8.0)), name=f"lower_bridge_{i}_raised")
        assembly.add(upper_seam_bridge(seam_angle, p).translate((0, 0, 22.0)), name=f"upper_bridge_{i}_raised")

    assembly.add(support_grate_bar_x(p).translate((0, 0, 45.0)), name="support_grate_bar_x_raised")
    assembly.add(support_grate_bar_y(p).translate((0, 0, 51.0)), name="support_grate_bar_y_raised")
    return assembly


def concept_v3_one_section_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v3 one sensor section")
    sensor_i = 0
    plain_i = 1
    sensor_angle = _segment_mid_angle(sensor_i, p)
    assembly.add(lower_sensor_segment(sensor_i, p), name="lower_sensor_segment_0")
    assembly.add(lower_plain_segment(plain_i, p), name="lower_plain_segment_1")
    assembly.add(upper_sensor_segment(sensor_i, p), name="upper_sensor_segment_0")
    assembly.add(upper_plain_segment(plain_i, p), name="upper_plain_segment_1")
    for name, body in sensor_stack_parts(0, sensor_angle, p):
        assembly.add(body, name=name)
    assembly.add(lower_seam_bridge(0.0, p), name="lower_bridge_left")
    assembly.add(lower_seam_bridge(45.0, p), name="lower_bridge_right")
    assembly.add(upper_seam_bridge(0.0, p), name="upper_bridge_left")
    assembly.add(upper_seam_bridge(45.0, p), name="upper_bridge_right")
    assembly.add(support_grate_bar_x(p), name="support_grate_bar_x")
    assembly.add(support_grate_bar_y(p), name="support_grate_bar_y")
    return assembly
