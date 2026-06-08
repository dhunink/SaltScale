# Print-Efficiency Redesign Review

Date: 2026-06-06

## Summary

The current `concept_v2` architecture is mechanically much cleaner than the earlier platform work, but it is not print-efficient. The main issue is not that any one part is too large; it is that the four lower quadrants and four upper quadrants are each too large to pair reliably on a 250 x 210 mm Prusa MK4/MK4S/Core One bed. The support grate is also a separate 178 x 178 mm print unless it is split.

The best print-efficiency candidate is an eight-segment ring with four alternating sensor segments and four plain filler segments, plus a split two-bar support grate. This keeps the validated four-sensor floating architecture and the same upper/lower separation, but makes the largest repeated parts roughly 108 x 113 mm instead of roughly 159 x 159 mm.

Recommendation: keep `concept_v2` as the current mechanically validated baseline, and create `concept_v3_print_optimized` as a print-efficiency candidate for inspection and future physical validation. `concept_v3` is not a release replacement until its extra seams, split support grate, and smaller upper/lower sectors are physically tested.

## Constraints Preserved

All evaluated strategies keep these rules unless noted otherwise:

- Four load sensors.
- Floating upper carrier over lower base.
- Upper and lower remain mechanically separate.
- No upper-to-lower fasteners, bridges, dowels, clips, walls, or spacers.
- Captured M3 nuts plus printed bridge plates remain the default seam strategy.
- Support-grate clearance remains `0.4 mm per side`.
- Engraved label standard remains `7-8 mm` text height and `0.8 mm` depth where space allows.
- Sensor remains serviceable from the outside after lifting/removing upper parts.

## Current Part Envelope Reference

Measured from current CAD bounding boxes:

| Part | Approximate envelope |
| --- | ---: |
| `concept_v2_lower_segment_0` | 159 x 159 x 21 mm |
| `concept_v2_upper_segment_0` | 153 x 153 x 14 mm |
| `concept_v2_support_grate` | 178 x 178 x 4 mm |
| Bridge plates | 64 x 32 x 4 mm |
| Lower pad | 44 x 44 x 2 mm |
| Upper pad | 56 x 56 x 3 mm |
| Sensor placeholder | 54 x 38 x 12 mm |

A 250 x 210 mm bed cannot comfortably take two current lower segments or two current upper segments. The small parts can be nested with larger sheets, but they do not solve the main plate count.

## Strategy 1: Current Concept v2

Description:

- 4 lower quadrants.
- 4 upper quadrants.
- 1 one-piece cross support grate.
- Small bridge plates, pads, and sensor placeholders.

Estimated print plates:

- About 9 practical plates: 4 lower, 4 upper, 1 support grate.
- Small pads and bridge plates can be nested into unused areas.

Largest part dimensions:

- Lower segment: about 159 x 159 mm.
- Upper segment: about 153 x 153 mm.
- Support grate: about 178 x 178 mm.

Expected print complexity:

- Low. Large, flat PETG-friendly parts.
- Few unique segment types.

Assembly complexity:

- Medium. Four seams per layer.
- Default full build uses 4 lower bridge plates and 4 upper bridge plates.

Fasteners:

- About 16 M3 bolts/nuts for the lower ring and 16 for the upper ring if each seam bridge uses four bolts.

Serviceability impact:

- Good. One large upper quadrant corresponds to one sensor region.

Load-path risk:

- Low. This is the clearest current architecture.

Beginner friendliness:

- Good mechanically, weaker on print commitment because it asks for many long sheets.

Verdict:

- Best mechanical baseline. Not the best build-accessibility path.

## Strategy 2: Smaller 8-Segment Ring

Description:

- 8 lower sectors.
- 8 upper sectors.
- Four alternating sectors include sensor station/contact land geometry.
- Four alternating sectors are plain ring sectors.
- Same captured M3 nut and bridge-plate seam strategy.

Estimated print plates:

- About 6 practical plates for the major ring parts if users can place two to three sectors per sheet.
- The estimate depends heavily on slicer spacing, brim settings, and whether the user prints sensor/plain sectors together.

Largest part dimensions:

- Lower sensor segment candidate: about 108 x 113 x 21 mm.
- Lower plain segment candidate: about 111 x 108 x 8 mm.
- Upper sensor segment candidate: about 102 x 107 x 14 mm.
- Upper plain segment candidate: about 107 x 102 x 14 mm.

Expected print complexity:

- Low to medium. Parts are smaller and less warp-prone, but there are more of them.

Assembly complexity:

- Higher than v2. Eight seams per layer instead of four.

Fasteners:

- Potentially doubles seam fasteners compared with v2 if the same four-bolt bridge is used at every seam.

Serviceability impact:

- Mixed. Smaller upper sectors are easier to handle, but there are more seams to loosen if a section needs removal.

Load-path risk:

- Low if upper/lower seams remain same-layer only.
- Slightly higher practical risk because more seams create more places for assembly mistakes.

