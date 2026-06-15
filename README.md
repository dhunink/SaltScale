# SaltScale CadQuery

Parametric CadQuery model for a compact round salt-tank scale for a water softener.

Current mechanical direction: `concept_v5_cartridge_scale`.

Target hardware:
- four 50 kg Kiwi/SparkFun-style load sensors
- round platform for a 290 mm diameter brine/salt tank
- printable quadrant segments, each below 200 x 200 x 200 mm
- removable sensor cartridges with support-free retainers
- side-access electronics bay for ESP32-C3, HX711, battery holder, button, and LED

The physically validated sensor-cartridge baseline is:

```text
cad/src/concept_v5_cartridge_scale.py
cad/exports/concept_v5_cartridge/step/concept_v5_cartridge_assembly.step
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_cartridge.stl
cad/exports/concept_v5_cartridge/stl/concept_v5_sensor_retainer_clip.stl
```

The older v1-v4 CAD and print-test artifacts are retained for traceability, but
they are no longer the active design. Start with:

```text
docs/project_state_summary.md
docs/concept_v5_cartridge_scale.md
docs/concept_v5_system_architecture.md
docs/archive/concept_v4_legacy_index.md
```

## Build in GitHub Codespaces

Open this repository in Codespaces. The devcontainer installs CadQuery and the small export script.

```bash
python cad/export_concept_v5_cartridge.py
```

Generated files appear in:

```text
cad/exports/
```

## Main parameters

Edit `cad/src/concept_v5_cartridge_scale.py`.

## Design intent

The load path must be:

```text
tank -> upper ring -> load puck -> load sensor -> cartridge -> lower base -> floor
```

Cartridge retainers, cable guides, lift-retention features, and alignment walls
must not bypass the sensor under normal weighing load.
