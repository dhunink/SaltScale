"""Concept v1: clean-sheet four-sensor annular floating scale.

This model intentionally does not reuse platform_v6 or earlier SaltScale
geometry. It demonstrates the recommended architecture:

- lower annular base, split into four printable segments
- floating upper annular carrier, split into four printable segments
- four low-cost load sensors at 45/135/225/315 degrees
- local contact pads, lateral guide rails, and overload stops

The exported model is an assembly demonstrator, not a final printable part set.
"""

from dataclasses import dataclass
import math

import cadquery as cq


@dataclass(frozen=True)
class ConceptParams:
    # Envelope
    outer_diameter_mm: float = 320.0
    tank_diameter_mm: float = 290.0
    centering_lip_inner_diameter_mm: float = 300.0
    segment_count: int = 4
    seam_gap_deg: float = 1.2

    # Annular carriers
    lower_inner_diameter_mm: float = 150.0
    upper_inner_diameter_mm: float = 190.0
    top_contact_outer_diameter_mm: float = 308.0
    lower_thickness_mm: float = 6.0
    upper_thickness_mm: float = 7.0
    upper_z_mm: float = 22.0

    # Centering lip on floating upper carrier
    lip_wall_thickness_mm: float = 4.0
    lip_height_mm: float = 5.0

    # Sensors and contact pads
    sensor_radius_mm: float = 112.0
    sensor_size_mm: float = 38.0
    sensor_height_mm: float = 12.0
    sensor_clearance_mm: float = 0.6
    lower_pad_size_mm: float = 44.0
    lower_pad_height_mm: float = 2.0
    upper_pad_size_mm: float = 56.0
    upper_pad_height_mm: float = 2.0

    # Service/overload features
    guide_wall_thickness_mm: float = 3.0
    guide_wall_height_mm: float = 13.0
    overload_stop_diameter_mm: float = 6.0
    overload_gap_mm: float = 1.0


P = ConceptParams()


def _annular_sector(
    outer_r: float,
    inner_r: float,
    height: float,
    start_deg: float,
    end_deg: float,
    z: float = 0.0,
    steps: int = 36,
) -> cq.Workplane:
    """Create an annular sector extruded from z."""
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
    """Box centered in local radial/tangential coordinates at a polar station."""
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
    """Cylinder centered in local radial/tangential coordinates at a polar station."""
    body = (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(height)
        .translate((radius + radial_offset, tangent_offset, z))
    )
    return body.rotate((0, 0, 0), (0, 0, 1), angle_deg)


def lower_base_segments(p: ConceptParams = P) -> list[cq.Workplane]:
    """Four lower base ring segments."""
    outer_r = p.outer_diameter_mm / 2.0
    inner_r = p.lower_inner_diameter_mm / 2.0
    segments = []
    for q in range(p.segment_count):
        start = q * 90.0 + p.seam_gap_deg / 2.0
        end = (q + 1) * 90.0 - p.seam_gap_deg / 2.0
        segments.append(_annular_sector(outer_r, inner_r, p.lower_thickness_mm, start, end))
    return segments


def upper_carrier_segments(p: ConceptParams = P) -> list[cq.Workplane]:
    """Four floating upper ring segments plus a non-load-bearing centering lip."""
    lip_inner_r = p.centering_lip_inner_diameter_mm / 2.0
    lip_outer_r = lip_inner_r + p.lip_wall_thickness_mm
    outer_r = max(p.top_contact_outer_diameter_mm / 2.0, lip_outer_r)
    inner_r = p.upper_inner_diameter_mm / 2.0

    segments = []
    for q in range(p.segment_count):
        start = q * 90.0 + p.seam_gap_deg / 2.0
        end = (q + 1) * 90.0 - p.seam_gap_deg / 2.0
        top = _annular_sector(outer_r, inner_r, p.upper_thickness_mm, start, end, p.upper_z_mm)
        lip = _annular_sector(
            lip_outer_r,
            lip_inner_r,
            p.lip_height_mm,
            start,
            end,
            p.upper_z_mm + p.upper_thickness_mm,
        )
        segments.append(top.union(lip))
    return segments


