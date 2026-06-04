# Codex prompt for CAD development

You are working in the SaltScale-CadQuery repository.

Goal: improve the CadQuery mechanical model for a round 320 mm diameter weighing base for a 290 mm diameter salt/brine tank. The base must be printable on a Prusa MK4: no part may exceed 200 x 200 x 200 mm.

Keep these design constraints:
- 4 quadrant segments for top platform and bottom base.
- One true 50 kg single-point loadcell mounted centrally.
- Normal load path: tank -> top platform -> central loadcell -> bottom base -> floor.
- Outer wall/lip may guide and protect but must not carry normal weight.
- Include overload stops with 1.0 mm nominal gap.
- Include side-access electronics bay for Seeed XIAO ESP32C3, SparkFun HX711, 3xAA battery holder, one button, one LED.
- Use parameters in src/params.py; do not hardcode dimensions except local small features.
- Generate STEP and STL via python build.py.

First tasks:
1. Refine the quadrant joints with M3 screw bosses and heat-set insert pockets.
2. Add parametric holes for the selected loadcell after datasheet dimensions are confirmed.
3. Add removable side battery door.
4. Add cable routing from loadcell to HX711 bay.
5. Keep exports valid and ensure each segment bounding box stays within 200 x 200 x 200 mm.
