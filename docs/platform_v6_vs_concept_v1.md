# Platform v6 vs Concept v1

Date: 2026-06-04

## Summary

`platform_v6` and `concept_v1` both point toward a four-sensor SaltScale, but they are not equivalent designs.

`platform_v6` is an exploratory segmented lower-platform model that embeds `sensor_module_v3` assemblies into each quadrant. It improves over earlier CAD by adding dowel holes and blind M3 pockets, but it does not cleanly model a floating upper carrier, and its exported segment appears to fuse serviceable sensor parts into one printable body.

`concept_v1` is a clean-sheet architecture demonstrator: separate lower annular base, separate floating upper annular carrier, four open sensor stations, lateral guide features, pads, and overload stops. It is less complete as a production printable part set, but the load path and maintenance model are much clearer.

Overall winner: `concept_v1`.

## Category winners

| Category | Winner |
| --- | --- |
| Printability | `concept_v1` |
| Serviceability | `concept_v1` |
| Load path clarity | `concept_v1` |
| Calibration complexity | `concept_v1` |
| Expected accuracy | `concept_v1` |
| Expected PETG creep behavior | `concept_v1` |
| Assembly complexity | `concept_v1` |
| Hardware cost | Tie, slight edge to `concept_v1` |
| Long-term maintainability | `concept_v1` |

## Printability

### platform_v6

Strengths:

- Each segment fits the Prusa MK4 envelope; prior checks measured about 171.8 x 171.8 x 42.0 mm.
- It is exported as four large quadrant segments, which is a familiar print workflow.
- Dowel holes and blind M3 pockets are already represented.

Weaknesses:

- The segment is a fused CAD compound containing the sensor module assembly, including pads and sensor placeholder.
- Internal pocket surfaces in a fused STL may not represent the actual serviceable printed parts.
- Automatic global filleting can fail silently or create hard-to-debug export differences.
- It is not obvious what should actually be printed versus what is assembly visualization.

### concept_v1

Strengths:

- Main segments are smaller: lower segments are about 159.2 x 159.2 x 6.0 mm; upper segments are about 153.0 x 153.0 x 12.0 mm.
- Annular geometry uses less material than a fuller platform.
- Upper and lower structures are naturally printable as separate flat parts.
- The model separates architecture roles even though final print exports still need to be split.

Weaknesses:

- It has more printable bodies once converted into a real part set.
- Seam hardware is not finalized.
- The current STL is an assembly demonstrator, not a final print plate.

Winner: `concept_v1`.

Reason: both fit the printer, but `concept_v1` has simpler, flatter, smaller structural parts and a clearer route to printable part separation.

## Serviceability

### platform_v6

Strengths:

- The intended v6 docs describe removable sensors and pads.
- Sensor stations are located one per segment, which is a good service concept.

Weaknesses:

- The actual `platform_v6_segment()` unions the entire `sensor_module_v3` assembly into each segment.
- A fused STL with placeholder sensor and pads contradicts sensor replacement.
- The model does not clearly define how the upper load-bearing platform is removed or separated.
- A real failed sensor replacement procedure is ambiguous.

### concept_v1

Strengths:

- The upper carrier and lower base are separate by design.
- Sensor stations are open on the outer radial side.
- Sensors, pads, lower base, upper carrier, guide features, and overload stops have distinct roles.
- Service sequence is straightforward: remove container, lift upper carrier, replace pad/sensor, recalibrate.

Weaknesses:

- Final retention features for pads and sensors are not yet designed.
- Repeated disassembly will need durable seam hardware.

Winner: `concept_v1`.

Reason: `platform_v6` talks about serviceability; `concept_v1` actually expresses it in the architecture.

## Load path clarity

### platform_v6

Strengths:

- It uses the `sensor_module_v3` idea, which has a good local pad -> sensor -> pad load path.
- It includes overload-stop concepts and avoids through-depth M3 holes in the lower plate.

Weaknesses:

- It does not clearly model the floating top/load-entry structure.
- Ribs rise high in the model, but their relationship to a future top plate is undefined.
- It still uses central-loadcell-derived parameters for rib clearance.
- The sensor module is inserted as a full assembly, blurring which bodies are real load path parts and which are placeholders.

### concept_v1

Strengths:

- The normal load path is explicit: container -> floating upper carrier -> upper pad -> sensor -> lower pad -> lower base -> floor.
- Upper and lower structures are separated.
- Guide rails are lateral features, not normal-load supports.
- Overload stops are intentional bypasses with a defined clearance target.

Weaknesses:

- The model still needs physical validation of guide and stop clearances.

Winner: `concept_v1`.

Reason: `concept_v1` makes the vertical load path legible at platform scale, not just at the local sensor module.

## Calibration complexity

### platform_v6

Strengths:

- If implemented as a normal four-sensor bridge, electronics could be simple: one HX711 and one summed reading.

Weaknesses:

- Because the upper load path is incomplete/unclear, calibration behavior is hard to predict.
- Accidental load bypass or fused printed contact geometry could produce nonlinear readings.
- Segment-to-segment stiffness variation may matter if load enters through unclear ribs or pads.

### concept_v1

Strengths:

- Four sensors can still be summed into one HX711 reading.
- The floating top architecture reduces ambiguity about what is being calibrated.
- Tare plus one known mass should be enough for first functional fill-level readings.
- Off-center validation is straightforward: place the same weight at several angular positions.

Weaknesses:

