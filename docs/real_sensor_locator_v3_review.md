# Real Sensor Locator v3 Review

Date: 2026-06-11

## Context

Physical test result:

- `concept_v4_real_sensor_locator_test_v2` used `0.4 mm per side` clearance.
- The real Kiwi sensor fit was still noticeably loose.

Decision:

- Do not generate another multi-variant locator plate.
- Create one tighter validation print only.
- Keep active `concept_v4` unchanged until this v3 coupon is tested.

## v3 Locator Geometry

File:

```text
cad/exports/experimental/stl/concept_v4_real_sensor_locator_test_v3.stl
```

Measured sensor body width:

```text
34.07 mm
```

Target clearance:

```text
0.20 mm per side
```

Exact target cavity:

```text
34.07 + 2 * 0.20 = 34.47 mm
```

Exported coupon bounding box:

```text
58.00 x 54.00 x 7.00 mm
```

## Contact Surface Review

The real sensor has visibly rounded outer corners. A strictly square locator envelope can create misleading fit behavior:

- The straight side clearance may be correct.
- The square corner region may still leave extra diagonal freedom around the rounded sensor corners.
- The sensor can feel looser than the nominal side clearance suggests.

For v3, the locator coupon keeps the current locator philosophy but better acknowledges the sensor shape:

- Low side locator features remain.
- Cable-side relief remains open.
- The locator still does not trap the sensor.
- A rounded-corner sensor reference outline is included in the coupon base.
- Contact/guide features are rounded rather than hard square-corner blocks.

The v3 coupon is still a validation print only. It does not change full concept_v4 yet.

## What Changed Compared With v2

| Feature | v2 | v3 |
| --- | ---: | ---: |
| Clearance per side | `0.40 mm` | `0.20 mm` |
| Target cavity | `34.87 mm` | `34.47 mm` |
| Sensor body reference | `34.07 mm` | `34.07 mm` |
| Cable-side relief | open | open |
| Corner treatment | mostly square/straight locator feel | rounded-corner reference/contact surfaces |
| Alternative variants | none | none |

## Expected Fit

Compared with the current `0.4 mm` locator:

- v3 should have much less perceptible lateral play.
- v3 may require cleaner PETG edges and light deburring.
- v3 should still be hand-assemblable if the printer is dimensionally accurate.
- v3 may be sensitive to elephant foot or over-extrusion because only `0.2 mm per side` clearance remains.

Expected pass result:

- Sensor drops in or slides in by hand after normal cleanup.
- Sensor does not rattle noticeably.
- Cable exits without being pinched.
- Sensor can be removed without prying against the cable or plastic strain-relief area.

Expected fail result:

- Sensor requires force to insert.
- Sensor cannot be removed cleanly.
- PETG edge cleanup changes the fit too much.
- Rounded-corner contact features still leave rotational looseness.

## Recommendation After Testing

If v3 passes:

- Promote `0.2 mm per side` as the next active concept_v4 sensor locator clearance.
- Keep the rounded-corner/cable-relief philosophy.
- Update the full lower segment locator only after confirming serviceability with the real sensor.

If v3 is too tight:

- Do not return to `0.4 mm` immediately.
- Consider `0.3 mm per side` as the next single validation print.

If v3 still feels loose:

- The issue is likely not only side clearance.
- Review rotation control and corner/outer-frame contact shape before reducing clearance further.
