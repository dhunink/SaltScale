# Concept v4 Manufacturing Review

Date: 2026-06-07

## Scope

This is a manufacturability and assembly review of `concept_v4_integrated_joining`. It does not redesign the architecture and does not modify CAD.

Reviewed source/export context:

- `cad/src/concept_v4_integrated_joining.py`
- `docs/integrated-m3-joining-review.md`
- active concept v4 STEP/STL exports

Validated assumptions preserved:

- Four-sensor floating architecture.
- Upper ring and lower ring remain mechanically separate.
- M3 bolts and standard captured M3 nuts are acceptable.
- No heat-set inserts.
- No metal dowels.
- Support-grate clearance remains `0.4 mm per side`.
- Sensor locator v3 direction remains active.

## Executive Summary

The integrated M3 idea is promising. The first manufacturing review found three seam details that had to be fixed before treating `concept_v4` as a credible baseline: upper bolt-head clearance, non-fastener alignment, and PETG lug-root stress.

Those fixes have now been applied in CAD. The current `concept_v4` uses top-access recessed M3 button-head screws for the upper seams, underside captured nuts, same-layer printed tongue/socket locators separate from the M3 bolts, broader flat lug-root shoulders, and the accepted Round Cup upper-pad locator.

`concept_v4` still needs physical seam-coupon validation before a full platform print.

## Key CAD Facts

Current concept v4 dimensions from CAD:

| Feature | Value |
| --- | ---: |
| Lower segment envelope after seam refinement | about `185.0 x 159.1 x 21.0 mm` |
| Upper segment envelope after seam refinement | about `179.0 x 158.1 x 18.0 mm` |
| Lower segment base | `z = 0..8 mm` |
| Lower sensor/locator features | up to about `z = 21 mm` |
| Lower integrated lugs | `z = 8..12 mm` |
| Upper segment body | `z = 25..39 mm` |
| Upper integrated lugs | `z = 21..25 mm` |
| Integrated lug size | `24 x 30 x 4 mm` |
| Seam bolt radii | `122 mm`, `145 mm` |
| M3 clearance hole | `3.4 mm` |
| Captured nut pocket | `5.9 mm` across flats |
| Captured nut retaining lip | `5.35 mm` across flats |


## 2026-06-07 Fastener Rework

The prior underside-access upper fastener direction has been replaced. The current full `concept_v4` assembly STEP exports show:

- Lower seam: button-head screw above, shaft downward, captured nut below.
- Upper seam: button-head screw above in a top-side recess, shaft downward, captured nut below in the underside lug.
- Nut visuals include center holes so bolt shafts do not occupy the same volume as solid nut placeholders.

The upper button-head assumption remains:

- Head diameter: `5.7 mm`.
- Head height: `1.8 mm`.
- Counterbore diameter: `6.4 mm`.
- Counterbore depth: `2.0 mm`.

With this assumption, the upper button head occupies `z = 31.2..33.0 mm`, flush/recessed from the upper carrier top surface. The upper captured nut sits in the underside lug at about `z = 21.85..24.25 mm`. Boolean checks show the upper fastener visuals have `0.0 mm^3` overlap with the lower base/features and support grate bars.


## 2026-06-07 Upper Pad Locator Decision

The Round Cup carrier-relative upper-pad locator has been accepted and integrated into active `concept_v4`.

Removed from active CAD:

- Small underside locator tabs.
- Through-hole boss/socket upper pad locator.
- Sensor-relative upper pad locator.

Current active dimensions:

- Round upper pad diameter: `56.0 mm`.
- Cup clearance: `0.45 mm per side`.
- Upper pad height: `3.0 mm`.

Why this is simpler:

- One broad circular cup replaces several competing locator concepts.
- No through-hole is required in the upper carrier.
- No sensor-relative features depend on the exact Kiwi sensor body.
- The pad remains removable by hand.
- The pad lower face remains plain for sensor contact.
- No fastener, clip, or upper-to-lower feature is added.

Checks after integration:

- Upper segment vs round upper pad: `0.0 mm^3` overlap.
- Upper segment vs sensor placeholder: `0.0 mm^3` overlap.
- Full upper carrier vs full lower base: `0.0 mm^3` overlap.
- Support grate bars vs upper/lower: `0.0 mm^3` overlap.

Remaining validation need: physically print the active upper segment and upper pad to confirm the Round Cup fit is removable by hand and not too loose.

## Issues

### 1. Upper bolt heads may protrude below the floating upper carrier

Severity: **Critical**

Location:

- `cad/src/concept_v4_integrated_joining.py`
- `upper_segment()`
- `_lug_body(outgoing_seam, p.upper_z_mm - LUG_HEIGHT_MM, ...)`
- Upper integrated lugs at `z = 21..25 mm`

