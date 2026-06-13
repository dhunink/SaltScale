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
from concept_v2 import (
    concept_v2_assembly,
    concept_v2_exploded_assembly,
    concept_v2_one_quadrant_assembly,
    concept_v2_one_quadrant_exploded_assembly,
    lower_bridge_plate,
    lower_pad,
    lower_segment,
    sensor_placeholder,
    sensor_station_coupon,
    support_grate,
    upper_bridge_plate,
    upper_pad,
    upper_segment,
)
from concept_v2_interface_coupons import (
    centering_lip_coupon_v1,
    lower_seam_coupon_v1,
    sensor_station_coupon_v2,
    support_grate_fit_coupon_v1,
    upper_lower_stack_coupon_v1,
    upper_seam_coupon_v1,
)
from concept_v2_sensor_station_v3 import sensor_station_locator_v3
from concept_v3_print_optimized import (
    concept_v3_assembly,
    concept_v3_exploded_assembly,
    concept_v3_one_section_assembly,
    lower_bridge_plate as concept_v3_lower_bridge_plate,
    lower_plain_segment as concept_v3_lower_plain_segment,
    lower_sensor_segment as concept_v3_lower_sensor_segment,
    support_grate_bar_x as concept_v3_support_grate_bar_x,
    support_grate_bar_y as concept_v3_support_grate_bar_y,
    upper_bridge_plate as concept_v3_upper_bridge_plate,
    upper_plain_segment as concept_v3_upper_plain_segment,
    upper_sensor_segment as concept_v3_upper_sensor_segment,
    P as CONCEPT_V3_P,
)
from concept_v4_integrated_joining import (
    concept_v4_assembly,
    concept_v4_exploded_assembly,
    concept_v4_lower_integrated_seam_coupon_v1,
    concept_v4_one_quadrant_assembly,
    concept_v4_sensor_clip_station_coupon_v1,
    concept_v4_sensor_clip_station_coupon_v2,
    concept_v4_sensor_clip_station_open_closed_assembly,
    concept_v4_upper_integrated_seam_coupon_v1,
    concept_v4_upper_pad_12mm_boss_test_v2,
    concept_v4_lower_support_test_v1,
    concept_v4_real_sensor_locator_test_v2,
    concept_v4_real_sensor_locator_test_v3,
    kiwi_sensor_reference_v1 as concept_v4_kiwi_sensor_reference_v1,
    lower_pad as concept_v4_lower_pad,
    lower_segment as concept_v4_lower_segment,
    sensor_quarter_turn_clip as concept_v4_sensor_quarter_turn_clip,
    support_grate_bar_x as concept_v4_support_grate_bar_x,
    support_grate_bar_y as concept_v4_support_grate_bar_y,
    upper_pad as concept_v4_upper_pad,
    upper_segment as concept_v4_upper_segment,
    P as CONCEPT_V4_P,
)
from concept_v4_micro_coupons import micro_coupon_exports
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
VALIDATED_STL = EXPORTS / "validated" / "stl"
VALIDATED_STEP = EXPORTS / "validated" / "step"
EXPERIMENTAL_STL = EXPORTS / "experimental" / "stl"
EXPERIMENTAL_STEP = EXPORTS / "experimental" / "step"
REJECTED_STL = EXPORTS / "rejected" / "stl"
REJECTED_STEP = EXPORTS / "rejected" / "step"
ARCHIVE_STL = EXPORTS / "archive" / "stl"
ARCHIVE_STEP = EXPORTS / "archive" / "step"


def _ensure_dirs() -> None:
    for directory in (
        ACTIVE_STL,
        ACTIVE_STEP,
        VALIDATED_STL,
        VALIDATED_STEP,
        EXPERIMENTAL_STL,
        EXPERIMENTAL_STEP,
        REJECTED_STL,
        REJECTED_STEP,
        ARCHIVE_STL,
        ARCHIVE_STEP,
    ):
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


def _to_z0(obj: object) -> object:
    if hasattr(obj, "val"):
        bb = obj.val().BoundingBox()
        return obj.translate((0, 0, -bb.zmin))
    return obj


def _upper_pad_print_orientation(obj: object) -> object:
    # Assembly orientation has the 12 mm contact boss downward. Flip standalone
    # pad exports so the broad 40 mm body prints flat on the bed and the boss
    # builds upward without support.
    if hasattr(obj, "rotate"):
        return obj.rotate((0, 0, 0), (1, 0, 0), 180)
    return obj


def _export_printable_pair(obj: object, name: str, stl_dir: Path, step_dir: Path) -> None:
    printable = _to_z0(obj)
    _export_stl(printable, stl_dir / f"{name}.stl")
    _export_step(printable, step_dir / f"{name}.step")


def _export_active() -> None:
    _export_concept_v4_active()

