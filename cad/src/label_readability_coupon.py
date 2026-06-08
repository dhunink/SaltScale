"""Label readability coupon for PETG validation.

This coupon compares engraved and raised text at three practical sizes/depths
for Prusa MK4/Core One style PETG printing.
"""

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class LabelCouponParams:
    width_mm: float = 80.0
    height_mm: float = 50.0
    base_thickness_mm: float = 3.0
    divider_width_mm: float = 0.8
    divider_depth_mm: float = 0.5


P = LabelCouponParams()


def _box(x: float, y: float, z: float, cx: float = 0.0, cy: float = 0.0, z0: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").box(x, y, z, centered=(True, True, False)).translate((cx, cy, z0))


def _text(label: str, size: float, depth: float, x: float, y: float, z: float = 0.0) -> cq.Workplane:
    return cq.Workplane("XY").workplane(offset=z).text(label, size, depth, combine=False).translate((x, y, 0.0))


def _engrave(part: cq.Workplane, label: str, size: float, depth: float, x: float, y: float, top_z: float) -> cq.Workplane:
    return part.cut(_text(label, size, -depth, x, y, top_z))


def _raise(part: cq.Workplane, label: str, size: float, height: float, x: float, y: float, top_z: float) -> cq.Workplane:
    return part.union(_text(label, size, height, x, y, top_z))


def label_readability_coupon_v1(p: LabelCouponParams = P) -> cq.Workplane:
    base = _box(p.width_mm, p.height_mm, p.base_thickness_mm)

    # Shallow divider helps identify left=engraved and right=raised without
    # spending printable area on long labels.
    divider = _box(p.divider_width_mm, p.height_mm - 6.0, p.divider_depth_mm + 0.1, 0.0, 0.0, p.base_thickness_mm - p.divider_depth_mm)
    base = base.cut(divider)

    rows = [
        # engraved word, raised word, text size, depth/height, y
        ("IN", "OUT", 5.0, 0.6, 16.0),
        ("PAD", "STOP", 7.0, 0.8, 0.0),
        ("STOP", "SENSOR", 8.0, 1.0, -17.0),
    ]

    for engraved_word, raised_word, size, depth, y in rows:
        base = _engrave(base, engraved_word, size, depth, -24.0, y, p.base_thickness_mm)
        base = _raise(base, raised_word, size, depth, 22.0, y, p.base_thickness_mm)

    return base


if __name__ == "__main__":
    show_object(label_readability_coupon_v1())  # type: ignore[name-defined]
