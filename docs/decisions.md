# Decision record

Short, dated entries. A decision stands until a dated entry reverses it.
(The exploration phase showed why this file exists: good decisions were
made, lost, and re-derived. Not again.)

## D-001 · 2026-08-31 · Regulatory envelope: FAR Part 103, hard target
No pilot license, no certification, no medical — the only regime where the
product promise is legally true. Consequences: 115 kg empty cap, 24 kt
stall in landing configuration, single seat. MOSAIC LSA is the documented
fallback, treated as product failure, not an option to drift toward.

## D-002 · 2026-08-31 · Configuration: joined-wing box, four elements
Front pair low/forward, rear pair high/aft, slanted fin joiners. Chosen for:
(a) folds as a linkage — the closed loop is 1-DOF when hinged; (b) no tail
boom; (c) propped-beam structure → light spars; (d) box-wing span
efficiency; (e) geometric (not commanded) stall recovery via stagger +
decalage. Precedent: Ligeti Stratos.

## D-003 · 2026-08-31 · Fold: two nested parallelograms, three locks/side
Stage 1 transverse (outer panels + fin fold inboard), stage 2 plan-view
scissor. Chosen over: single-stage scissor (folds to ~6.7 m — fails the
parking-space requirement) and span reduction to ~7 m (destroys glide
performance the product depends on). Fold is ground-only; interlocked
against propulsion arming.

## D-004 · 2026-08-31 · Folded footprint target: standard parking space
~4.4 × 1.9 m. Drives the two-stage fold (D-003). Scooter-class width was
considered and rejected as the driver — it would force skewed-hinge
complexity everywhere; kept as a possible refinement of stage 2 only.

## D-005 · 2026-08-31 · Ground mode: off-road self-mobility, tricycle gear
Not road-legal, by design — automotive homologation is the trap that killed
prior roadable aircraft. Two driven mains + steerable nose; no
self-balancing single wheel (energy, failure modes, and landings need a
statically stable platform). Drive folded; deployed taxi speed-limited.

## D-006 · 2026-08-31 · Propulsion: two tractor motors on the rear wing
Twin ~3 kW, counter-rotating, folding props, ±1.2 m from centerline.
Redundancy is the requirement (owner decision, exploration phase): one
motor is a full sustainer; differential thrust is backup control authority.
Single pylon prop (better L/D) rejected for single-point failure. Ducted
fans rejected: ~2 points of L/D for stopped-duct drag.

## D-007 · 2026-08-31 · Camber flap on front pair is compliance-critical
At realistic flying weight the clean wing stalls at ~23.9 kt — inside
measurement error of the Part 103 limit. The morphing trailing edge
(CLmax ≥ 1.7 in landing config) is what puts stall at ≤ 23.1 kt with
margin. It is a required system, sized and tested as such.

## D-008 · 2026-08-31 · Battery is the residual claimant of all mass
Goal is maximum battery, not minimum weight. Core empty (no battery) = 92 kg
target; battery = 115 − core, carried as 2–4 swappable ~0.9 kWh modules.
Gear load cells measure weight & CG at power-on; software enforces MTOW 205
and CG — module count is the trim variable (heavier pilot, fewer modules).
Rule: any kg added must name the kg it displaces or the Wh it forfeits.

## D-009 · 2026-08-31 · Fold: all-vertical axes, double-back + FORWARD scissor
Both stages are parallelograms with vertical hinge axes: gravity-neutral,
max height 2.1 m throughout, 1-DOF per stage. Scissor sweeps FORWARD —
forced by the chord-flip trap (doubling flips outer-panel chords; aft sweep
buries the front inner TE in the cabin — model-verified, unfixable).
Consequences owned: 240 mm fixed root stubs (swing-arc clearance), equal
2.25 m panel spans, nacelles above the wing plane, and a hull footwell
≤ 0.32 m wide over the first 0.8 m. Folded 3.91 × 2.46 × 2.08 m.
Carrier-style over-the-top folding rejected: gravity-fighting actuators,
4 m height excursion, 2-axis mid joints.
