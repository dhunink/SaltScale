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
LOCATOR_CLEARANCE_PER_SIDE_MM = 0.3

# Default fastener assumption for integrated v4 seams.
# ISO 7380 style M3 button-head screws keep top-access upper fasteners low
# enough to recess flush with the upper carrier top surface.
M3_BUTTON_HEAD_DIAMETER_MM = 5.7
M3_BUTTON_HEAD_HEIGHT_MM = 1.8
M3_HEAD_RECESS_DIAMETER_MM = 6.4
M3_HEAD_RECESS_DEPTH_MM = 2.0
LOWER_HEAD_SEAT_DEPTH_MM = 1.0

KIWI_SENSOR_BODY_WIDTH_MM = 34.07
KIWI_SENSOR_THICKNESS_MM = 6.84

LOWER_PAD_DEFAULT_SIZE_MM = 36.0
LOWER_PAD_CORNER_RADIUS_MM = 4.0

UPPER_PAD_ROUND_DIAMETER_MM = 40.0
UPPER_PAD_CONTACT_BOSS_DIAMETER_MM = 12.0
UPPER_PAD_LOCATOR_DIAMETER_MM = 36.0
UPPER_PAD_LOCATOR_HEIGHT_MM = 3.0
UPPER_PAD_SOCKET_CLEARANCE_PER_SIDE_MM = 0.6
UPPER_PAD_SOCKET_THROAT_WIDTH_MM = 22.0
SENSOR_LOCATOR_CLEARANCE_PER_SIDE_MM = 0.2
SENSOR_CLIP_POST_DIAMETER_MM = 5.5
SENSOR_CLIP_POST_CLEARANCE_MM = 0.5
SENSOR_CLIP_THICKNESS_MM = 2.2
SENSOR_CLIP_ARM_LEN_MM = 13.0
SENSOR_CLIP_ARM_WIDTH_MM = 5.0
SENSOR_CLIP_DISC_DIAMETER_MM = 10.0
SENSOR_CLIP_BOTTOM_CLEARANCE_MM = 0.35
SENSOR_REAR_PILLAR_DIAMETER_MM = 4.5


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
            # Upper bolts install from the top of the neighboring segment.
            # The integrated same-plane lug carries the underside captured M3 nut
            # without hanging below the main upper segment body.
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



def _kiwi_stack_heights(p: ConceptV2Params = P) -> dict[str, float]:
    lower_pad_z = p.lower_thickness_mm
    sensor_z = lower_pad_z + p.lower_pad_height_mm
    sensor_top_z = sensor_z + KIWI_SENSOR_THICKNESS_MM
    upper_pad_z = sensor_top_z
    upper_pad_body_z = p.upper_z_mm - p.upper_pad_height_mm
    boss_height = upper_pad_body_z - upper_pad_z
    return {
        "lower_pad_z": lower_pad_z,
        "sensor_z": sensor_z,
        "sensor_top_z": sensor_top_z,
        "upper_pad_z": upper_pad_z,
        "upper_pad_body_z": upper_pad_body_z,
        "upper_carrier_z": p.upper_z_mm,
        "upper_pad_boss_height": boss_height,
        "upper_pad_total_height": p.upper_z_mm - upper_pad_z,
        "stop_top_z": p.upper_z_mm - p.overload_gap_mm,
    }


def _rounded_box(x_len: float, y_len: float, height: float, radius: float) -> cq.Workplane:
    body = cq.Workplane("XY").box(x_len, y_len, height, centered=(True, True, False))
    if radius <= 0:
        return body
    return body.edges("|Z").fillet(radius)


def _rounded_cylinder_or_box_round(diameter: float, height: float) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(height)


def sensor_quarter_turn_clip(p: ConceptV2Params = P) -> cq.Workplane:
    """Separate printable quarter-turn sensor retention clip.

    Print flat. In assembly, the arm sits above the sensor with clearance and
    only prevents accidental lift-out during handling; it is not part of the
    weighing load path.
    """
    disc = cq.Workplane("XY").circle(SENSOR_CLIP_DISC_DIAMETER_MM / 2.0).extrude(SENSOR_CLIP_THICKNESS_MM)
    arm = _rounded_box(
        SENSOR_CLIP_ARM_LEN_MM,
        SENSOR_CLIP_ARM_WIDTH_MM,
        SENSOR_CLIP_THICKNESS_MM,
        1.2,
    ).translate((-(SENSOR_CLIP_DISC_DIAMETER_MM / 2.0 + SENSOR_CLIP_ARM_LEN_MM / 2.0 - 1.0), 0.0, 0.0))
    hole = cq.Workplane("XY").circle((SENSOR_CLIP_POST_DIAMETER_MM + SENSOR_CLIP_POST_CLEARANCE_MM) / 2.0).extrude(SENSOR_CLIP_THICKNESS_MM + 0.6).translate((0, 0, -0.3))
    return disc.union(arm).cut(hole)


