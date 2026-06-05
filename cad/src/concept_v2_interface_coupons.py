"""Small mechanical interface coupons for SaltScale concept_v2.

These are validation coupons, not replacement platform geometry. The goal is
to test the critical interfaces before committing to full ring segment prints.
Multi-part coupons are laid out as separated print-flat kits on one build plate.
"""

import cadquery as cq

from concept_v2 import (
    P,
    ConceptV2Params,
    _annular_sector,
    sensor_station_coupon,
)


LABEL_DEPTH_MM = 0.6


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .box(x, y, z, centered=(True, True, False))
        .translate((cx, cy, z0))
    )


def _cylinder(diameter: float, height: float, cx: float, cy: float, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(height).translate((cx, cy, z0))


def _compound(parts: list[cq.Workplane]) -> cq.Compound:
    return cq.Compound.makeCompound([part.val() for part in parts])


def _engrave(
    part: cq.Workplane,
    label: str,
    x: float,
    y: float,
    z: float,
    size: float = 5.0,
    angle_deg: float = 0.0,
) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    if angle_deg:
        text = text.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    return part.cut(text.translate((x, y, 0)))


def _labeled_sensor_station(p: ConceptV2Params = P) -> cq.Workplane:
    station = sensor_station_coupon(p)
    station = _engrave(station, "LOWER BASE", -12.0, 40.0, p.lower_thickness_mm, 4.5)
    station = _engrave(station, "OVERLOAD STOP", 0.0, 16.0, p.lower_thickness_mm, 4.0)
    station = _engrave(station, "INSIDE", -28.0, -40.0, p.lower_thickness_mm, 4.0)
    station = _engrave(station, "OUTSIDE", 26.0, -40.0, p.lower_thickness_mm, 4.0)
    return station


def _sensor_dummy(p: ConceptV2Params = P) -> cq.Workplane:
    body = _box(p.sensor_size_mm, p.sensor_size_mm, p.sensor_height_mm)
    cable_tab = _box(16.0, 4.0, 2.0, p.sensor_size_mm / 2.0 + 8.0, 0.0, 4.0)
    return _engrave(body.union(cable_tab), "SENSOR DUMMY", 0.0, 0.0, p.sensor_height_mm, 4.0)


def _lower_pad_dummy(p: ConceptV2Params = P) -> cq.Workplane:
    pad = _box(p.lower_pad_size_mm, p.lower_pad_size_mm, p.lower_pad_height_mm)
    return _engrave(pad, "LOWER PAD", 0.0, 0.0, p.lower_pad_height_mm, 4.0)


def _upper_pad_dummy(p: ConceptV2Params = P) -> cq.Workplane:
    pad = _box(p.upper_pad_size_mm, p.upper_pad_size_mm, p.upper_pad_height_mm)
    return _engrave(pad, "UPPER PAD", 0.0, 0.0, p.upper_pad_height_mm, 4.5)


def _upper_carrier_patch(p: ConceptV2Params = P) -> cq.Workplane:
    patch = _box(78.0, 78.0, p.upper_thickness_mm)
    patch = _engrave(patch, "UPPER CARRIER", 0.0, 8.0, p.upper_thickness_mm, 4.5)
    patch = _engrave(patch, "FRONT", 0.0, -24.0, p.upper_thickness_mm, 4.0)
    return patch


def _translate(part: cq.Workplane, x: float, y: float, z: float = 0.0) -> cq.Workplane:
    return part.translate((x, y, z))


def sensor_station_coupon_v2(p: ConceptV2Params = P) -> cq.Compound:
    """Current fixed sensor station plus printable dummy fit pieces."""

    station = _translate(_labeled_sensor_station(p), -44.0, 0.0)
    lower_pad = _translate(_lower_pad_dummy(p), 52.0, -34.0)
    sensor = _translate(_sensor_dummy(p), 52.0, 8.0)
    upper_pad = _translate(_upper_pad_dummy(p), 52.0, 82.0)
    return _compound([station, lower_pad, sensor, upper_pad])


def upper_lower_stack_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    """Local print-flat kit for checking upper/lower stack clearance."""

    lower_station = _translate(_labeled_sensor_station(p), -52.0, -22.0)
    upper_patch = _translate(_upper_carrier_patch(p), 56.0, -32.0)
    lower_pad = _translate(_lower_pad_dummy(p), -52.0, 58.0)
    sensor = _translate(_sensor_dummy(p), 0.0, 58.0)
    upper_pad = _translate(_upper_pad_dummy(p), 70.0, 58.0)
    return _compound([lower_station, upper_patch, lower_pad, sensor, upper_pad])


def _seam_segment_block(
    p: ConceptV2Params,
    pocket_from_top: bool = True,
    cy: float = 0.0,
    label: str = "SEAM",
) -> cq.Workplane:
    block = _box(84.0, 34.0, p.lower_thickness_mm, 0.0, cy)
    x_positions = (-24.0, 24.0)
    for x in x_positions:
        block = block.union(_cylinder(p.seam_boss_diameter_mm, p.lower_thickness_mm, x, cy))
        pocket_z = p.lower_thickness_mm - p.m3_insert_depth_mm if pocket_from_top else 0.0
        block = block.cut(_cylinder(p.m3_insert_diameter_mm, p.m3_insert_depth_mm, x, cy, pocket_z))

    block = block.union(_cylinder(p.seam_boss_diameter_mm, p.lower_thickness_mm, 0.0, cy))
    dowel_z = p.lower_thickness_mm - p.dowel_socket_depth_mm if pocket_from_top else 0.0
    block = block.cut(_cylinder(p.dowel_diameter_mm, p.dowel_socket_depth_mm, 0.0, cy, dowel_z))
    block = _engrave(block, label, -27.0, cy + 10.5, p.lower_thickness_mm, 3.6)
    block = _engrave(block, "M3 INSERT", 16.0, cy + 10.5, p.lower_thickness_mm, 3.6)
    block = _engrave(block, "DOWEL TEST", 0.0, cy - 10.5, p.lower_thickness_mm, 3.6)
    return block


def _seam_bridge_plate(label: str, p: ConceptV2Params = P) -> cq.Workplane:
    plate = _box(84.0, 28.0, p.seam_bridge_height_mm)
    for x in (-24.0, 24.0):
        plate = plate.cut(_cylinder(p.m3_clearance_diameter_mm, p.seam_bridge_height_mm + 0.4, x, 0.0, -0.2))
    plate = plate.cut(_cylinder(p.dowel_diameter_mm + 0.4, p.seam_bridge_height_mm + 0.4, 0.0, 0.0, -0.2))
    plate = _engrave(plate, label, 0.0, 10.0, p.seam_bridge_height_mm, 3.8)
    plate = _engrave(plate, "M3 + DOWEL", 0.0, -10.0, p.seam_bridge_height_mm, 3.6)
    return plate


def lower_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    """Two lower segment edges plus a separate lower seam bridge plate."""

    lower_a = _seam_segment_block(p, pocket_from_top=True, cy=-19.0, label="LOWER")
    lower_b = _seam_segment_block(p, pocket_from_top=True, cy=19.0, label="LOWER")
    bridge = _translate(_seam_bridge_plate("LOWER BRIDGE", p), 0.0, 70.0)
    return _compound([lower_a, lower_b, bridge])


def upper_seam_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    """Two upper segment underside edges plus a separate upper seam bridge plate.

    The coupon is printed with the underside insert pockets facing up.
    """

    upper_a = _seam_segment_block(p, pocket_from_top=True, cy=-19.0, label="UPPER")
    upper_b = _seam_segment_block(p, pocket_from_top=True, cy=19.0, label="UPPER")
    bridge = _translate(_seam_bridge_plate("UPPER BRIDGE", p), 0.0, 70.0)
    return _compound([upper_a, upper_b, bridge])


def support_grate_fit_coupon_v1(p: ConceptV2Params = P) -> cq.Compound:
    """Small upper-carrier section plus a removable grate-arm tab."""

    carrier = _box(92.0, 52.0, p.upper_thickness_mm, -18.0, 0.0)
    channel_clearance = 0.8
    channel = _box(
        74.0,
        p.grate_arm_width_mm + channel_clearance,
        p.grate_thickness_mm + 0.2,
        -28.0,
        0.0,
        p.upper_thickness_mm - p.grate_thickness_mm,
    )
    carrier = carrier.cut(channel)
    end_stop = _box(5.0, p.grate_arm_width_mm + 8.0, 2.0, 11.5, 0.0, p.upper_thickness_mm - 2.0)
    carrier = carrier.union(end_stop)
    carrier = _engrave(carrier, "UPPER CARRIER", -30.0, 19.0, p.upper_thickness_mm, 4.0)
    carrier = _engrave(carrier, "SLOT", -30.0, -19.0, p.upper_thickness_mm, 4.0)

    grate_tab = _box(68.0, p.grate_arm_width_mm, p.grate_thickness_mm, 74.0, 0.0)
    grate_tab = _engrave(grate_tab, "TAB", 74.0, 0.0, p.grate_thickness_mm, 4.2)
    return _compound([carrier, grate_tab])


def centering_lip_coupon_v1(p: ConceptV2Params = P) -> cq.Workplane:
    """Curved section of the 300 mm centering lip and upper carrier."""

    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    carrier = _annular_sector(lip_outer_r, lip_inner_r - 24.0, p.upper_thickness_mm, -14.0, 14.0, 0.0, steps=18)
    lip = _annular_sector(lip_outer_r, lip_inner_r, p.lip_height_mm, -14.0, 14.0, p.upper_thickness_mm, steps=18)
    coupon = carrier.union(lip)
    coupon = _engrave(coupon, "CENTERING LIP", 139.0, 0.0, p.upper_thickness_mm, 4.0, 90.0)
    coupon = _engrave(coupon, "INSIDE", 132.0, -18.0, p.upper_thickness_mm, 3.6, 90.0)
    coupon = _engrave(coupon, "OUTSIDE", 150.0, 18.0, p.upper_thickness_mm, 3.6, 90.0)
    return coupon


def concept_v2_interface_coupons(p: ConceptV2Params = P) -> dict[str, cq.Workplane | cq.Compound]:
    return {
        "sensor_station_coupon_v2": sensor_station_coupon_v2(p),
        "upper_lower_stack_coupon_v1": upper_lower_stack_coupon_v1(p),
        "lower_seam_coupon_v1": lower_seam_coupon_v1(p),
        "upper_seam_coupon_v1": upper_seam_coupon_v1(p),
        "support_grate_fit_coupon_v1": support_grate_fit_coupon_v1(p),
        "centering_lip_coupon_v1": centering_lip_coupon_v1(p),
    }


if __name__ == "__main__":
    show_object(sensor_station_coupon_v2())  # type: ignore[name-defined]
