# Parts evaluation log

Every candidate part gets a verdict here, so rejections don't get re-shopped
and accepted parts carry their caveats. Format: date · part · verdict · why.

## Batteries

**2026-08-31 · WattCycle 12V 314Ah Mini LiFePO4 (4.0 kWh, 27 kg, 200 A BMS, ~$510)**
Verdict: **NO for flight / YES for ground.** One 27 kg brick exceeds the
entire 23 kg battery allowance and kills the modular W&B scheme; 12.8 V bus
means 400+ A at climb power (BMS caps at 200 A); LiFePO4 ~149 Wh/kg claimed.
Excellent as the field charging station (4 kWh ≈ one full recharge of the
3.6 kWh module set, $127/kWh), bench power, and ground-mule battery.

**2026-08-31 · AliExpress "48V 100Ah citycoco pack", claimed 3 kg**
Verdict: **FRAUD.** 4.8 kWh at 3 kg = 1,600 Wh/kg, ~6x the best cells that
exist. Listing-quality tell; do not buy batteries with impossible density.

**2026-08-31 · Fullymax 12S 44.4V 22Ah smart pack (978 Wh, 6.5 kg, 20C, $769)**
Verdict: **YES — prototype flight battery, 3 per aircraft.** Purpose-built
ag-drone flight pack, smart BMS (cycle logging, auto-storage, firmware),
150 Wh/kg. 3 packs = 19.5 kg / 2.93 kWh -> empty 111.5 kg, inside the
115 kg cap; ~70 min sustain / ~1,450 m cumulative climb. Consequence:
**propulsion bus frozen at 44.4 V nominal (12S)** — size ESCs and motors
to it. Caveats: ~200-cycle life (yearly replacement in service — prototype
only), 20C power-cell weight penalty vs energy cells (~0.5 kWh forfeited
vs custom 21700 modules at equal mass), LiPo fire discipline (contained
module bays, charge off-vehicle). Verify weight and true capacity on
receipt. Production path remains custom energy-optimized 21700 modules.

**2026-09-01 · LiTech LP13S6P17A150AL001 — 13S6P li-ion, 48V/25.2Ah/1210 Wh,
CAN/RS485/BT BMS, IP65 metal case, ~150 A cont. (per part-number code), OEM**
Verdict: **RFQ — potential production module, pending weight.** Li-ion
energy cells (the right chemistry for our ~1.4C draw), product-grade cycle
life, CAN BMS, and 2-pack redundancy (one pack alone sustains level flight).
Weight unpublished: at <=7.5 kg (161 Wh/kg) it displaces Fullymax AND the
self-built module plan; at ~9 kg it loses. RFQ spec: 48V-class, ~1.2 kWh,
<=7.5 kg, >=100 A continuous, CAN, named 21700 energy cells, UN38.3, real
datasheet mass. NOTE: 13S conflicts with the Fullymax 12S bus — softened
freeze below.

**Bus voltage freeze, amended:** "48 V-class" — all propulsion components
(motors, ESCs, wiring, contactors) rated for 54.6 V max (13S ceiling), so
both 12S (Fullymax) and 13S (LiTech) packs remain compatible until the
pack decision lands. Do not mix pack types on one aircraft.
