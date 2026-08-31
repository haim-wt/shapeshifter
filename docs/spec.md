# Shapeshifter — Specification v0.2

Status: concept definition. Every number here is a target with a stated
derivation, not a measured value. Numbers that bind the design are marked
**(binding)**.

## 1. Mission

Single occupant. Drive folded from storage to an open field under its own
power, unfold, take off in ~50–70 m of grass, fly as a genuine glider with
electric assist (launch, saves, go-around, powered slow landing), land,
fold, drive away. Pilot supplies intent; fly-by-wire supplies control and
envelope protection.

## 2. Regulatory envelope — FAR Part 103 (binding)

| requirement | limit | our position |
|---|---|---|
| Empty weight, powered | 254 lb / 115 kg | ~103 kg target + 12 kg margin |
| Ballistic parachute | excluded from empty weight | fitted, ~7 kg physical |
| Power-off stall, landing config | ≤ 24 kt CAS | 22.6–23.1 kt (flap, see §5) |
| Max level speed | ≤ 55 kt | ~35 kt cruise, not binding |
| Occupants | 1 | 1 |

Consequences: no license, no certification, no medical — this is what makes
"as easy as riding a bike" legally true, and it is why Part 103 is a hard
target rather than a preference. It also means nobody certifies the
fly-by-wire system; every safety property is self-imposed (§9).

Fallback if mass discipline fails: MOSAIC LSA (effective 2025-10-22) allows
electric propulsion, no weight cap, 59 kt stall — but requires a sport-pilot
certificate and consensus-standard certification. Different product; avoid.

## 3. Configuration

Joined-wing box: front wing pair low and forward on the capsule, rear pair
high and aft (~1.5 m stagger = tail arm), tips joined by slanted fins.
Decalage ~2.5° makes the front pair stall first — pitch stability and stall
recovery are geometric, not commanded. Four identical wing elements from one
mold; front/rear differ only in root-fitting incidence.

- Span 10.1 m, area 13.0 m², chord 0.72 m constant
- Element per side: 0.24 m fixed root stub + 2.25 m inner panel + 2.25 m
  outer panel (equal spans — a fold requirement, see docs/fold-mechanism.md)
- Effective span ≈ 11.7 m (Prandtl box-wing), effective AR ≈ 10.5
- Section: D-nose torsion box to 30% chord, sail aft, ~14% t/c, morphing
  trailing edge (camber flap) on the front pair
- Moving aerodynamic surfaces in flight: 2 elevons (rear outboard, actuators
  in fin nodes) + camber flaps. Yaw: fins + differential thrust/regen.

## 4. Mass budget (binding — every line is a not-to-exceed)

| group | kg |
|---|---|
| 4 wing elements (13 m², D-nose + sail + flap) | 26 |
| Fins / tip nodes (2) | 6 |
| Fold system: 4 root pivots, 4 mid-span joints, locks, actuators | 12 |
| Capsule survival cell + canopy | 16 |
| Seat, harness, cockpit controls | 4 |
| Landing gear: 3 wheels, 2 hub motors, brakes, suspension | 13 |
| Propulsion: 2 motors, ESCs, folding props, mounts | 9 |
| Flight battery — modular, 2–4 × 0.9 kWh @ 5.75 kg | 11.5–23 |
| Avionics, FBW actuators, actuator battery, wiring | 6 |
| **Empty (Part 103 accounting)** | **103.5–115** |
| Ballistic parachute (physical, excluded from Part 103 count) | +7 |
| Pilot (design range 60–100 kg) | +85 nominal |
| **Flying weight, nominal** | **~195 kg** |

Core empty (everything except battery) = 92 kg; battery fills the gap to
the 115 kg cap as swappable modules. Full audit, line justifications, and
the battery-as-residual-claimant rule: **docs/mass-audit.md**.

## 5. Speeds and compliance stall (binding)

At 195 kg flying weight, S = 13.0 m², sea level:

- Stall, clean, CLmax 1.5: 12.3 m/s = 23.9 kt — no margin. Therefore:
- **Stall, landing config, camber flap, CLmax 1.7: 11.9 m/s = 23.1 kt** ✓
  (at 100 kg pilot + chute: 23.5 kt ✓)
- The camber flap is REQUIRED for Part 103 compliance, not an option.
- Rotate ~13.5 m/s; approach ~1.3 Vs ≈ 15 m/s, reduced further by partial
  thrust unloading on final
- Best glide ~16 m/s, L/D ≈ 16–17; min sink ≈ 0.9 m/s at ~13 m/s
- Vne 40 m/s (structural placard, to be confirmed by aeroelastic analysis)

