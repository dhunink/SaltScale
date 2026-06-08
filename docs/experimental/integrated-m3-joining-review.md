# Integrated M3 Joining Review

Date: 2026-06-06

## Summary

Integrated M3 joining is a better default direction than separate printed bridge plates. The bridge-plate approach is mechanically understandable, but it creates too many extra printed parts, too many bolts, and too many assembly steps.

The recommended candidate is a four-segment integrated-lug strategy: four lower segments, four upper segments, integrated same-layer lap lugs, and captured M3 nuts printed into the neighboring segment. This keeps the simple one-sensor-per-quadrant mental model while removing separate bridge plates entirely.

A new CAD candidate was created:

```text
cad/src/concept_v4_integrated_joining.py
```

`concept_v4` is not a release replacement yet. It needs physical validation of the integrated lugs before retiring `concept_v2` or `concept_v3`.

## Integrated Joint Concept

Each segment has two seam roles:

- One seam edge has integrated lap lugs with M3 clearance holes.
- The opposite seam edge has captured M3 nut pockets.

Assembly uses:

```text
M3 bolt -> integrated lug on segment A -> clearance hole/nut pocket in segment B -> captured standard M3 nut
```

There are no separate printed bridge plates. The connection is still same-layer only:

- lower segment to lower segment
- upper segment to upper segment

No fastener, lug, nut pocket, or printed feature connects upper to lower.

## Option 1: Four-Segment Integrated Joining

Description:

- 4 lower segments.
- 4 upper segments.
- Each seam uses integrated lugs and captured M3 nuts.
- 2 M3 bolts per seam per layer.
- Split two-bar support grate retained from the print-efficiency work.

Approximate largest part dimensions from the v4 CAD candidate:

| Part | Approximate envelope |
| --- | ---: |
| Lower segment with integrated lug | 175 x 167 x 21 mm |
| Upper segment with integrated lug | 169 x 164 x 18 mm |
| Support grate bar | 178 x 22 x 4 mm |

Printed parts for a full mechanical prototype, excluding real sensors:

- 4 lower segments.
- 4 upper segments.
- 2 support grate bars.
- 4 lower pads.
- 4 upper pads.
- Optional 4 printed sensor placeholders for dry assembly.

M3 hardware:

- Lower ring: 4 seams x 2 bolts = 8 M3 bolts and 8 M3 nuts.
- Upper ring: 4 seams x 2 bolts = 8 M3 bolts and 8 M3 nuts.
- Total: 16 M3 bolts and 16 standard M3 nuts.

Estimated print plates:

- About 8 major segment plates plus nested small parts.
- The split grate bars and pads can likely be nested with other plates.

Assembly complexity:

- Low to medium.
- No bridge plates to sort, orient, or hold.
- Fewer bolts than concept_v2 or concept_v3.

Serviceability:

- Good. One upper quadrant still maps to one sensor region.
- Upper carrier may still need to be lifted for underside upper-lug bolt access, similar to concept_v2 upper bridge service.

Warping risk:

- Similar to concept_v2, slightly higher local risk at integrated lugs because they extend beyond the annular sector.
- Still PETG-friendly and within the Prusa MK4 bed.

Load-path bypass risk:

- Low if lugs remain same-layer only.
- CAD checks found zero overlap between upper and lower segments in the sampled quadrant.

Open-source maker fit:

- Strong. It uses common M3 bolts/nuts, no heat-set inserts, no dowels, and fewer parts.

Verdict:

- Best current default candidate if the integrated lugs physically validate.

## Option 2: Eight-Segment Integrated Joining

Description:

- 8 lower segments.
- 8 upper segments.
- Integrated lugs replace bridge plates.

Printed parts:

- 8 lower segments.
- 8 upper segments.
- 2 support grate bars.
- Pads and optional placeholders.

M3 hardware:

- Lower ring: 8 seams x 2 bolts = 16 M3 bolts and 16 M3 nuts.
- Upper ring: 8 seams x 2 bolts = 16 M3 bolts and 16 M3 nuts.
- Total: 32 M3 bolts and 32 standard M3 nuts.

Estimated print plates:

- About 6 major plates if parts are packed efficiently.

Assembly complexity:

- Medium to high. Smaller parts are easier to print, but there are twice as many seams.

Serviceability:

- Mixed. Smaller upper parts are easier to handle, but there are more fasteners and more segment boundaries.

Warping risk:

- Lower than four-segment large parts because each segment is smaller.

Load-path bypass risk:

- Low by principle, but more seams create more chances for builder error.

