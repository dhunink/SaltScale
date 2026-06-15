"""Export only the concept_v5 cartridge-based SaltScale artifacts."""

from pathlib import Path
import sys

import cadquery as cq
from cadquery import exporters


BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
EXPORT_ROOT = BASE / "exports" / "concept_v5_cartridge"
STEP_DIR = EXPORT_ROOT / "step"
STL_DIR = EXPORT_ROOT / "stl"

sys.path.append(str(SRC))

from concept_v5_cartridge_scale import concept_v5_assembly, printable_parts


def _ensure_dirs() -> None:
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)


def _to_z0(obj: cq.Workplane) -> cq.Workplane:
    bb = obj.val().BoundingBox()
    return obj.translate((0.0, 0.0, -bb.zmin))


def _export_step(obj: object, path: Path) -> None:
    if hasattr(obj, "save"):
        obj.save(str(path))
    else:
        exporters.export(obj, str(path))


def _export_stl(obj: cq.Workplane, path: Path) -> None:
    exporters.export(obj, str(path), tolerance=0.15, angularTolerance=0.2)


def main() -> None:
    _ensure_dirs()
    _export_step(concept_v5_assembly(), STEP_DIR / "concept_v5_cartridge_assembly.step")

    for name, part in printable_parts().items():
        printable = _to_z0(part)
        _export_step(printable, STEP_DIR / f"{name}.step")
        _export_stl(printable, STL_DIR / f"{name}.stl")

    print(f"Exported concept_v5 cartridge artifacts to {EXPORT_ROOT}")


if __name__ == "__main__":
    main()
