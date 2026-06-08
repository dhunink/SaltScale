# Test Coupon v1 — Print & Measurement Guide

Purpose
- Validate the riskiest mechanical details before printing a full platform segment: pocket fit, pad fit, overload-stop clearance, dowel fit, and M3 blind pocket behavior.

Coupon dimensions
- Overall coupon XY: 140 × 140 mm.
- Base thickness: 6 mm (matches module base top reference).
- Sensor pocket: uses the `sensor_module_v3` pocket (38 × 38 × 12 mm) and is placed centered on the coupon.

Recommended print orientation
- Lay the coupon flat on the build plate with the coupon lower face down (same orientation used in CAD). This preserves pocket verticality and hole tolerances.

What this coupon validates
- Sensor placeholder fit in pocket (insert/remove force, lateral play).
- Lower pad seating and contact height.
- Upper pad seating and clearance to module stops (verify ~1.0 mm gap before stop contact).
- Module overload stop position and clearance.
- Dowel hole fit (4.2 mm clearance) and boss strength for press-fit or slip-fit dowels.
- M3 blind pocket depth and screw fit.

Measurements to make after printing
- Pocket internal XY dimensions at several depths (top/mid/bottom) — compare to nominal 38 mm and verify clearance.
- Vertical clearance: measure underside of upper pad seating to module stop top (should be ≈1.0 mm gap).
- Dowel hole ID (mm) and roundness — confirm fit with your chosen dowel (e.g., 4.0 mm).
- M3 pocket depth and diameter — verify screw engagement and that screw head clears surrounding features.

Print settings (starting point)
- Material: PETG
- Nozzle: 0.4 mm, temp 240–250 °C; bed 80–90 °C
- Layer height: 0.2 mm for coupon; 0.15–0.2 mm for pads if higher accuracy needed
- Perimeters: 3–4; infill 20–30%
- Brim: 8–12 mm recommended

Procedure
1. Slice and print `test_coupon_v1.stl` and the three part STLs (`upper_pad`, `lower_pad`, `sensor_placeholder`).
2. After cooling, remove brim and clean any stringing.
3. Try inserting `sensor_placeholder` into the pocket; note insertion/removal force and lateral play.
4. Seat `lower_pad` and then `sensor_placeholder` and `upper_pad` in sequence; measure the gap to module stops.
5. Test dowel fit and M3 screw insertion.

Decision gates
- If pocket clearance is too tight (>0.1–0.2 mm interference), increase pocket clearance in CAD (e.g., to 0.6 mm) and repeat coupon print.
- If dowel boss or hole is too loose/tight, adjust boss geometry or dowel diameter.
- If M3 pocket depth is incorrect, update pocket depth in `platform_v6.py` and re-export.
