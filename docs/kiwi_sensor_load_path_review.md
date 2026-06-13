# Kiwi Sensor Load Path Review

Date: 2026-06-11

## Scope

This review interprets the intended force path of the real Kiwi/SparkFun-style 50 kg load sensor using the supplied photos and measured dimensions.

It does not modify `concept_v4` and does not resize any pads. The goal is to decide what pad/contact geometry should be tested next.

Known measured dimensions:

- Overall sensor width: `34.07 mm`.
- Overall sensor thickness: `6.84 mm`.

Photo-based interpretation:

- The sensor is not a simple square load block.
- It has a rounded outer metal frame.
- It has a central sprung/load plate inside that frame.
- It has a raised central load button/bridge on top.
- It has white plastic/adhesive strain-element and cable regions near one side.
- The cable exits from one side and must not be crushed or used as a locating stop.

## 1. Real Sensor Geometry

The visible hardware appears to have four functional regions:

| Region | Function | Contact implication |
| --- | --- | --- |
| Outer rounded metal frame | Structural support frame | Good candidate for lower support if supported evenly |
| Central sprung/load plate | Flexible/load-transfer element | Should not be clamped broadly unless the sensor design expects that |
| Raised central button/bridge | Primary upper load entry feature | Best candidate for upper pad contact |
| White plastic/cable/strain region | Gauge/wiring/insulation region | Should not be primary contact or locator surface |

The photos strongly suggest the load should enter near the raised central button/bridge, not across the whole `34.07 mm` outer frame.

The photos also suggest the lower support should be taken by the outer frame or broad underside perimeter, not by pushing upward into the central sprung feature from below.

## 2. Intended Upper Contact Area

Likely intended upper contact:

- The central raised button/bridge region.
- Centered on the sensor body.
- Small enough to avoid loading the surrounding outer frame directly.
- Large enough to be stable and tolerant of print variation.

Estimated photo-derived dimensions:

| Feature | Estimated dimension |
| --- | ---: |
| Central raised button/contact spot | about `5-7 mm` diameter |
| Raised bridge width | about `10-12 mm` |
| Raised bridge length | about `24-28 mm` |
| Practical upper contact target | about `10-14 mm` round or rounded-rectangle contact |

Interpretation:

A small circular or rounded-rectangle upper pressure foot should contact the central raised bridge/button area. A full `56 mm` pad is far too broad if it becomes a flat contact surface.

The upper pad may still need a larger non-contact body for handling or locating, but its actual lower contact boss should be much smaller than the current full pad diameter.

## 3. Intended Lower Support Area

Likely intended lower support:

- The underside of the outer metal frame.
- Broad and stable, but not so broad that it contacts cable/glue regions or pushes on delicate features.
- Ideally supports the frame perimeter or the flat lower metal footprint without point-loading the sprung center.

Estimated photo-derived dimensions:

| Feature | Estimated dimension |
| --- | ---: |
| Outer metal frame overall | measured `34.07 mm` wide |
| Outer frame rim width | roughly `3-5 mm` |
| Inner opening / sprung region | roughly `22-26 mm` across |
| Practical lower support target | about `32-35 mm` rounded square or ring-like support |

Interpretation:

The lower pad should probably support the outer frame, not the central moving plate. A simple flat lower pad can work if it contacts only stable underside frame areas, but a shaped support may be better after inspecting the physical underside.

## 4. Areas That Should Not Be Primary Contact Surfaces

Avoid primary force contact on:

- White plastic/adhesive regions near the cable exit.
- Cable strain relief.
- Wires.
- Thin inner sprung regions outside the intended raised load feature.
- The outer frame from above, if the goal is to load the central button/bridge.
- Any region that rocks because the stamped metal surface is not flat.

Avoid using the cable side as a hard locator unless there is a clearance relief for the cable/glue area.

## 5. Comparison To Current Concept v4 Pads

### Current upper pad

Current geometry:

- Round pad diameter: `56.0 mm`.
- Pad thickness: `3.0 mm`.

Comparison:

- Sensor overall width: `34.07 mm`.
- Estimated intended upper contact: roughly `10-14 mm` contact area.
- Current upper pad is larger than the whole sensor body by `21.93 mm` total.
- Current upper pad is roughly `4-5x` wider than the likely intended raised load contact.

Assessment:

The current upper pad is oversized as a force-introduction surface. If it is a flat disk, it risks contacting the outer frame, not just the central raised bridge/button. That can create a poor or nonlinear load path.

Recommendation:

- Do not use the full `56 mm` lower face as the active pressure surface.
- Test a smaller central pressure boss/foot on a removable upper pad.
- Candidate starting geometries:
  - `10 mm` diameter round boss.
  - `12 mm` diameter round boss.
  - `14 mm` diameter round boss.
  - Optional rounded rectangle: about `12 x 24 mm`, aligned with the bridge, if round bosses are unstable.

### Current lower pad

Current geometry:

- Square pad: `44.0 x 44.0 mm`.
- Thickness: `2.0 mm`.

Comparison:

- Sensor overall width: `34.07 mm`.
- Current lower pad is about `9.93 mm` wider than the sensor body, about `4.97 mm` surplus per side.
- If flat and centered, it will support the entire sensor footprint plus margin.

