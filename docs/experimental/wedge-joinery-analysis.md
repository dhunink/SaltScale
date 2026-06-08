# Wedge Joinery Analysis

Date: 2026-06-05

## Summary

`printed_lower_seam_wedge_coupon_v2` is a tapered sliding key in a matching top-open tapered pocket. It is a useful no-metal seam test, but the current geometry should be understood as an anti-separation and play-reduction feature, not as a true draw-clamp.

The wedge does not actively pull the two segment edges together. The seam should be pushed closed by hand first; then the wedge is inserted to resist the seam opening again.

## Source geometry

The lower wedge coupon uses the values in `cad/src/concept_v2_printed_joinery_coupons.py`.

| Feature | Narrow end | Wide end | Length | Width change | Half taper angle | Included taper angle |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pocket slot | 18.0 mm | 28.0 mm | 78.0 mm | 10.0 mm | 3.67 deg | 7.34 deg |
| Printed key | 16.8 mm | 26.8 mm | 70.0 mm | 10.0 mm | 4.09 deg | 8.17 deg |

The nominal key is 1.2 mm narrower than the pocket at matching local width positions, which is 0.6 mm clearance per side before the key is advanced into tighter engagement. Because the key is shorter than the pocket, sliding it farther into the tapered pocket can reduce that free clearance and create side contact.

Coordinate convention from the CAD:

- `+X` is `OUT`.
- `-X` is `IN`.
- The slot is narrower at `IN`.
- The slot is wider at `OUT`.

## Intended insertion

1. Place the two seam-edge blocks together with their seam faces touching.
2. Align the two top-open tapered pocket halves so they form one continuous tapered slot across the seam.
3. Orient the key with its narrow end toward `IN` and its wide end toward `OUT`.
4. Start the key from the `OUT` side.
5. Slide or press the key toward `IN`.
6. Stop when the key starts to feel snug.

The intended direction is:

```text
OUT / wide side                         IN / narrow side
     key starts here  ---- push ---->   key wedges tighter here
```

The key remains removable because the pocket is open from above and the key is not undercut like a true dovetail.

## How clamping force is generated

The wedge generates local side contact by moving a tapered key into a tapered pocket. As the key advances toward the narrower end, the side faces of the key bear against the side faces of the slot. That contact creates normal force on the pocket walls. PETG friction and geometric bearing then resist the key backing out and resist the two blocks moving apart.

In simplified terms:

```text
Top view

                insertion force
OUT / wide       F_insert       IN / narrow
    +X          --------->          -X

      block A        seam        block B
   +----------+      ||      +----------+
   |          |\     ||     /|          |
   |          | \  WEDGE  / |          |
   |          |  \______ /  |          |
   +----------+      ||      +----------+

              N <---    ---> N
            side-wall normal forces
```

Those side-wall normal forces help the key resist motion:

```text
Attempted seam separation

      block A                    block B
        <--- F_sep      F_sep --->

The key spans both pocket halves. When the seam tries to open,
the key bears against the pocket walls and blocks the motion.
```

## Does it pull the seam closed?

No, not in the current form.

The current wedge does not actively draw the two segment edges together. It mainly prevents separation after the seam has already been brought together. It can also reduce looseness by taking up clearance in the tapered slot.

For the wedge to actively pull the seam closed, the geometry would need a draw action: for example opposed ramps, hooked/captured features, a draw-key shape, or a dovetail-like undercut arranged so insertion creates an inward force component across the seam.

## Practical implication

For physical testing, the correct question is not "does the wedge pull the seam closed by itself?" The correct questions are:

- Can the seam be pushed closed by hand?
- Can the key be inserted without splitting or shaving PETG?
- Does the inserted key remove perceptible seam play?
- Does the seam stay closed under handling?
- Can the key be removed with light hand-tool assistance?

If the coupon passes those tests, the wedge-key strategy may still be a good default no-metal joinery option because it is simpler and less tolerance-sensitive than a true dovetail. If the seam remains loose unless the key is overdriven, the design needs a future draw-key or captured-ramp refinement.

## Risks

- Overdriving the wedge can spread the pocket walls instead of improving seam closure.
- The top-open pocket means the key is not vertically captured.
- PETG friction may change with print orientation, surface texture, salt dust, and wear.
- A 0.6 mm per-side nominal clearance may feel loose on well-tuned printers and tight on over-extruded PETG prints.
- Because the coupon is straight and local, it does not fully represent the stiffness of a curved full ring segment.

