# CAD Task 001

Create the first real SaltScale platform model.

Read:

- docs/mechanical-spec-v1.md
- hardware/loadcell-spec.md

Requirements:

- Circular platform
- Outer diameter 320 mm
- Split into 4 identical quarter segments
- Printable on Prusa MK4
- Parametric dimensions
- Segment alignment features
- Segment fastening using M3 screws
- Central placeholder region for loadcell
- Placeholder only, no mounting holes yet
- Overload stop locations
- PETG friendly geometry

Do not add:

- electronics compartment
- battery compartment
- LED
- button

Create:

cad/src/platform_v1.py

Update:

cad/build.py

to export:

platform_v1.step
platform_v1.stl