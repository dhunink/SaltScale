# SaltScale Redesign Review

Date: 2026-06-04

## Summary

SaltScale should be redesigned as a four-sensor floating annular scale:

- Four low-cost bathroom-scale style 50 kg load sensors.
- One HX711 reading the four sensors as a combined bridge, like a bathroom scale.
- A floating upper annular carrier that supports the salt container.
- A separate lower annular base that sits on the floor.
- Four removable sensor stations between upper and lower structures.
- No electronics bay, battery compartment, firmware assumptions, or central loadcell geometry in the first mechanical concept.

This is not a continuation of `platform_v6`. The previous CAD should be treated as exploratory evidence only. The new design keeps the useful high-level idea of distributed low-cost sensing, but discards the previous geometry, fused module exports, central-loadcell leftovers, and unclear upper/lower plate relationship.

The reason to choose four sensors is not that prior work chose four sensors. It is the best fit for the product goals: low cost, stable support for a large round container, forgiving off-center loading, one-HX711 electronics, and simple two-point calibration.

## Evaluation of current repository concepts

### Central single-point loadcell concepts

The early repository direction used a true central single-point loadcell. That is attractive electrically because one four-wire bridge loadcell connects directly to one HX711. It is also mechanically clean in abstract form: top platform -> loadcell -> lower base.

For SaltScale, it is not the best first open-source architecture:

- A good single-point loadcell for a 290 mm container is more expensive than commodity bathroom-scale sensors.
- The printed structure must deliver all off-center loads into the central loadcell without side loading it.
- A large PETG platform can introduce compliance and creep that changes calibration under eccentric loading.
- Loadcell mounting geometry becomes vendor-specific very early.
- The design becomes less hobby-friendly if exact metal loadcell dimensions, screw torque, or machined contact interfaces matter.

Verdict: discard for the first open-source target. It may be a premium alternate architecture later.

### Four-sensor exploratory concepts

The later repository work moved toward four 50 kg bathroom-scale style sensors. That direction is mechanically and economically stronger for this application:

- The scale naturally supports the container at multiple points.
- The load is shared around the perimeter, reducing demands on any single PETG span.
- The electrical bridge can still be read by one HX711.
- A one-weight calibration is plausible because the sum of four sensors is the useful measurement.
- Cheap replacement sensors are available from hobby suppliers and marketplace vendors.

The problem is not the four-sensor idea. The problem is the previous implementation. `platform_v6` appears to union serviceable sensor parts into one body, does not clearly implement a floating top carrier, and still inherits stale central-loadcell parameter ideas. It is useful as a warning, not as a base.

Verdict: keep the distributed sensing principle, discard the geometry.

### Two-sensor or three-sensor alternatives

Two sensors are tempting because they reduce hardware count, but they create worse mechanical constraints. A two-point support needs a third non-measuring support, flexure, hinge, or sliding constraint. That support either bypasses the sensors or makes readings sensitive to tank placement.

Three sensors provide a stable plane with fewer sensors than four, but common low-cost half-bridge bathroom-scale wiring is naturally four-sensor. Three-sensor wiring either needs different full-bridge load cells, multiple ADC channels, or more calibration complexity.

Verdict: discard for the main design.

## What should be kept

- Keep the 320 mm class outer envelope for a 290 mm container.
- Keep Prusa MK4/PETG segmentation as a hard manufacturing constraint.
- Keep the 300 mm-ish centering clearance idea, but implement it as a non-load-bearing side guide on the floating top carrier.
- Keep the low-cost four-sensor direction.
- Keep the concept of local overload stops with about 1 mm normal clearance.
- Keep the principle that sensors are replaceable and not trapped.
- Keep one HX711 as the default electronics path.
- Keep mechanical validation before electronics or firmware.

## What should be discarded

- Discard `platform_v6` geometry.
- Discard `sensor_module_v3` geometry as a final module shape, even though its load-path lesson is useful.
- Discard all central single-point loadcell assumptions for the default architecture.
- Discard fused STL exports that include placeholder sensors or service parts as one solid.
- Discard any upper-to-lower fastening scheme.
- Discard electronics bays and battery doors until the mechanical scale is physically validated.
- Discard full solid disks unless testing proves the container needs center support.

## Recommended final architecture

Use a four-sensor annular floating platform.

Parts:

- Four printable lower annular base segments.
- Four printable upper annular carrier segments.
- Four sensor stations at 45, 135, 225, and 315 degrees.
- Four low-cost 50 kg load sensors.
- Four lower contact pads and four upper contact pads, preferably metal washers/plates or printed placeholders during validation.
- Four sets of local overload stops.
- Optional M3 seam hardware only within the upper ring or within the lower ring. No hardware should connect upper to lower.

Normal stack:

```text
salt container
-> floating upper annular carrier
-> upper contact pad
-> load sensor
-> lower contact pad
-> lower annular base
-> floor
```

The recommended first CAD concept is an annular ring rather than a full disk. It supports the outer region of the salt container, saves material, reduces print time, and makes the load path visible. A center support can be added later only if a real salt container bottom proves too flexible.

