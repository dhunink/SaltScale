# Open Questions & Assumptions — Platform CAD

This document collects all dimensional assumptions, unfrozen decisions, places the CAD depends on the loadcell geometry, and recommended next measurements to finalize the platform mechanical design.

## 1) Dimensions currently assumed (from `cad/src/params.py` and `cad/src/platform_v2.py`)

- Platform outer diameter: 320.0 mm (P.outer_diameter_mm)
 - Tank/platform interface diameter (centering lip inner): 300.0 mm (P.centering_lip_inner_diameter_mm) — updated from 294.0 mm per decision
- Total platform height: 42.0 mm (P.total_height_mm)
- Top plate thickness: 6.0 mm (P.top_plate_thickness_mm)
- Bottom plate thickness: 6.0 mm (P.bottom_plate_thickness_mm)
- Wall thickness (rim): 3.0 mm (P.wall_thickness_mm)
- Radial joint width (reference): 8.0 mm (P.radial_joint_width_mm)
- Clearance gap (rim fit): 1.0 mm (P.clearance_gap_mm)
- Overload stop nominal gap: 1.0 mm (P.overload_stop_gap_mm)

- Loadcell placeholder (params):
  - length: 130.0 mm (P.loadcell_length_mm)
  - width: 30.0 mm (P.loadcell_width_mm)
  - height: 22.0 mm (P.loadcell_height_mm)
  - mount hole spacing (base/load): 25.0 mm (P.loadcell_mount_hole_spacing_base_mm / _load.._load)
  - mount hole diameter: 5.2 mm (P.loadcell_mount_hole_diameter_mm)
  - recommended fastener: M5 (P.loadcell_mount_screw)

- platform_v2.py hard-coded/derived values:
  - inner clearance radius used to free the central area: (P.loadcell_length_mm / 2) + 24.0
  - radial ribs per quadrant: 3; rib width: 5.0 mm; rib vertical height: (P.total_height_mm - P.bottom_plate_thickness_mm - 2.0)
  - internal alignment pin diameter: 4.0 mm; pin height: 8.0 mm; socket clearance: +0.6 mm
  - M3 seam screw clearance diameter (modeled): 3.5 mm (clearance for M3)
  - seam screw radial offset when placing holes: (r_outer - 20.0) mm
  - seam screw angular offsets from seam center: +/- 14 degrees
  - overload stop pad nominal radius: 100 mm from center (placed at angles 45/135/225/315)
  - overload stop pad footprint: ~18 x 12 mm (varies by code path)
  - central top pad: (P.loadcell_length_mm + 12) x (P.loadcell_width_mm + 12) x 6 mm (quarter pieces)

Notes: many of the above (especially values in `platform_v2.py`) are conservative engineering guesses intended to produce a printable, stiff platform for PETG. They are not final.

## 2) Dimensions NOT yet frozen (need verification)

- Exact loadcell envelope and mounting geometry (critical): overall length, width, height, mounting hole diameter and spacing, cable exit position.
- Exact loadcell mounting fastener type (M4 vs M5 vs shoulder screws) and requirement for inserts or captive nuts.
- Precise location and size of loadcell mounting bosses / flanges used in the top plate.
- Internal alignment pin/socket diameters, positions and depth tolerances (fit clearance may need +0.1–0.5 mm tuning per printer and PETG shrink).
- Radial rib widths, heights, counts and exact fillets/chamfers for stiffness vs printability tradeoffs.
- Seam screw positions (radial offset and angular offset) — currently guessed for clearance and access.
- Overload stop exact topography: pad width, radius, and precise 1 mm clearance when assembled.
- Any countersink/cap/insert geometry for M3 seam screws or loadcell fasteners.

## 3) Places the design depends on loadcell geometry

- Central inner clearance radius: `inner_clearance_r = (P.loadcell_length_mm / 2) + 24.0` — the inner void that frees the loadcell region is directly sized from loadcell length.
- Central top pad and boss geometry: sizes are expressed as `P.loadcell_* ± offsets`; these directly determine the contact area and how the loadcell will mount to the upper plate.
- Any load path contact ring or boss (if present) must align to the loadcell reaction faces — its radius and position depend on loadcell width and recommended mounting points.
- Mounting holes for the loadcell (not hard-coded yet, but if added) will define required through-holes and reinforcement in both upper and lower plates.
- Cable exit location or side-clearance may require a notch or slot in the skirt near the center; currently not modeled.

Note: design changed from a central single-point loadcell to a four-sensor architecture. The central cavity has been removed in CAD and replaced by four sensor placeholders.