Finding:

The current upper seam logic implies bolts install from below through the integrated underside lug into captured nuts in the neighboring upper segment. There is no modeled counterbore or recess for bolt heads. A normal M3 socket-head or pan-head bolt would protrude below `z = 21 mm`.

This is dangerous because `z = 21 mm` is also the lower end of the floating upper hardware zone. Any protruding bolt head could become the lowest part of the upper carrier. It may touch lower locator features, overload stops, debris, or the lower base before the intended sensor stack does. That would create an accidental load bypass or assembly interference.

Recommended fix:

- Add an underside counterbore/recess to every upper integrated lug so the selected M3 bolt head sits flush with, or slightly above, the bottom of the upper lug.
- Define the intended bolt type, for example M3 socket-head cap screw or M3 button-head screw, and size the counterbore accordingly.
- Preserve at least the current upper/lower clearance after the bolt head is installed.
- Re-run boolean/clearance checks with bolt-head visual solids included.

Alternative fix:

- Change the upper seam to top-access bolts with captured nuts in the underside lug, but only if the bolt heads can be recessed on the top surface without interfering with the support grate or salt container. This may improve serviceability but needs a separate CAD pass.

### 2. Upper seam fasteners are not serviceable in installed orientation

Severity: **Medium**

Location:

- Upper integrated lugs on underside of upper segments.
- Upper bolts implied to insert from below.

Finding:

The current upper seam fastener orientation is consistent with the previous underside bridge strategy: mechanically simple, but not accessible while the upper carrier is installed on the sensor stack. To tighten or remove upper seam bolts, the salt container and support grate must be removed, then the upper carrier assembly must be lifted off and flipped or accessed from below on the bench.

This is serviceable, but it should be documented as the intended procedure. It does not support easy in-place removal of one upper segment.

Recommended fix:

- If keeping underside upper bolts, explicitly document the service sequence: remove container, remove support grate, lift upper carrier assembly, flip/access underside, remove upper seam bolts.
- If easier in-place service becomes important, investigate top-access upper fasteners with recessed heads.
- Do not solve this by adding any upper-to-lower fastener, spacer, or support.

### 3. Lower seam bolts are blocked after the upper carrier is installed

Severity: **Medium**

Location:

- Lower integrated lugs at `z = 8..12 mm`.
- Lower bolts implied to insert from above.
- Upper carrier sits above the lower ring during normal operation.

Finding:

Lower seam bolts are easy to install during lower-ring assembly. Once the upper carrier and sensor stack are installed, the lower seam bolts are not conveniently accessible from above.

This is acceptable for normal service because a sensor replacement should not require lower-ring disassembly. But if a lower segment ever needs replacement, the upper assembly must be removed first.

Recommended fix:

- Keep lower bolt heads above and lower captured nuts below; this is still the best orientation for lower ring assembly.
- Document that lower-ring service requires removing the upper carrier first.
- Do not move lower bolt heads below unless there is a strong reason; underside bolt access would be worse once the scale is on the floor.

### 4. No bolt-head counterbores or seating features are modeled

Severity: **High for upper, Minor for lower**

Location:

- `_lug_body()` creates M3 clearance holes through plain rectangular lugs.
- No counterbore, countersink, washer seat, or flat head-seat geometry is present.

Finding:

M3 bolt heads will protrude from the lug surfaces. On the lower ring, this is probably acceptable because the lower bolt heads are on top of lower lugs at about `z = 12 mm`, well below the floating upper carrier. On the upper ring, protruding underside bolt heads are not acceptable without a clearance check.

Flat seating is also not defined. FDM top surfaces are usable, but a proper head seat improves repeatability and reduces local crushing.

Recommended fix:

- Add upper-lug underside counterbores as a required fix.
- Add lower-lug shallow counterbores or washer seats as an optional improvement.
- Choose one standard bolt head style for the default BOM before finalizing recess dimensions.
- Avoid countersunk screws unless there is a strong reason; countersinks can split printed plastic and introduce wedging forces.

### 5. Bolts are currently doing too much alignment work

Severity: **High**

Location:

- Integrated seam between neighboring upper or lower segments.
- M3 clearance holes: `3.4 mm`.
- No separate locator features in concept v4 seam geometry.

Finding:

The integrated seam currently relies on bolt holes/lugs for both clamping and positional alignment. That is not ideal. M3 clearance holes need play so builders can insert screws. That same play allows seam shift, ring ovality, and inconsistent support-grate receiver alignment.

Fasteners should clamp. Separate printed features should locate.

