# SaltScale Loadcell Specification v2 — four-sensor architecture

## Selected sensors (architectural placeholder)

Project changed from a single central single-point loadcell to four distributed half-bridge style sensors (Kiwi / SparkFun style) rated ~50 kg each.

## Placeholder CAD footprint used

- Sensor footprint (placeholder): 38 x 38 mm (square)
- Sensor height (placeholder): 12 mm
- Planned sensor positions: radial 100 mm at angles 45°, 135°, 225°, 315°

## Reason

- Four-sensor architecture distributes load and uses commodity low-cost sensors.

## Mechanical CAD status

Exact sensor package and mounting geometry are not frozen. The CAD currently models a conservative placeholder box and support bosses to exercise the structural load path.

Before final mounting features are added, obtain from the chosen sensor vendor or product page:

- exact footprint (length × width)
- exact height
- mounting tab/hole positions (if any)
- recommended fastener type/size or adhesive strategy

## CAD rule

- Model sensors as parametric placeholders (currently 38×38×12 mm).
- Do not hard-code mounting holes until the sensor datasheet is available.