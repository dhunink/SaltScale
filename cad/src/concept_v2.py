"""Concept v2: prototype-candidate four-sensor annular SaltScale.

This is a clean-sheet successor to concept_v1, not a continuation of
platform_v6. It keeps the preferred floating annular architecture and adds
prototype-level details:

- realistic replaceable 38 x 38 x 12 mm sensor stations
- lower-only and upper-only segment joining features
- validated captured M3 nut pockets, M3 bolt holes, and printed seam bridge plates
- low-profile sensor locator geometry based on sensor_station_locator_v3
- removable upper support grate for uncertain salt-container bottoms

The model still avoids electronics and firmware packaging.
"""

from dataclasses import dataclass
import math

import cadquery as cq


@dataclass(frozen=True)
class ConceptV2Params:
    # Envelope and segmentation
    outer_diameter_mm: float = 320.0
    tank_diameter_mm: float = 290.0
    centering_lip_inner_diameter_mm: float = 300.0
    segment_count: int = 4
    seam_gap_deg: float = 1.4

    # Lower base
    lower_outer_diameter_mm: float = 320.0
    lower_inner_diameter_mm: float = 145.0
    lower_thickness_mm: float = 8.0

    # Floating upper carrier
    upper_outer_diameter_mm: float = 308.0
    upper_inner_diameter_mm: float = 145.0
    upper_z_mm: float = 25.0
    upper_thickness_mm: float = 8.0
    lip_wall_thickness_mm: float = 4.0
    lip_height_mm: float = 6.0

    # Removable upper-only support grate
    grate_z_mm: float = 29.0
    grate_thickness_mm: float = 4.0
    grate_arm_length_mm: float = 178.0
    grate_arm_width_mm: float = 22.0
    grate_hub_diameter_mm: float = 48.0
    support_grate_clearance_per_side_mm: float = 0.4
    support_grate_receiver_depth_mm: float = 4.0
    support_grate_receiver_overlap_mm: float = 22.0

    # Sensor station
    sensor_radius_mm: float = 112.0
    sensor_size_mm: float = 38.0
    sensor_height_mm: float = 12.0
    sensor_clearance_mm: float = 0.7
    lower_pad_size_mm: float = 44.0
    lower_pad_height_mm: float = 2.0
    upper_pad_size_mm: float = 56.0
    upper_pad_height_mm: float = 3.0
    guide_wall_thickness_mm: float = 3.0
    guide_wall_height_mm: float = 12.0
    overload_stop_diameter_mm: float = 7.0
    overload_gap_mm: float = 1.0

    # Same-layer segment joining: validated default is M3 bolt + standard nut + printed bridge.
    m3_clearance_diameter_mm: float = 3.4
    captured_nut_across_flats_mm: float = 5.9
    captured_nut_lip_across_flats_mm: float = 5.35
    captured_nut_pocket_depth_mm: float = 3.0
    captured_nut_lip_depth_mm: float = 0.7
    seam_boss_diameter_mm: float = 13.0
    seam_bolt_radii_mm: tuple[float, float] = (118.0, 146.0)
    seam_feature_inset_deg: float = 4.5
    seam_bridge_radius_mm: float = 132.0
    seam_bridge_radial_len_mm: float = 64.0
    seam_bridge_tangent_len_mm: float = 32.0
    seam_bridge_height_mm: float = 4.0

    # Labels: validated PETG default. Use engraved labels only on non-contact surfaces.
    label_text_height_mm: float = 7.0
    label_engrave_depth_mm: float = 0.8

    # Legacy-only compatibility for archived superseded coupons.
    # These are not used by the active concept_v2 segment geometry.
    m3_insert_diameter_mm: float = 4.8
    m3_insert_depth_mm: float = 5.0
    dowel_diameter_mm: float = 4.2
    dowel_socket_depth_mm: float = 6.0


P = ConceptV2Params()


