# 1:10 printed model — build plan

Printer: Bambu Lab P2S, 256 × 256 × 256 mm. Geometry: `tools/model_geometry.py`
→ `models/1to10/*.stl` (all watertight, all fit the bed, report in
`parts_report.json`). Preview: `docs/model_1to10_preview.png`.

## What this model is for — and what it is not

**Tests (worth building for):**
1. **The fold, with real locks.** Kinematics scale exactly, so both
   parallelogram stages, the forward scissor, the knuckle z-offset, and the
   lock sequencing are all faithfully represented. Note: *clearances scale
   too* — the full-scale 18 mm footwell margin becomes 1.8 mm here, inside
   print tolerance. If the model binds at the footwell, that is a finding
   about the full-scale margin, not a print defect: the answer is to widen
   the full-scale margin to ≥ 30 mm, not to file the model.
2. **Configuration stability.** Stagger as tail arm, decalage making the
   front pair stall first, spiral/Dutch-roll tendency with these fins —
   all visible in hand-glide tosses before any electronics go in.
3. **Elevon authority and the two-motor control backup** (phase 3).

**Does not test (do not draw conclusions):** aerodynamic coefficients
(Re ≈ 45k at this chord — the 14.3% section will run a laminar bubble and
glide at maybe L/D 6–8; full scale is Re ≈ 800k), flutter, the sail
structure (printed skins are rigid), mass properties, or actuator loads.

## Geometry at 1:10

| item | full scale | model |
|---|---|---|
| Span | 10.1 m | 1,010 mm |
| Chord | 0.72 m | 72 mm |
| Root stub / inner / outer panel | 0.24 / 2.25 / 2.25 m | 24 / 225 / 225 mm |
| Stagger / gap | 1.50 / 1.40 m | 150 / 140 mm |
| Fin | 2.05 m × 0.35 m, 12% | 205 × 35 mm |
| Pod | 2.1 × 0.74 × 1.4 m | 210 × 74 × 140 mm |
| Outer-panel washout | 3° | 3° (built into the STL) |
| Decalage | front +2.5° vs rear | built into `root_stub_front` |
| Knuckle z-offset | 120 mm | 12 mm (`hinge_lug_offset`) |
| Wing area | 13.0 m² | 0.135 m² |

## Parts and print counts

| STL | qty | material | orientation / notes |
|---|---|---|---|
| `wing_inner` | 4 | LW-PLA | span-vertical, as printed (no twist → not chiral) |
| `wing_outer` | 2 + 2 **mirrored** | LW-PLA | span-vertical. **Chiral:** washout has handedness. Print 2, then mirror in Bambu Studio (right-click → Mirror → X) and print 2 |
| `fin_blank` | 2 | LW-PLA or PLA | vertical; 3.2 mm spar hole |
| `root_stub_front` / `_rear` | 2 + 2 | PETG | these carry the decalage; glue to pod |
| `capsule_pod` | 1 | PLA / PETG | lying on its side; 3 walls, 0–4% infill; nose taper *is* the footwell (fold-critical) |
| `hinge_lug` | 24 | PETG | flat; 3.2 mm hole for M3 pins |
| `hinge_lug_offset` | 8 | PETG | flat; the 12 mm knuckle z-offset lugs |

Slicer settings for the LW-PLA airfoils: 2 walls (0.42 mm), 0% infill,
no top/bottom layers except 2 at the ends, 0.16–0.20 mm layers, LW-PLA
foaming temp per the filament (typically 230–250 °C, flow ~50%), dry the
spool, slow (≤ 60 mm/s). Spar and pin holes are through-holes along the
print axis, so they print clean without supports.

## Hardware (glider phase)

- Spars: 8 × carbon tube Ø5 × 225 mm (one per panel; the fold joints break
  the spar, as they do full scale). Alignment pins: 8 × carbon rod Ø2 × 30 mm.
- Fin spars: 2 × carbon rod Ø3 × 205 mm.
- Fold pins: M3 × 16 screws with nyloc nuts as hinge pins (12 knuckles: 4 root
  pivots, 4 mid-span knuckles, 4 fin-tip hinges). Fold locks: 4 mm Ø
  neodymium magnet pairs at the deployed position (phase 1), replaced by a
  9 g servo-driven pin (phase 2) to test the interlock logic.
- CA + kicker for PETG lugs to LW-PLA; epoxy for spars in the pod stubs.

## Mass and CG

Estimate: 8 panels ≈ 140 g, fins 16, pod ≈ 70, stubs 8, lugs/pins 25,
spars 40 → **~300 g airframe.** Glider-phase electronics (4 × 9 g servos,
RX, 1S 500 mAh) ≈ 60 g → ~360 g before ballast. Powered (phase 3): + 2 ×
(2204 motor, 12 A ESC, 5" prop) + 3S 850 mAh ≈ +210 g → ~570 g.

Wing loading ≈ 4.2 kg/m² powered → flies at ~9–12 m/s. That is faster than
Froude scaling would give (~4 m/s) because the model is ~3× "scale weight";
expected and acceptable — the fold and the stability signatures do not
depend on it.

**First CG guess: 115–120 mm aft of the nose** (≈ 10% of the stagger ahead
of the estimated neutral point at ~130 mm, taking the rear pair at ~70%
efficiency in the front pair's downwash). Start nose-heavy; move aft by
5 mm steps on glide tosses until the glide flattens without hunting.

## Build phases and test cards

**Phase 1 — bench article (no electronics).** Print, spar, assemble both
sides on the pod with magnet locks. Tests: (a) fold both stages by hand;
photograph every interference; (b) measure freeplay at each lock with a
dial indicator against the panel tip; (c) hang 200 g at each tip node
deployed — the propped-beam box should barely deflect; note any joint
that opens. Record in `docs/test-log.md` (create on first test).

**Phase 2 — hand-glide.** Ballast to CG, toss on grass. Looking for:
straight glide, no pitch hunting (decalage working), no wing-drop at the
end of the glide (front stalls first), spiral tendency. Then deliberately
mis-rig: rear stubs at 0° vs front 0° (no decalage) to confirm it matters.

**Phase 3 — RC.** Elevons on the rear outer panels (cut 25% chord, tape
hinges — the flexure idea, cheaply), 2 motors on the rear inner panels at
±120 mm, differential-thrust yaw. Fold servos + lock pins with the
"cannot arm unless locked" interlock in the flight controller — the
first end-to-end exercise of the safety logic.

## Known limitations of this geometry (v0)

- Panels are solid lofts; skins come from slicer wall settings, not modeled
  ribs. Fine for LW-PLA at this size.
- Hinge lugs are generic plates; their placement on panel end-faces is
  by hand (glue at 25% chord, pin axis vertical). A v1 should merge lug
  pockets into the panel ends.
- Pod is a clean loft with no canopy line, hatch, or gear — a shape and
  mass placeholder. The nose taper approximates the footwell requirement.
- No nacelles yet; phase-3 motors mount on printed saddles.
