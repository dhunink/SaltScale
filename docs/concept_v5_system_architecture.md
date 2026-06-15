# Concept v5 System Architecture

Date: 2026-06-13

Updated: 2026-06-15

## Design Decision

The puck is part of the upper load path and must be lightly captive in the upper ring. It must not be a loose part between the sensor and upper platform.

The capture feature must not become the normal force path. In normal weighing, force should travel:

```text
upper ring -> puck shoulder/contact -> sensor measuring bridge -> sensor cartridge -> lower ring
```

All other geometry is retention, assembly guidance, overload protection, or transport safety.

The sensor cartridge decision is now stronger than the puck decision: the `7.1 mm` raised-wall cartridge with the over-wall retainer is physically validated and should be treated as the concept-v5 baseline. The puck keyhole/captive concept is still experimental.

## Why The Keyhole Concept Is Suspicious

The first keyhole/T-slot coupon made the puck captive, but it also made the capture geometry look like a sliding fit in the load path. That is risky for a weighing design because sliding contact can add:

- lateral force into the sensor,
- friction and hysteresis,
- sensitivity to print tolerance and surface texture,
- overconstraint between the four sensor stations.

For a low-cost printed scale, a little clearance in non-load-bearing retainers is better than a precise sliding interface that accidentally carries load.

## Reference Principles

Common load-cell and weigh-module design guidance tends to converge on these principles:

- Introduce load as close as possible to the intended measuring axis.
- Avoid side loads, torque, bending moments, and force shunts.
- Use a defined load button, ball/cup, rocker, or similar contact when self-alignment matters.
- Let overload stops and transport retainers be separate from the normal measuring load path.
- Avoid overconstraining a floating platform; constrain only the degrees of freedom needed for safety and repeatability.

Useful reference families:

- Load-cell and weigh-module application guides from manufacturers such as HBK/HBM, Flintec, Interface, Rice Lake, Vishay/VPG, and METTLER TOLEDO.
- Kinematic coupling and exact-constraint design literature for the broader principle of avoiding overconstraint.
- OIML R60 and NIST Handbook 44 as standards context for load cells and weighing devices, though they are not product design tutorials.

## Proposed Mechanical Architecture

### Lower Ring

The lower ring is the fixed base.

- Holds four removable sensor cartridges.
- Carries overload stops.
- Carries wire routing and electronics interfaces.
- Segment joints should use printed sliding/wedge/dovetail features where possible, with minimal metal fasteners.
- It must never directly support the upper ring in normal weighing.

### Sensor Cartridge

The cartridge is a serviceable sensor station.

- Sensor is laterally snug in the printed pocket.
- Sensor is held down by the support-free over-wall retainer.
- The validated locator walls are `7.1 mm` above the cartridge floor.
- The 2026-06-15 print test confirmed that this wall height gives the desired snug sensor fit.
- Sensor bridge, button, glue, cable, and active flexing areas remain free.
- Cartridge and retainer are lower-ring components, not part of the upper load path.

### Captive Puck

The puck is retained by the upper ring but mechanically contacts the sensor.

- Puck lower face contacts the sensor bridge area.
- Puck upper shoulder/contact face carries load from the upper ring.
- Captive head/neck should prevent drop-out without becoming the normal force path.
- 2026-06-15 PETG tests showed that `0.20 mm` radial clearance is the best tested head fit; `0.35 mm` and `0.50 mm` are too loose.
- The `0.20 mm` puck stays in place when inverted but can still be removed by hand without meaningful force.
- The intended side-slide insertion path did not work in PETG; PETG gives too little and the puck installs only by top-down pressing.
- Therefore the puck is not yet a validated captive mount. The next concept should avoid relying on elastic side-slide insertion unless a compliant feature is added.

### Upper Ring

The upper ring is the floating load receptor.

- It carries the captive puck cages.
- It transfers load only through the four pucks.
- It has no normal contact with lower ring, cartridge retainers, or overload stops.
- It can include non-contact lateral guards, but those need measurable clearance.

### Upper/Lower Retention

The upper and lower rings need transport/lift retention, but not a rigid connection.

- Use printed safety clips or captive hooks at the perimeter.
- Retention features should have vertical free play in normal use.
- They should engage only when the scale is lifted, inverted, or overloaded.

### Overload Stops

Overload stops are independent lower-ring features.

- Set the free gap around `0.8-1.2 mm` initially.
- Stops should contact the upper ring before the sensor is permanently damaged.
- Stops should not touch during ordinary weighing.

## Next Test Direction

The next puck print should move away from the current rigid side-slide keyhole and test one of these directions:

- top-down insertion with a separate printed keeper or cover,
- a compliant latch/finger that is not in the load path,
- a two-piece upper-ring insert that captures the puck after placement,
- or a captive-but-serviceable puck that is retained by the final upper/lower assembly rather than by a snap/keyhole alone.

Success criteria:

- Puck cannot fall out when the upper ring is inverted.
- Puck cannot be removed without a deliberate service motion.
- Puck can still self-seat slightly on the sensor.
- Upper ring presses the puck via its load shoulder/contact face, not via the keeper.
- Retention can be printed without support and with minimal metal fasteners.
- No underside supports are required for any printed part.
