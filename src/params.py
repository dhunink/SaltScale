from dataclasses import dataclass

@dataclass(frozen=True)
class Params:
    # Tank / platform
    tank_diameter_mm: float = 290.0
    outer_diameter_mm: float = 320.0
    centering_lip_inner_diameter_mm: float = 294.0
    centering_lip_height_mm: float = 5.0
    segment_count: int = 4
    total_height_mm: float = 42.0

    # Printable constraints for Prusa MK4
    max_part_x_mm: float = 200.0
    max_part_y_mm: float = 200.0
    max_part_z_mm: float = 200.0

    # Structural dimensions
    top_plate_thickness_mm: float = 6.0
    bottom_plate_thickness_mm: float = 6.0
    wall_thickness_mm: float = 3.0
    radial_joint_width_mm: float = 8.0
    clearance_gap_mm: float = 1.0
    overload_stop_gap_mm: float = 1.0

    # Loadcell: Henk Maas LA360-C 50kg assumed first CAD target.
    # Verify against purchased datasheet before drilling/printing final parts.
    loadcell_model: str = "LA360-C-50kg"
    loadcell_length_mm: float = 130.0
    loadcell_width_mm: float = 30.0
    loadcell_height_mm: float = 22.0
    loadcell_mount_hole_spacing_base_mm: float = 25.0
    loadcell_mount_hole_spacing_load_mm: float = 25.0
    loadcell_mount_hole_diameter_mm: float = 5.2
    loadcell_mount_screw: str = "M5"

    # Electronics bay rough envelopes
    electronics_bay_width_mm: float = 92.0
    electronics_bay_depth_mm: float = 48.0
    electronics_bay_height_mm: float = 28.0
    battery_holder_length_mm: float = 58.0
    battery_holder_width_mm: float = 48.0
    battery_holder_height_mm: float = 17.0
    button_hole_diameter_mm: float = 12.2
    led_hole_diameter_mm: float = 5.2

P = Params()
