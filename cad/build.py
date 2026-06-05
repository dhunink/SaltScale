import importlib
import importlib.util
import os
import sys
from pathlib import Path

import cadquery as cq


BASE = Path(__file__).resolve().parent
SRC = BASE / "src"
EXPORTS = BASE / "exports"

sys.path.append(str(SRC))

from concept_v1 import concept_v1_assembly, concept_v1_compound
from concept_v2 import concept_v2_assembly, lower_segment, sensor_station_coupon, support_grate, upper_segment
from concept_v2_interface_coupons import (
    centering_lip_coupon_v1,
    lower_seam_coupon_v1,
    sensor_station_coupon_v2,
    support_grate_fit_coupon_v1,
    upper_lower_stack_coupon_v1,
    upper_seam_coupon_v1,
)
from concept_v2_sensor_station_v3 import sensor_station_locator_v3
from params import P as LEGACY_P
from platform_v1 import platform_compound
from platform_v2 import platform_v2_full
from platform_v3 import platform_v3_full
from platform_v4 import platform_v4_full
from platform_v5 import platform_v5_assembly, platform_v5_segment
from platform_v6 import platform_v6_assembly, platform_v6_segment
from saltscale_base import assembly_preview, bottom_segment, top_segment
from sensor_module_v1 import sensor_module
from sensor_module_v2 import sensor_module_v2
from sensor_module_v3 import sensor_module_v3
from test_coupon_v1 import test_coupon_v1


ACTIVE_STL = EXPORTS / "active" / "stl"
ACTIVE_STEP = EXPORTS / "active" / "step"
VALIDATION_STL = EXPORTS / "validation" / "stl"
VALIDATION_STEP = EXPORTS / "validation" / "step"
ARCHIVE_STL = EXPORTS / "archive" / "stl"
ARCHIVE_STEP = EXPORTS / "archive" / "step"


def _ensure_dirs() -> None:
    for directory in (ACTIVE_STL, ACTIVE_STEP, VALIDATION_STL, VALIDATION_STEP, ARCHIVE_STL, ARCHIVE_STEP):
        directory.mkdir(parents=True, exist_ok=True)


def _export_stl(obj: object, path: Path) -> None:
    cq.exporters.export(obj, str(path))


def _export_step(obj: object, path: Path) -> None:
    if hasattr(obj, "save"):
        obj.save(str(path))
    else:
        cq.exporters.export(obj, str(path))


def _export_pair(obj: object, name: str, stl_dir: Path, step_dir: Path) -> None:
    _export_stl(obj, stl_dir / f"{name}.stl")
    _export_step(obj, step_dir / f"{name}.step")