- Four cheap sensors still need correct bridge wiring.
- It will not be a precision scale without multi-position validation.

Winner: `concept_v1`.

Reason: same basic electronics, fewer mechanical unknowns.

## Expected accuracy

### platform_v6

Strengths:

- Four sensor placement at quadrant centers is directionally good.
- Local module stops and pads could be accurate if separated and printed correctly.

Weaknesses:

- Current CAD does not define the true container-to-sensor load entry.
- Fused placeholders make the exported geometry poor evidence for real contact behavior.
- The platform may have unmodeled bypasses once a top structure is added.
- Accuracy will be sensitive to how someone interprets and modifies the incomplete model.

### concept_v1

Strengths:

- The top carrier floats explicitly on the four sensor stacks.
- Sensor radius is near the perimeter, which should help with eccentric salt loads.
- The annular upper carrier reduces central-span load-transfer ambiguity.
- The design invites simple off-center testing and correction.

Weaknesses:

- The annular support may not suit every salt container bottom; a flexible container bottom could need cross-spokes or a thin top support.
- Contact pads need metal or validated printed surfaces for stable repeatability.

Winner: `concept_v1`.

Reason: expected accuracy is governed more by load-path control than by CAD detail count. `concept_v1` controls the load path better.

## Expected PETG creep behavior

### platform_v6

Strengths:

- It has a lot of printed material and ribs, so it may be stiff in the short term.
- Sensor modules are locally supported.

Weaknesses:

- More printed material in unclear load-bearing positions can create long-term drift paths.
- Printed pads and fused contact surfaces are suspect under constant 20-35 kg loading.
- If ribs or guide walls accidentally share vertical load, PETG creep could change calibration over time.

### concept_v1

Strengths:

- The intended compressive load path is short and localized through pads and sensors.
- The annular top reduces large central PETG spans.
- It naturally encourages metal contact pads at the sensor interfaces.
- Creep-prone printed features are easier to classify as either structural support, guide, or overload stop.

Weaknesses:

- The upper annular carrier still needs enough thickness and contact area to avoid local sag.
- PETG seams and pad pockets need physical validation.

Winner: `concept_v1`.

Reason: less ambiguous PETG in the measuring path means lower creep risk.

## Assembly complexity

### platform_v6

Strengths:

- Fewer apparent printed segment parts.
- Dowels and M3 pockets are already sketched.

Weaknesses:

- Apparent simplicity is misleading if sensors and pads are fused into the print.
- The real assembly sequence for a working scale is underdefined.
- It is unclear how to install real sensors after printing the segment.
- It is unclear how upper and lower load-bearing structures are assembled without bypassing sensors.

### concept_v1

Strengths:

- More parts, but each part has a clear role.
- Assembly is conceptually simple: lower ring, pads, sensors, upper pads, upper ring.
- Sensor access is not an afterthought.
- Upper-to-lower fasteners are avoided.

Weaknesses:

- Eight main ring segments plus pads and sensors is more handling than four fused segments.
- Final seam hardware still needs design.

Winner: `concept_v1`.

Reason: `concept_v1` has more pieces but less confusion. For hobby assembly, understandable beats nominally fewer parts.

## Hardware cost

### platform_v6

Expected hardware:

- Four low-cost 50 kg sensors.
- HX711.
- ESP32-C3.
- Dowel pins.
- M3 screws.
- Contact pads or washers if implemented serviceably.

### concept_v1

Expected hardware:

- Four low-cost 50 kg sensors.
- HX711.
- ESP32-C3.
- Sensor contact pads or washers.
- Seam hardware for upper ring and lower ring.
- Possible dowels or keys later.

Winner: Tie, slight edge to `concept_v1`.

Reason: sensor/electronics cost is essentially the same. `concept_v1` may use less filament because it is annular, but it may need more ring-joining hardware. Net cost difference is small.

## Long-term maintainability

### platform_v6

Strengths:

- It has more local development history and supporting docs.
- It includes some practical seam/alignment ideas.

Weaknesses:

- It inherits stale central-loadcell parameter assumptions.
- It depends on `sensor_module_v3` as an inserted assembly rather than a clean platform-level design.
- It is easy for future agents to misunderstand what is printable, what is placeholder, and what is validated.
- Fixing it requires untangling prior CAD decisions.

### concept_v1

Strengths:

- Clean source with local parameters for the concept.
- Separate upper/lower architecture is easier to reason about.
- Maintainers can evolve sensor station details without preserving obsolete platform geometry.
- The model is honest about being a concept and not a production print package.

Weaknesses:

- It is newer and has less accumulated testing.
- It needs follow-up work to become a complete printable part set.

Winner: `concept_v1`.

Reason: maintainability starts with clear architecture. `platform_v6` carries too much ambiguity and historical baggage.

## Overall recommendation

Use `concept_v1` as the basis for the next mechanical design phase. Do not continue `platform_v6`.

The best next step is not to polish either full platform. Instead, derive a small physical validation coupon from `concept_v1`: one lower sensor station, one matching upper carrier section, one real sensor, and real contact pads. Validate fit, serviceability, overload clearance, repeatability, and off-center response.

Only after that should the project create production-style split STL exports, seam hardware, electronics mounting, or firmware.

## Critical caution

`concept_v1` wins the architecture comparison, but it is not finished product CAD. It is a cleaner foundation. The current exports demonstrate the mechanical idea; they should not be treated as final printable release files.