def _export_concept_v3_active() -> None:
    _export_step(concept_v3_assembly(), ACTIVE_STEP / "concept_v3_assembly.step")
    _export_step(concept_v3_exploded_assembly(), ACTIVE_STEP / "concept_v3_exploded_assembly.step")
    _export_step(concept_v3_one_section_assembly(), ACTIVE_STEP / "concept_v3_one_section_assembly.step")

    _export_printable_pair(concept_v3_lower_sensor_segment(0), "concept_v3_lower_sensor_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_lower_plain_segment(1), "concept_v3_lower_plain_segment_1", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_upper_sensor_segment(0), "concept_v3_upper_sensor_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_upper_plain_segment(1), "concept_v3_upper_plain_segment_1", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_support_grate_bar_x(), "concept_v3_support_grate_bar_x", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_support_grate_bar_y(), "concept_v3_support_grate_bar_y", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_lower_bridge_plate(), "concept_v3_lower_bridge_plate", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v3_upper_bridge_plate(), "concept_v3_upper_bridge_plate", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(lower_pad(CONCEPT_V3_P), "concept_v3_lower_pad", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(upper_pad(CONCEPT_V3_P), "concept_v3_upper_pad", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(sensor_placeholder(CONCEPT_V3_P), "concept_v3_sensor_placeholder", ACTIVE_STL, ACTIVE_STEP)
    print("Exported active concept_v3 print-optimized candidate files")


def _export_concept_v4_active() -> None:
    _export_step(concept_v4_assembly(), ACTIVE_STEP / "concept_v4_assembly.step")
    _export_step(concept_v4_exploded_assembly(), ACTIVE_STEP / "concept_v4_exploded_assembly.step")
    _export_step(concept_v4_one_quadrant_assembly(), ACTIVE_STEP / "concept_v4_one_quadrant_assembly.step")

    _export_printable_pair(concept_v4_lower_segment(0), "concept_v4_lower_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_upper_segment(0), "concept_v4_upper_segment_0", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_support_grate_bar_x(CONCEPT_V4_P), "concept_v4_support_grate_bar_x", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_support_grate_bar_y(CONCEPT_V4_P), "concept_v4_support_grate_bar_y", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_lower_pad(CONCEPT_V4_P), "concept_v4_lower_pad", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(_upper_pad_print_orientation(concept_v4_upper_pad(CONCEPT_V4_P)), "concept_v4_upper_pad", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_sensor_quarter_turn_clip(CONCEPT_V4_P), "concept_v4_sensor_quarter_turn_clip", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_kiwi_sensor_reference_v1(CONCEPT_V4_P), "concept_v4_sensor_placeholder", ACTIVE_STL, ACTIVE_STEP)
    _export_printable_pair(concept_v4_kiwi_sensor_reference_v1(CONCEPT_V4_P), "concept_v4_kiwi_sensor_reference_v1", ACTIVE_STL, ACTIVE_STEP)
    print("Exported active concept_v4 integrated joining candidate files")


def _export_validation() -> None:
    _export_pair(sensor_station_locator_v3(), "sensor_station_locator_v3", VALIDATED_STL, VALIDATED_STEP)
    _export_pair(centering_lip_coupon_v1(), "centering_lip_coupon_v1", ARCHIVE_STL, ARCHIVE_STEP)
    _export_optional_support_grate_variants()
    _export_optional_label_readability_coupon()
    _export_optional_practical_test_prints()
    _export_optional_upper_pad_positioning_coupons()
    _export_optional_upper_pad_pocket_alternatives()
    _export_optional_bolted_joinery_coupons()
    _export_optional_printed_joinery_coupons()
    _export_printable_pair(
        concept_v4_lower_integrated_seam_coupon_v1(),
        "concept_v4_lower_integrated_seam_coupon_v1",
        EXPERIMENTAL_STL,
        EXPERIMENTAL_STEP,
    )
    _export_printable_pair(
        concept_v4_upper_integrated_seam_coupon_v1(),
        "concept_v4_upper_integrated_seam_coupon_v1",
        EXPERIMENTAL_STL,
        EXPERIMENTAL_STEP,
    )
    for name, body in micro_coupon_exports().items():
        _export_printable_pair(body, name, EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(_upper_pad_print_orientation(concept_v4_upper_pad_12mm_boss_test_v2()), "concept_v4_upper_pad_12mm_boss_test_v2", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(concept_v4_lower_support_test_v1(), "concept_v4_lower_support_test_v1", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(concept_v4_real_sensor_locator_test_v2(), "concept_v4_real_sensor_locator_test_v2", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(concept_v4_real_sensor_locator_test_v3(), "concept_v4_real_sensor_locator_test_v3", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(concept_v4_sensor_clip_station_coupon_v1(), "concept_v4_sensor_clip_station_coupon_v1", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_printable_pair(concept_v4_sensor_clip_station_coupon_v2(), "concept_v4_sensor_clip_station_coupon_v2", EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    _export_step(concept_v4_sensor_clip_station_open_closed_assembly(), EXPERIMENTAL_STEP / "concept_v4_sensor_clip_station_open_closed.step")
    print("Exported classified validation artifacts")


def _optional_module(name: str):
    if importlib.util.find_spec(name) is None:
        print(f"Skipped optional export module {name} (not present)")
        return None
    return importlib.import_module(name)


def _export_optional_support_grate_variants() -> None:
    module = _optional_module("support_grate_fit_variants")
    if module is None:
        return

    names = (
        "support_grate_fit_0p4mm_per_side",
        "support_grate_fit_0p6mm_per_side",
        "support_grate_fit_0p8mm_per_side",
    )
    for name in names:
        target_stl, target_step = (VALIDATED_STL, VALIDATED_STEP) if "0p4" in name else (REJECTED_STL, REJECTED_STEP)
        _export_pair(getattr(module, name)(), name, target_stl, target_step)



def _export_optional_label_readability_coupon() -> None:
    module = _optional_module("label_readability_coupon")
    if module is None:
        return

    _export_pair(module.label_readability_coupon_v1(), "label_readability_coupon_v1", VALIDATED_STL, VALIDATED_STEP)
    print("Exported label readability coupon")


def _export_optional_practical_test_prints() -> None:
    module = _optional_module("concept_v2_practical_test_prints")
    if module is None:
        return

    prints = module.practical_test_prints() if hasattr(module, "practical_test_prints") else {
        name: getattr(module, name)()
        for name in (
            "test_label_readability_v1",
            "test_m3_captured_nut_v1",
            "test_support_grate_fit_v1",
            "test_sensor_locator_v3_fit_v1",
            "test_bolted_seam_slice_v1",
        )
    }
    validated_names = {
        "test_label_readability_v1",
        "test_m3_captured_nut_v1",
        "test_support_grate_fit_v1",
        "test_sensor_locator_v3_fit_v1",
    }
    for name, body in prints.items():
        target_stl, target_step = (VALIDATED_STL, VALIDATED_STEP) if name in validated_names else (EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
        _export_pair(body, name, target_stl, target_step)
    print("Exported practical test prints")


def _export_optional_upper_pad_positioning_coupons() -> None:
    module = _optional_module("concept_v4_upper_pad_positioning_coupons")
    if module is None:
        return

    for name, body in module.upper_pad_positioning_coupon_exports().items():
        _export_pair(body, name, REJECTED_STL, REJECTED_STEP)
    print("Exported rejected concept_v4 upper pad positioning coupons")


def _export_optional_upper_pad_pocket_alternatives() -> None:
    module = _optional_module("concept_v4_upper_pad_pocket_alternatives")
    if module is None:
        return

    for name, body in module.pocket_alternative_exports().items():
        target_stl, target_step = (VALIDATED_STL, VALIDATED_STEP) if "round_cup" in name else (REJECTED_STL, REJECTED_STEP)
        _export_pair(body, name, target_stl, target_step)
    print("Exported classified concept_v4 upper pad pocket alternatives")


def _export_optional_bolted_joinery_coupons() -> None:
    module = _optional_module("concept_v2_bolted_joinery_coupons")
    if module is None:
        return

    if hasattr(module, "bolted_joinery_coupons"):
        coupons = module.bolted_joinery_coupons()
        for name, body in coupons.items():
            _export_pair(body, name, VALIDATED_STL, VALIDATED_STEP)
        print("Exported bolted joinery coupons")
        return

    for name in (
        "bolted_lower_seam_coupon_v1",
        "bolted_upper_seam_coupon_v1",
        "bolted_lower_seam_captured_nut_coupon_v1",
        "bolted_upper_seam_captured_nut_coupon_v1",
    ):
        _export_pair(getattr(module, name)(), name, VALIDATED_STL, VALIDATED_STEP)
    print("Exported bolted joinery coupons")


def _export_optional_printed_joinery_coupons() -> None:
    module = _optional_module("concept_v2_printed_joinery_coupons")
    if module is None:
        return

    if hasattr(module, "printed_joinery_coupons"):
        coupons = module.printed_joinery_coupons()
        for name, body in coupons.items():
            _export_pair(body, name, EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
        print("Exported experimental printed-only joinery coupons")
        return

    for name in (
        "printed_lower_seam_sliding_key_coupon_v1",
        "printed_upper_seam_sliding_key_coupon_v1",
        "printed_lower_seam_true_dovetail_coupon_v1",
        "printed_upper_seam_true_dovetail_coupon_v1",
        "printed_lower_seam_wedge_coupon_v2",
        "printed_upper_seam_wedge_coupon_v2",
    ):
        _export_pair(getattr(module, name)(), name, EXPERIMENTAL_STL, EXPERIMENTAL_STEP)
    print("Exported experimental printed-only joinery coupons")


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
    print("Exported SaltScale CAD files to cad/exports/{active,validated,experimental,rejected,archive}")


if __name__ == "__main__":
    main()
