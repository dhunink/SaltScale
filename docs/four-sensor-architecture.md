# Four-Sensor Architecture — Background and Recommendation

This note explains how the common Kiwi / SparkFun style ~50 kg load sensors work, how domestic bathroom scales mount similar sensors, the recommended structural force path for SaltScale, and two mounting architectures with a final recommendation.

## 1. How these sensors work (short primer)

- Basic principle: the small commodity sensors are metal flexures (bending beams or diaphragm) instrumented with strain gauges. Under load the flexure bends or compresses, the strain gauges change resistance and the change is read as a small differential voltage in a Wheatstone bridge.
- Output: the sensor itself provides a low-level analog change (millivolt-level). An amplifier/ADC (e.g., HX711) conditions the bridge and provides a digital reading.
- Typical packaged size: small rectangular flexure with two mounting faces. Electrically they are often wired as a half-bridge or full-bridge depending on the supplier; the amplifier wiring determines sensitivity and polarity.
- Important mechanical behavior: they are designed for compressive or bending loads along a defined axis and are relatively fragile in shear or torsion. They must be mounted so the intended bending/compression axis is loaded cleanly.

## 2. How bathroom scales mount these sensors (typical patterns)

- Four-corner arrangement: many scales use four identical sensors near the corners. Each sensor sits between the top weighing platform and a rigid lower base.
- Sandwich mounting: the sensor is sandwiched between two rigid contact pads; the top platform applies vertical load, the bottom is supported by the scale housing or feet.
- Local frame: sensors are held inside small pockets or frames that locate the sensor, often with a single screw or adhesive to prevent lateral movement. Some designs use metal contact plates or domed washers to ensure repeatable contact.
- Isolation from shear: mechanical features keep lateral/shock loads off the sensor (e.g., guide pins, walls or recesses) so the sensor only sees near-vertical compression/bending.

## 3. Recommended force path (structural best practice)

Maintain a clear, repeatable vertical load path:

- Upper platform span → rigid upper contact pad (stiff boss or plate) → sensor top face → sensor body → sensor bottom face → rigid lower contact pad/boss → lower platform / floor.

Design rules:
- Avoid point loads and concentrated sharp edges at sensor faces — use a flat pad or small washer to distribute load over the sensor contact area.
- Keep the path continuous and stiff so deflection in the surrounding structure does not bypass the sensor (which would reduce accuracy and change mechanical behavior).
- Prevent shear/side loads with guide features or shallow pockets that allow vertical motion but block lateral movement.

## 4. Recommended mounting strategy for a 320 mm PETG platform

- Use a structural frame (pocket) in the plastic that holds each sensor in a pocket sized slightly larger than the sensor footprint (e.g., placeholder 38×38 mm): the sensor sits on a lower hard contact boss and is capped by an upper hard contact boss when the platform is assembled.
- Provide small metal hardened contact pads or M3 washers on both top and bottom faces where the sensor mates with the bosses to reduce wear and provide repeatable contact.
- Do not make the sensor itself a load-bearing structural member — give it a supporting pocket and let the stiff plastic frame carry lateral loads.
- Use M3 screws with heat-set or captive nuts in reinforced plastic bosses to clamp the top plate to the lower plate, if you need positive mechanical retention; otherwise use a small clamp or adhesive and rely on compression between bosses for load transfer.
- Add a shallow lead-in chamfer on boss edges to aid assembly and ensure the sensor seats squarely.

Practical PETG considerations:
- Make ribs and bosses reasonably thick (≥4–6 mm solid in compression zones) and avoid long cantilevers near sensors.
- Provide fillets at transitions to reduce stress concentrations.

## 5. Two architecture comparisons

A) Sensor as structural member
- Concept: the sensor body is used as the mechanical link between upper and lower platforms (no separate bosses); the top plate bears directly on the sensor's faces.
- Pros: minimal parts, direct load path, compact.
- Cons: sensors are delicate; they can be damaged by lateral loads, and the printed plastic may not reliably align or protect the sensor. Repair or replacement is harder.

B) Sensor inside a structural frame (recommended)
- Concept: each sensor sits inside a rigid pocket/frame. The plastic frame transmits and distributes loads and protects the sensor; the sensor only senses vertical deformation between upper and lower contact pads.
- Pros: protects sensors from lateral loads and impacts, easier replacement, allows robust plastic geometry to carry shear and guide the load. Provides repeatable positioning and easier insertion of hardened contact pads or washers.
- Cons: slightly more material and geometry complexity, small extra clearance required for insertion.

## 6. Recommendation for SaltScale

Adopt architecture B: place each Kiwi/SparkFun-style sensor inside a small structural pocket with hardened contact pads on top and bottom, and design the plastic bosses so the upper plate compresses the sensor against the lower boss along a clean vertical axis. Key points:

- Sensor footprint: use placeholder 38×38×12 mm in CAD until exact part dimensions are obtained.
- Sensor placement: at 45°, 135°, 225°, 315° on a ~100 mm radius as implemented in `platform_v3.py`.
- Load path: upper plate → rigid upper pad → sensor → rigid lower pad → lower plate/floor.
- Fastening: use clamps or screws into reinforced bosses if positive retention is needed; prefer compression-only contact for primary sensing.
- Protection: provide guide walls and fillets to prevent shear loads on the sensor and to ease insertion/removal.

## 7. Validation steps (practical)

1. Obtain exact sensor drawing and update the CAD placeholder size and boss geometry.
2. Print alignment and boss test coupons to confirm the sensor seats correctly in PETG and that the hardened pads give repeatable seating.
3. Calibrate sensors together: place a known weight and verify linearity and symmetry across four sensors; adjust placement radius if needed.

---

This document focuses on structural mechanics and mounting strategy only; electronics and wiring are out of scope for this note.