## 6. Propulsion and energy

- 2 × ~3 kW continuous tractor motors, rear wing leading edge at ±1.2 m,
  counter-rotating (tops inboard), Ø1.0–1.1 m folding props
- Static thrust ~550 N combined; + wheel drive → grass takeoff roll 45–70 m
- Climb ~1.0–1.3 m/s at full power (195 kg); one motor = full sustainer
- Cruise/sustain power: ~2.2 kW electrical → 40–85 min powered (2–4 modules)
- Energy reality: one climb to 500 m costs ~600–700 Wh. The pack buys one
  launch + saves + reserved go-around (~25 Wh, never spendable by the
  planner), or two modest launches. Soaring is the range extender.
- Regen: props windmill under regen for glide-path control (replaces
  spoilers) and descent recovery
- Ground drive: 2 hub motors, 25–40 km/h, ~20 Wh/km — ground range is
  effectively free relative to flight

## 7. Fold architecture (the novel mechanism)

Fully defined in **docs/fold-mechanism.md**; verified by the parametric
model `tools/fold_kinematics.py` (collision-checked through the complete
sequence); figure: docs/fold_sequence.png. Summary:

- Two nested parallelogram linkages, **all hinge axes vertical** → the fold
  is gravity-neutral; actuators are sized by wind (≤ 4 m/s fold limit),
  not by lifting panels.
- Stage 1: outer panels + fin double back 177° about mid-span knuckles
  (fin translates — parallelogram coupler). Stage 2: inner panels scissor
  88° **forward** about 240 mm root stubs; wings wrap the nose.
- **Folded: 3.91 × 2.46 × 2.08 m** — standard parking space.
- Flight loads cross every hinge perpendicular to its free axis: bearing
  couples carry bending (5–6 kN ultimate); locks carry only in-plane
  moments (< 0.7 kN). Two lock groups per side, spring-loaded to locked,
  position-sensed, tapered pins for zero freeplay.
- The fold owns one hull constraint: the footwell (first 0.8 m, below
  z ≈ 0.5) must stay ≤ 0.32 m wide — the doubled front-outer trailing
  edges sweep past it with 18 mm margin.
- Fold is ground-only: interlocked against airspeed and prop arming;
  propulsion cannot arm until all locks confirm and a control sweep passes.

## 8. Ground mode

- Tricycle: two main wheels (hub motors, regen + friction brakes) just aft
  of CG, ~1.1 m track; steerable nosewheel. No self-balancing single wheel:
  static stability, no balance energy, and a stable rollout platform for
  automated landings.
- Off-road self-mobility only (field, campground, private ways). Not
  road-legal, by decision — avoids automotive homologation entirely.
- Drive folded; unfold at the launch point. Deployed taxi is limited to
  walking pace by software (13 m² of wing in a gust is a kite).

## 9. Safety architecture

1. Envelope protection: alpha and load-factor limits in software; stall is
   unreachable by command. Elevon travel limiter implements the guarantee.
2. Redundancy: twin motors (one = sustainer; differential thrust is backup
   yaw/pitch authority after a control failure), dual elevon paths,
   isolated actuator/avionics battery (control survives total propulsion
   pack loss).
3. Interlocks: props cannot arm unless all 6 fold locks confirm + control
   sweep passes; fold cannot actuate with airspeed > 0 or props armed.
4. Ballistic parachute, capsule as survival cell: crushable nose,
   energy-absorbing seat sized for ~7 m/s descent under canopy.
5. Landing assist: powered slow approach (partial thrust unloading),
   propwash over elevons keeps control authority below free-flight stall,
   reserved go-around energy, auto-flare.

## 10. Open risks (ranked)

1. **Fin/tip-node stiffness** — the joined wing's stability margin and the
   propped-beam structural savings both assume a stiff fin loop. Physical
   torsion test before tooling.
2. **Fold-joint stiffness and freeplay** — 6 locked joints now sit in the
   primary structure; lash there is the flutter path. Budget < 0.5 mm at
   the lock, measured, per joint.
3. **Mass growth** — 12 kg margin against Part 103; every kg over cascades
   into the stall limit via §5.
4. **Aeroelastics of the final configuration** — no flutter analysis exists
   yet for the box with fold joints; required before Vne is trusted.
5. **Stage-1 fold collision/clearance geometry** — panels, fin, props, and
   capsule must clear through the full fold arc; resolve in CAD + sub-scale.
6. **Sail behavior at 13 m² with flap** — camber-flap CLmax 1.7 on a
   sail-over-D-nose section is assumed, not demonstrated; wind-tunnel or
   instrumented RC validation.
