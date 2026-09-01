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
Weight confirmed: **6,800 g ±30 g → 177.9 Wh/kg** — beats the module spec
(157) and Fullymax (150), with IP65 metal case and CAN included. Internally
consistent: 78 x ~4.9 Ah 21700 energy cells (~5.5 kg) + 1.3 kg case/BMS.
Verdict: **ADOPTED as the flight battery** (displaces Fullymax, which is
struck). Aircraft fit: 3 packs = 20.4 kg / 3.63 kWh -> empty 112.4 kg
(2.6 kg under the Part 103 cap), ~87 min sustain / ~1,870 m cumulative
climb, max pilot ~85 kg; 2 packs -> pilot ~92 kg; 1 pack -> ~99 kg. Climb
draw 42 A/pack vs ~150 A rating; any single pack sustains level flight.
Verify on receipt: shipped weight incl. connectors, actual cell model and
its continuous discharge rating (150 A is decoded from the part number,
unconfirmed), UN38.3.

**Bus voltage FROZEN: 13S — 48.1 V nominal, 54.6 V max.** All propulsion
components (motors, ESCs, wiring, contactors) sized to 54.6 V. Do not mix
pack types on one aircraft.

## Motors

**2026-09-01 · BadAss 6245-155Kv outrunner ($300, giant-scale RC)**
Verdict: **NO — Kv mismatch.** 155 Kv on the 13S bus = ~5,800 rpm loaded;
our O~1.05 m folding props need 2,000-2,400 rpm. Flying it means either a
~0.5 m prop (static thrust drops ~35%, grass takeoff stretches from
~60 m to 120+ m — kills the short-field story) or a 2.5-3:1 belt redrive
in the nacelle (rejected class of solution). Likely also 12S-max rating vs
our 54.6 V bus ceiling. Same lesson as the e-bike motor in the exploration,
mirrored: match the motor to the prop's rpm, then shop.

**Motor filter (frozen):** Kv 50-65 · rated >= 54.6 V (14S label) ·
>= 3 kW continuous / ~4 kW 30 s · ~13 N.m continuous · <= 2 kg ·
tractor mount, folding-prop hub. This lives in the paramotor /
heavy-lift-drone catalog (O120-155 mm outrunners: MAD M-series, T-Motor
U15 family, Hacker Q150 class), not giant-scale RC.

## ESCs

**2026-09-01 · T-Motor Alpha 80A 12S FOC ESC ($130, 110 g, 80 A cont / 100 A 10 s)**
Verdict: **NO — voltage ceiling 52.2 V vs our 54.6 V (13S full charge).**
Right class in every other respect (current margin over 62 A climb draw,
FOC, companion series to the U-family motors our filter targets). Pick the
14S/HV sibling instead.

**ESC filter (frozen):** rated >= 14S / 58 V · >= 80 A continuous ·
FOC · telemetry out (current/temp/rpm) to the FC · low-voltage cutoff
configurable OFF (the energy manager owns sag decisions, never the ESC) ·
<= 200 g · nacelle-mountable with propwash cooling.
