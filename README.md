# Shapeshifter

A single-seat, folding, electric assisted glider — hang-glider freedom with
fly-by-wire safety, in a vehicle that drives itself to the launch point.

## The three modes

1. **Drive** — folded (3.9 × 2.5 m footprint), self-propelled on its wheels
   at scooter speeds. Off-road / field / garage-to-launch; not road-legal by
   design. Folded ground handling also removes the classic wind-on-the-ground
   hazard of foot-launched gliders.
2. **Unfold** — two automated fold stages (nested parallelogram
   linkages, all-vertical hinge axes, gravity-neutral), sensor-verified locks. The aircraft will not arm propulsion
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
| Battery | modular 2–4 × 0.9 kWh swappable packs + isolated actuator pack |
| Folded | 3.91 × 2.46 × 2.08 m — standard parking space |
| Regulatory | FAR Part 103 ultralight (no license, no certification) |
| Recovery | ballistic parachute (excluded from Part 103 empty weight) |

## Status

Concept definition. See [docs/spec.md](docs/spec.md) for the numbers,
[docs/fold-mechanism.md](docs/fold-mechanism.md) for the fold design,
[docs/mass-audit.md](docs/mass-audit.md) for the mass/battery ledger,
[docs/decisions.md](docs/decisions.md) for the decision record, and
[docs/exploration-history.md](docs/exploration-history.md) for how the
configuration was reached and what was rejected on the way.

## 1:10 printed model

Printable STLs for a Bambu P-series (256 mm cube) live in `models/1to10/`
(`tools/model_geometry.py`); editable STEP solids in `models/1to10/step/`
(`tools/model_step.py`, CadQuery); a native parametric Fusion 360 build
script in `tools/fusion360/`. Build plan, print counts, and test cards in
[docs/model-1to10.md](docs/model-1to10.md).

## Driving Fusion 360 directly

Autodesk's Fusion MCP server (Fusion: *Preferences > General > API > enable
Fusion MCP Server*, default port 27182) is registered in `.mcp.json` as a
project-scoped MCP server. It listens on loopback, so it is reachable only
from a Claude Code session running on the same machine as Fusion:

```
git clone <repo> && cd shapeshifter
git checkout claude/shared-conversation-review-vau7yj
claude            # approve the "fusion" MCP server when prompted
```

Then ask Claude to build the 1:10 model in the open Fusion design — it can
drive Fusion's API live instead of running the blind script in
`tools/fusion360/`.

## Next physical articles (in order)

1. Sub-scale fold mechanism (both parallelogram stages + locks) — the fold
   is the novel mechanism; prove 1-DOF behavior, lock integrity, and
   repeatability before any aerodynamic work.
2. Fin/tip node with stub wings, torsion-tested — the fin carries three
   jobs (joiner, yaw surface, wing-to-"tail" load path); its stiffness is
   the number the stability margin hangs on.
3. One full-scale wing element (D-nose, sail, camber flap, mid-span fold
   joint) — the entire aircraft in miniature.
