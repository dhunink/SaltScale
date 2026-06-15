"""Export concept_v5 puck and upper-contact test coupons."""

from pathlib import Path
import sys

import cadquery as cq
from cadquery import exporters


BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
EXPORT_ROOT = BASE / "exports" / "concept_v5_contact_tests"
STEP_DIR = EXPORT_ROOT / "step"
STL_DIR = EXPORT_ROOT / "stl"

sys.path.append(str(SRC))

from concept_v5_contact_tests import printable_contact_tests  # noqa: E402


def _ensure_dirs() -> None:
    STEP_DIR.mkdir(parents=True, exist_ok=True)
    STL_DIR.mkdir(parents=True, exist_ok=True)


def _to_z0(obj: cq.Workplane) -> cq.Workplane:
    bb = obj.val().BoundingBox()
    return obj.translate((0.0, 0.0, -bb.zmin))


def main() -> None:
    _ensure_dirs()
    for name, part in printable_contact_tests().items():
        printable = _to_z0(part)
        exporters.export(printable, str(STEP_DIR / f"{name}.step"))
        exporters.export(printable, str(STL_DIR / f"{name}.stl"), tolerance=0.12, angularTolerance=0.18)
    print(f"Exported concept_v5 contact tests to {EXPORT_ROOT}")


if __name__ == "__main__":
    main()
