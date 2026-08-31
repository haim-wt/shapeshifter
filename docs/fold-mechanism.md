# Fold mechanism — design definition v1

Derived and verified with `tools/fold_kinematics.py` (parametric plan-view
kinematics with z-band collision checking through the full fold sequence).
Sequence figure: `docs/fold_sequence.png`.

## Architecture: two nested parallelograms, all hinge axes vertical

**Stage 1 — double-back.** Each side's outer-panel pair + fin rotates 177°
about vertical axes at the mid-span knuckles. The fin is the coupler of a
parallelogram four-bar (equal outer spans, tip separation = knuckle
separation), so it translates without rotating. Outer panels end doubled
back over the inner panels, raised 120 mm by an offset knuckle.

**Stage 2 — forward scissor.** Each side's inner-panel pair (carrying its
folded bundle) rotates 88° **forward** about vertical axes on the root
stubs. Same parallelogram logic; the folded bundle is the coupler. The
wings end up wrapped around the nose, hull in the middle of the package.

**Folded envelope: 3.91 × 2.46 × 2.08 m** — inside a standard parking
space. Deployed span 10.1 m (0.24 stub + 2.25 inner + 2.25 outer per side).

## Why these choices (each was forced, not preferred)

1. **All hinge axes vertical → the fold is gravity-neutral.** Panels swing
   in plan on their bearings; no actuator ever lifts a panel. Fold
   actuators are sized by *wind* on the swinging panel, not gravity:
   ~65 N·m (stage 1) / ~115 N·m (stage 2) for folding in up to 4 m/s wind
   — sub-kilogram motors. The alternative (carrier-style over-the-top
   folding) costs ~130 N·m of continuous gravity torque per joint, a 4 m
   height excursion mid-fold, and 2-axis mid joints. Rejected.
2. **Forward scissor, not aft — forced by the chord-flip trap.** Doubling a
   panel back 180° in plan flips its chord. After the scissor, inner-panel
   trailing edges point one way and outer-panel TEs the other; whichever
   sweep direction clears the inners buries the outers. Model result:
   aft sweep buries the front inner TE in the cabin (unfixable); forward
   sweep leaves only the front *outer* TE low near the hull — fixable (next
   item). Verified: aft collides at φ=27°, forward runs clean.
3. **Narrow footwell — a hull constraint owned by the fold.** The doubled
   front-outer TEs sweep through y ≥ ±0.18 m at z 0.30–0.45 over the first
   0.8 m of hull. The hull must be ≤ 0.32 m wide there. Anthropometry
   allows it (two feet side by side ≈ 0.30 m); the capsule spec now carries
   this as a frozen interface. Min clearance through the full sequence:
   18 mm — tight; recover with footwell −20 mm or stub +20 mm if CAD needs it.
4. **240 mm fixed root stubs — forced by the swing arc.** Any chordwise
   overhang ahead of a vertical hinge sweeps an *arc* inboard during
   rotation (LE corner dips 137 mm past the hull wall with roots on the
   hull). The stub moves the arc clear and gives the root bearing pair a
   rigid home. (This resurrects the exploration's "fixed center section.")
5. **Equal inner/outer spans (2.25/2.25)** — the outer folds back exactly
   onto the inner, its tip landing at the stub; unequal spans left the
   folded tip's TE corner grazing the hull by 7 mm mid-scissor.
6. **Nacelles above the wing plane** — slung under the LE they sweep the
   canopy top during the scissor; above the LE they clear (and precedent
   for over-wing pods on self-launchers is good).

## Joints and loads (from the model, ultimate)

| item | free axis | carries via bearings | lock carries |
|---|---|---|---|
| Root pivot (×4) | vertical | flap bending 1.14 kN·m → 5.7 kN couple (200 mm spacing) | in-plane moment incl. prop thrust: 0.63 kN link load |
| Mid knuckle (×4) | vertical | flap bending 0.80 kN·m → 5.3 kN couple (150 mm spacing) | in-plane moment: 0.28 kN pin load |

Key property, worth stating twice: **flight loads cross every hinge
perpendicular to its free axis.** Bearings (preloaded, zero-clearance)
carry bending and torsion; locks carry only small in-plane moments. The
locks are sub-kilonewton pins — the exploration's design rule ("bearings
carry bending; the constrained axis carries only its own load") holds at
every joint.

- Locks: 2 groups per side — one tapered pin + over-center toggle at each
  mid knuckle TE, one over-center drag strut at the scissor. Spring-loaded
  toward locked, position-sensed, tapered engagement for zero freeplay.
  Freeplay budget: ≤ 0.5 mm at each lock, measured, per preflight.
- 1-DOF per stage per side → one lock rigidifies each stage; the second
  pin at the mid knuckle is redundancy, not kinematic necessity.

## Sequence and interlocks

Unfold: (1) stubs live, scissor drives forward→deployed, scissor struts
over-center + pinned; (2) stage-1 knuckles drive outers out, TE pins seat;
(3) controller sweeps all surfaces, reads all 6 lock sensors + 4 knuckle
encoders, then and only then allows propulsion arming. Fold is the reverse,
permitted only at zero airspeed, props stopped and folded, on wheels.
Operational limit: no folding above 4 m/s wind (actuator sizing case;
above that, wait or point nose into wind).

## Open items

1. 18 mm minimum hull clearance → re-verify in surfaced CAD with real hull
   curvature (box model is conservative inboard, optimistic at corners).
2. Wiring: CAN + power to outer panels and fin (elevon actuator lives in
   the fin node) crosses two vertical-axis joints → service loops on the
   hinge axes, hard travel stops; no slip rings.
3. Sail continuity at the mid knuckle: sail is per-panel (decided in
   exploration); the knuckle gap needs a shroud that tolerates ±177°.
4. Stage-1 drive synchronization L/R (fold one side at a time is
   acceptable and halves actuator count — decide at prototype).
5. Sub-scale mechanism prototype (1:5): prove lock seating repeatability,
   measure real freeplay, confirm the parallelogram tracks under sail loads.