## Mechanical design rationale

The salt container is large, slow-moving, and normally static. It does not need a precision lab scale mechanism. It needs a repeatable, low-cost, robust support that survives utility-closet conditions and gives useful fill-level measurements.

An annular floating top ring is a better first structure than a solid platform:

- It uses less PETG.
- It fits naturally into four quarter segments.
- It keeps sensors close to the perimeter, where container loads are most likely to land.
- It avoids a large central printed span that can creep under 20-35 kg.
- It leaves the center open for inspection and later wiring routes.

The lower ring should be a separate floor reference. It should locate sensor stations and resist lateral motion, but it should never be tied to the upper ring except through sensors and overload stops.

Sensor stations should be open or removable from above/outside. A sensor should not be installed by trapping it between permanent printed features. In the first physical prototype, the sensor should be replaceable with hand tools after the container is removed.

## Load path rationale

The primary load path must pass through the sensors during normal use. Every upper-to-lower feature must be classified:

- Sensor stack: normal load path.
- Guide walls or guide pins: lateral alignment only, with vertical clearance.
- Overload stops: intentional bypass only after about 1 mm of upper-carrier travel.
- Segment screws: join upper-to-upper or lower-to-lower only, never upper-to-lower.
- Centering lip: side guidance only, not vertical support.

Four sensors improve eccentric-load behavior. Salt may settle unevenly, and users may not place the container perfectly. With four support points, the summed bridge output is less sensitive to where the load lands than a two-sensor or central PETG transfer structure.

## Serviceability rationale

Serviceability should be designed around replacement of the cheapest failure-prone parts:

- Load sensors.
- Contact pads.
- Fasteners.
- Battery/electronics later.

The sensor station should allow this sequence:

1. Remove the salt container.
2. Lift or remove the affected upper ring segment.
3. Remove the upper contact pad.
4. Slide or lift out the sensor.
5. Replace the sensor and pad.
6. Reassemble and recalibrate.

No sensor should be bonded permanently into the structure. Adhesive can be used for optional pad retention, but not as the primary service strategy.

## Cost estimate

Prices are volatile, so these are rough June 2026 maker-scale estimates, not a purchasing lock. Supplier spot checks used:

- SparkFun generic 50 kg load sensor: about USD 6.25 each at retail: https://www.sparkfun.com/products/10245
- SparkFun HX711 board: about USD 11.50 at retail: https://www.sparkfun.com/sparkfun-load-cell-amplifier-hx711.html
- Seeed Studio XIAO ESP32-C3: about USD 4.99: https://www.seeedstudio.com/seeed-xiao-esp32c3-p-5431.html
- General PETG filament range: roughly USD 15-40 per kg depending on supplier and quality.

Estimated prototype cost, excluding shipping and batteries:

| Item | Conservative maker retail | Low-cost marketplace path |
| --- | ---: | ---: |
| 4x 50 kg load sensors | USD 25 | USD 6-16 |
| HX711 module | USD 12 | USD 1-4 |
| ESP32-C3 board | USD 5-8 | USD 3-6 |
| PETG, 300-600 g | USD 5-24 | USD 5-15 |
| Fasteners, pads, wire | USD 6-15 | USD 4-10 |
| Total | USD 48-79 | USD 19-47 |

The four-sensor architecture is still cheaper than a quality single-point loadcell design when the mechanical mounting risk and vendor-specific hardware are included.

## Risk analysis

### Highest risks

- Sensor package variation: cheap sensors vary in shape, wiring, and contact geometry. Mitigation: keep the sensor station parametric and validate against the purchased sensor before finalizing.
- PETG creep: long-term load can relax printed contact features. Mitigation: use metal contact pads, broad compression surfaces, and avoid printed flexures as measuring elements.
- Off-center calibration error: four sensors reduce this but do not eliminate it. Mitigation: test with weights at several positions on the container footprint.
- Moisture/corrosion: utility closets and brine tanks are not friendly environments. Mitigation: keep sensors away from liquid paths, add drainage gaps, and use corrosion-resistant pads/fasteners.

### Medium risks

- Wiring four half-bridge sensors incorrectly can produce unstable readings. Mitigation: document the bridge wiring and use a known bathroom-scale wiring pattern.
- The annular top may not support every container bottom shape. Mitigation: validate with the actual container; add removable cross-spokes or a thin top disk only if needed.
- Segment seams can introduce uneven support if assembled poorly. Mitigation: use dowels or simple seam keys within the upper ring and lower ring separately.
- Overload stops can become accidental normal-load bypasses if printed too tall. Mitigation: measure stop gaps and keep them adjustable in CAD.

### Lower risks

- Build volume: four 90-degree annular segments fit comfortably under 200 x 200 x 200 mm.
- Firmware complexity: one HX711 and summed sensor output keeps firmware simple once mechanics are stable.

## Recommendation

Proceed with `concept_v1`: a clean-sheet four-sensor annular floating platform. Build it as a mechanical demonstrator only. The next physical validation should be a single sensor station and one quarter of the annular upper/lower stack, not a complete product print.
