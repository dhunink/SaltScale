"""Concept v2: prototype-candidate four-sensor annular SaltScale.

This is a clean-sheet successor to concept_v1, not a continuation of
platform_v6. It keeps the preferred floating annular architecture and adds
prototype-level details:

- realistic replaceable 38 x 38 x 12 mm sensor stations
- lower-only and upper-only segment joining features
- M3 heat-set insert pockets, 4 mm dowel sockets, and seam bridge plates
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

    # Same-layer segment joining
    m3_insert_diameter_mm: float = 4.8
    m3_insert_depth_mm: float = 5.0
    m3_clearance_diameter_mm: float = 3.4
    dowel_diameter_mm: float = 4.2
    dowel_socket_depth_mm: float = 6.0
    seam_boss_diameter_mm: float = 13.0
    seam_insert_radii_mm: tuple[float, float] = (118.0, 146.0)
    seam_dowel_radius_mm: float = 134.0
    seam_feature_inset_deg: float = 4.5
    seam_bridge_radius_mm: float = 124.0
    seam_bridge_radial_len_mm: float = 72.0
    seam_bridge_tangent_len_mm: float = 26.0
    seam_bridge_height_mm: float = 3.0


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


def _add_vertical_insert_features(
    body: cq.Workplane,
    quadrant: int,
    z_base: float,
    thickness: float,
    pocket_from_top: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
    feature_angles = (start + p.seam_feature_inset_deg, end - p.seam_feature_inset_deg)

    for angle in feature_angles:
        for radius in p.seam_insert_radii_mm:
            boss = _local_cylinder(p.seam_boss_diameter_mm, thickness, radius, angle, z_base)
            body = body.union(boss)

            if pocket_from_top:
                pocket_z = z_base + thickness - p.m3_insert_depth_mm
            else:
                pocket_z = z_base
            insert_pocket = _local_cylinder(
                p.m3_insert_diameter_mm,
                p.m3_insert_depth_mm,
                radius,
                angle,
                pocket_z,
            )
            body = body.cut(insert_pocket)

        dowel_boss = _local_cylinder(p.seam_boss_diameter_mm, thickness, p.seam_dowel_radius_mm, angle, z_base)
        body = body.union(dowel_boss)
        if pocket_from_top:
            dowel_z = z_base + thickness - p.dowel_socket_depth_mm
        else:
            dowel_z = z_base
        dowel_socket = _local_cylinder(
            p.dowel_diameter_mm,
            p.dowel_socket_depth_mm,
            p.seam_dowel_radius_mm,
            angle,
            dowel_z,
        )
        body = body.cut(dowel_socket)

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
    locator_span = p.lower_pad_size_mm + 1.2
    wall_clearance = 0.8
    rail_offset = locator_span / 2.0 + wall_clearance + p.guide_wall_thickness_mm / 2.0
    rail_len = p.upper_pad_size_mm + 10.0
    guide_h = min(p.guide_wall_height_mm, h["stop_top_z"] - z)

    left_rail = _local_box(rail_len, p.guide_wall_thickness_mm, guide_h, p.sensor_radius_mm, angle_deg, z, tangent_offset=rail_offset)
    right_rail = _local_box(rail_len, p.guide_wall_thickness_mm, guide_h, p.sensor_radius_mm, angle_deg, z, tangent_offset=-rail_offset)
    inner_stop = _local_box(
        p.guide_wall_thickness_mm,
        locator_span + 2.0 * p.guide_wall_thickness_mm,
        guide_h,
        p.sensor_radius_mm,
        angle_deg,
        z,
        radial_offset=-(locator_span / 2.0 + wall_clearance + p.guide_wall_thickness_mm / 2.0),
    )

    stop_h = h["stop_top_z"] - z
    stop_offset = locator_span / 2.0 + p.guide_wall_thickness_mm + p.overload_stop_diameter_mm / 2.0 + 2.0
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

    body = left_rail.union(right_rail).union(inner_stop)
    for stop in stops:
        body = body.union(stop)
    return body


def sensor_stack_parts(index: int, angle_deg: float, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    h = _sensor_stack_heights(p)
    lower_pad = _local_box(p.lower_pad_size_mm, p.lower_pad_size_mm, p.lower_pad_height_mm, p.sensor_radius_mm, angle_deg, h["lower_pad_z"])
    sensor = _local_box(p.sensor_size_mm, p.sensor_size_mm, p.sensor_height_mm, p.sensor_radius_mm, angle_deg, h["sensor_z"])
    upper_pad = _local_box(p.upper_pad_size_mm, p.upper_pad_size_mm, p.upper_pad_height_mm, p.sensor_radius_mm, angle_deg, h["upper_pad_z"])

    cable_slot = _local_box(16.0, 4.0, 2.0, p.sensor_radius_mm, angle_deg, h["sensor_z"] + 4.0, radial_offset=p.sensor_size_mm / 2.0 + 8.0)
    sensor = sensor.union(cable_slot)

    return [
        (f"sensor_{index}_lower_contact_pad", lower_pad),
        (f"sensor_{index}_placeholder_with_cable_exit", sensor),
        (f"sensor_{index}_upper_contact_pad", upper_pad),
    ]


def lower_segment(quadrant: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
    outer_r = p.lower_outer_diameter_mm / 2.0
    inner_r = p.lower_inner_diameter_mm / 2.0
    segment = _annular_sector(outer_r, inner_r, p.lower_thickness_mm, start, end)

    sensor_angle = quadrant * 90.0 + 45.0
    segment = segment.union(_sensor_station_lower_features(sensor_angle, p))

    # Keep the lower pad on solid base material; guide walls provide lateral location.
    segment = _add_vertical_insert_features(segment, quadrant, 0.0, p.lower_thickness_mm, True, p)
    return segment


def upper_segment(quadrant: int = 0, p: ConceptV2Params = P) -> cq.Workplane:
    start, end = _segment_angles(quadrant, p)
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.upper_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segment = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
    lip = _annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, start, end, p.upper_z_mm + p.upper_thickness_mm)
    segment = segment.union(lip)

    # Small underside contact land for the upper pad. It is part of the floating upper structure.
    sensor_angle = quadrant * 90.0 + 45.0
    land = _local_box(p.upper_pad_size_mm + 4.0, p.upper_pad_size_mm + 4.0, 1.0, p.sensor_radius_mm, sensor_angle, p.upper_z_mm)
    segment = segment.union(land)

    # Underside insert/dowel sockets for upper-only seam bridge plates.
    segment = _add_vertical_insert_features(segment, quadrant, p.upper_z_mm, p.upper_thickness_mm, False, p)
    return segment


def lower_seam_bridge(seam_angle: float, p: ConceptV2Params = P) -> cq.Workplane:
    return _local_box(
        p.seam_bridge_radial_len_mm,
        p.seam_bridge_tangent_len_mm,
        p.seam_bridge_height_mm,
        p.seam_bridge_radius_mm,
        seam_angle,
        p.lower_thickness_mm,
    )


def upper_seam_bridge(seam_angle: float, p: ConceptV2Params = P) -> cq.Workplane:
    return _local_box(
        p.seam_bridge_radial_len_mm,
        p.seam_bridge_tangent_len_mm,
        p.seam_bridge_height_mm,
        p.seam_bridge_radius_mm,
        seam_angle,
        p.upper_z_mm - p.seam_bridge_height_mm,
    )


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


def concept_v2_compound(p: ConceptV2Params = P) -> cq.Compound:
    return cq.Compound.makeCompound([body.val() for _, body in concept_v2_parts(p)])


if __name__ == "__main__":
    show_object(concept_v2_compound())  # type: ignore[name-defined]