Beginner friendliness:

- Better for printing, worse for assembly.

Verdict:

- Promising enough to model as `concept_v3_print_optimized`.

## Strategy 3: Hybrid Lower 4 / Upper 8

Description:

- Keep four lower sensor-bearing segments.
- Split the upper carrier into eight smaller sectors.
- Split or nest support grate parts.

Estimated print plates:

- About 7 practical plates: 4 lower plus around 2-3 upper/support plates.

Largest part dimensions:

- Lower remains about 159 x 159 mm.
- Upper becomes about 102 x 107 mm per sector.

Expected print complexity:

- Medium-low.

Assembly complexity:

- Medium-high because upper and lower seam patterns differ.

Fasteners:

- Lower stays about the same as v2; upper doubles.

Serviceability impact:

- Potentially good, because upper service pieces are smaller.
- Documentation burden increases because lower and upper segment counts differ.

Load-path risk:

- Low if documented well, but mismatch between upper/lower seams could confuse builders.

Beginner friendliness:

- Moderate. It saves plates without fully doubling lower seams, but the asymmetry is harder to explain.

Verdict:

- Useful fallback if eight lower segments prove too annoying, but not the cleanest default story.

## Strategy 4: More Rectangular/Cropped Four-Segment Shape

Description:

- Keep four segments but crop away nonessential corner material or alter the annular sector boundary to make parts pack better.

Estimated print plates:

- Likely still 8-9 plates.
- Cropping may reduce material and time, but probably will not allow two major sectors per 250 x 210 mm bed.

Largest part dimensions:

- Could reduce local material, but the outer diameter and 90-degree sector still drive a roughly 150-160 mm footprint.

Expected print complexity:

- Medium. More complex outlines and possibly less intuitive support.

Assembly complexity:

- Similar to v2.

Fasteners:

- Similar to v2.

Serviceability impact:

- Similar to v2 if sensor stations stay intact.

Load-path risk:

- Medium if cropping removes stiffness or makes upper carrier support less predictable.

Beginner friendliness:

- Mixed. Fewer grams, not necessarily fewer plates.

Verdict:

- Not enough benefit for the risk.

## Strategy 5: Split Support Grate Only

Description:

- Keep the current four-segment upper/lower rings.
- Split the one-piece support grate into two interlocking bars or four removable arms that can nest with other plates.

Estimated print plates:

- About 8 instead of 9 if the grate pieces fit on lower/upper segment sheets.

Largest part dimensions:

- Ring segments unchanged.
- Support grate bars can be about 178 x 22 mm.

Expected print complexity:

- Low.

Assembly complexity:

- Slightly higher because the grate is now multiple parts.

Fasteners:

- No additional fasteners required if the grate remains captured by gravity/container load.

Serviceability impact:

- Good if bars remain removable by hand.

Load-path risk:

- Low, as long as grate remains upper-only.

Beginner friendliness:

- Good, but the plate-count improvement is modest.

Verdict:

- Worth combining with the eight-segment strategy. Alone, it is helpful but not transformative.

## Recommendation

Create `concept_v3_print_optimized` as a candidate, not a replacement.

Recommended v3 strategy:

- 8 lower sectors: 4 sensor sectors, 4 plain sectors.
- 8 upper sectors: 4 sensor/contact-land sectors, 4 plain sectors.
- Same captured M3 nut pockets and printed bridge plates.
- Same four sensor stacks.
- Split two-bar half-lap support grate.

Expected benefit:

- Current concept_v2 practical major-part print count: about 9 plates.
- Concept v3 practical major-part print count: about 6 plates, assuming two to three small sectors can be placed per sheet and grate bars are nested with other parts.

Main cost:

- Twice as many upper/lower seams.
- More M3 hardware.
- More opportunities for assembly error.

This is a good trade to evaluate because the most common maker failure mode may be abandoning the project before finishing eight large plates. Smaller parts lower that psychological and practical barrier, especially for PETG warping risk and partial reprints.

## New Risks Introduced By Concept v3

- Eight seams per ring may reduce ring stiffness unless bridge plates work well at full scale.
- Fastener count may feel tedious.
- Alternating sensor/plain segment types must be labeled clearly.
- The split support grate half-lap needs physical validation.
- Smaller upper sectors may distribute load less smoothly unless the support grate is installed correctly.
- Builders must not accidentally mix upper/lower bridge plates or create any upper-to-lower connection.

## What To Inspect First

Inspect first:

```text
cad/exports/active/step/concept_v3_one_section_assembly.step
```

Then inspect:

```text
cad/exports/active/step/concept_v3_assembly.step
```

First printable STL to inspect in PrusaSlicer:

```text
cad/exports/active/stl/concept_v3_lower_sensor_segment_0.stl
```

Second printable STL to inspect:

```text
cad/exports/active/stl/concept_v3_upper_sensor_segment_0.stl
```
