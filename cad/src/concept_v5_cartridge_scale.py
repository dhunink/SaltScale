"""Concept v5: cartridge-based four-sensor SaltScale concept.

This is a clean-sheet concept that keeps the same four Kiwi/SparkFun-style
50 kg sensors and electronics direction, but reorganizes the mechanics around
replaceable sensor cartridges, isolated load pucks, and a dry outer electronics
pod. It is intentionally separate from active concept_v4 geometry.
"""

from dataclasses import dataclass, replace
import math

import cadquery as cq

from concept_v2 import _annular_sector, _engrave_top


@dataclass(frozen=True)
class ConceptV5Params:
    segment_count: int = 4
    seam_gap_deg: float = 1.6

    lower_outer_diameter_mm: float = 320.0
    lower_inner_diameter_mm: float = 145.0
    lower_thickness_mm: float = 8.0

    upper_outer_diameter_mm: float = 308.0
    upper_inner_diameter_mm: float = 145.0
    upper_z_mm: float = 25.0
    upper_thickness_mm: float = 8.0
    upper_lip_height_mm: float = 6.0
    upper_lip_wall_mm: float = 4.0

    sensor_radius_mm: float = 112.0
    sensor_body_width_mm: float = 34.07
    sensor_thickness_mm: float = 6.84
    sensor_clearance_per_side_mm: float = 0.25
    sensor_bottom_bump_diameter_mm: float = 4.95
    sensor_bottom_bump_height_mm: float = 1.0
    sensor_bottom_bump_spacing_mm: float = 18.8
    sensor_bottom_relief_diameter_mm: float = 7.0

    cartridge_x_mm: float = 52.0
    cartridge_y_mm: float = 44.0
    cartridge_floor_mm: float = 3.0
    cartridge_wall_mm: float = 3.0
    cartridge_rail_height_mm: float = 2.0
    cartridge_rail_width_mm: float = 4.0
    cartridge_datum_height_mm: float = 2.0
    cartridge_locator_clearance_mm: float = 0.0
    cartridge_locator_wall_mm: float = 2.0
    cartridge_locator_height_mm: float = 7.1

    cartridge_z_mm: float = 5.0
    sensor_z_mm: float = 10.0
    clip_clearance_mm: float = 0.75
    retainer_clearance_mm: float = 0.0
    retainer_frame_compression_mm: float = 0.12
    retainer_thickness_mm: float = 2.4
    retainer_boss_diameter_mm: float = 8.0
    retainer_boss_collar_diameter_mm: float = 4.2
    retainer_boss_above_frame_mm: float = 2.75
    retainer_boss_pilot_mm: float = 2.8
    retainer_hole_mm: float = 5.1
    retainer_wall_clearance_mm: float = 0.35
    retainer_mount_eye_diameter_mm: float = 14.0
    retainer_mount_ring_outer_mm: float = 9.8
    retainer_mount_ring_height_mm: float = 1.4
    sensor_frame_retainer_height_mm: float = 1.45

    puck_body_diameter_mm: float = 32.0
    puck_body_height_mm: float = 3.0
    puck_lobe_diameter_mm: float = 24.0
    puck_lobe_height_mm: float = 2.0
    puck_bridge_x_mm: float = 12.0
    puck_bridge_y_mm: float = 24.0
    puck_boss_height_mm: float = 5.16

    overload_stop_diameter_mm: float = 8.0
    overload_gap_mm: float = 1.0

    electronics_pod_x_mm: float = 78.0
    electronics_pod_y_mm: float = 42.0
    electronics_pod_z_mm: float = 16.0
    electronics_wall_mm: float = 2.4

    m3_clearance_mm: float = 3.4
    m3_head_recess_mm: float = 6.4


P = ConceptV5Params()


def _segment_angles(index: int, p: ConceptV5Params = P) -> tuple[float, float]:
    span = 360.0 / p.segment_count
    start = index * span + p.seam_gap_deg / 2.0
    end = (index + 1) * span - p.seam_gap_deg / 2.0
    return start, end


def _segment_mid_angle(index: int, p: ConceptV5Params = P) -> float:
    start, end = _segment_angles(index, p)
    return (start + end) / 2.0


