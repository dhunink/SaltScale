# Physical Validation 2026-06-06

## Captured M3 Nut Pocket

The captured M3 nut pocket geometry passed the first physical validation.

Observed result:

- The standard M3 nut required a light press fit.
- The nut did not rotate during screw tightening.
- The nut did not fall out during assembly.
- The M3 screw fit was correct.

Decision:

- Keep the current captured-nut pocket dimensions unchanged.
- Do not change the CAD unless larger seam or quadrant prints reveal assembly issues.
- Continue using captured standard M3 nuts as the preferred no-heat-set default segment-joining direction.

## Design Implication

The captured-nut approach is now a validated small-interface result, not just a CAD proposal. It supports the current default joining strategy:

- M3 bolt.
- Standard M3 hex nut.
- Printed captured nut pocket.
- Printed bridge plate.
- No heat-set insert required.
- No metal dowel required.

The next validation should move from the single-pocket interface to the complete lower bolted seam coupon, then to the upper seam coupon if the lower seam passes.
