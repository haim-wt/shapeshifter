# Shapeshifter

A single-seat, folding, electric assisted glider — hang-glider freedom with
fly-by-wire safety, in a vehicle that drives itself to the launch point.

## The three modes

1. **Drive** — folded (~4.4 × 1.9 m footprint), self-propelled on its wheels
   at scooter speeds. Off-road / field / garage-to-launch; not road-legal by
   design. Folded ground handling also removes the classic wind-on-the-ground
   hazard of foot-launched gliders.
2. **Unfold** — two automated fold stages (nested parallelogram linkages),
   three sensor-verified locks per side. The aircraft will not arm propulsion
   unless every lock confirms.
3. **Fly** — a 10 m joined-wing box glider, L/D ≈ 16–17, with twin electric
   tractor motors for takeoff (~50–70 m of grass), climb, go-around, and
   powered slow landings. Fly-by-wire with a hard flight envelope: stall is
   a software limit, not a pilot skill.

## Configuration at a glance

| | |
|---|---|
| Configuration | joined-wing box (Ligeti Stratos geometry), no tail boom |
| Span / area | 10.0 m / 13.0 m² (4 identical elements, one mold) |
| Empty weight | ~103 kg target (Part 103 cap: 115 kg / 254 lb) |
| Stall (landing config, camber flap) | ≤ 23 kt — Part 103 limit is 24 kt |
| Best glide | L/D ≈ 16–17 at ~16 m/s; min sink ≈ 0.9 m/s |
| Propulsion | 2 × ~3 kW tractor motors, folding props, rear wing LE |
| Battery | 1.6 kWh flight pack + isolated avionics/actuator pack |
| Folded | ~4.4 × 1.9 × 1.7 m — standard parking space |
| Regulatory | FAR Part 103 ultralight (no license, no certification) |
| Recovery | ballistic parachute (excluded from Part 103 empty weight) |

## Status

Concept definition. See [docs/spec.md](docs/spec.md) for the v0.2 numbers,
[docs/decisions.md](docs/decisions.md) for the decision record, and
[docs/exploration-history.md](docs/exploration-history.md) for how the
configuration was reached and what was rejected on the way.

## Next physical articles (in order)

1. Sub-scale fold mechanism (both parallelogram stages + locks) — the fold
   is the novel mechanism; prove 1-DOF behavior, lock integrity, and
   repeatability before any aerodynamic work.
2. Fin/tip node with stub wings, torsion-tested — the fin carries three
   jobs (joiner, yaw surface, wing-to-"tail" load path); its stiffness is
   the number the stability margin hangs on.
3. One full-scale wing element (D-nose, sail, camber flap, mid-span fold
   joint) — the entire aircraft in miniature.
