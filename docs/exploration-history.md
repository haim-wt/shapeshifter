# How we got here — exploration summary

Condensed from the design exploration conversation (Aug 2026). Recorded so
the reasoning survives; each rejected branch names why, because several
"new" ideas will turn out to be these.

## The arc

e-bike motor pushing a hang glider → powered flying wing with motorized
surfaces → rigid pilot mount, fly-by-wire → all-moving wing panels on
robotic actuators (CubeMars AK class) → three-section rotating wing →
morphing sail wing (D-nose + bending trailing edge, 6 actuators) →
sectioned wing, actuators local per section → four-element box wing,
actuated at both ends → "assisted glider" reframing (e-bike principle) →
fixed joined wing + 2 elevons, intelligence in software → + folding,
wheels, capsule = Shapeshifter.

## Rejected branches and why

| branch | killed by |
|---|---|
| E-bike hub/mid-drive motor | RPM mismatch (500 vs 2800), torque reaction |
| Stock e-bike battery | BMS current cap, hard cutoff |
| Swept flying wing, hanging pilot FBW | 0.5 Hz pendulum inside pitch-loop bandwidth |
| All-moving panels, cambered airfoil | 250 N·m hinge moments — actuator mass |
| Steppers / worm industrial gearboxes | power density, backlash (flutter path), holding heat |
| Spanwise pushrods / torsion shafts (4 m) | buckling, windup, ~3 kg/side |
| Spoilerons as primary control | no pitch, deadband + hysteresis |
| Balanced elevons (conventional) | survived on merit — became the final answer |
| Ducted fans | stopped-duct drag ≈ 2 points of L/D |
| Single pylon folding prop | single-point propulsion/control failure (owner call) |
| Four rotors | cruise efficiency; twins + fins cover the failure cases |
| One-piece sail over joints | structural unknown in fabric; serial rigging |

## Ideas that survived and where they live now

- Reflexed/low-Cm sections, pivot-at-AC logic → informs flap hinge moments
- D-nose + sail + battens construction → the wing build (spec §3)
- Morphing trailing edge → the camber flap, now compliance-critical (D-007)
- Torque-controlled actuators, current-as-load-sensing → FBW actuator spec
- Actuator-per-section, wiring-only across joints → fold-joint electrical
  interlock concept
- Thrust unloading for slow approach → landing assist (spec §9)
- Sub-scale first: mechanism testbed, not aerodynamic testbed → build plan

## Corrections carried forward from the review

- Launch was the unsolved half of the safety story → solved by wheels +
  thrust: 45–70 m grass roll (spec §6)
- Old mass budget (60.6 kg) was stale and configuration-lagged → rebuilt
  honestly at 103 kg with fold + gear + capsule (spec §4)
- Part 103 stall margin was ~3% at 130 kg and negative at real weight →
  wing grown to 13 m² + flap made mandatory (spec §5, D-007)
- Min-sink figures in the exploration were internally inconsistent
  (quoted above best-glide sink) → recomputed (spec §5)
- No ballistic chute in any budget → fitted; excluded from Part 103 empty
  weight, included in flying weight
- Propped-beam spar sizing assumed a rigid fin prop → fin stiffness is
  open risk #1 with a physical test gate (spec §10)
