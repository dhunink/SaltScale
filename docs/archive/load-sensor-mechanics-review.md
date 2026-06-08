# Load Sensor Mechanics Review

This note summarizes the mechanical behavior and common mounting practices for small commodity strain-gauge load sensors (SparkFun / Kiwi-style ~50 kg sensors), based on the SparkFun HX711/load-cell tutorial and product guidance. It concludes with a recommendation for SaltScale.

Sources and context
- SparkFun tutorial: "Load Cell Amplifier HX711 Breakout Hookup Guide" (SparkFun Learn) — describes bar-type, S-type, disc/button sensors and typical scale mounting patterns. (See SparkFun Learn: Load Cell Amplifier HX711 Hookup Guide.)

Assumptions
- The sensors discussed are small strain-gauge elements sold as "load sensors" (SparkFun product family). Exact packaging varies by vendor; SaltScale currently uses a 38×38×12 mm CAD placeholder.
- The sensors are rated ~50 kg and are strain-gauge based (millivolt-level Wheatstone bridge output).

Answers

1) Which parts of the metal frame are intended to be fixed?
- Typical small sensors have mounting faces or tabs intended to be fixed to one of the rigid reference plates (usually the lower plate). In "button/disc" or "single strain gauge" sensors SparkFun documents, the bottom mounting surface is fastened to the lower structure ("screw in the disc to a bottom plate"). For bar-type cells one end is often rigidly fastened to produce the intended bending moment.
- In practice: the lower reaction surface or mounting tab is fixed to the chassis/base; the surrounding structural frame (pocket) is fixed to the base and remains stationary relative to the sensor's lower face.

2) Which parts are intended to move?
- The sensing element (metal flexure or diaphragm) is intended to flex or deform under load. The top contact region (the face that the measured object presses on) moves relative to the fixed lower face by a very small amount (micro- to sub-millimetres), generating strain read by the gauge(s).
- The top plate or contact pad that transmits the user's load moves downwards under weight, compressing/bending the sensor between upper and lower reaction surfaces.

3) How is the sensor mounted in a typical bathroom scale?
- Typical approach (per SparkFun examples and scale photos): four sensors are positioned near the corners under the top platform. Each sensor is seated between an upper contact pad (on the platform) and a lower mounting surface fixed to the enclosure or base.
- Sensors may be screwed into the bottom plate or sit in small pockets; the top plate rests on the sensors when assembled. A combinator board or wiring bundle connects the sensors electrically to the HX711 amplifier.
- The assembly intentionally isolates lateral loads: guide walls, pockets, or frames locate the sensor while preventing shear from being applied to the sensing element.

4) Is the sensor itself normally a structural member?
- No. While the sensor is part of the vertical load path (sandwiched between top and bottom), it is not intended to carry lateral loads, act as a primary structural member, or bear shear/impact. SparkFun guidance shows sensors sandwiched between plates or screwed to a base, but recommends correct mounting to avoid undesired loading modes. Many scale designs place sensors in pockets or on reaction bosses so plastic/metal structure carries lateral and shear loads.

5) Should SaltScale use:
   A) sensor-as-structure
   B) sensor-inside-pocket

- Recommendation: B) sensor-inside-pocket.

Rationale and explanation (no unstated assumptions)
- Protection and repeatability: sensors are delicate to shear and torsion; pockets with upper/lower reaction pads provide repeatable contact and protect the sensing element from lateral shock. SparkFun examples show discs/buttons and single strain sensors mounted between plates with additional fixtures to ensure repeatable contact.
- Serviceability: pockets allow sensors to be replaced individually without cutting structural members.
- Accuracy and load path control: a pocketed frame with stiff bosses focuses the bending/compression into the intended axis and reduces parasitic compliance in surrounding plastic, improving repeatability and calibration stability.
- PETG print behavior: printed parts have dimensional variability; using a pocket with a small clearance plus hardened contact pads avoids wearing the printed plastic and keeps electrical characteristics stable.

Practical notes for SaltScale
- Use hardened metal contact pads or small washers on the sensor faces to spread load and prevent wear.
- Provide guide walls and shallow pockets sized for test clearance (e.g., +0.3..+0.6 mm) so sensors can be hand-inserted and removed.
- Ensure the lower boss is solid and not removed by pocketing operations — verify boolean order in CAD.
- Avoid routing shear loads through the sensor; add standoffs or guide pins where needed.

Remaining unknowns to finalize design
- Exact sensor package and mounting features (obtain vendor drawing). If the sensor includes mounting holes or tabs, the pocket and boss geometry should be updated to match.
- Whether to use screw retention, adhesive, or simply compression seating for each sensor — choose based on vibration, serviceability, and enclosure constraints.

Conclusion
- Based on SparkFun's tutorial and common bathroom-scale practice, place each 50 kg sensor inside a structural pocket with dedicated upper and lower reaction pads, protect it from shear, and avoid making the sensor the main structural member. This approach matches SaltScale's PETG platform constraints and provides the best balance of protectability, repeatability, and serviceability.
