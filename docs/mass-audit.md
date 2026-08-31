# Mass audit v1 — every kilogram justified, battery as the residual claimant

Goal restated: the point of mass discipline is not a lighter vehicle — it is
**more battery**. This document sets the algebra that converts saved mass
into energy, then justifies every line.

## 1. The constraint algebra

Three independent caps:

1. **FAA empty weight** (Part 103): empty ≤ 115 kg, *battery included*,
   ballistic chute excluded.
2. **Stall** (Part 103, landing config ≤ 24 kt): at S = 13 m², CLmax 1.7
   → max flying weight **210 kg** (we operate to 205 for margin).
3. **Folded envelope** (parking space): fixed by the fold design, not mass.

Define **core empty = everything except battery**. Then:

- **Max battery = 115 − core.** Today core = 92 kg → max battery 23 kg.
- **At full battery, max pilot = 205 − 115 − 7 (chute) = 83 kg** — and this
  is *invariant*: shrinking core raises battery, not pilot allowance.
  Heavier pilots fly with fewer modules (see §3).

**The exchange rate: 1 kg of core saved = 1 kg of battery = ~160 Wh
= ~95 m of powered climb or ~4 min of sustain.** Every design argument
about mass now terminates in this number.

## 2. Line-by-line justification (core = 92 kg)

| line | kg | basis | confidence | path to battery |
|---|---|---|---|---|
| Wing panels, 4× (13 m² total) | 26 | 2.0 kg/m², D-nose + sail + battens + flap; comparable: ATOS-class rigid wings ~2.3 kg/m² incl. control frame | med | none — already aggressive; growth risk +2 |
| Fins / tip nodes, 2× | 6 | 0.7 m² surface + elevon actuator + propped-beam reaction fitting each | med | none; growth risk +2 (stiffness-critical part) |
| Fold system | 12 | model-derived: 4 root pivots (bearing couples @5.7 kN ult) ~1.3 ea; 4 mid knuckles (@5.3 kN) ~0.9 ea; 6 locks ~0.25 ea; 4 fold drives ~0.45 ea | med-high (loads computed) | **−1**: gravity-neutral fold means sub-kg drives; consolidate stage-1 drive to one side at a time |
| Capsule cell + canopy | 16 | 2.1 m carbon monocoque + bubble; sailplane forward-fuselage comparables 12–18; crash cell adds | med | none — safety-critical line |
| Seat, harness, controls | 4 | includes energy-absorbing seat stroke (chute descent ~7 m/s) | high | none |
| Landing gear + ground drive | 13 | 3 wheels, suspension, brakes + 2 hub motors @3.5 kg | high | **−3**: one driven main + freewheel + steered nose. Ground spec (30 km/h, grass) needs ~2 kW, not two motors. Takeoff traction: verify single-wheel slip on wet grass before committing |
| Propulsion | 9 | 2 × 3 kW outrunners ~1.4 ea, ESCs, Ø1.05 folding props ~0.9 ea, over-wing mounts | high | none |
| Avionics + FBW | 6 | 2 elevon + 2 flap actuators, FC + IMU + air data, isolated 150 Wh actuator pack (~1.0), wiring | med | none; growth risk +1 (wiring always grows) |
| **Core empty** | **92** | | | **identified: −4 → core 88** |

Growth risks total +5; identified savings −4. Honest expectation: core
stays 88–95. **Rule from here: any kilogram added must name the kilogram
it displaces or the watt-hours it forfeits.** Battery absorbs every saving
and every bust — it is the flexible line, by design.

## 3. Battery architecture: modular, and the W&B is measured

**4 swappable modules × ~0.9 kWh, ~5.75 kg each** (21700 cells, ~160 Wh/kg
at pack level — conservative; good pack engineering reaches 175+, which is
battery headroom at zero kg). One-hand carry, charge off-vehicle, no
charging infrastructure needed at the field.

The vehicle weighs itself: load cells in the three gear legs give total
weight and CG at power-on. Software enforces MTOW 205 kg and CG limits —
module count is the trim variable:

| pilot | modules | battery | flying wt | powered endurance* | cumulative climb* |
|---|---|---|---|---|---|
| ≤ 83 kg | 4 | 3.6 kWh | ≤ 205 | ~85 min | ~1800 m |
| ≤ 89 kg | 3 | 2.7 kWh | ≤ 205 | ~63 min | ~1350 m |
| ≤ 95 kg | 2 | 1.8 kWh | ≤ 205 | ~40 min | ~880 m |
| ≤ 100 kg | 1+ | 0.9 kWh | ≤ 204 | launch + reserve only | ~430 m |

*usable 88% of nominal; sustain ~2.2 kW; climb conversion ~0.32 (drag paid
during climb); go-around reserve (~25 Wh) always withheld by the planner.

This turns the Part 103 weight problem into a UX feature: the aircraft
tells you how many modules today's pilot + mission can carry, and refuses
to arm overweight. Nothing is placarded on trust.

## 4. What we deliberately do NOT chase

- Sub-2.0 kg/m² wings, exotic capsule layups, titanium anything: each buys
  1–3 kg at large cost and schedule risk; the same money buys pack-level
  Wh/kg, which scales all four modules at once.
- Removing the second flight motor: −4.5 kg, but redundancy is a standing
  owner decision (D-006).
- Removing gear/suspension travel: it is the landing-assist crumple margin
  and the W&B sensor mount.
