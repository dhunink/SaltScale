# Concept v5 Cartridge Scale

Date: 2026-06-13

Updated: 2026-06-15

## Summary

`concept_v5_cartridge_scale` is a clean-sheet SaltScale concept using the same four Kiwi/SparkFun-style 50 kg sensors, but reorganized around replaceable sensor cartridges, removable load pucks, and a dry outer electronics pod.

The intent is to make the next prototype easier to print, easier to service, and less sensitive to accidental preload around the real sensor body.

## Architecture

- Four-sensor floating upper/lower annular scale.
- Four printed lower segments and four printed upper segments.
- One removable sensor cartridge per quadrant.
- One removable load puck per sensor.
- Outer electronics pod for HX711/MCU/battery/connector packaging.
- No upper-to-lower fasteners.
- Overload stops remain lower-only and sit `1.0 mm` below the upper carrier underside.

## Sensor Cartridge

The cartridge is a separate printable tray:

- Sensor body reference: `34.07 mm` wide, `6.84 mm` thick.
- V2 physical-test corrections:
  - Underside protrusions treated as `4.95 mm` diameter, `1.0 mm` high.
  - Protrusion spacing treated as approximately `18.8 mm` center-to-center.
  - Cartridge relief pockets are widened to `7.0 mm` diameter to absorb measurement and print tolerance.
- V3/final-candidate physical-test corrections:
  - Cartridge footprint reduced to `42 x 39 mm`, close to the compact physical test print.
  - Cartridge side rails reduced to `2.0 mm` above the floor so they do not enter the sensor envelope.
  - Low lateral bumpers locate the sensor with `1.25 mm` nominal clearance instead of squeezing it.
  - Two cable-side posts accept a separate keeper clip.
  - The keeper clip sits `0.65 mm` above the measured sensor top, so it captures lift-out without preload.
- V4 lock-frame correction after physical test:
  - Fragile post-mounted keepers removed.
  - Cartridge footprint increased to `52 x 44 mm` to make room for robust boss supports.
  - Low pocket walls constrain horizontal sensor movement with `0.4 mm` nominal clearance.
  - Retainer is now a broad screw/pin-down frame, not two loose arms.
  - Retainer underside sits `0.35 mm` above the outer metal frame top and bottoms on printed bosses, not on the sensor.
  - Boss holes are `2.8 mm` pilot holes in the cartridge; retainer holes are `3.4 mm` clearance holes.
- V5 clamp correction after lock-frame physical test:
  - Horizontal sensor clearance reduced to `0.15 mm`.
  - Retainer now intentionally overlaps the inactive outer frame by `0.12 mm` for light clamp preload.
  - Boss shoulders lowered with the retainer so the clamp force reaches the sensor frame instead of bottoming plastic-on-plastic.
  - Retainer side/rear/front pads avoid the raised measuring bridge, center button, cable, and glue lump.
- V6 support-free screw-clamp correction:
  - Horizontal sensor clearance reduced further to `0.08 mm` per side.
  - Retainer is one connected flat frame, no disconnected clamp bars.
  - Retainer prints flat without support.
  - Mounting is explicit: two M3 clearance holes through the retainer into `2.8 mm` pilot holes in the cartridge bosses.
  - Long side rails and rear rail are materially connected to both screw eyes.
- V7 fit correction after printed screw-clamp test:
  - Locator clearance is now `0.0 mm` in the model to compensate for measured print fit play.
  - Side and rear locator walls are raised by `1.25 mm`, to `4.25 mm` above the cartridge floor.
  - Cable-side stops stay lower so the cartridge remains support-free and the retainer does not collide with them.
  - Retainer rails are shifted slightly inward and narrowed so they clear the raised walls while still pressing on the inactive outer sensor frame.
  - Bosses now include a `4.2 mm` collar through the retainer hole, protruding `1.25 mm` above the sensor-frame top so the clamp indexes on the boss instead of floating on the sensor.
- V8 cap-retainer correction after snug cartridge test:
  - Sensor cartridge dimensions are left unchanged because the sensor fit is now snug.
  - Retainer is widened into a flat, support-free cap with inner clamp rails and outer wall rails.
  - The raised cartridge walls pass through the gap between those rails instead of colliding with the clamp.
  - Retainer screw eyes are enlarged and tied into the outside rails for a stiffer part.
  - Retainer holes are opened to `5.1 mm`; cartridge boss collars now protrude `2.75 mm` above the sensor-frame top and pass through raised retainer rings.
  - Raised retainer rings add screw-area stiffness and make the boss registration more forgiving in print.