def sensor_station(angle_deg: float, p: ConceptParams = P) -> dict[str, cq.Workplane]:
    """Return the bodies that make one sensor station.

    The station is open on the outer radial side so the sensor can be serviced
    after lifting the upper carrier.
    """
    lower_pad_z = p.lower_thickness_mm
    sensor_z = lower_pad_z + p.lower_pad_height_mm
    upper_pad_z = sensor_z + p.sensor_height_mm
    stop_top_z = upper_pad_z - p.overload_gap_mm
    stop_h = stop_top_z - p.lower_thickness_mm

    sensor_span = p.sensor_size_mm + p.sensor_clearance_mm
    guide_height = min(p.guide_wall_height_mm, stop_h)
    guide_z = p.lower_thickness_mm

    lower_pad = _local_box(
        p.lower_pad_size_mm,
        p.lower_pad_size_mm,
        p.lower_pad_height_mm,
        p.sensor_radius_mm,
        angle_deg,
        lower_pad_z,
    )
    sensor = _local_box(
        p.sensor_size_mm,
        p.sensor_size_mm,
        p.sensor_height_mm,
        p.sensor_radius_mm,
        angle_deg,
        sensor_z,
    )
    upper_pad = _local_box(
        p.upper_pad_size_mm,
        p.upper_pad_size_mm,
        p.upper_pad_height_mm,
        p.sensor_radius_mm,
        angle_deg,
        upper_pad_z,
    )

    # Two tangential guide rails plus an inner radial stop. The outer side is
    # deliberately open for sensor removal.
    rail_len = p.upper_pad_size_mm + 8.0
    rail_offset = sensor_span / 2.0 + p.guide_wall_thickness_mm / 2.0
    left_rail = _local_box(
        rail_len,
        p.guide_wall_thickness_mm,
        guide_height,
        p.sensor_radius_mm,
        angle_deg,
        guide_z,
        tangent_offset=rail_offset,
    )
    right_rail = _local_box(
        rail_len,
        p.guide_wall_thickness_mm,
        guide_height,
        p.sensor_radius_mm,
        angle_deg,
        guide_z,
        tangent_offset=-rail_offset,
    )
    inner_stop = _local_box(
        p.guide_wall_thickness_mm,
        sensor_span + 2.0 * p.guide_wall_thickness_mm,
        guide_height,
        p.sensor_radius_mm,
        angle_deg,
        guide_z,
        radial_offset=-(sensor_span / 2.0 + p.guide_wall_thickness_mm / 2.0),
    )

    stops = []
    stop_offset = p.sensor_size_mm / 2.0 + p.overload_stop_diameter_mm / 2.0 + 1.0
    for radial_offset in (-stop_offset, stop_offset):
        for tangent_offset in (-stop_offset, stop_offset):
            stops.append(
                _local_cylinder(
                    p.overload_stop_diameter_mm,
                    stop_h,
                    p.sensor_radius_mm,
                    angle_deg,
                    p.lower_thickness_mm,
                    radial_offset=radial_offset,
                    tangent_offset=tangent_offset,
                )
            )

    stop_body = stops[0]
    for stop in stops[1:]:
        stop_body = stop_body.union(stop)

    guide_body = left_rail.union(right_rail).union(inner_stop)

    return {
        "lower_pad": lower_pad,
        "sensor_placeholder": sensor,
        "upper_pad": upper_pad,
        "guide_body": guide_body,
        "overload_stops": stop_body,
    }


def concept_v1_parts(p: ConceptParams = P) -> list[tuple[str, cq.Workplane]]:
    """Return named bodies for the concept assembly."""
    parts: list[tuple[str, cq.Workplane]] = []

    for i, segment in enumerate(lower_base_segments(p)):
        parts.append((f"lower_base_segment_{i}", segment))

    for i, segment in enumerate(upper_carrier_segments(p)):
        parts.append((f"upper_carrier_segment_{i}", segment))

    for i, angle in enumerate((45.0, 135.0, 225.0, 315.0)):
        station = sensor_station(angle, p)
        for name, body in station.items():
            parts.append((f"sensor_{i}_{name}", body))

    return parts


def concept_v1_compound(p: ConceptParams = P) -> cq.Compound:
    """Return a multi-solid compound for STL export."""
    solids = [body.val() for _, body in concept_v1_parts(p)]
    return cq.Compound.makeCompound(solids)


def concept_v1_assembly(p: ConceptParams = P) -> cq.Assembly:
    """Return a CadQuery assembly for STEP export."""
    assembly = cq.Assembly(name="SaltScale concept_v1")
    for name, body in concept_v1_parts(p):
        assembly.add(body, name=name)
    return assembly


if __name__ == "__main__":
    show_object(concept_v1_compound())  # type: ignore[name-defined]