Open-source maker fit:

- Good for printers, less good for assembly patience.

Verdict:

- Useful if print bed efficiency is the only goal, but less beginner-friendly than four integrated segments.

## Option 3: Hybrid Segmentation

Description:

- Lower 4 / upper 8, or lower 8 / upper 4.
- Integrated M3 lugs on each layer separately.

Printed parts:

- Between four-segment and eight-segment strategies.

M3 hardware:

- Between 24 and 32 total M3 bolt/nut pairs depending on which layer has eight seams.

Estimated print plates:

- About 7 major plates.

Assembly complexity:

- Medium-high because upper and lower segmentation differ.

Serviceability:

- Potentially good if only the upper is split into 8 pieces, but documentation becomes harder.

Warping risk:

- Better than full four-segment if the larger-risk layer is split.

Load-path bypass risk:

- Low if same-layer rules are obeyed.
- Documentation risk is higher because builders must understand different upper/lower seam patterns.

Open-source maker fit:

- Mixed. It saves some printing pain but adds mental overhead.

Verdict:

- Not the best default. Consider later only if v4 four-segment lugs print poorly.

## Comparison Table

| Strategy | Printed parts excluding real sensors | M3 bolt/nut pairs | Estimated plates | Assembly complexity | Beginner fit |
| --- | ---: | ---: | ---: | --- | --- |
| concept_v2 bridge plates | about 25 plus optional placeholders | 32 | about 9 | Medium | Good but many parts |
| concept_v3 bridge plates | about 42 plus optional placeholders | 64 | about 6 | High | Print-friendly, assembly-heavy |
| 4-segment integrated | about 18 plus optional placeholders | 16 | about 8 | Low-medium | Best balance |
| 8-segment integrated | about 26 plus optional placeholders | 32 | about 6 | Medium-high | Good printability, more assembly |
| Hybrid integrated | about 22 plus optional placeholders | 24-32 | about 7 | Medium-high | Mixed |

## Recommendation

Use four-segment integrated M3 joining as the next candidate to inspect and validate. It does not minimize print plates as aggressively as concept_v3, but it removes the bigger practical burden: loose bridge plates and excessive M3 hardware.

This is the most beginner-friendly path because builders get:

- one lower part per quadrant
- one upper part per quadrant
- no bridge plates
- no dowels
- no heat-set inserts
- standard M3 bolts and nuts
- fewer fasteners

## Concept v4 CAD Candidate

Created:

```text
cad/src/concept_v4_integrated_joining.py
```

Active exports:

```text
cad/exports/active/step/concept_v4_assembly.step
cad/exports/active/step/concept_v4_exploded_assembly.step
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
cad/exports/active/stl/concept_v4_lower_segment_0.stl
cad/exports/active/stl/concept_v4_upper_segment_0.stl
cad/exports/active/stl/concept_v4_support_grate_bar_x.stl
cad/exports/active/stl/concept_v4_support_grate_bar_y.stl
cad/exports/active/stl/concept_v4_lower_pad.stl
cad/exports/active/stl/concept_v4_upper_pad.stl
cad/exports/active/stl/concept_v4_sensor_placeholder.stl
```

## CAD Checks Performed

Initial sampled boolean overlap checks showed:

- Upper segment 0 vs lower segment 0: `0.0 mm^3` overlap.
- Support grate bar X vs upper segment 0: `0.0 mm^3` overlap.
- Support grate bar Y vs upper segment 0: `0.0 mm^3` overlap.
- Support grate bar X vs lower segment 0: `0.0 mm^3` overlap.
- Upper segment 0 integrated lug vs neighboring lower segment 1: `0.0 mm^3` overlap.

## New Risks

- Integrated lugs are part of large ring segments, so a damaged lug may require reprinting the segment instead of only a bridge plate.
- Lugs may be more vulnerable to PETG layer-edge damage during repeated assembly.
- Bolt access and screwdriver angle need physical validation.
- Seam alignment no longer has a separate bridge plate that can be replaced or modified independently.
- The larger lugged segments are slightly bigger than concept_v2 segments, though still within the Prusa MK4 bed.

## First Inspection Target

Inspect first:

```text
cad/exports/active/step/concept_v4_one_quadrant_assembly.step
```

Then inspect in PrusaSlicer:

```text
cad/exports/active/stl/concept_v4_lower_segment_0.stl
cad/exports/active/stl/concept_v4_upper_segment_0.stl
```

Do not retire `concept_v2` or `concept_v3` until the integrated-lug seam is physically validated.
