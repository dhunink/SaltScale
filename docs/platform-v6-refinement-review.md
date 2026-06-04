# Platform v6 — Refinement Review

Summary
- Platform v6 refines the printable segmented design (v5) to add stronger alignment, PETG-friendly features, improved seam joining, and cleaned sensor-zone geometry while preserving the four-sensor architecture and `sensor_module_v3` force path.

What changed compared to v5
- Alignment: replaced fragile 2 mm printed pins with reinforced 4.2 mm dowel holes (clearance) plus local bosses for stiffness.
- Joining: seam M3 pockets are now blind pockets limited to the lower plate depth; screws do not create through top→bottom bridges near sensor areas.
- PETG-friendly tweaks: small fillets applied where practical; chamfered/reinforced bosses around dowel holes.
- Sensor zone: geometry cleaned (no change to force path) and module assemblies remain intact inside each segment.

How alignment works
- Each segment includes two alignment features on its bounding seams (near outer perimeter): a 4.2 mm clearance hole through the lower plate and a surrounding stiffening boss. When the four segments are assembled, metal dowel pins placed through these holes ensure accurate alignment and repeatability under load.

How segment joining works
- M3 seam pockets are blind (depth = lower plate thickness + 2 mm) so the screw path does not pass through the full platform height. Screws join segments near the rim but do not create a rigid metal bridge that would route forces from the top plate directly to the lower plate through the sensor areas.
- The M3 locations reuse the existing rim pattern but are restricted in depth and remain well outside sensor-supported zones.

Why no new load bypass was introduced
- All new holes and pockets are confined to the lower plate region or to peripheral bosses; none penetrate the top plate or create continuous stiff metallic paths across the sensor footprints.
- Sensor modules retain their internal overload stops and continue to be the primary local force path for each sensor region.

Remaining risks
- Dowel hole tolerance: 4.2 mm clearance is nominal; choose dowel diameter and tolerance based on supplier and press-fit vs slip-fit requirement.
- Boss shear: the local boss around the dowel hole strengthens the feature but consider using metal inserts if repeated assembly is expected.
- Fillet robustness: automatic filleting may fail or be ignored by some exporters; visually inspect STEP for clean edges.

Files modified/added
- `cad/src/platform_v6.py` — segmented platform with dowel holes, blind M3 pockets, fillets.
- `cad/build.py` — exports for v6 segments and assembly.
- `docs/platform-v6-refinement-review.md` — this document.
