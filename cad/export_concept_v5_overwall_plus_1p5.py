"""Export the concept_v5 over-wall clip test with 1.5 mm taller locator walls."""

from pathlib import Path
import sys

import cadquery as cq
from cadquery import exporters


BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
EXPORT_ROOT = BASE / "exports" / "concept_v5_overwall_plus_1p5"
STEP_DIR = EXPORT_ROOT / "step"
STL_DIR = EXPORT_ROOT / "stl"

sys.path.append(str(SRC))

from concept_v5_cartridge_scale import (  # noqa: E402
    P,
    kiwi_sensor_reference_v2,
    sensor_cartridge_over_wall_plus_1p5,
    sensor_retainer_over_wall_plus_1p5,
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
    exporters.export(printable, str(STL_DIR / f"{name}.stl"), tolerance=0.12, angularTolerance=0.18)


def _export_preview() -> None:
    p = P
    assembly = cq.Assembly(name="concept_v5_overwall_plus_1p5_preview")
    assembly.add(sensor_cartridge_over_wall_plus_1p5(), name="cartridge_plus_1p5")
    assembly.add(kiwi_sensor_reference_v2(), name="sensor_reference", loc=cq.Location(cq.Vector(0, 0, p.sensor_z_mm - p.cartridge_z_mm)))
    assembly.add(sensor_retainer_over_wall_plus_1p5(), name="retainer_plus_1p5")
    assembly.save(str(STEP_DIR / "concept_v5_overwall_plus_1p5_preview.step"))


def main() -> None:
    _ensure_dirs()
    _export_part("concept_v5_sensor_cartridge_overwall_plus_1p5", sensor_cartridge_over_wall_plus_1p5())
    _export_part("concept_v5_retainer_overwall_plus_1p5", sensor_retainer_over_wall_plus_1p5())
    _export_preview()
    print(f"Exported concept_v5 over-wall +1.5 mm test to {EXPORT_ROOT}")


if __name__ == "__main__":
    main()