Recommended fix:

Add dedicated same-layer alignment geometry separate from the M3 fasteners. Good candidates:

- A shallow tongue-and-groove along each radial seam.
- A printed rectangular shear key and matching pocket.
- Two small tapered printed locator bosses with matching sockets.
- A stepped lap edge that constrains tangential shift while bolts only clamp.

Design rules for locators:

- Lower locators connect only lower-to-lower.
- Upper locators connect only upper-to-upper.
- No locator may bridge upper to lower.
- Locator clearance is now validated at `0.3 mm per side` for the concept v4 tongue/socket seam locator.
- Locators should not be so tight that segment assembly requires hammering.

### 6. Integrated lug roots may be PETG stress concentrators

Severity: **Medium**

Location:

- `_lug_body()`
- Rectangular integrated lugs, about `24 x 30 x 4 mm`, joined to annular segment edge.

Finding:

The lugs are printed flat, which is good. The load from seam tightening is mostly in-plane, which is also good for FDM. But the current lugs appear as simple rectangular pads with sharp transitions into the segment. Repeated tightening, overtightening, or twisting during assembly may concentrate stress at the lug root.

Recommended fix:

- Add generous fillets or rounded root transitions where lugs meet the ring segment.
- Add broad triangular or curved gusset-like shoulders in the XY plane where practical.
- Keep lugs thick enough for bolt-head/nut seating after counterbores are added.
- Add a physical lug coupon before committing to full v4 printing.

### 7. Integrated lugs increase replacement cost if damaged

Severity: **Medium**

Location:

- All integrated seam lugs.

Finding:

Bridge plates were extra parts, but they were also sacrificial and replaceable. In v4, if a lug cracks, is over-tightened, or prints poorly, the full upper or lower segment may need reprinting.

Recommended fix:

- Keep the integrated approach because it reduces assembly burden, but validate lug durability before treating v4 as default.
- Consider making the lug area more robust than the minimum needed.
- Specify torque guidance in assembly docs, for example snug by hand, do not crush PETG.

### 8. Nut insertion sequence must be documented clearly

Severity: **Minor**

Location:

- Lower captured nuts: underside of receiving seam.
- Upper captured nuts: top side of receiving seam.

Finding:

The captured nut dimensions are already physically validated. The issue is assembly order, not geometry. Lower nuts must be pressed into the underside before the lower ring is placed on the floor. Upper nuts press in from the top side, but support grate parts may need to be removed for inspection or access.

Recommended fix:

- Document nut insertion before ring assembly.
- Show lower nut orientation and upper nut orientation in an exploded view.
- Add `NUT` or `M3` engraved labels only on non-contact surfaces if there is enough room.

### 9. Support grate must be removed before upper service

Severity: **Minor**

Location:

- Split support grate bars imported from concept v3.
- Upper support-grate receiver remains upper-only.

Finding:

The support grate does not appear to create a load-path issue, but it spans upper regions and will obstruct handling the upper carrier. Any upper seam or sensor service sequence should start by removing the salt container and support grate bars.

Recommended fix:

- Document support grate removal as the first mechanical service step after removing the salt container.
- Keep the grate removable by hand.
- Do not add grate fasteners until the full upper-carrier fit is physically tested.

### 10. Fastener length is undefined

Severity: **Minor**

Location:

- Integrated M3 lug stack: 4 mm lug plus segment thickness/nut pocket region.

Finding:

The model defines clearances and nut pockets but not screw length or head style. Builders need a standard length that engages the nut reliably without bottoming out or protruding into a forbidden area.

Recommended fix:

- After counterbore choice, define a default screw length in the docs and BOM.
- Likely candidates are M3x12 or M3x14, but this should be confirmed from the final stack depth and selected head style.
- Include a note that bolts should not protrude into support-grate receivers or below the upper lug plane.

## Fastener Orientation Recommendation

### Lower ring

Recommended orientation:

```text
bolt head above -> integrated lower lug -> neighboring lower segment -> captured nut below
```

Reason:

- Easiest lower-ring assembly on the bench.
- Avoids needing access below a floor-supported scale.
- Lower bolt head protrusion is unlikely to affect the measurement stack if it remains below the floating upper structure.

Recommended refinement:

- Optional shallow head seat/counterbore.
- Required clear assembly note that lower nuts are inserted before final placement.

### Upper ring

Current implied orientation:

```text
bolt head below -> integrated upper underside lug -> neighboring upper segment -> captured nut above
```

This is mechanically consistent but needs a required underside counterbore so bolt heads do not protrude below the upper carrier.

Best near-term recommendation:

- Keep this orientation for now because it preserves a clean upper surface for the support grate and salt container.
- Add flush underside counterbores.
- Document that upper seam service requires lifting/removing the upper carrier assembly.

Possible future improvement:

- Top-access upper bolts with recessed heads, only if they can avoid support-grate and container interference.

## Serviceability Review

### Can one segment be removed later?

Conditionally yes. A segment can be removed if both seam connections around it are accessible and all bolts are removed. However, because v4 uses integrated lap lugs, the removal direction may be more constrained than with loose bridge plates. This should be validated with a two-segment seam coupon before printing a full ring.

### Can one sensor be replaced later?

Yes in principle. The sensor replacement sequence remains:

1. Remove salt container.
2. Remove support grate bars.
3. Lift upper carrier assembly or remove the local upper segment if fasteners are accessible.
4. Remove upper pad.
5. Remove/replace sensor from the outside.
6. Reassemble and recalibrate.

The current upper fastener orientation means lifting the upper carrier assembly is the realistic service path.

### Does support grate interfere with service?

Yes, but acceptably. It must be removed before upper carrier service. It remains upper-only and does not create a load bypass.

## Printability Review

Strengths:

- Integrated lugs print flat.
- No support generation should be needed for the main lug shape.
- The segments still fit the Prusa MK4/MK4S/Core One bed.
- The captured nut geometry has already been validated in a coupon.

Risks:

- Lug roots may curl or lift if placed near bed edges.
- Sharp lug transitions may crack if overtightened.
- Counterbores, once added, may reduce lug thickness if not sized carefully.
- Upper underside lugs and bolt heads need careful slicer inspection because they are near the intentional upper/lower clearance boundary.

Recommended validation before full v4 print:

1. Print a two-segment lower integrated-lug seam coupon.
2. Print a two-segment upper integrated-lug seam coupon with bolt-head recess.
3. Test assembly, tightening, removal, and repeated cycles.
4. Check whether segments align without relying on bolt shanks.
5. Add locator geometry if seam shift is visible.

## Overall Recommendation

Do not modify the architecture, but do refine the integrated seam before treating `concept_v4` as the new baseline.

Required before full-platform v4 printing:

1. Add upper bolt-head recesses or choose a safer upper fastener orientation.
2. Add dedicated same-layer alignment features separate from M3 bolts.
3. Add PETG-friendly lug root radii/shoulders.
4. Validate with lower and upper integrated seam coupons.

`concept_v4` remains a promising assembly-simplification candidate, but the current fastener/head/alignment details need another CAD pass.


## 2026-06-07 CAD Fix Status

Applied in `cad/src/concept_v4_integrated_joining.py`:

- Selected M3 button-head screws as the default integrated-seam fastener assumption.
- Added underside counterbores to upper integrated lugs.
- Modeled simple M3 button-head visual solids in assembly STEP exports.
- Added same-layer printed tongue/socket seam locators separate from M3 holes.
- Offset receiving M3 holes/nut pockets into the receiving segment to remove same-layer seam overlap.
- Added broad flat XY lug-root shoulders for PETG-friendly reinforcement.
- Added cropped real-geometry lower and upper integrated seam coupons.

Current fastener assumption:

- M3 button-head screw.
- Modeled head diameter: `5.7 mm`.
- Modeled head height: `1.8 mm`.
- Upper counterbore diameter: `6.4 mm`.
- Upper counterbore depth: `2.0 mm`.

Current locator geometry:

- Printed tongue/socket at the same seam layer.
- Validated `0.3 mm per side` PETG-friendly clearance.
- Bolts clamp; locators align.
- `0.4 mm` and `0.5 mm` were physically tested and showed unnecessary play; no tighter variant is currently required.

Verification checks after the CAD pass:

- Lower segment 0 vs lower segment 1: `0.0 mm^3` overlap.
- Upper segment 0 vs upper segment 1: `0.0 mm^3` overlap.
- Upper segment 0 vs lower segment 0: `0.0 mm^3` overlap.
- Support grate bar X vs upper segment 0: `0.0 mm^3` overlap.
- Support grate bar Y vs upper segment 0: `0.0 mm^3` overlap.
- Support grate bar X vs lower segment 0: `0.0 mm^3` overlap.

Generated validation coupons:

```text
cad/exports/experimental/stl/concept_v4_lower_integrated_seam_coupon_v1.stl
cad/exports/experimental/stl/concept_v4_upper_integrated_seam_coupon_v1.stl
```

Updated recommendation:

Print the upper integrated seam coupon first. It tests the most critical fix: recessed underside upper bolt-head clearance. Do not print full v4 ring segments until both seam coupons pass fit, tightening, removal, and repeated assembly tests.