If the loadcell footprint or mounting pattern changes, the following parts of the CAD will need updates: `inner_clearance_r`, central pad size, boss geometry, and any through-holes for mounting screws.

## 4) Recommended next measurements / actions to finalize CAD

1. Obtain the Henk Maas LA360-C datasheet or 2D drawing, and confirm these exact values:
   - overall length (end-to-end)
   - overall width
   - overall height (including cable gland if present)
   - mounting hole diameter(s) and exact hole spacing (center-to-center)
   - recommended fastener size and torque
   - location of cable exit relative to mounting holes and center

2. Decide mounting hardware strategy:
   - use threaded inserts (heat-set) in PETG or through-bolted nuts on the underside?
   - choose M4 vs M5 and whether countersinks or shims are required.

3. Print test coupons:
   - single radial rib section (5 mm × 30–40 mm length) to validate stiffness and bond in PETG.
   - alignment pin/socket pair (4 mm pin with 0.6 mm clearance) to test fit after printing.
   - overload stop pad test: two mating pads with 1.0 mm nominal gap when assembled.

4. Tune tolerances for printer and PETG shrink:
   - run fit tests for alignment pins (±0.1 mm increments) and seam M3 screw clearance holes.

5. After datasheet: update `cad/src/params.py` with final loadcell numbers and modify `platform_v2.py` to add exact mounting holes and insert pockets.

Note: update process for four-sensor architecture — update `hardware/loadcell-spec.md` with vendor part and revise `cad/src/platform_v3.py` to add exact mounting holes/pockets when sensor datasheet is available.

## 5) Quick checklist before freezing dimensions

- [ ] Datasheet received and verified
- [ ] Mounting hardware decided (screws vs inserts)
- [ ] Alignment test prints validated
- [ ] Overload stop clearance confirmed with assembled mock-up
- [ ] Final FEA or hand calculations (optional) to validate rib layout for 30 kg+ loads

## 6) Contact / notes

If you want, I can:
- import an official Henk Maas part drawing into the CAD and place the exact mounting holes
- add heat-set insert pockets or nut pockets for the chosen fasteners
- generate the test-print STL files for the alignment pins, ribs, and overload stop test coupons

Tag: CAD Task 004 — Open questions

## 7) Tank centering geometry — evaluation and recommendation

- Salt container nominal diameter: 290 mm (spec).
 - Current centering inner diameter: 300 mm (updated from 294 mm) → total radial clearance = 300 - 290 = 10 mm; radial clearance per side = 5.0 mm.

Evaluation of tolerances and practical fit:
- Container manufacturing tolerance: typically ±0.5–1.0 mm (depends on supplier and process). If the container is at the high end (+1.0 mm) the effective diameter could be ~291 mm.
- 3D print dimensional tolerances (PETG): typical printed inner features may be undersized by ~0.2–0.8 mm depending on slicer/printer — inner holes/slots commonly print smaller. That means a designed 294 mm ID could print as ~293.2–293.8 mm ID on some setups.
- Combined worst-case (container +1 mm, printed lip −0.5 mm) → effective clearance = 293.5 − 291 = 2.5 mm total → radial = 1.25 mm. This is still usable but a bit tight for hand assembly if the operator expects easy placement.
- Installer/assembly tolerance: users need enough clearance to place the container without fighting the lip; ~1–2 mm radial clearance (total 2–4 mm) is a reasonable practical target for easy assembly while still providing centering.

Recommendation
- Set the centering lip inner diameter to 300 mm (updated).
   - Rationale: 300 mm yields 10 mm total clearance (5.0 mm radial) for the nominal 290 mm container. This increased clearance accommodates container manufacturing tolerances (±0.5–1.0 mm), potential printed undersize, and practical hand placement without sacrificing centering guidance. If tighter centering is required later, the lip can be reduced after validation prints.
   - Note: this change has been applied to `cad/src/params.py`.

Practical next steps to validate
- Measure a production sample container (or ask supplier for tolerance band). Record real-world outer diameter and maximum variation.
- Print a short test ring (inner diameter 294 mm and 295 mm) in the same PETG/printer settings intended for production and test fit with the container. Adjust final CAD based on measured fits.
- Consider adding a shallow lead-in chamfer on the centering lip inner edge (e.g., 1–2 mm × 15°) to help guide the container into position without increasing static clearance.

Action: updated `cad/src/params.py` `centering_lip_inner_diameter_mm` to 300.0. Run test prints to validate; reduce to a tighter value only if tests confirm.
