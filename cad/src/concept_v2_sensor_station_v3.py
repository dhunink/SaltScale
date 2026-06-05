"""Concept v2 sensor station locator v3 coupon.

This is a focused validation coupon for a lower-profile, sensor-shaped locator.
It does not replace the concept_v2 platform architecture. The normal force path
remains upper carrier -> upper pad -> sensor -> lower pad -> lower base.
"""

import cadquery as cq

from concept_v2 import P, ConceptV2Params

LABEL_DEPTH_MM = 0.5


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _cylinder(diameter: float, height: float, cx: float, cy: float, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").circle(diameter / 2.0).extrude(height).translate((cx, cy, z0))


def _engrave(part: cq.Workplane, label: str, x: float, y: float, z: float, size: float = 4.0) -> cq.Workplane:
    text = cq.Workplane("XY").workplane(offset=z).text(label, size, -LABEL_DEPTH_MM, combine=False)
    return part.cut(text.translate((x, y, 0)))


def _sensor_dummy(p: ConceptV2Params = P) -> cq.Workplane:
    body = _box(p.sensor_size_mm, p.sensor_size_mm, p.sensor_height_mm)
    cable = _box(16.0, 4.0, 2.0, p.sensor_size_mm / 2.0 + 8.0, 0.0, 4.0)
    sensor = body.union(cable)
    return _engrave(sensor, "SENSOR", 0.0, 0.0, p.sensor_height_mm, 4.0)


def _locator_features(p: ConceptV2Params = P) -> cq.Workplane:
    base_z = p.lower_thickness_mm
    locator_h = 5.0
    wall_t = 3.0
    total_clearance = 1.0
    cavity = p.sensor_size_mm + total_clearance
    half = cavity / 2.0

    # Short side tabs constrain tangential sliding and rotation without forming
    # long debris-catching rails. The open outer side remains serviceable.
    side_len = 19.0
    side_x = -3.0
    side_y = half + wall_t / 2.0
    upper_side = _box(side_len, wall_t, locator_h, side_x, side_y, base_z)
    lower_side = _box(side_len, wall_t, locator_h, side_x, -side_y, base_z)

    # Inner rounded locator posts and a short inner stop constrain inward motion.
    # The broken shape leaves cleaning gaps and avoids a closed pocket.
    inner_x = -(half + wall_t / 2.0)
    inner_stop = _box(wall_t, 16.0, locator_h, inner_x, 0.0, base_z)
    inner_top = _cylinder(6.0, locator_h, inner_x, 13.5, base_z)
    inner_bottom = _cylinder(6.0, locator_h, inner_x, -13.5, base_z)

    # Low rounded outer cradles catch gross rotation but keep the center of the
    # outer side open for lifting/sliding the sensor out during service.
    outer_x = half + wall_t / 2.0
    outer_top = _cylinder(6.0, locator_h, outer_x, 14.0, base_z)
    outer_bottom = _cylinder(6.0, locator_h, outer_x, -14.0, base_z)
    outer_top_tail = _box(8.0, wall_t, locator_h, outer_x - 4.0, 14.0, base_z)
    outer_bottom_tail = _box(8.0, wall_t, locator_h, outer_x - 4.0, -14.0, base_z)

    locator = upper_side.union(lower_side).union(inner_stop).union(inner_top).union(inner_bottom)
    locator = locator.union(outer_top).union(outer_bottom).union(outer_top_tail).union(outer_bottom_tail)
    return locator


def _overload_stops(p: ConceptV2Params = P) -> cq.Workplane:
    base_z = p.lower_thickness_mm
    stop_h = p.lower_pad_height_mm + p.sensor_height_mm - p.overload_gap_mm
    stop_offset = 31.0
    stops = None
    for x in (-stop_offset, stop_offset):
        for y in (-stop_offset, stop_offset):
            stop = _cylinder(p.overload_stop_diameter_mm, stop_h, x, y, base_z)
            stops = stop if stops is None else stops.union(stop)
    assert stops is not None
    return stops


def sensor_station_locator_v3(p: ConceptV2Params = P) -> cq.Compound:
    """Return a print-kit coupon: station base plus separate sensor dummy."""

    base = _box(104.0, 104.0, p.lower_thickness_mm)
    base = base.union(_locator_features(p)).union(_overload_stops(p))
    base = _engrave(base, "SENSOR LOCATOR", -4.0, 42.0, p.lower_thickness_mm, 4.0)
    base = _engrave(base, "OUTSIDE", 31.0, -43.0, p.lower_thickness_mm, 4.0)
    base = _engrave(base, "STOP", -30.5, -43.0, p.lower_thickness_mm, 4.0)

    sensor = _sensor_dummy(p).translate((82.0, 0.0, 0.0))
    return cq.Compound.makeCompound([base.val(), sensor.val()])


if __name__ == "__main__":
    show_object(sensor_station_locator_v3())  # type: ignore[name-defined]