- V9 validated cartridge correction after over-wall physical test:
  - Locator wall height is now `7.1 mm` above the cartridge floor.
  - This is the default cartridge geometry, not a separate test variant.
  - The taller side and rear walls make the real sensor sit snugly with only minimal movement.
  - The over-wall retainer/cap remains support-free and registers around the raised walls.
  - This cartridge/retainer direction is accepted as the baseline for the whole concept.
- Cartridge assembly z: `5.0 mm`, with the sensor top at `16.84 mm`.
- Cable/glue side remains open.
- The sensor is carried by two outboard ledges under the flat perimeter frame, not by the earlier three-bar datum layout.
- The retainer frame is outside the active measuring bridge and avoids the cable/glue lump.
- Side rails slide into matching lower-segment receiver rails.

This should make the sensor serviceable without reprinting or disassembling the whole lower ring.

## Load Pucks

Status after 2026-06-15 PETG keyhole tests:

- The `0.20 mm` hand-tight keyhole variant is the best tested puck retention fit.
- The `0.35 mm` and `0.50 mm` variants are too loose.
- The `0.20 mm` puck does not fall out when the assembly is inverted.
- It is still loose enough to remove by hand without meaningful force, so it is not yet a true hand-tight captive mount.
- PETG does not flex enough for the intended side-slide insertion path; the puck can only be installed reliably by pressing it in from above.
- Therefore the puck interface remains an open design item. Do not treat the side-entry keyhole as validated yet.

Two puck styles are exported:

- `concept_v5_bridge_load_puck`: `12 x 24 mm` rounded bridge boss, intended to match the real raised bridge.
- `concept_v5_round_load_puck`: `12 mm` round boss, retained as a conservative baseline.

Both are standalone printable parts so force-contact tests do not require reprinting the upper segment.

In assembly orientation the bridge puck starts on the sensor top at `z = 16.84 mm`, its main body ends at the upper-carrier underside at `z = 25.0 mm`, and the upper locating lobe enters the support-free socket in the upper segment.

## Electronics Pod

The electronics pod is intentionally outside the salt-ring footprint:

- `78 x 42 x 16 mm` outer envelope.
- Hollow printed box with four cable-entry holes toward the scale.
- Two M3-ish lid screw bosses.

This is still a first-pass packaging envelope, not a sealed enclosure design.

## Exports

Generated files:

```text
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
cad/exports/concept_v5_cartridge/step/concept_v5_lower_segment_0.step
cad/exports/concept_v5_cartridge/step/concept_v5_upper_segment_0.step
cad/exports/concept_v5_cartridge/step/concept_v5_sensor_cartridge.step
cad/exports/concept_v5_cartridge/step/concept_v5_sensor_retainer_clip.step
cad/exports/concept_v5_cartridge/step/concept_v5_bridge_load_puck.step
cad/exports/concept_v5_cartridge/step/concept_v5_round_load_puck.step
cad/exports/concept_v5_cartridge/step/concept_v5_electronics_pod.step
```

Printable STL counterparts are in:

```text
cad/exports/concept_v5_cartridge/stl/
```

## First Physical Test Order

Print first:

```text
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_cartridge.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_retainer_clip.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_bridge_load_puck.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_round_load_puck.stl
```

Check:

- Real sensor drops into the cartridge after normal cleanup.
- Cable/glue side remains free.
- Side and rear walls locate the sensor with minimal horizontal play. The `7.1 mm` wall version has been physically validated.
- Retainer drops over both boss collars and lightly clamps the inactive outer frame.
- Retainer rails do not touch the raised measuring bridge, center button, cable, or glue lump.
- Two screws or printed pins through the retainer holes hold the clamp down into the cartridge bosses.
- Bridge puck contacts the intended raised bridge/button area.
- Round puck remains a usable fallback.

Print second:

```text
cad/exports/concept_v5_cartridge/stl/concept_v5_lower_segment_0.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_upper_segment_0.stl
```

Check cartridge slide-in feel, upper/lower clearance, and overload-stop gap before printing all quadrants.
