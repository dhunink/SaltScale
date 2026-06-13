# Validated Design Decisions

Date: 2026-06-06

## Purpose

This record captures SaltScale design decisions that are now based on physical validation prints, not only CAD assumptions.

These decisions should be treated as frozen defaults for future `concept_v2` CAD work unless a later, larger print produces a clear conflicting result.

## Captured M3 Nut Pocket

Physical result:

- M3 nut requires light press-fit insertion.
- Nut does not rotate.
- Nut does not fall out.
- M3 bolt fit is correct.

Decision:

- Freeze current captured M3 nut pocket dimensions.
- Do not enlarge the captured nut pocket unless future larger seam or quadrant prints show assembly issues.
- Use captured standard M3 nuts as the default no-heat-set segment-joining direction.

Current accepted dimensions are documented in `docs/bolted-captured-nut-coupon-plan.md`.

## Label Standard

Physical result:

- `7-8 mm` text is clearly readable.
- `0.8 mm` engraved depth is sufficient.
- Smaller text becomes difficult to read.
- Larger labels are preferred.

Decision:

- Standard label height: `7-8 mm`.
- Standard engraved depth: `0.8 mm`.
- Use short labels whenever possible.

Preferred label words:

- `IN`
- `OUT`
- `PAD`
- `STOP`
- `SENSOR`
- `NUT`
- `M3`
- `KEY`

Avoid long labels on validation or functional parts unless the part has enough non-contact area.

## Engraved vs Raised Text

Physical result:

- Labels must not interfere with mechanical interfaces.
- Many SaltScale parts stack, slide, clamp, or contact each other.

Decision:

- Engraved text is the default for all functional parts.
- Raised text is not allowed on functional contact surfaces.
- Raised text may only be used on presentation or demo parts where it cannot affect assembly or load paths.

Functional parts include:

- sensor stations
- upper pads
- lower pads
- support grate interfaces
- bridge plates
- seam hardware
- upper carrier segments
- lower base segments

## Support-Grate Tab/Slot Clearance

Physical result:

- `0.4`, `0.6`, and `0.8 mm` per side variants all remained removable.
- None of the tested variants fell out.
- All tested variants still allowed visible/playable movement.
- `0.4 mm per side` had the least play and is the best tested option.

Decision:

- Use `0.4 mm per side` as the current default support-grate tab/slot clearance.
- Do not make the support-grate interface looser by default.
- If the full upper-carrier implementation still feels too loose, create and test a `0.2 mm per side` variant before changing the active design.
- Future work may explore self-centering or tapered support-grate locator geometry, but that is an improvement path, not a reason to loosen the current default.

## Concept v4 Seam Locator Clearance

Physical result:

- `0.5 mm per side` showed unnecessary play.
- `0.4 mm per side` still showed unnecessary play.
- `0.3 mm per side` remained easy to assemble.
- `0.3 mm per side` provided the best alignment of the tested variants.
- Locators are positioning features only.
- M3 fasteners provide clamping.

Decision:

- Use `0.3 mm per side` as the active `concept_v4` seam locator clearance.
- Do not create a tighter locator variant unless a future full-size segment print shows measurable play.
- Keep M3 bolts responsible for clamping.
- Keep printed locators responsible only for segment positioning.

## Future CAD Rule

For all future CAD work:

- Use engraved text by default.
- Use `7-8 mm` text height.
- Use `0.8 mm` engraving depth.
- Avoid long labels.
- Do not re-test label geometry unless a future print reveals a problem.

## Superseded Guidance

Earlier documents may mention smaller labels, shallow engraving, heat-set insert-first seams, or dowel-focused seam tests. Those notes are historical unless they are explicitly repeated in this document or in newer `concept_v2` strategy docs.

Specifically:

- `docs/test-coupon-v1.md` is historical platform-v6-era coupon guidance.
- `docs/coupon-label-reference.md` documents an earlier label pass and should not override the label standard above.
- `docs/label-readability-coupon.md` remains useful as the test description, but the validated decision is now this document.

## Next Validation Step

After freezing these small-interface decisions, proceed to larger same-geometry checks:

1. Lower captured-nut bolted seam coupon.
2. Upper captured-nut bolted seam coupon.
3. One realistic quadrant stack with lower segment, upper segment, support grate using `0.4 mm per side` clearance, sensor stack, and same-layer seam hardware.


## Applied To Full Concept v2

The validated captured M3 nut pocket, default bolted bridge-plate seam strategy, engraved label standard, and v3-style sensor locator direction have been applied to `cad/src/concept_v2.py`.

Support-grate clearance is now frozen at `0.4 mm per side` as the current default. Full upper-carrier integration still needs a larger-part fit check.