Assessment:

The current lower pad is oversized relative to the sensor body, but less obviously wrong than the upper pad. Lower support may intentionally be broad if it supports the outer frame. However, a `44 mm` square pad may be larger than needed and may interfere with a tighter sensor locator.

Recommendation:

- Review rather than immediately reject.
- Test a lower support closer to the sensor frame size.
- Candidate starting geometries:
  - `35-36 mm` rounded-square lower pad.
  - `34-35 mm` round-corner frame support.
  - Optional ring/frame pad that supports the outer frame while relieving the central sprung region.

## 6. Round Cup Implication

Current Round Cup geometry:

- Cup inner diameter: `56.9 mm`.
- Cup outer diameter: `64.9 mm`.
- Cup wall: `4.0 mm`.
- Cup height: `4.0 mm`.

The Round Cup is appropriate as a carrier-relative locator concept, but its current diameter follows the oversized `56 mm` upper pad.

Assessment:

- The Round Cup concept can remain appropriate.
- The current cup diameter is probably oversized if the upper pad becomes a smaller pressure part.
- A revised upper pad may need two functional zones:
  - a larger upper body for cup location and hand removal;
  - a smaller lower boss/foot for real sensor contact.

Recommended direction:

Keep the Round Cup philosophy, but separate pad location diameter from force-contact diameter.

Example future concept:

- Upper pad body: still large enough to locate in a cup, perhaps `36-44 mm` diameter after testing.
- Lower contact boss: `10-14 mm` round or `12 x 24 mm` rounded rectangle.
- Cup resized only after the upper pad body size is chosen.

## 7. Recommended Load Path

Recommended normal load path:

```text
upper carrier
-> removable upper pad body
-> small central upper pressure boss
-> raised central load button/bridge on Kiwi sensor
-> sensor mechanism / sprung plate
-> outer lower sensor frame
-> lower pad or lower frame support
-> lower base
-> floor
```

Load should enter:

- Through the central raised button/bridge region.

Load should leave:

- Through the stable lower outer frame / underside support region.

Load should not intentionally pass through:

- Cable/glue area.
- White plastic/strain element area.
- Broad top contact on the outer frame.
- Sensor locator tabs.
- Overload stops during normal weighing.

## 8. What Dimensions Should Be Tested Next

### Upper contact tests

Create a small real-sensor contact coupon with interchangeable upper pressure feet:

| Variant | Purpose |
| --- | --- |
| `10 mm` round boss | Tests small central point/area loading |
| `12 mm` round boss | Likely first practical default candidate |
| `14 mm` round boss | More tolerant if smaller bosses feel unstable |
| `12 x 24 mm` rounded rectangle | Matches the visible raised bridge better than a circle |

The `12 mm` round boss is the best first test because it is likely large enough to print cleanly and small enough to avoid broad outer-frame contact.

### Lower support tests

Create a lower support coupon with these options:

| Variant | Purpose |
| --- | --- |
| `35-36 mm` rounded-square flat pad | Simple support close to sensor body size |
| `34-35 mm` ring/frame support | Supports outer frame while relieving center |
| Existing `44 mm` square pad | Baseline comparison |

The lower pad should be judged by whether the real sensor sits flat without rocking and whether it avoids cable/glue interference.

### Sensor locator tests

The sensor locator should be retested around the measured `34.07 mm` body width, but with extra relief for the cable/glue side.

Suggested body clearance targets:

| Clearance per side | Use |
| --- | --- |
| `0.4 mm` | Tight PETG fit candidate |
| `0.6 mm` | Likely safer first default |
| `0.8 mm` | Dust/salt tolerant fallback |

Do not use the `2.465 mm per side` current clearance as the final sensor locator target.

## 9. Recommendations

### Upper pad

Classification: **CHANGE**

The current `56 mm` flat upper pad is oversized for force entry. Keep the idea of a removable upper pad, but test a smaller contact boss that loads the central raised bridge/button.

### Lower pad

Classification: **REVIEW**

The lower pad is oversized but may still be functionally acceptable if it supports the outer frame. Test a smaller rounded-square or ring/frame lower support before changing the full design.

### Round Cup

Classification: **REVIEW / KEEP CONCEPT**

The Round Cup locator concept remains good. The current diameter should be reviewed after choosing a corrected upper pad body/contact design.

### Sensor locator

Classification: **CHANGE**

The current sensor locator is far too loose for the measured sensor body. Retest around the real sensor width with cable-side relief.

### Overload stops

Classification: **REVIEW**

Do not finalize overload stop height until the corrected sensor stack and upper contact boss are defined.

## Summary

Load should enter through the central raised button/bridge, not across the full sensor body.

Load should leave through the lower outer frame / stable underside support region, not through the cable or white plastic strain/cable region.

The current upper pad is oversized as a force-contact surface.

The current lower pad is moderately oversized but may be acceptable as a broad lower frame support.

The Round Cup concept remains appropriate, but its current diameter is tied to the oversized upper pad.

Next test dimensions should focus on `10-14 mm` upper contact bosses, a possible `12 x 24 mm` rounded rectangular boss, and `35-36 mm` lower support options.