def _rounded_box(x_len: float, y_len: float, height: float, radius: float) -> cq.Workplane:
    body = cq.Workplane("XY").box(x_len, y_len, height, centered=(True, True, False))
    if radius > 0:
        body = body.edges("|Z").fillet(radius)
    return body


def _local_transform(
    body: cq.Workplane,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    body = body.translate((radius + radial_offset, tangent_offset, z))
    return body.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def _local_box(
    radial_len: float,
    tangent_len: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
    fillet: float = 0.0,
) -> cq.Workplane:
    return _local_transform(
        _rounded_box(radial_len, tangent_len, height, fillet),
        radius,
        angle_deg,
        z,
        radial_offset,
        tangent_offset,
    )


def _local_cylinder(
    diameter: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
) -> cq.Workplane:
    body = cq.Workplane("XY").circle(diameter / 2.0).extrude(height)
    return _local_transform(body, radius, angle_deg, z, radial_offset, tangent_offset)


def _cut_local_box(
    body: cq.Workplane,
    radial_len: float,
    tangent_len: float,
    height: float,
    radius: float,
    angle_deg: float,
    z: float,
    radial_offset: float = 0.0,
    tangent_offset: float = 0.0,
    fillet: float = 0.0,
) -> cq.Workplane:
    return body.cut(_local_box(radial_len, tangent_len, height, radius, angle_deg, z, radial_offset, tangent_offset, fillet))


def kiwi_sensor_reference_v2(p: ConceptV5Params = P) -> cq.Workplane:
    """Visual envelope of the measured sensor, with bridge and cable keepout."""
    width = p.sensor_body_width_mm
    height = p.sensor_thickness_mm
    frame = _rounded_box(width, width, 1.45, 3.2).cut(
        _rounded_box(22.2, 22.2, 2.0, 3.0).translate((0.0, 0.0, -0.25))
    )
    center_plate = _rounded_box(19.0, 22.0, 1.7, 2.0).translate((0.0, 0.0, 1.05))
    bridge = _rounded_box(11.5, 27.0, 2.0, 2.0).translate((0.0, 0.0, 2.95))
    button = cq.Workplane("XY").circle(3.0).extrude(1.15).translate((0.0, 0.0, height - 1.15))
    rivet_a = cq.Workplane("XY").circle(2.1).extrude(0.65).translate((0.0, 9.2, height - 0.65))
    rivet_b = cq.Workplane("XY").circle(2.1).extrude(0.65).translate((0.0, -9.2, height - 0.65))
    glue = cq.Workplane("XY").ellipse(4.0, 5.4).extrude(1.2).translate((width / 2.0 - 2.0, 0.0, 1.45))
    cable = cq.Workplane("XY").box(30.0, 3.0, 1.2, centered=(True, True, False)).translate((width / 2.0 + 15.0, 0.0, 1.35))
    return frame.union(center_plate).union(bridge).union(button).union(rivet_a).union(rivet_b).union(glue).union(cable)


def sensor_cartridge(p: ConceptV5Params = P) -> cq.Workplane:
    """Printable removable tray for one real sensor.

    Local +X is the cable exit direction and remains open. The sensor is
    carried by the outer frame rim, with underside clearance for rivet bumps.
    """
    base = _rounded_box(p.cartridge_x_mm, p.cartridge_y_mm, p.cartridge_floor_mm, 4.0)

    # Side rails slide into the lower segment receiver and make the cartridge
    # serviceable from the outside of the scale.
    rail_y = p.cartridge_y_mm / 2.0 - p.cartridge_rail_width_mm / 2.0
    rail_top = _rounded_box(p.cartridge_x_mm - 8.0, p.cartridge_rail_width_mm, p.cartridge_rail_height_mm, 1.2).translate(
        (0.0, rail_y, p.cartridge_floor_mm)
    )
    rail_bottom = _rounded_box(p.cartridge_x_mm - 8.0, p.cartridge_rail_width_mm, p.cartridge_rail_height_mm, 1.2).translate(
        (0.0, -rail_y, p.cartridge_floor_mm)
    )

    # V2: the first print showed the sensor floating on the old three-bar
    # datum layout. These wider, outboard ledges support the flat perimeter of
    # the metal frame while leaving the active bridge and underside bumps free.
    ledge_y = p.sensor_body_width_mm / 2.0 - 1.7
    ledge_x = -2.0
    ledge_a = _rounded_box(25.0, 3.2, p.cartridge_datum_height_mm, 1.2).translate(
        (ledge_x, ledge_y, p.cartridge_floor_mm)
    )
    ledge_b = _rounded_box(25.0, 3.2, p.cartridge_datum_height_mm, 1.2).translate(
        (ledge_x, -ledge_y, p.cartridge_floor_mm)
    )
    rear_x = -(p.sensor_body_width_mm / 2.0 + 2.0)
    rear_a = _rounded_box(5.0, 6.5, p.cartridge_datum_height_mm, 1.2).translate(
        (rear_x, 10.5, p.cartridge_floor_mm)
    )
    rear_b = _rounded_box(5.0, 6.5, p.cartridge_datum_height_mm, 1.2).translate(
        (rear_x, -10.5, p.cartridge_floor_mm)
    )

    # V9: physical tests confirmed that the raised over-wall pocket gives the
    # sensor the desired snug lateral fit without touching the active bridge.
    wall_h = p.cartridge_locator_height_mm
    wall_w = p.cartridge_locator_wall_mm
    wall_z = p.cartridge_floor_mm
    side_y = p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0
    side_x = -2.5
    side_a = _rounded_box(27.5, wall_w, wall_h, 0.6).translate((side_x, side_y, wall_z))
    side_b = _rounded_box(27.5, wall_w, wall_h, 0.6).translate((side_x, -side_y, wall_z))
    rear_x_stop = -(p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0)
    rear_stop = _rounded_box(wall_w, 27.0, wall_h, 0.6).translate((rear_x_stop, 0.0, wall_z))
    front_x_stop = p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0
    # The cable-side stops locate the front edge only; keeping them below the
    # retainer avoids any print-support overhang or assembly interference.
    front_stop_h = p.sensor_frame_retainer_height_mm + p.retainer_clearance_mm + 1.45
    front_stop_a = _rounded_box(wall_w, 7.5, front_stop_h, 0.6).translate((front_x_stop, 12.0, wall_z))
    front_stop_b = _rounded_box(wall_w, 7.5, front_stop_h, 0.6).translate((front_x_stop, -12.0, wall_z))

    # Broad retainer bosses accept M3 clearance screws or printed pins. The
    # retainer bottoms on these shoulders, not on the sensor.
    retainer_z = (
        p.sensor_z_mm
        - p.cartridge_z_mm
        + p.sensor_frame_retainer_height_mm
        + p.retainer_clearance_mm
        - p.retainer_frame_compression_mm
    )
    boss_h = retainer_z - p.cartridge_floor_mm
    boss_x = p.sensor_body_width_mm / 2.0 + 6.3
    boss_y = 13.5
    collar_top = p.sensor_z_mm - p.cartridge_z_mm + p.sensor_frame_retainer_height_mm + p.retainer_boss_above_frame_mm
    collar_h = collar_top - p.cartridge_floor_mm
    boss_a = cq.Workplane("XY").circle(p.retainer_boss_diameter_mm / 2.0).extrude(boss_h).translate((boss_x, boss_y, p.cartridge_floor_mm))
    boss_b = cq.Workplane("XY").circle(p.retainer_boss_diameter_mm / 2.0).extrude(boss_h).translate((boss_x, -boss_y, p.cartridge_floor_mm))
    collar_a = cq.Workplane("XY").circle(p.retainer_boss_collar_diameter_mm / 2.0).extrude(collar_h).translate(
        (boss_x, boss_y, p.cartridge_floor_mm)
    )
    collar_b = cq.Workplane("XY").circle(p.retainer_boss_collar_diameter_mm / 2.0).extrude(collar_h).translate(
        (boss_x, -boss_y, p.cartridge_floor_mm)
    )

    # Cable trough points outward and deliberately stays wide.
    cable_cut = _rounded_box(28.0, 9.0, p.cartridge_floor_mm + 1.0, 2.0).translate(
        (p.cartridge_x_mm / 2.0 - 8.0, 0.0, -0.2)
    )

    body = (
        base.union(rail_top)
        .union(rail_bottom)
        .union(ledge_a)
        .union(ledge_b)
        .union(rear_a)
        .union(rear_b)
        .union(side_a)
        .union(side_b)
        .union(rear_stop)
        .union(front_stop_a)
        .union(front_stop_b)
        .union(boss_a)
        .union(boss_b)
        .union(collar_a)
        .union(collar_b)
    )
    body = body.cut(cable_cut)
    for y in (-boss_y, boss_y):
        pilot = cq.Workplane("XY").circle(p.retainer_boss_pilot_mm / 2.0).extrude(collar_h + 0.8).translate(
            (boss_x, y, p.cartridge_floor_mm - 0.2)
        )
        body = body.cut(pilot)
    relief_y = p.sensor_bottom_bump_spacing_mm / 2.0
    relief_h = p.cartridge_datum_height_mm + p.sensor_bottom_bump_height_mm + 0.5
    for y in (-relief_y, relief_y):
        relief = cq.Workplane("XY").circle(p.sensor_bottom_relief_diameter_mm / 2.0).extrude(relief_h).translate(
            (0.0, y, p.cartridge_floor_mm - 0.25)
        )
        body = body.cut(relief)
    body = _engrave_top(body, "CART V9", -20.0, -20.5, p.cartridge_floor_mm, size=4.0)
    body = _engrave_top(body, "CABLE", 18.0, 4.5, p.cartridge_floor_mm, size=3.5)
    return body


def sensor_retainer_clip(p: ConceptV5Params = P) -> cq.Workplane:
    """Rigid hold-down frame that lightly clamps only the inactive outer frame."""
    z = (
        p.sensor_z_mm
        - p.cartridge_z_mm
        + p.sensor_frame_retainer_height_mm
        + p.retainer_clearance_mm
        - p.retainer_frame_compression_mm
    )
    boss_x = p.sensor_body_width_mm / 2.0 + 6.3
    boss_y = 13.5
    wall_w = p.cartridge_locator_wall_mm
    wall_clearance = p.retainer_wall_clearance_mm
    side_wall_y = p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0
    rear_wall_x = -(p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0)
    inner_w = 2.4
    outer_w = 2.2
    side_inner_y = side_wall_y - wall_w / 2.0 - wall_clearance - inner_w / 2.0
    side_outer_y = side_wall_y + wall_w / 2.0 + wall_clearance + outer_w / 2.0
    rear_inner_x = rear_wall_x + wall_w / 2.0 + wall_clearance + inner_w / 2.0
    rear_outer_x = rear_wall_x - wall_w / 2.0 - wall_clearance - outer_w / 2.0
    side_len = 48.0
    rear_len = 43.0

    # V9: keep the support-free flat print, but make the retainer a cap around
    # the raised cartridge walls. Inner rails clamp the inactive sensor frame;
    # outer rails sit outside the walls so the wall can pass through the gap.
    bridge = _rounded_box(side_len, inner_w, p.retainer_thickness_mm, 0.9).translate((3.0, side_inner_y, z))
    bridge = bridge.union(_rounded_box(side_len, inner_w, p.retainer_thickness_mm, 0.9).translate((3.0, -side_inner_y, z)))
    bridge = bridge.union(_rounded_box(side_len, outer_w, p.retainer_thickness_mm, 0.9).translate((3.0, side_outer_y, z)))
    bridge = bridge.union(_rounded_box(side_len, outer_w, p.retainer_thickness_mm, 0.9).translate((3.0, -side_outer_y, z)))
    bridge = bridge.union(_rounded_box(inner_w, 34.0, p.retainer_thickness_mm, 0.9).translate((rear_inner_x, 0.0, z)))
    bridge = bridge.union(_rounded_box(outer_w, rear_len, p.retainer_thickness_mm, 0.9).translate((rear_outer_x, 0.0, z)))

    for y in (-boss_y, boss_y):
        pad = cq.Workplane("XY").circle(p.retainer_mount_eye_diameter_mm / 2.0).extrude(p.retainer_thickness_mm).translate(
            (boss_x, y, z)
        )
        arm = _rounded_box(18.0, 6.4, p.retainer_thickness_mm, 1.2).translate((boss_x - 7.8, y, z))
        ring = (
            cq.Workplane("XY")
            .circle(p.retainer_mount_ring_outer_mm / 2.0)
            .circle(p.retainer_hole_mm / 2.0)
            .extrude(p.retainer_mount_ring_height_mm)
            .translate((boss_x, y, z + p.retainer_thickness_mm))
        )
        bridge = bridge.union(pad).union(arm).union(ring)
        hole = cq.Workplane("XY").circle(p.retainer_hole_mm / 2.0).extrude(
            p.retainer_thickness_mm + p.retainer_mount_ring_height_mm + 0.7
        ).translate((boss_x, y, z - 0.35))
        bridge = bridge.cut(hole)
    return _engrave_top(
        bridge,
        "CAP V9",
        -8.5,
        -2.4,
        z + p.retainer_thickness_mm,
        size=3.0,
    )


def sensor_retainer_closed_cap(p: ConceptV5Params = P) -> cq.Workplane:
    """V8A: closed-top cap for the current lower walls.

    The side/rear rails are visually and structurally closed from above, but
    have a shallow underside relief so the current walls can still enter
    without becoming the primary locating feature.
    """
    z = (
        p.sensor_z_mm
        - p.cartridge_z_mm
        + p.sensor_frame_retainer_height_mm
        + p.retainer_clearance_mm
        - p.retainer_frame_compression_mm
    )
    boss_x = p.sensor_body_width_mm / 2.0 + 6.3
    boss_y = 13.5
    wall_w = p.cartridge_locator_wall_mm
    wall_clearance = p.retainer_wall_clearance_mm
    side_wall_y = p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0
    rear_wall_x = -(p.sensor_body_width_mm / 2.0 + p.cartridge_locator_clearance_mm + wall_w / 2.0)
    inner_w = 2.4
    outer_w = 2.2
    side_inner_y = side_wall_y - wall_w / 2.0 - wall_clearance - inner_w / 2.0
    side_outer_y = side_wall_y + wall_w / 2.0 + wall_clearance + outer_w / 2.0
    rear_inner_x = rear_wall_x + wall_w / 2.0 + wall_clearance + inner_w / 2.0
    rear_outer_x = rear_wall_x - wall_w / 2.0 - wall_clearance - outer_w / 2.0

    side_span = (side_outer_y + outer_w / 2.0) - (side_inner_y - inner_w / 2.0)
    side_center = (side_outer_y + outer_w / 2.0 + side_inner_y - inner_w / 2.0) / 2.0
    rear_span = (rear_inner_x + inner_w / 2.0) - (rear_outer_x - outer_w / 2.0)
    rear_center = (rear_inner_x + inner_w / 2.0 + rear_outer_x - outer_w / 2.0) / 2.0
    side_len = 48.0
    rear_len = 43.0

    bridge = _rounded_box(side_len, side_span, p.retainer_thickness_mm, 0.9).translate((3.0, side_center, z))
    bridge = bridge.union(_rounded_box(side_len, side_span, p.retainer_thickness_mm, 0.9).translate((3.0, -side_center, z)))
    bridge = bridge.union(_rounded_box(rear_span, rear_len, p.retainer_thickness_mm, 0.9).translate((rear_center, 0.0, z)))

    # Only relieve the underside enough for the present wall height. This closes
    # the long top slot while keeping assembly clearance.
    wall_top = p.cartridge_floor_mm + p.cartridge_locator_height_mm
    relief_h = min(max(wall_top - z + 0.25, 0.0), p.retainer_thickness_mm - 0.65)
    if relief_h > 0:
        side_relief = _rounded_box(side_len + 0.8, wall_w + 2.0 * wall_clearance, relief_h + 0.2, 0.35).translate(
            (3.0, side_wall_y, z - 0.1)
        )
        rear_relief = _rounded_box(wall_w + 2.0 * wall_clearance, 34.0, relief_h + 0.2, 0.35).translate(
            (rear_wall_x, 0.0, z - 0.1)
        )
        bridge = bridge.cut(side_relief).cut(
            _rounded_box(side_len + 0.8, wall_w + 2.0 * wall_clearance, relief_h + 0.2, 0.35).translate(
                (3.0, -side_wall_y, z - 0.1)
            )
        ).cut(rear_relief)

    for y in (-boss_y, boss_y):
        pad = cq.Workplane("XY").circle(p.retainer_mount_eye_diameter_mm / 2.0).extrude(p.retainer_thickness_mm).translate(
            (boss_x, y, z)
        )
        arm = _rounded_box(18.0, 6.4, p.retainer_thickness_mm, 1.2).translate((boss_x - 7.8, y, z))
        ring = (
            cq.Workplane("XY")
            .circle(p.retainer_mount_ring_outer_mm / 2.0)
            .circle(p.retainer_hole_mm / 2.0)
            .extrude(p.retainer_mount_ring_height_mm)
            .translate((boss_x, y, z + p.retainer_thickness_mm))
        )
        bridge = bridge.union(pad).union(arm).union(ring)
        hole = cq.Workplane("XY").circle(p.retainer_hole_mm / 2.0).extrude(
            p.retainer_thickness_mm + p.retainer_mount_ring_height_mm + 0.7
        ).translate((boss_x, y, z - 0.35))
        bridge = bridge.cut(hole)

    return _engrave_top(bridge, "CAP A", -8.5, -2.4, z + p.retainer_thickness_mm, size=3.0)


def tall_wall_params(p: ConceptV5Params = P) -> ConceptV5Params:
    """Legacy V8B test: raised walls before the final 7.1 mm validation."""
    return replace(p, cartridge_locator_height_mm=5.6)


def over_wall_plus_1p5_params(p: ConceptV5Params = P) -> ConceptV5Params:
    """V9 validated cartridge: 7.1 mm locator walls with over-wall retainer."""
    return replace(p, cartridge_locator_height_mm=7.1)


def sensor_cartridge_tall_wall(p: ConceptV5Params = P) -> cq.Workplane:
    return sensor_cartridge(tall_wall_params(p))


def sensor_retainer_over_wall_clip(p: ConceptV5Params = P) -> cq.Workplane:
    return sensor_retainer_clip(tall_wall_params(p))


def sensor_cartridge_over_wall_plus_1p5(p: ConceptV5Params = P) -> cq.Workplane:
    return sensor_cartridge(over_wall_plus_1p5_params(p))


def sensor_retainer_over_wall_plus_1p5(p: ConceptV5Params = P) -> cq.Workplane:
    return sensor_retainer_clip(over_wall_plus_1p5_params(p))


def bridge_load_puck(p: ConceptV5Params = P) -> cq.Workplane:
    """Default candidate puck: broad lobe above, bridge-shaped boss below."""
    boss = _rounded_box(p.puck_bridge_x_mm, p.puck_bridge_y_mm, p.puck_boss_height_mm, 2.5)
    body = cq.Workplane("XY").circle(p.puck_body_diameter_mm / 2.0).extrude(p.puck_body_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm)
    )
    lobe = cq.Workplane("XY").circle(p.puck_lobe_diameter_mm / 2.0).extrude(p.puck_lobe_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm + p.puck_body_height_mm)
    )
    puck = boss.union(body).union(lobe)
    return _engrave_top(puck, "12x24", 0.0, -11.0, p.puck_boss_height_mm + p.puck_body_height_mm + p.puck_lobe_height_mm, size=4.0)


