"""Export quick concept_v5 clamp test variants without rebuilding the assembly."""

from pathlib import Path
import sys

import cadquery as cq
from cadquery import exporters


BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
EXPORT_ROOT = BASE / "exports" / "concept_v5_clamp_variants"
STEP_DIR = EXPORT_ROOT / "step"
STL_DIR = EXPORT_ROOT / "stl"

sys.path.append(str(SRC))

from concept_v5_cartridge_scale import (  # noqa: E402
    sensor_cartridge_tall_wall,
    sensor_retainer_closed_cap,
    sensor_retainer_over_wall_clip,
)


def _ensure_dirs() -> None:
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)


def _to_z0(obj: cq.Workplane) -> cq.Workplane:
    bb = obj.val().BoundingBox()
    return obj.translate((0.0, 0.0, -bb.zmin))


def _export_part(name: str, part: cq.Workplane) -> None:
    printable = _to_z0(part)
    exporters.export(printable, str(STEP_DIR / f"{name}.step"))
    exporters.export(printable, str(STL_DIR / f"{name}.stl"), tolerance=0.15, angularTolerance=0.2)


def main() -> None:
    _ensure_dirs()
    _export_part("concept_v5_retainer_closed_current_wall", sensor_retainer_closed_cap())
    _export_part("concept_v5_sensor_cartridge_tall_wall", sensor_cartridge_tall_wall())
    _export_part("concept_v5_retainer_over_wall_tall", sensor_retainer_over_wall_clip())
    print(f"Exported concept_v5 clamp variants to {EXPORT_ROOT}")


if __name__ == "__main__":
    main()