def _annular_sector(
    outer_r: float,
    inner_r: float,
    height: float,
    start_deg: float,
    end_deg: float,
    z: float = 0.0,
    steps: int = 36,
) -> cq.Workplane:
    points = []
    for i in range(steps + 1):
        a = math.radians(start_deg + (end_deg - start_deg) * i / steps)
        points.append((outer_r * math.cos(a), outer_r * math.sin(a)))
    for i in range(steps, -1, -1):
        a = math.radians(start_deg + (end_deg - start_deg) * i / steps)
        points.append((inner_r * math.cos(a), inner_r * math.sin(a)))
    return cq.Workplane("XY").polyline(points).close().extrude(height).translate((0, 0, z))


def _local_box(
    radial_len: float,
    tangent_len: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    body = (
        cq.Workplane("XY")
        .box(radial_len, tangent_len, height, centered=(True, True, False))
        .translate((radius + radial_offset, tangent_offset, z))
    )
    return body.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def _local_cylinder(
    diameter: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    body = (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(height)
        .translate((radius + radial_offset, tangent_offset, z))
    )
    return body.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def _hex_cut(
    across_flats: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    diameter = 2.0 * across_flats / math.sqrt(3.0)
    body = (
        cq.Workplane("XY")
        .polygon(6, diameter)
        .extrude(height)
        .rotate((0, 0, 0), (0, 0, 1), 30)
        .translate((radius + radial_offset, tangent_offset, z))
    )
    return body.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def _engrave_top(
    body: cq.Workplane,
    label: str,
    x: float,
    y: float,
    z: float,
    size: float | None = None,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    text_size = p.label_text_height_mm if size is None else size
    text = cq.Workplane("XY").workplane(offset=z).text(label, text_size, -p.label_engrave_depth_mm, combine=False)
    return body.cut(text.translate((x, y, 0.0)))


def _engrave_local(
    body: cq.Workplane,
    label: str,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
    size: float | None = None,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    text_size = p.label_text_height_mm if size is None else size
    text = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .text(label, text_size, -p.label_engrave_depth_mm, combine=False)
        .translate((radius + radial_offset, tangent_offset, 0.0))
    )
    return body.cut(text.rotate((0, 0, 0), (0, 0, 1), angle_deg))


def _slot_cut(
    radial_len: float,
    tangent_len: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    return _local_box(radial_len, tangent_len, height, radius, angle_deg, z, radial_offset, tangent_offset)


def _segment_angles(quadrant: int, p: ConceptV2Params = P) -> tuple[float, float]:
    start = quadrant * 90.0 + p.seam_gap_deg / 2.0
    end = (quadrant + 1) * 90.0 - p.seam_gap_deg / 2.0
    return start, end


def _add_captured_nut_seam_features(
    body: cq.Workplane,
    quadrant: int,
    z_base: float,
    thickness: float,
    nut_from_top: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
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


def _sensor_stack_heights(p: ConceptV2Params = P) -> dict[str, float]:
    lower_pad_z = p.lower_thickness_mm
    sensor_z = lower_pad_z + p.lower_pad_height_mm
    upper_pad_z = sensor_z + p.sensor_height_mm
    stop_top_z = upper_pad_z - p.overload_gap_mm
    return {
        "lower_pad_z": lower_pad_z,
        "sensor_z": sensor_z,
        "upper_pad_z": upper_pad_z,
        "upper_carrier_z": upper_pad_z + p.upper_pad_height_mm,
        "stop_top_z": stop_top_z,
    }


def _sensor_station_lower_features(angle_deg: float, p: ConceptV2Params = P) -> cq.Workplane:
    h = _sensor_stack_heights(p)
    z = p.lower_thickness_mm
    locator_h = 5.0
    wall_t = p.guide_wall_thickness_mm
    total_clearance = 1.0
    cavity = p.sensor_size_mm + total_clearance
    half = cavity / 2.0

    # Low, broken v3-style locator features. They prevent sliding/rotation while
    # keeping the outer side open for service and staying below upper-pad contact.
    side_len = 19.0
    side_x = -3.0
    side_y = half + wall_t / 2.0
    upper_side = _local_box(side_len, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=side_x, tangent_offset=side_y)
    lower_side = _local_box(side_len, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=side_x, tangent_offset=-side_y)

    inner_x = -(half + wall_t / 2.0)
    inner_stop = _local_box(wall_t, 16.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=inner_x)
    inner_top = _local_cylinder(6.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=inner_x, tangent_offset=13.5)
    inner_bottom = _local_cylinder(6.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=inner_x, tangent_offset=-13.5)

    outer_x = half + wall_t / 2.0
    outer_top = _local_cylinder(6.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x, tangent_offset=14.0)
    outer_bottom = _local_cylinder(6.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x, tangent_offset=-14.0)
    outer_top_tail = _local_box(8.0, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x - 4.0, tangent_offset=14.0)
    outer_bottom_tail = _local_box(8.0, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x - 4.0, tangent_offset=-14.0)

    stop_h = h["stop_top_z"] - z
    stop_offset = 31.0
    stops = []
    for radial_offset in (-stop_offset, stop_offset):
        for tangent_offset in (-stop_offset, stop_offset):
            stops.append(
                _local_cylinder(
                    p.overload_stop_diameter_mm,
                    stop_h,
                    p.sensor_radius_mm,
                    angle_deg,
                    z,
                    radial_offset=radial_offset,
                    tangent_offset=tangent_offset,
                )
            )

    body = upper_side.union(lower_side).union(inner_stop).union(inner_top).union(inner_bottom)
    body = body.union(outer_top).union(outer_bottom).union(outer_top_tail).union(outer_bottom_tail)
    for stop in stops:
        body = body.union(stop)
    return body


def lower_pad(p: ConceptV2Params = P) -> cq.Workplane:
    return cq.Workplane("XY").box(p.lower_pad_size_mm, p.lower_pad_size_mm, p.lower_pad_height_mm, centered=(True, True, False))


def upper_pad(p: ConceptV2Params = P) -> cq.Workplane:
    return cq.Workplane("XY").box(p.upper_pad_size_mm, p.upper_pad_size_mm, p.upper_pad_height_mm, centered=(True, True, False))


def sensor_placeholder(p: ConceptV2Params = P) -> cq.Workplane:
    body = cq.Workplane("XY").box(p.sensor_size_mm, p.sensor_size_mm, p.sensor_height_mm, centered=(True, True, False))
    cable = cq.Workplane("XY").box(16.0, 4.0, 2.0, centered=(True, True, False)).translate((p.sensor_size_mm / 2.0 + 8.0, 0.0, 4.0))
    return body.union(cable)


def sensor_stack_parts(index: int, angle_deg: float, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    h = _sensor_stack_heights(p)
    lower_p = lower_pad(p).translate((p.sensor_radius_mm, 0, h["lower_pad_z"]))
    sensor = sensor_placeholder(p).translate((p.sensor_radius_mm, 0, h["sensor_z"]))
    upper_p = upper_pad(p).translate((p.sensor_radius_mm, 0, h["upper_pad_z"]))

    lower_p = lower_p.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    sensor = sensor.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    upper_p = upper_p.rotate((0, 0, 0), (0, 0, 1), angle_deg)

    return [
        (f"sensor_{index}_lower_contact_pad", lower_p),
        (f"sensor_{index}_placeholder_with_cable_exit", sensor),
        (f"sensor_{index}_upper_contact_pad", upper_p),
    ]


def lower_segment(quadrant: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
    outer_r = p.lower_outer_diameter_mm / 2.0
    inner_r = p.lower_inner_diameter_mm / 2.0
    segment = _annular_sector(outer_r, inner_r, p.lower_thickness_mm, start, end)

    sensor_angle = quadrant * 90.0 + 45.0
    segment = segment.union(_sensor_station_lower_features(sensor_angle, p))

    # Keep the lower pad on solid base material; guide walls provide lateral location.
    segment = _add_captured_nut_seam_features(segment, quadrant, 0.0, p.lower_thickness_mm, False, p)
    mid_angle = (start + end) / 2.0
    segment = _engrave_local(segment, "LOWER", 126.0, mid_angle, p.lower_thickness_mm, size=7.0, p=p)
    segment = _engrave_local(segment, "OUT", 151.0, mid_angle, p.lower_thickness_mm, size=7.0, p=p)
    return segment



def _add_support_grate_receivers(
    segment: cq.Workplane,
    quadrant: int,
    inner_r: float,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    """Cut upper-only receivers for the removable support-grate cross arms.

    The support grate is a cross-shaped upper-only part. Earlier concept_v2
    receiver cuts only cleared small seam-adjacent tabs, which left a real
    solid overlap between the grate and upper carrier. These full cross-arm
    receivers clear the actual grate footprint using the validated 0.4 mm
    per-side lateral clearance while preserving upper/lower separation.
    """
    slot_width = p.grate_arm_width_mm + 2.0 * p.support_grate_clearance_per_side_mm
    slot_len = p.grate_arm_length_mm + 2.0 * p.support_grate_clearance_per_side_mm
    slot_z = p.upper_z_mm + p.upper_thickness_mm - p.support_grate_receiver_depth_mm
    cut_h = p.support_grate_receiver_depth_mm + 0.4

    horizontal = (
        cq.Workplane("XY")
        .box(slot_len, slot_width, cut_h, centered=(True, True, False))
        .translate((0.0, 0.0, slot_z))
    )
    vertical = (
        cq.Workplane("XY")
        .box(slot_width, slot_len, cut_h, centered=(True, True, False))
        .translate((0.0, 0.0, slot_z))
    )
    return segment.cut(horizontal).cut(vertical)


def upper_segment(quadrant: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.upper_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segment = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
    segment = _add_support_grate_receivers(segment, quadrant, inner_r, p)
    lip = _annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, start, end, p.upper_z_mm + p.upper_thickness_mm)
    segment = segment.union(lip)

    # Small underside contact land for the upper pad. It is part of the floating upper structure.
    sensor_angle = quadrant * 90.0 + 45.0
    land = _local_box(p.upper_pad_size_mm + 4.0, p.upper_pad_size_mm + 4.0, 1.0, p.sensor_radius_mm, sensor_angle, p.upper_z_mm)
    segment = segment.union(land)

    # Top-side captured nut pockets for underside upper-only seam bridge plates.
    segment = _add_captured_nut_seam_features(segment, quadrant, p.upper_z_mm, p.upper_thickness_mm, True, p)
    mid_angle = (start + end) / 2.0
    segment = _engrave_local(segment, "UPPER", 124.0, mid_angle, p.upper_z_mm + p.upper_thickness_mm, size=7.0, p=p)
    return segment


def _bridge_hole_centers(seam_angle: float, p: ConceptV2Params = P) -> list[tuple[float, float, float]]:
    centers = []
    for delta in (-p.seam_feature_inset_deg, p.seam_feature_inset_deg):
        for radius in p.seam_bolt_radii_mm:
            centers.append((radius, seam_angle + delta, delta))
    return centers


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


def support_grate(p: ConceptV2Params = P) -> cq.Workplane:
    arm_a = cq.Workplane("XY").box(p.grate_arm_length_mm, p.grate_arm_width_mm, p.grate_thickness_mm, centered=(True, True, False)).translate((0, 0, p.grate_z_mm))
    arm_b = cq.Workplane("XY").box(p.grate_arm_width_mm, p.grate_arm_length_mm, p.grate_thickness_mm, centered=(True, True, False)).translate((0, 0, p.grate_z_mm))
    hub = cq.Workplane("XY").circle(p.grate_hub_diameter_mm / 2.0).extrude(p.grate_thickness_mm).translate((0, 0, p.grate_z_mm))
    return arm_a.union(arm_b).union(hub)


def sensor_station_coupon(p: ConceptV2Params = P) -> cq.Workplane:
    coupon = cq.Workplane("XY").box(96.0, 96.0, p.lower_thickness_mm, centered=(True, True, False)).translate((p.sensor_radius_mm, 0, 0))
    coupon = coupon.union(_sensor_station_lower_features(0.0, p))
    # Lower pad remains on solid base material; guide walls provide lateral location.
    # Move the coupon so the sensor station is centered on the print.
    return coupon.translate((-p.sensor_radius_mm, 0, 0))


def concept_v2_parts(p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    parts: list[tuple[str, cq.Workplane]] = []
    for q in range(p.segment_count):
        parts.append((f"lower_segment_{q}", lower_segment(q, p)))
    for q in range(p.segment_count):
        parts.append((f"upper_segment_{q}", upper_segment(q, p)))

    for i, angle in enumerate((45.0, 135.0, 225.0, 315.0)):
        parts.extend(sensor_stack_parts(i, angle, p))

    for seam_angle in (0.0, 90.0, 180.0, 270.0):
        parts.append((f"lower_seam_bridge_{int(seam_angle)}", lower_seam_bridge(seam_angle, p)))
        parts.append((f"upper_seam_bridge_{int(seam_angle)}", upper_seam_bridge(seam_angle, p)))

    parts.append(("removable_upper_support_grate", support_grate(p)))
    return parts


def concept_v2_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v2")
    for name, body in concept_v2_parts(p):
        assembly.add(body, name=name)
    return assembly


def concept_v2_exploded_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v2 exploded")
    for q in range(p.segment_count):
        assembly.add(lower_segment(q, p), name=f"lower_segment_{q}")
        assembly.add(upper_segment(q, p).translate((0, 0, 30.0)), name=f"upper_segment_{q}_raised")

    for i, angle in enumerate((45.0, 135.0, 225.0, 315.0)):
        for name, body in sensor_stack_parts(i, angle, p):
            lift = 0.0
            if "upper_contact" in name:
                lift = 20.0
            elif "placeholder" in name:
                lift = 12.0
            assembly.add(body.translate((0, 0, lift)), name=name)

    for seam_angle in (0.0, 90.0, 180.0, 270.0):
        assembly.add(lower_seam_bridge(seam_angle, p).translate((0, 0, 8.0)), name=f"lower_seam_bridge_{int(seam_angle)}_raised")
        assembly.add(upper_seam_bridge(seam_angle, p).translate((0, 0, 22.0)), name=f"upper_seam_bridge_{int(seam_angle)}_raised")

    assembly.add(support_grate(p).translate((0, 0, 45.0)), name="support_grate_raised")
    return assembly



def _m3_bolt_visual(height: float = 16.0, p: ConceptV2Params = P) -> cq.Workplane:
    shaft = cq.Workplane("XY").circle(1.5).extrude(height)
    head = cq.Workplane("XY").circle(3.0).extrude(2.0).translate((0, 0, height))
    return shaft.union(head)


def _m3_nut_visual(p: ConceptV2Params = P) -> cq.Workplane:
    diameter = 2.0 * p.captured_nut_across_flats_mm / math.sqrt(3.0)
    return cq.Workplane("XY").polygon(6, diameter).extrude(2.4).rotate((0, 0, 0), (0, 0, 1), 30)


def _place_local(body: cq.Workplane, radius: float, angle_deg: float, z: float, radial_offset: float = 0.0, tangent_offset: float = 0.0) -> cq.Workplane:
    return body.translate((radius + radial_offset, tangent_offset, z)).rotate((0, 0, 0), (0, 0, 1), angle_deg)

def concept_v2_one_quadrant_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="SaltScale concept_v2 one quadrant")
    q = 0
    assembly.add(lower_segment(q, p), name="lower_segment_0")
    assembly.add(upper_segment(q, p), name="upper_segment_0")
    for name, body in sensor_stack_parts(0, 45.0, p):
        assembly.add(body, name=name)
    assembly.add(lower_seam_bridge(0.0, p), name="lower_bridge_left")
    assembly.add(lower_seam_bridge(90.0, p), name="lower_bridge_right")
    assembly.add(upper_seam_bridge(0.0, p), name="upper_bridge_left")
    assembly.add(upper_seam_bridge(90.0, p), name="upper_bridge_right")
    assembly.add(support_grate(p), name="support_grate_visual_full")
    return assembly



def concept_v2_one_quadrant_exploded_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    """True exploded view of one quadrant with realistic assembly order spacing."""
    assembly = cq.Assembly(name="SaltScale concept_v2 one quadrant exploded")
    q = 0
    sensor_angle = 45.0

    # Vertical stack explosion. XY remains aligned so the load path is obvious.
    z_lower_segment = 0.0
    z_lower_pad = 22.0
    z_sensor = 38.0
    z_upper_pad = 58.0
    z_upper_segment = 82.0
    z_support_grate = 118.0

    assembly.add(lower_segment(q, p).translate((0, 0, z_lower_segment)), name="01_lower_segment_printed")

    h = _sensor_stack_heights(p)
    lower_p = lower_pad(p).translate((p.sensor_radius_mm, 0, z_lower_pad)).rotate((0, 0, 0), (0, 0, 1), sensor_angle)
    sensor = sensor_placeholder(p).translate((p.sensor_radius_mm, 0, z_sensor)).rotate((0, 0, 0), (0, 0, 1), sensor_angle)
    upper_p = upper_pad(p).translate((p.sensor_radius_mm, 0, z_upper_pad)).rotate((0, 0, 0), (0, 0, 1), sensor_angle)
    assembly.add(lower_p, name="02_lower_pad_printed")
    assembly.add(sensor, name="03_sensor_or_placeholder")
    assembly.add(upper_p, name="04_upper_pad_printed")

    upper_lift = z_upper_segment - p.upper_z_mm
    assembly.add(upper_segment(q, p).translate((0, 0, upper_lift)), name="05_upper_segment_printed")
    grate_lift = z_support_grate - p.grate_z_mm
    assembly.add(support_grate(p).translate((0, 0, grate_lift)), name="06_support_grate_printed_0p4_clearance_default")

    # Same-layer seam hardware is pulled outward and upward from each seam.
    for seam_angle, side_name, tangent_shift in ((0.0, "left", -20.0), (90.0, "right", 20.0)):
        lower_bridge = lower_seam_bridge(seam_angle, p).translate((0, 0, 12.0))
        upper_bridge = upper_seam_bridge(seam_angle, p).translate((0, 0, upper_lift - 18.0))
        assembly.add(lower_bridge, name=f"07_lower_bridge_plate_{side_name}_printed")
        assembly.add(upper_bridge, name=f"08_upper_bridge_plate_{side_name}_printed")

        for delta in (-p.seam_feature_inset_deg, p.seam_feature_inset_deg):
            for i, radius in enumerate(p.seam_bolt_radii_mm):
                angle = seam_angle + delta
                # Lower bolts enter from above into underside captured nuts.
                bolt = _place_local(_m3_bolt_visual(14.0, p), radius, angle, p.lower_thickness_mm + 19.0)
                nut = _place_local(_m3_nut_visual(p), radius, angle, -8.0)
                assembly.add(bolt, name=f"09_lower_m3_bolt_{side_name}_{int(delta*10)}_{i}")
                assembly.add(nut, name=f"10_lower_captured_m3_nut_{side_name}_{int(delta*10)}_{i}")

                # Upper bolts enter from below into top-side captured nuts.
                upper_bolt_z = p.upper_z_mm + upper_lift - 23.0
                upper_nut_z = p.upper_z_mm + p.upper_thickness_mm + upper_lift + 8.0
                upper_bolt = _place_local(_m3_bolt_visual(14.0, p).rotate((0, 0, 0), (1, 0, 0), 180), radius, angle, upper_bolt_z)
                upper_nut = _place_local(_m3_nut_visual(p), radius, angle, upper_nut_z)
                assembly.add(upper_bolt, name=f"11_upper_m3_bolt_{side_name}_{int(delta*10)}_{i}")
                assembly.add(upper_nut, name=f"12_upper_captured_m3_nut_{side_name}_{int(delta*10)}_{i}")

    return assembly

def concept_v2_compound(p: ConceptV2Params = P) -> cq.Compound:
    return cq.Compound.makeCompound([body.val() for _, body in concept_v2_parts(p)])


if __name__ == "__main__":
    show_object(concept_v2_compound())  # type: ignore[name-defined]
