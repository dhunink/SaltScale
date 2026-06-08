# Segment Joining Strategy

Date: 2026-06-05

## Summary

Default `concept_v2` segment joining should use common M3 bolts, standard M3 nuts, and printed bridge plates.

This replaces the earlier assumption that printed-only wedge, dovetail, or sliding-key joints should become the default. Those printed-only joints remain useful experiments, but they are not robust enough yet for the main open-source assembly path.

Physical validation on 2026-06-06 confirmed that the current captured M3 nut pocket works as intended: light press fit, no nut rotation, no nut fallout during assembly, and correct M3 screw fit. Keep the current captured-nut dimensions unchanged unless larger prints expose a new issue.

## Default: M3 Bolt + Nut + Printed Bridge Plate

The default joint is:

- Two same-layer segment edges.
- One removable printed bridge plate spanning the seam.
- M3 clearance holes through the bridge plate and segment edges.
- Standard M3 nuts in printed nut pockets or accessible nut recesses.
- No heat-set inserts.
- No metal dowel pins.

This applies separately to:

- Lower-to-lower segment seams.
- Upper-to-upper segment seams.

The upper floating carrier and lower base must remain mechanically separate.

## Why This Is The Default

M3 bolts and standard nuts are more reliable and beginner-friendly than the printed-only concepts because they:

- Are easy to source globally.
- Do not require a soldering iron, insert press, or heat-set insert technique.
- Give adjustable clamping force.
- Are removable and serviceable.
- Are tolerant of normal PETG print variation.
- Are easier to diagnose during assembly.
- Let builders replace damaged bridge plates without reprinting large ring segments.

The hardware cost is low, but the assembly reliability is much higher than relying on friction-fit printed keys.

## Optional: Heat-Set Inserts

Heat-set inserts may remain an optional stronger variant.

They are useful when a builder wants:

- Faster repeated disassembly.
- Cleaner one-sided screw access.
- Higher wear resistance in the screw threads.

They should not be required for the default open-source build because they add tooling, technique, part sourcing, and failure modes around insert installation.

## Experimental: Printed-Only Joints

The printed-only concepts remain experimental validation coupons:

- Sliding key.
- True dovetail.
- Wedge key.

The wedge analysis showed that the current wedge does not actively draw the seam closed. It mainly prevents separation after the seam is manually closed and can reduce play as it wedges into the tapered slot.

That is useful, but not enough for the default build. Printed-only joints may be revisited after physical testing, especially as optional low-hardware variants.

## Upper And Lower Rings Must Stay Separate

The SaltScale force path depends on a floating upper carrier:

```text
salt container
-> upper carrier / support grate
-> upper pad
-> load sensor
-> lower pad
-> lower base
-> floor
```

Segment joining must preserve that path.

Allowed:

- Lower segment to lower segment.
- Upper segment to upper segment.
- Upper-only support grate to upper carrier.

Not allowed:

- Any fastener from upper carrier to lower base.
- Any bridge plate touching both upper and lower structures.
- Any dowel, clip, screw, spacer, rib, or wall that carries load around the sensors.

## Why No Upper-To-Lower Fastener Is Allowed

An upper-to-lower fastener would create a parallel structural path around the sensors. That would let some salt-container load bypass the load sensors, causing:

- Low readings.
- Nonlinear readings.
- Drift as PETG creeps.
- Position-dependent error.
- Calibration that changes after assembly or service.

Overload stops are the only intentional upper-to-lower contact, and they should engage only after the designed clearance is consumed. Seam fasteners are never overload stops.


## Bolted Coupon Hardware

For one coupon, use:

- 4x standard M3 hex nuts.
- 4x M3 bolts, start with M3x14.
- Optional M3 washers under the bolt heads.

M3x12 may be marginal because the stack is approximately 4 mm bridge plate plus 8 mm segment block. M3x16 should work for testing if slight protrusion below the nut pocket is acceptable.

The coupon uses underside nut recesses in the two segment-edge blocks. The bridge plate has M3 clearance holes only; it does not contain heat-set inserts.

## Captured-Nut Variant

`bolted_lower_seam_captured_nut_coupon_v1` and `bolted_upper_seam_captured_nut_coupon_v1` add press-in captured nut traps. The older `bolted_lower_seam_coupon_v2` and `bolted_upper_seam_coupon_v2` exports use the same geometry but have less explicit names. The nut is pushed into an underside hex pocket through a smaller printed retaining lip. The larger hex pocket prevents rotation; the retaining lip should keep the nut from falling out while the bridge plate is positioned.

This variant should allow assembly with one screwdriver after the nuts are preloaded into the segment blocks. It still uses only standard M3 nuts and bolts.

The captured pocket itself has passed first physical validation. The remaining seam-level question is whether the bridge plate and two segment-edge blocks clamp cleanly in a larger coupon and later in a quadrant.

## Bolted Coupon Assembly

1. Print `bolted_lower_seam_captured_nut_coupon_v1.stl` as a flat kit.
2. Separate the two segment-edge blocks and the bridge plate if the slicer imports them as one multi-body object.
3. Clean the M3 clearance holes and nut pockets.
4. Place the two segment-edge blocks seam-to-seam by hand.
5. Press one M3 nut into each underside captured nut pocket.
6. Place the printed bridge plate over the seam.
7. Insert four M3 bolts through the bridge and segment blocks into the nuts.
8. Tighten gradually, alternating bolts, until the seam is held without crushing PETG.

The coupon should be assembled as lower-to-lower only or upper-to-upper only. It must never be used as an upper-to-lower bridge.

## Bolted Coupon Pass Criteria

A successful coupon should:

- Let standard M3 nuts seat without heat.
- Let M3 bolts pass through without drilling beyond light cleanup.
- Pull the bridge plate flat against both segment blocks.
- Hold the seam closed under hand handling.
- Remain removable after repeated assembly.
- Show no cracking around nut pockets after light tightening.

If the nuts spin, enlarge or reshape the nut pockets. If the seam does not close before tightening, improve the printed seam faces. If the PETG crushes around the holes, increase local boss thickness or add washers.

## Prototype Direction

The captured nut pocket has passed as a small interface. The next seam validation should prioritize:

```text
cad/exports/validation/stl/bolted_lower_seam_captured_nut_coupon_v1.stl
```

This coupon validates the preferred one-screwdriver default: printed bridge plate, M3 bolts, captured standard M3 nuts, no heat-set inserts, and no dowels. Keep `bolted_lower_seam_coupon_v1` as the open-nut baseline.