def _sensor_clip_z(p: ConceptV2Params = P) -> float:
    h = _kiwi_stack_heights(p)
    return h["sensor_top_z"] + SENSOR_CLIP_BOTTOM_CLEARANCE_MM


def _sensor_clip_post_height(p: ConceptV2Params = P) -> float:
    return _sensor_clip_z(p) + SENSOR_CLIP_THICKNESS_MM + 0.8 - p.lower_thickness_mm


def _place_sensor_clip(
    angle_deg: float,
    radial_offset: float,
    tangent_offset: float,
    closed: bool,
    top_side: bool,
    p: ConceptV2Params = P,
) -> cq.Workplane:
    clip = sensor_quarter_turn_clip(p)
    if not closed:
        open_angle = -90.0 if top_side else 90.0
        clip = clip.rotate((0, 0, 0), (0, 0, 1), open_angle)
    clip = clip.translate((p.sensor_radius_mm + radial_offset, tangent_offset, _sensor_clip_z(p)))
    return clip.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def sensor_clip_parts(index: int, angle_deg: float, closed: bool = True, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    cavity = KIWI_SENSOR_BODY_WIDTH_MM + 2.0 * SENSOR_LOCATOR_CLEARANCE_PER_SIDE_MM
    half = cavity / 2.0
    outer_x = half + SENSOR_CLIP_POST_DIAMETER_MM / 2.0 + 0.6
    return [
        (
            f"sensor_{index}_front_clip_top_{'closed' if closed else 'open'}",
            _place_sensor_clip(angle_deg, outer_x, 13.0, closed, True, p),
        ),
        (
            f"sensor_{index}_front_clip_bottom_{'closed' if closed else 'open'}",
            _place_sensor_clip(angle_deg, outer_x, -13.0, closed, False, p),
        ),
    ]


def lower_pad(p: ConceptV2Params = P, size: float = LOWER_PAD_DEFAULT_SIZE_MM) -> cq.Workplane:
    return _rounded_box(size, size, p.lower_pad_height_mm, LOWER_PAD_CORNER_RADIUS_MM)


def lower_pad_frame_support(p: ConceptV2Params = P) -> cq.Workplane:
    outer = _rounded_box(36.0, 36.0, p.lower_pad_height_mm, 4.0)
    center_relief = _rounded_box(23.0, 23.0, p.lower_pad_height_mm + 0.4, 3.0).translate((0, 0, -0.2))
    return outer.cut(center_relief)


def upper_pad_round_boss(boss_diameter: float, p: ConceptV2Params = P) -> cq.Workplane:
    h = _kiwi_stack_heights(p)
    boss_h = h["upper_pad_boss_height"]
    if boss_h <= 0:
        raise ValueError("Upper pad boss height must be positive for real Kiwi stack")
    boss = cq.Workplane("XY").circle(boss_diameter / 2.0).extrude(boss_h)
    body_z = boss_h
    body = cq.Workplane("XY").circle(UPPER_PAD_ROUND_DIAMETER_MM / 2.0).extrude(p.upper_pad_height_mm).translate((0, 0, body_z))

    # Upper locating lobe. It drops into an open-to-inner-edge pocket in the
    # upper carrier. The lobe is smaller than the 40 mm body, leaving a shoulder
    # that bears on the flat underside of the upper carrier while the lobe
    # prevents sideways drift.
    lobe_z = body_z + p.upper_pad_height_mm
    lobe = (
        cq.Workplane("XY")
        .circle(UPPER_PAD_LOCATOR_DIAMETER_MM / 2.0)
        .extrude(UPPER_PAD_LOCATOR_HEIGHT_MM)
        .translate((0.0, 0.0, lobe_z))
    )
    return boss.union(body).union(lobe)


def upper_pad_rect_boss(p: ConceptV2Params = P) -> cq.Workplane:
    h = _kiwi_stack_heights(p)
    boss_h = h["upper_pad_boss_height"]
    boss = _rounded_box(12.0, 24.0, boss_h, 2.5)
    body = cq.Workplane("XY").circle(UPPER_PAD_ROUND_DIAMETER_MM / 2.0).extrude(p.upper_pad_height_mm).translate((0, 0, boss_h))
    return boss.union(body)


def upper_pad(p: ConceptV2Params = P) -> cq.Workplane:
    return upper_pad_round_boss(UPPER_PAD_CONTACT_BOSS_DIAMETER_MM, p)

def kiwi_sensor_reference_v1(p: ConceptV2Params = P) -> cq.Workplane:
    """Dimensionally representative Kiwi/SparkFun-style 50 kg sensor.

    The measured reference sensor is about 34.07 mm wide and 6.84 mm
    thick. This is a visual/reference assembly body, not a printable part and
    not a redesign of the active pad, locator, or upper/lower stack geometry.
    """
    width = 34.07
    height = 6.84

    # Lower stamped outer frame: rounded square loop with a central opening.
    outer = _rounded_box(width, width, 1.45, 3.2)
    inner_cut = _rounded_box(22.2, 22.2, 2.0, 3.0).translate((0.0, 0.0, -0.25))
    frame = outer.cut(inner_cut)

    # Central sprung plate and raised bridge approximate the visible load path.
    center_plate = _rounded_box(19.0, 22.0, 1.7, 2.0).translate((0.0, 0.0, 1.05))
    bridge = _rounded_box(11.5, 27.0, 2.0, 2.0).translate((0.0, 0.0, 2.95))

    # Rivet/contact features: center load button plus two rivet heads.
    button = cq.Workplane("XY").circle(3.0).extrude(1.15).translate((0.0, 0.0, height - 1.15))
    rivet_a = cq.Workplane("XY").circle(2.1).extrude(0.65).translate((0.0, 9.2, height - 0.65))
    rivet_b = cq.Workplane("XY").circle(2.1).extrude(0.65).translate((0.0, -9.2, height - 0.65))

    # Cable/strain-relief approximation. The cable exits toward local +X,
    # matching the existing service direction in concept_v4 assemblies.
    glue = cq.Workplane("XY").ellipse(3.9, 5.2).extrude(1.2).translate((width / 2.0 - 2.2, 0.0, 1.45))
    cable = cq.Workplane("XY").box(24.0, 3.2, 1.3, centered=(True, True, False)).translate((width / 2.0 + 12.0, 0.0, 1.25))

    return frame.union(center_plate).union(bridge).union(button).union(rivet_a).union(rivet_b).union(glue).union(cable)


def _kiwi_sensor_station_lower_features(angle_deg: float, p: ConceptV2Params = P) -> cq.Workplane:
    h = _kiwi_stack_heights(p)
    z = p.lower_thickness_mm
    locator_h = 5.0
    wall_t = p.guide_wall_thickness_mm
    cavity = KIWI_SENSOR_BODY_WIDTH_MM + 2.0 * SENSOR_LOCATOR_CLEARANCE_PER_SIDE_MM
    half = cavity / 2.0

    side_len = 18.0
    side_x = -2.0
    side_y = half + wall_t / 2.0
    upper_side = _local_box(side_len, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=side_x, tangent_offset=side_y)
    lower_side = _local_box(side_len, wall_t, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=side_x, tangent_offset=-side_y)

    inner_x = -(half + wall_t / 2.0)
    inner_stop = _local_box(wall_t, 14.0, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=inner_x)
    rear_pillar_x = inner_x - 1.2
    inner_top = _local_cylinder(SENSOR_REAR_PILLAR_DIAMETER_MM, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=rear_pillar_x, tangent_offset=12.0)
    inner_bottom = _local_cylinder(SENSOR_REAR_PILLAR_DIAMETER_MM, locator_h, p.sensor_radius_mm, angle_deg, z, radial_offset=rear_pillar_x, tangent_offset=-12.0)

    outer_x = half + SENSOR_CLIP_POST_DIAMETER_MM / 2.0 + 0.6
    front_post_h = _sensor_clip_post_height(p)
    outer_top = _local_cylinder(SENSOR_CLIP_POST_DIAMETER_MM, front_post_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x, tangent_offset=13.0)
    outer_bottom = _local_cylinder(SENSOR_CLIP_POST_DIAMETER_MM, front_post_h, p.sensor_radius_mm, angle_deg, z, radial_offset=outer_x, tangent_offset=-13.0)

    # Keep the cable/glue side open. Retention now comes from separate
    # quarter-turn clips on these posts, so no fixed front tails are needed.

    stop_h = h["stop_top_z"] - z
    stops = []
    for radial_offset in (-31.0, 31.0):
        for tangent_offset in (-31.0, 31.0):
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
    body = body.union(outer_top).union(outer_bottom)
    for stop in stops:
        body = body.union(stop)
    return body


def _add_upper_pad_key_notch(body: cq.Workplane, angle_deg: float, inner_r: float, p: ConceptV2Params = P) -> cq.Workplane:
    socket_diameter = UPPER_PAD_LOCATOR_DIAMETER_MM + 2.0 * UPPER_PAD_SOCKET_CLEARANCE_PER_SIDE_MM
    socket = _local_cylinder(
        socket_diameter,
        p.upper_thickness_mm + 0.8,
        p.sensor_radius_mm,
        angle_deg,
        p.upper_z_mm - 0.4,
    )
    throat_len = max(p.sensor_radius_mm - inner_r + socket_diameter / 2.0 + 2.0, 0.0)
    throat_radius = inner_r + throat_len / 2.0 - 1.0
    throat = _local_box(
        throat_len,
        UPPER_PAD_SOCKET_THROAT_WIDTH_MM,
        p.upper_thickness_mm + 0.8,
        throat_radius,
        angle_deg,
        p.upper_z_mm - 0.4,
    )
    return body.cut(socket).cut(throat)


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
    segment = segment.union(_kiwi_sensor_station_lower_features(mid, p))

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
    segment = _add_upper_pad_key_notch(segment, mid, inner_r, p)

    receive_seam = index * (360.0 / p.segment_count)
    outgoing_seam = (index + 1) * (360.0 / p.segment_count)
    segment = _add_upper_top_bolt_features(segment, receive_seam, p.upper_z_mm, p.upper_thickness_mm, p)
    segment = _add_seam_locator_features(segment, receive_seam, outgoing_seam, p.upper_z_mm, p.upper_thickness_mm, p)
    segment = segment.union(_lug_body(outgoing_seam, p.upper_z_mm, "M3", upper_lug=True, p=p))
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
        # counterbore and the shaft points downward to the same-plane underside
        # captured nut pocket.
        head_z = p.upper_z_mm + p.upper_thickness_mm - M3_BUTTON_HEAD_HEIGHT_MM
        shaft_z = p.upper_z_mm
        shaft_h = head_z - shaft_z

    head = cq.Workplane("XY").circle(M3_BUTTON_HEAD_DIAMETER_MM / 2.0).extrude(M3_BUTTON_HEAD_HEIGHT_MM).translate((0, 0, head_z))
    shaft = cq.Workplane("XY").circle(1.5).extrude(shaft_h).translate((0, 0, shaft_z))
    return head.union(shaft)


def seam_fastener_visuals(lower: bool, p: ConceptV2Params = P) -> list[tuple[str, cq.Workplane]]:
    bodies = []
    nut_z = 0.85 if lower else p.upper_z_mm + 0.85
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
    h = _kiwi_stack_heights(p)
    lower_p = lower_pad(p).translate((p.sensor_radius_mm, 0, h["lower_pad_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    sensor = kiwi_sensor_reference_v1(p).translate((p.sensor_radius_mm, 0, h["sensor_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    upper_p = upper_pad(p).translate((p.sensor_radius_mm, 0, h["upper_pad_z"])).rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return [
        (f"sensor_{index}_lower_pad", lower_p),
        (f"sensor_{index}_kiwi_reference_v1", sensor),
        (f"sensor_{index}_upper_pad", upper_p),
    ]


def concept_v4_parts(p: ConceptV2Params = P, include_fastener_visuals: bool = True) -> list[tuple[str, cq.Workplane]]:
    parts: list[tuple[str, cq.Workplane]] = []
    for i in range(p.segment_count):
        parts.append((f"lower_segment_{i}", lower_segment(i, p)))
    for i in range(p.segment_count):
        parts.append((f"upper_segment_{i}", upper_segment(i, p)))
    for i in range(p.segment_count):
        angle = _segment_mid_angle(i, p)
        parts.extend(sensor_stack_parts(i, angle, p))
        parts.extend(sensor_clip_parts(i, angle, closed=True, p=p))
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
        angle = _segment_mid_angle(i, p)
        for name, body in sensor_stack_parts(i, angle, p):
            lift = 0.0
            if "upper_pad" in name:
                lift = 20.0
            elif "kiwi_reference" in name:
                lift = 12.0
            assembly.add(body.translate((0, 0, lift)), name=name)
        for name, body in sensor_clip_parts(i, angle, closed=False, p=p):
            assembly.add(body.translate((0, 0, 16.0)), name=f"{name}_open_raised")
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
    angle = _segment_mid_angle(0, p)
    for name, body in sensor_stack_parts(0, angle, p):
        assembly.add(body, name=name)
    for name, body in sensor_clip_parts(0, angle, closed=True, p=p):
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


def concept_v4_upper_pad_12mm_boss_test_v2(p: ConceptV2Params = P) -> cq.Workplane:
    pad = upper_pad_round_boss(12.0, p)
    bb = pad.val().BoundingBox()
    pad = _engrave_top(pad, "12", 0.0, -16.0, bb.zmax, size=6.5, p=p)
    return pad


def concept_v4_lower_support_test_v1(p: ConceptV2Params = P) -> cq.Workplane:
    current = _rounded_box(44.0, 44.0, p.lower_pad_height_mm, 4.0).translate((-52.0, 0, 0))
    rounded = lower_pad(p, 36.0).translate((0.0, 0, 0))
    frame = lower_pad_frame_support(p).translate((52.0, 0, 0))
    current = _engrave_top(current, "44", -52.0, -26.0, p.lower_pad_height_mm, size=6.5, p=p)
    rounded = _engrave_top(rounded, "36", 0.0, -26.0, p.lower_pad_height_mm, size=6.5, p=p)
    frame = _engrave_top(frame, "FRAME", 52.0, -26.0, p.lower_pad_height_mm, size=6.0, p=p)
    return current.union(rounded).union(frame)


def _locator_variant(clearance: float, label: str, p: ConceptV2Params = P) -> cq.Workplane:
    z = 0.0
    locator_h = 5.0
    wall_t = p.guide_wall_thickness_mm
    cavity = KIWI_SENSOR_BODY_WIDTH_MM + 2.0 * clearance
    half = cavity / 2.0
    base = cq.Workplane("XY").box(58.0, 54.0, 2.0, centered=(True, True, False))
    side_y = half + wall_t / 2.0
    upper_side = cq.Workplane("XY").box(18.0, wall_t, locator_h, centered=(True, True, False)).translate((-2.0, side_y, 2.0))
    lower_side = cq.Workplane("XY").box(18.0, wall_t, locator_h, centered=(True, True, False)).translate((-2.0, -side_y, 2.0))
    inner_x = -(half + wall_t / 2.0)
    inner = cq.Workplane("XY").box(wall_t, 14.0, locator_h, centered=(True, True, False)).translate((inner_x, 0, 2.0))
    outer_x = half + wall_t / 2.0
    outer_top = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((outer_x, 13.0, 2.0))
    outer_bottom = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((outer_x, -13.0, 2.0))
    body = base.union(upper_side).union(lower_side).union(inner).union(outer_top).union(outer_bottom)
    body = _engrave_top(body, label, 0.0, -22.0, 2.0, size=6.5, p=p)
    return body



def _sensor_clip_station_supported_coupon_body(p: ConceptV2Params = P) -> cq.Workplane:
    angle = 0.0
    features = _kiwi_sensor_station_lower_features(angle, p)
    fbb = features.val().BoundingBox()
    margin = 3.0
    base_x = fbb.xlen + 2.0 * margin
    base_y = fbb.ylen + 2.0 * margin
    base_cx = (fbb.xmin + fbb.xmax) / 2.0
    base_cy = (fbb.ymin + fbb.ymax) / 2.0
    base = (
        cq.Workplane("XY")
        .box(base_x, base_y, p.lower_thickness_mm, centered=(True, True, False))
        .translate((base_cx, base_cy, 0.0))
    )
    coupon = base.union(features)
    return _engrave_top(coupon, "CLIP", base_cx, fbb.ymin + 8.0, p.lower_thickness_mm, size=6.5, p=p)


def concept_v4_sensor_clip_station_coupon_v1(p: ConceptV2Params = P) -> cq.Workplane:
    angle = 0.0
    base = cq.Workplane("XY").box(70.0, 64.0, p.lower_thickness_mm, centered=(True, True, False)).translate((p.sensor_radius_mm, 0, 0))
    features = _kiwi_sensor_station_lower_features(angle, p)
    coupon = base.union(features)
    coupon = _engrave_top(coupon, "CLIP", p.sensor_radius_mm, -28.0, p.lower_thickness_mm, size=6.5, p=p)
    bb = coupon.val().BoundingBox()
    return coupon.translate((-bb.xmin + 2.0, -bb.ymin + 2.0, 0.0))


def concept_v4_sensor_clip_station_coupon_v2(p: ConceptV2Params = P) -> cq.Workplane:
    coupon = _sensor_clip_station_supported_coupon_body(p)
    bb = coupon.val().BoundingBox()
    return coupon.translate((-bb.xmin + 2.0, -bb.ymin + 2.0, 0.0))


def concept_v4_sensor_clip_station_open_closed_assembly(p: ConceptV2Params = P) -> cq.Assembly:
    assembly = cq.Assembly(name="concept_v4 sensor clip station open closed")
    angle = 0.0
    coupon = concept_v4_sensor_clip_station_coupon_v2(p)
    # The printable coupon is translated to positive XY; keep a second local
    # supported station in assembly coordinates so clip positions remain legible.
    station = _sensor_clip_station_supported_coupon_body(p)
    assembly.add(station, name="sensor_station_coupon_body")
    h = _kiwi_stack_heights(p)
    sensor = kiwi_sensor_reference_v1(p).translate((p.sensor_radius_mm, 0, h["sensor_z"]))
    assembly.add(sensor, name="kiwi_sensor_reference")
    for name, body in sensor_clip_parts(0, angle, closed=True, p=p):
        assembly.add(body, name=name)
    for name, body in sensor_clip_parts(0, angle, closed=False, p=p):
        assembly.add(body.translate((0, 46.0, 0)), name=name)
    return assembly


def concept_v4_real_sensor_locator_test_v2(p: ConceptV2Params = P) -> cq.Workplane:
    body = _locator_variant(SENSOR_LOCATOR_CLEARANCE_PER_SIDE_MM, "0.4", p)
    body = _engrave_top(body, "KIWI", 0.0, 20.0, 2.0, size=6.5, p=p)
    return body


def _rounded_sensor_locator_variant(clearance: float, label: str, p: ConceptV2Params = P) -> cq.Workplane:
    locator_h = 5.0
    wall_t = p.guide_wall_thickness_mm
    cavity = KIWI_SENSOR_BODY_WIDTH_MM + 2.0 * clearance
    half = cavity / 2.0
    corner_r = 3.2 + clearance

    base = cq.Workplane("XY").box(58.0, 54.0, 2.0, centered=(True, True, False))

    # Side bars remain open and printable, but their ends are rounded to avoid
    # creating artificial clearance around the real sensor's rounded corners.
    side_y = half + wall_t / 2.0
    side_len = 17.0
    upper_side = _rounded_box(side_len, wall_t, locator_h, 1.4).translate((-2.0, side_y, 2.0))
    lower_side = _rounded_box(side_len, wall_t, locator_h, 1.4).translate((-2.0, -side_y, 2.0))

    inner_x = -(half + wall_t / 2.0)
    inner_mid = _rounded_box(wall_t, 12.0, locator_h, 1.4).translate((inner_x, 0, 2.0))
    inner_top = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((inner_x + 0.8, 11.8, 2.0))
    inner_bottom = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((inner_x + 0.8, -11.8, 2.0))

    outer_x = half + wall_t / 2.0
    outer_top = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((outer_x - 0.8, 12.8, 2.0))
    outer_bottom = cq.Workplane("XY").circle(2.75).extrude(locator_h).translate((outer_x - 0.8, -12.8, 2.0))

    # A thin reference outline on the base shows the intended rounded sensor
    # envelope without becoming a retaining cap. It is outside the contact area
    # and shallow enough to remain support-free.
    sensor_outline_outer = _rounded_box(cavity, cavity, 0.6, corner_r).translate((0, 0, 2.0))
    sensor_outline_inner = _rounded_box(max(cavity - 1.2, 1.0), max(cavity - 1.2, 1.0), 1.0, max(corner_r - 0.6, 0.5)).translate((0, 0, 1.8))
    outline = sensor_outline_outer.cut(sensor_outline_inner)

    body = base.union(outline).union(upper_side).union(lower_side).union(inner_mid).union(inner_top).union(inner_bottom).union(outer_top).union(outer_bottom)
    body = _engrave_top(body, label, 0.0, -22.0, 2.0, size=6.5, p=p)
    body = _engrave_top(body, "KIWI", 0.0, 20.0, 2.0, size=6.5, p=p)
    return body


def concept_v4_real_sensor_locator_test_v3(p: ConceptV2Params = P) -> cq.Workplane:
    return _rounded_sensor_locator_variant(0.2, "0.2", p)


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
