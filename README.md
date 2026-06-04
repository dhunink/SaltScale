# SaltScale CadQuery

Parametric CadQuery model for a compact round salt-tank scale for a water softener.

Target hardware v1:
- 50 kg single-point loadcell, centrally mounted
- round platform for a 290 mm diameter brine/salt tank
- 4 printable quadrant segments, each below 200 x 200 x 200 mm
- side-access electronics bay for ESP32-C3, HX711, 3xAA battery holder, button and LED

## Build in GitHub Codespaces

Open this repository in Codespaces. The devcontainer installs CadQuery and the small export script.

```bash
python build.py
```

Generated files appear in:

```text
exports/stl/
exports/step/
```

## Main parameters

Edit `src/params.py`:

- `TANK_DIAMETER_MM = 290`
- `OUTER_DIAMETER_MM = 320`
- `SEGMENT_COUNT = 4`
- `TOTAL_HEIGHT_MM = 42`
- `LOADCELL_MODEL = "LA360-C-50kg"`

## Design intent

The load path must be:

```text
tank -> top platform -> central loadcell -> bottom base -> floor
```

Outer ring features are only for centering and protection. They must not carry normal weight.
