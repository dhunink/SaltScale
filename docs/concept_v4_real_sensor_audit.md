# Concept v4 Real Sensor Audit

Date: 2026-06-11

## Scope

This audit reviews the current `concept_v4` assembly after integrating `kiwi_sensor_reference_v1`.

It does not redesign concept_v4 and does not modify CAD. It evaluates the current geometry against the measured Kiwi/SparkFun-style sensor dimensions and the supplied reference photos.

Measured sensor inputs:

- Sensor body width: `34.07 mm`.
- Sensor body thickness: `6.84 mm`.
- Photos show a rounded outer metal frame, central sprung/load plate, central raised load button/bridge, and cable exiting from one side.

## 1. Actual Stack Geometry

Current CAD values:

| Feature | Current value |
| --- | ---: |
| Kiwi reference metal body | `34.07 x 34.07 x 6.84 mm` |
| Kiwi reference total body including cable visual | `58.07 x 34.07 x 6.84 mm` |
| Lower pad | `44.0 x 44.0 x 2.0 mm` |
| Upper pad | `56.0 mm diameter x 3.0 mm` |
| Round cup inner diameter | `56.9 mm` |
| Round cup outer diameter | `64.9 mm` |
| Round cup wall thickness | `4.0 mm` |
| Round cup height | `4.0 mm` |
| Sensor locator cavity, approximate | `39.0 x 39.0 mm` |

Current vertical stack positions:

| Feature | Z range |
| --- | ---: |
| Lower pad | `8.0..10.0 mm` |
| Kiwi reference sensor | `10.0..16.84 mm` |
| Upper pad | `22.0..25.0 mm` |
| Overload stop top | `21.0 mm` |

Important finding:

- The current stack still uses the old `12.0 mm` sensor-placeholder height for upper-pad placement.
- The real Kiwi reference is `6.84 mm` thick.
- Therefore the current assembly has a `5.16 mm` vertical gap between the top of the Kiwi sensor reference and the bottom of the upper pad.

That means the current assembly is not a physically closed weighing stack with the real sensor. This audit reports the issue but does not change the stack height.

## 2. Contact Analysis

### Upper pad to sensor

Current CAD contact:

- No contact.
- The upper pad bottom is at `z = 22.0 mm`.
- The Kiwi sensor top is at `z = 16.84 mm`.
- Gap: `5.16 mm`.

If the vertical stack were corrected without changing pad diameter, the upper pad would be very broad relative to the real sensor:

- Upper pad diameter: `56.0 mm`.
- Sensor body width: `34.07 mm`.
- Pad surplus over sensor width: `21.93 mm` total.

The photos suggest the intended load-sensitive region is the central raised button/bridge area, not the whole outer frame. A `56 mm` round pad is therefore likely too large for controlled loading. It may contact or overhang areas that should not receive the primary upper load.

Assessment:

- Current state: upper pad does not contact the sensor.
- Size: likely oversized.
- Load path confidence: low until upper contact geometry is redesigned and tested.

### Lower pad to sensor

Current CAD contact:

- The lower pad top is at `z = 10.0 mm`.
- The Kiwi sensor bottom starts at `z = 10.0 mm`.
- So the lower pad contacts the underside of the sensor reference.

Size comparison:

- Lower pad: `44.0 x 44.0 mm`.
- Sensor body: `34.07 x 34.07 mm`.
- Lower pad surplus: `9.93 mm` total, about `4.97 mm` per side.

The lower pad is oversized relative to the measured sensor body, but less dramatically than the upper pad. A broad lower support may be acceptable if the sensor is designed to sit on its outer frame. However, the current pad likely supports more of the sensor footprint than necessary.

Assessment:

- Current state: lower pad contacts the sensor.
- Size: somewhat oversized.
- Load path confidence: medium; verify against real sensor underside behavior.

### Does the load enter the intended sensor region?

Currently, no. Because the upper pad does not touch the sensor, the vertical load path is open in the CAD assembly.

After stack-height correction, the current upper pad diameter would likely be too broad to guarantee that load enters only through the intended central sensor region. The photos show a central raised button/bridge and a distinct outer frame. The upper contact should probably be smaller and centered on the load button/bridge region, but that is a future CAD change, not part of this audit.

## 3. Locator Analysis

Current approximate sensor locator cavity:

- CAD cavity target: `39.0 x 39.0 mm`.
- Measured sensor body: `34.07 x 34.07 mm`.
- Total clearance: `4.93 mm`.
- Clearance per side: `2.465 mm`.

This does not reflect the recently validated `0.3 mm per side` seam-locator philosophy. That validation applies to same-layer segment seam locators, not the sensor station. However, the sensor locator is now much looser than expected for a real sensor-shaped locator.

Current sensor locator implications:

- It will not precisely locate the real sensor.
- It may allow noticeable sensor sliding or rotation before load is applied.
- It may still be serviceable and tolerant, but it is not a controlled fit.
- The cable exit side remains directionally useful, but the sensor body clearance is too large for accurate positioning.

Assessment:

- Current state: serviceable but loose.
- Size: oversized.
- Load-path risk: medium, because sensor drift could affect repeatability or pad alignment.

## 4. Overload Stop Analysis

Current nominal geometry:

- Overload stop top: `z = 21.0 mm`.
- Upper pad bottom: `z = 22.0 mm`.
- Nominal unloaded clearance to the current upper pad: `1.0 mm`.

This is the intended overload travel before engagement in the old stack model.

With the real Kiwi sensor reference inserted, the stack is not closed:

- Kiwi sensor top: `z = 16.84 mm`.
- Overload stop top: `z = 21.0 mm`.
- Upper pad bottom: `z = 22.0 mm`.

Because the upper pad is currently floating `5.16 mm` above the sensor, overload-stop behavior is not physically meaningful until the sensor stack height is corrected. In the current assembly, the upper structure would have to move downward far more than intended before the sensor is even contacted.

Assessment:

- Current nominal stop gap: `1.0 mm` to upper pad.
- Real-sensor stack validity: not valid yet.
- Expected overload behavior: must be re-evaluated after upper pad/contact geometry is corrected.

## 5. Recommendations

### Upper pad

Classification: **CHANGE**

Reasons:

- Does not contact the real sensor in the current stack.
- Diameter is likely too large for the intended central load path.
- It may load the outer frame rather than the central load button/bridge if stack height is corrected without resizing.

Recommended next adjustment:

- Rework upper contact geometry around the real sensor height and central raised load region.
- Use the photos to target the central load button/bridge, not the entire outer frame.

### Lower pad

Classification: **REVIEW**

Reasons:

- It contacts the sensor correctly in Z.
- It is about `9.93 mm` wider than the measured sensor body.
- The broad support may be acceptable if it supports the lower outer frame, but this should be confirmed physically.

Recommended next adjustment:

- Check the real sensor underside and decide whether lower support should remain broad or become shaped to the metal frame.

### Round cup

Classification: **REVIEW**

Reasons:

- The cup is correct for the current `56 mm` upper pad.
- If the upper pad changes, the cup will almost certainly need to change with it.
- The cup itself is not the immediate problem; it is downstream of the upper pad diameter.

Recommended next adjustment:

- Do not change the cup independently.
- Revisit after choosing the corrected upper pad diameter/contact shape.

### Sensor locator

Classification: **CHANGE**

Reasons:

- Current cavity is about `39.0 mm` for a `34.07 mm` sensor body.
- Clearance is about `2.465 mm per side`, which is too loose for reliable positioning.
- It is serviceable, but not a precision locator.

Recommended next adjustment:

- Create a real-sensor locator revision using the `34.07 mm` measured body width.
- Keep enough PETG tolerance and cable clearance, but reduce body clearance substantially.
- Preserve outside removal and avoid any upper-to-lower bypass.

### Overload stops

Classification: **REVIEW**

Reasons:

- The intended nominal stop gap is `1.0 mm` to the current upper pad position.
- The current real-sensor stack has a `5.16 mm` vertical gap, so the overload-stop relationship is invalid until the stack is corrected.

Recommended next adjustment:

- Recalculate overload stop height only after upper pad and sensor contact geometry are corrected.
- Keep the overload stop concept, but do not trust the current stop height with the real sensor.

## What Is Already Correct

- The Kiwi sensor reference is now much closer to the real hardware than the old block placeholder.
- Cable exit direction is represented and remains compatible with outside service access.
- Lower pad and sensor currently meet in Z.
- Upper/lower architecture remains mechanically separate.
- No upper-to-lower load bypass has been introduced by the reference sensor model.
- The Round Cup concept remains mechanically clean, but it is tied to an upper pad that now appears too large.

## What Remains Oversized

- Upper pad: strongly oversized relative to the sensor body and likely load region.
- Sensor locator cavity: clearly oversized relative to the measured sensor body.
- Lower pad: moderately oversized, but may still be acceptable depending on sensor underside support.
- Round cup: oversized only because it follows the current oversized upper pad.

## What Should Be Adjusted Next

Next CAD work should focus on a real-hardware sensor station revision, not on the full ring:

1. Correct the vertical stack for the `6.84 mm` sensor thickness.
2. Redesign the upper pad/contact area around the central load region.
3. Tighten the sensor locator around the `34.07 mm` body while preserving outside removal.
4. Re-evaluate the lower pad support footprint.
5. Recalculate overload stop height after the corrected stack is defined.

Do not print a full concept_v4 segment until these real-sensor stack issues are resolved.