def _export_active() -> None:
    _export_step(concept_v2_assembly(), ACTIVE_STEP / "concept_v2_assembly.step")
    _export_pair(lower_segment(0), "concept_v2_lower_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_pair(upper_segment(0), "concept_v2_upper_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_pair(support_grate(), "concept_v2_support_grate", ACTIVE_STL, ACTIVE_STEP)
    print("Exported active concept_v2 files")


def _export_validation() -> None:
    _export_pair(sensor_station_locator_v3(), "sensor_station_locator_v3", VALIDATION_STL, VALIDATION_STEP)
    _export_pair(centering_lip_coupon_v1(), "centering_lip_coupon_v1", VALIDATION_STL, VALIDATION_STEP)
    _export_optional_support_grate_variants()
    _export_optional_printed_joinery_coupons()
    print("Exported current validation coupons")


def _optional_module(name: str):
    if importlib.util.find_spec(name) is None:
        print(f"Skipped optional export module {name} (not present)")
        return None
    return importlib.import_module(name)


def _export_optional_support_grate_variants() -> None:
    module = _optional_module("support_grate_fit_variants")
    if module is None:
        return

    if hasattr(module, "support_grate_fit_variants"):
        variants = module.support_grate_fit_variants()
        for name, body in variants.items():
            _export_pair(body, name, VALIDATION_STL, VALIDATION_STEP)
        return

    for name in (
        "support_grate_fit_0p4mm_per_side",
        "support_grate_fit_0p6mm_per_side",
        "support_grate_fit_0p8mm_per_side",
    ):
        _export_pair(getattr(module, name)(), name, VALIDATION_STL, VALIDATION_STEP)


def _export_optional_printed_joinery_coupons() -> None:
    module = _optional_module("concept_v2_printed_joinery_coupons")
    if module is None:
        return

    if hasattr(module, "printed_joinery_coupons"):
        coupons = module.printed_joinery_coupons()
        for name, body in coupons.items():
            _export_pair(body, name, VALIDATION_STL, VALIDATION_STEP)
        return

    for name in (
        "printed_lower_seam_dovetail_coupon_v1",
        "printed_upper_seam_dovetail_coupon_v1",
        "printed_lower_seam_wedge_coupon_v1",
        "printed_upper_seam_wedge_coupon_v1",
    ):
        _export_pair(getattr(module, name)(), name, VALIDATION_STL, VALIDATION_STEP)


def _export_archive() -> None:
    _export_legacy_saltscale_v1()
    _export_legacy_platforms()
    _export_legacy_sensor_modules()
    _export_legacy_test_coupon()
    _export_concept_v1()
    _export_superseded_concept_v2_coupons()
    print("Exported historical archive files")


def _export_legacy_saltscale_v1() -> None:
    for q in range(4):
        _export_pair(bottom_segment(q), f"bottom_segment_{q}", ARCHIVE_STL, ARCHIVE_STEP)
        _export_pair(top_segment(q), f"top_segment_{q}", ARCHIVE_STL, ARCHIVE_STEP)
    _export_step(assembly_preview(), ARCHIVE_STEP / "saltscale_v1_assembly.step")


def _export_legacy_platforms() -> None:
    _export_pair(platform_compound(), "platform_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(platform_v2_full(), "platform_v2", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(platform_v3_full(), "platform_v3", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(platform_v4_full(), "platform_v4", ARCHIVE_STL, ARCHIVE_STEP)

    for q in range(LEGACY_P.segment_count):
        _export_pair(platform_v5_segment(q), f"platform_v5_segment_{q}", ARCHIVE_STL, ARCHIVE_STEP)
    _export_step(platform_v5_assembly(), ARCHIVE_STEP / "platform_v5_assembly.step")

    for q in range(LEGACY_P.segment_count):
        _export_pair(platform_v6_segment(q), f"platform_v6_segment_{q}", ARCHIVE_STL, ARCHIVE_STEP)
    _export_step(platform_v6_assembly(), ARCHIVE_STEP / "platform_v6_assembly.step")


def _export_legacy_sensor_modules() -> None:
    sensor_base, _sensor_upper = sensor_module()
    _export_pair(sensor_base, "sensor_module_v1", ARCHIVE_STL, ARCHIVE_STEP)

    base2, lower2, upper2, sensor_ph, assembly2 = sensor_module_v2()
    _export_stl(base2, ARCHIVE_STL / "sensor_module_base.stl")
    _export_stl(lower2, ARCHIVE_STL / "sensor_module_lower_pad.stl")
    _export_stl(upper2, ARCHIVE_STL / "sensor_module_upper_pad.stl")
    _export_stl(sensor_ph, ARCHIVE_STL / "sensor_module_sensor_placeholder.stl")
    _export_step(assembly2, ARCHIVE_STEP / "sensor_module_v2_assembly.step")

    base3, lower3, sensor_ph3, upper3, assembly3 = sensor_module_v3()
    _export_stl(base3, ARCHIVE_STL / "sensor_module_v3_base.stl")
    _export_stl(lower3, ARCHIVE_STL / "sensor_module_v3_lower_pad.stl")
    _export_stl(upper3, ARCHIVE_STL / "sensor_module_v3_upper_pad.stl")
    _export_stl(sensor_ph3, ARCHIVE_STL / "sensor_module_v3_sensor_placeholder.stl")
    _export_step(assembly3, ARCHIVE_STEP / "sensor_module_v3_assembly.step")


def _export_legacy_test_coupon() -> None:
    coupon, coupon_upper, coupon_lower, coupon_sensor = test_coupon_v1()
    _export_pair(coupon, "test_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_stl(coupon_upper, ARCHIVE_STL / "test_coupon_upper_pad.stl")
    _export_stl(coupon_lower, ARCHIVE_STL / "test_coupon_lower_pad.stl")
    _export_stl(coupon_sensor, ARCHIVE_STL / "test_coupon_sensor_placeholder.stl")


def _export_concept_v1() -> None:
    _export_stl(concept_v1_compound(), ARCHIVE_STL / "concept_v1.stl")
    _export_step(concept_v1_assembly(), ARCHIVE_STEP / "concept_v1.step")


def _export_superseded_concept_v2_coupons() -> None:
    _export_pair(sensor_station_coupon(), "concept_v2_sensor_station", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(sensor_station_coupon_v2(), "sensor_station_coupon_v2", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(upper_lower_stack_coupon_v1(), "upper_lower_stack_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(lower_seam_coupon_v1(), "lower_seam_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(upper_seam_coupon_v1(), "upper_seam_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_pair(support_grate_fit_coupon_v1(), "support_grate_fit_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)


def main() -> None:
    os.chdir(BASE.parent)
    _ensure_dirs()
    _export_active()
    _export_validation()
    _export_archive()
    print("Exported SaltScale CAD files to cad/exports/{active,validation,archive}")


if __name__ == "__main__":
    main()