def round_load_puck(p: ConceptV5Params = P) -> cq.Workplane:
    boss = cq.Workplane("XY").circle(6.0).extrude(p.puck_boss_height_mm)
    body = cq.Workplane("XY").circle(p.puck_body_diameter_mm / 2.0).extrude(p.puck_body_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm)
    )
    lobe = cq.Workplane("XY").circle(p.puck_lobe_diameter_mm / 2.0).extrude(p.puck_lobe_height_mm).translate(
        (0.0, 0.0, p.puck_boss_height_mm + p.puck_body_height_mm)
    )
    puck = boss.union(body).union(lobe)
    return _engrave_top(puck, "12", 0.0, -11.0, p.puck_boss_height_mm + p.puck_body_height_mm + p.puck_lobe_height_mm, size=5.0)


def lower_segment(index: int = 0, p: ConceptV5Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    mid = _segment_mid_angle(index, p)
    segment = _annular_sector(
        p.lower_outer_diameter_mm / 2.0,
        p.lower_inner_diameter_mm / 2.0,
        p.lower_thickness_mm,
        start,
        end,
    )

    # Cartridge receiver: two open radial rails plus a rear datum stop. The
    # cartridge slides in from the outer edge; the cable also exits outward.
    rail_y = p.cartridge_y_mm / 2.0 + 0.7
    receiver_len = p.cartridge_x_mm + 5.0
    segment = segment.union(_local_box(receiver_len, 4.5, 4.0, p.sensor_radius_mm, mid, p.lower_thickness_mm, fillet=1.4, tangent_offset=rail_y))
    segment = segment.union(_local_box(receiver_len, 4.5, 4.0, p.sensor_radius_mm, mid, p.lower_thickness_mm, fillet=1.4, tangent_offset=-rail_y))
    segment = segment.union(
        _local_box(
            4.5,
            p.cartridge_y_mm - 8.0,
            4.0,
            p.sensor_radius_mm,
            mid,
            p.lower_thickness_mm,
            radial_offset=-(p.cartridge_x_mm / 2.0 + 2.5),
            fillet=1.4,
        )
    )

    # Overload stops are lower-only and clear the upper ring by 1 mm unloaded.
    stop_top = p.upper_z_mm - p.overload_gap_mm
    stop_h = stop_top - p.lower_thickness_mm
    for radial_offset in (-32.0, 32.0):
        for tangent_offset in (-31.0, 31.0):
            segment = segment.union(
                _local_cylinder(p.overload_stop_diameter_mm, stop_h, p.sensor_radius_mm, mid, p.lower_thickness_mm, radial_offset, tangent_offset)
            )

    # Simple seam bolt holes/recesses for M3 joining, intentionally same-layer.
    for seam_angle in (start, end):
        for radius in (122.0, 145.0):
            segment = segment.cut(_local_cylinder(p.m3_clearance_mm, p.lower_thickness_mm + 0.8, radius, seam_angle, -0.4))
            segment = segment.cut(_local_cylinder(p.m3_head_recess_mm, 1.2, radius, seam_angle, p.lower_thickness_mm - 1.0))

    segment = _engrave_top(segment, "V5 LOWER", 82.0 * math.cos(math.radians(mid)), 82.0 * math.sin(math.radians(mid)), p.lower_thickness_mm, size=6.0)
    return segment


def upper_segment(index: int = 0, p: ConceptV5Params = P) -> cq.Workplane:
    start, end = _segment_angles(index, p)
    mid = _segment_mid_angle(index, p)
    segment = _annular_sector(
        p.upper_outer_diameter_mm / 2.0,
        p.upper_inner_diameter_mm / 2.0,
        p.upper_thickness_mm,
        start,
        end,
        z=p.upper_z_mm,
    )

    # Low centering lip for the salt container. This is upper-only and never
    # touches lower-base features.
    lip_outer = _annular_sector(
        150.0,
        146.0,
        p.upper_lip_height_mm,
        start,
        end,
        z=p.upper_z_mm + p.upper_thickness_mm,
    )
    segment = segment.union(lip_outer)

    # Puck lobe socket opens to the inner edge to avoid underside support.
    socket_d = p.puck_lobe_diameter_mm + 1.2
    socket = _local_cylinder(socket_d, p.upper_thickness_mm + 0.8, p.sensor_radius_mm, mid, p.upper_z_mm - 0.4)
    throat_len = p.sensor_radius_mm - p.upper_inner_diameter_mm / 2.0 + socket_d / 2.0 + 2.0
    throat_radius = p.upper_inner_diameter_mm / 2.0 + throat_len / 2.0 - 1.0
    throat = _local_box(throat_len, 18.0, p.upper_thickness_mm + 0.8, throat_radius, mid, p.upper_z_mm - 0.4, fillet=1.0)
    segment = segment.cut(socket).cut(throat)

    for seam_angle in (start, end):
        for radius in (122.0, 145.0):
            segment = segment.cut(_local_cylinder(p.m3_clearance_mm, p.upper_thickness_mm + 0.8, radius, seam_angle, p.upper_z_mm - 0.4))
            segment = segment.cut(_local_cylinder(p.m3_head_recess_mm, 2.0, radius, seam_angle, p.upper_z_mm + p.upper_thickness_mm - 1.8))

    segment = _engrave_top(segment, "V5 UPPER", 82.0 * math.cos(math.radians(mid)), 82.0 * math.sin(math.radians(mid)), p.upper_z_mm + p.upper_thickness_mm, size=6.0)
    return segment


def electronics_pod(p: ConceptV5Params = P) -> cq.Workplane:
    outer = _rounded_box(p.electronics_pod_x_mm, p.electronics_pod_y_mm, p.electronics_pod_z_mm, 5.0)
    inner = _rounded_box(
        p.electronics_pod_x_mm - 2.0 * p.electronics_wall_mm,
        p.electronics_pod_y_mm - 2.0 * p.electronics_wall_mm,
        p.electronics_pod_z_mm - p.electronics_wall_mm,
        3.5,
    ).translate((0.0, 0.0, p.electronics_wall_mm))
    pod = outer.cut(inner)
    # Four cable glands toward the scale and two small screw bosses for a lid.
    for y in (-13.5, -4.5, 4.5, 13.5):
        pod = pod.cut(cq.Workplane("YZ").circle(2.0).extrude(8.0).translate((-p.electronics_pod_x_mm / 2.0 - 0.5, y, 7.0)))
    boss_a = cq.Workplane("XY").circle(3.5).extrude(8.0).translate((25.0, 13.5, 0.0))
    boss_b = cq.Workplane("XY").circle(3.5).extrude(8.0).translate((25.0, -13.5, 0.0))
    pod = pod.union(boss_a).union(boss_b)
    pod = pod.cut(cq.Workplane("XY").circle(1.7).extrude(9.0).translate((25.0, 13.5, -0.3)))
    pod = pod.cut(cq.Workplane("XY").circle(1.7).extrude(9.0).translate((25.0, -13.5, -0.3)))
    return _engrave_top(pod, "E-POD", -12.0, -8.0, p.electronics_pod_z_mm, size=6.0)


def _place_at_station(body: cq.Workplane, angle_deg: float, z: float, p: ConceptV5Params = P) -> cq.Workplane:
    return _local_transform(body, p.sensor_radius_mm, angle_deg, z)


def concept_v5_assembly(p: ConceptV5Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="concept_v5_cartridge_scale")
    for i in range(p.segment_count):
        mid = _segment_mid_angle(i, p)
        assembly.add(lower_segment(i, p), name=f"lower_segment_{i}")
        assembly.add(upper_segment(i, p), name=f"upper_segment_{i}")
        assembly.add(_place_at_station(sensor_cartridge(p), mid, p.cartridge_z_mm, p), name=f"sensor_cartridge_{i}")
        assembly.add(_place_at_station(kiwi_sensor_reference_v2(p), mid, p.sensor_z_mm, p), name=f"kiwi_sensor_{i}")
        assembly.add(_place_at_station(sensor_retainer_clip(p), mid, p.cartridge_z_mm, p), name=f"sensor_retainer_clip_{i}")
        assembly.add(_place_at_station(bridge_load_puck(p), mid, p.sensor_z_mm + p.sensor_thickness_mm, p), name=f"bridge_load_puck_{i}")
    pod = electronics_pod(p).translate((0.0, -(p.lower_outer_diameter_mm / 2.0 + p.electronics_pod_y_mm / 2.0 + 4.0), 4.0))
    assembly.add(pod, name="dry_outer_electronics_pod")
    return assembly


def printable_parts(p: ConceptV5Params = P) -> dict[str, cq.Workplane]:
    return {
        "concept_v5_lower_segment_0": lower_segment(0, p),
        "concept_v5_upper_segment_0": upper_segment(0, p),
        "concept_v5_sensor_cartridge": sensor_cartridge(p),
        "concept_v5_sensor_retainer_clip": sensor_retainer_clip(p),
        "concept_v5_bridge_load_puck": bridge_load_puck(p),
        "concept_v5_round_load_puck": round_load_puck(p),
        "concept_v5_electronics_pod": electronics_pod(p),
        "concept_v5_kiwi_sensor_reference": kiwi_sensor_reference_v2(p),
    }


def gen_step() -> cq.Assembly:
    return concept_v5_assembly()
