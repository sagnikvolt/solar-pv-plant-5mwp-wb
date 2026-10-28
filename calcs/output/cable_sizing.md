# Cable sizing and AC-side losses (preliminary)

Desk calculation. Ampacities are typical datasheet values, rates and lengths are assumptions (see ASSUMPTIONS.md).

## 1. DC string cables (copper, H1Z2Z2-K type, 1.5 kV DC)

Design current = 1.25 x Isc x (1 + 10% rear gain) = **18.9 A**. Temperature derating 0.91 (cable at 70 C ambient, rated 120 C), grouping 0.80.

| One-way length (m) | Section (mm2) | Ampacity after derating (A) | Voltage drop at Imp | % of string Vmp | Pass |
|---|---|---|---|---|---|
| 40 | **4** | 40 | 5.8 V | 0.52% | yes |
| 70 | **4** | 40 | 10.2 V | 0.90% | yes |
| 100 | **6** | 51 | 9.7 V | 0.86% | yes |
| 130 | **10** | 72 | 7.6 V | 0.67% | yes |

Rule used: smallest standard section meeting ampacity and a 1.0% drop at Imp. 4 mm2 serves strings up to about 70 m, 6 mm2 beyond that. PVsyst uses a 1.5% DC ohmic loss at STC; the string cables stay below it.

## 2. Inverter-to-transformer AC cables (aluminium XLPE, 1.1 kV class, 800 V)

Inverter current 180.5 A at 800 V, unity power factor, 80 m run. Ampacity after buried-installation derating 0.80 (ASSUMPTION). Target: drop at rated current at most 0.5%.

| Section (mm2) | Resistance at 90 C (ohm/km) | Ampacity after derating (A) | Drop at rated current | Pass |
|---|---|---|---|---|
| 95 | 0.387 | 164 | 1.21% | no |
| 120 | 0.307 | 188 | 0.96% | no |
| 150 | 0.245 | 212 | 0.77% | no |
| 185 | 0.199 | 240 | 0.62% | no |
| 240 | 0.153 | 280 | 0.48% | yes |
| 300 | 0.123 | 316 | 0.38% | yes |

Chosen: **240 mm2 aluminium** (3 single-core per inverter). Loss at rated current 0.48%.

## 3. Step-up transformers

2 x 2.5 MVA, 0.8/33 kV, Dyn11, ONAN, outdoor. Each takes 8 inverters = 2.0 MVA at 30 C rating (80% loading), less in summer when inverters derate (225 kVA at 40 C). Typical losses (ASSUMPTION, check vendor): no-load 2.1 kW, load loss 20 kW at rated.

## 4. 33 kV evacuation

Full output 4.0 MW at 33 kV: **70 A**. Concept: 33 kV RMU (VCB + metering) at the plant, then a 3 km overhead line (ACSR Dog 100 mm2, ampacity about 270 A) to the grid substation. Resistive drop 0.30% of 33 kV; loss 11.9 kW at full output. The line length and the grid substation are placeholders until the plot and the DISCOM feasibility are known.

## 5. AC-side energy loss (PVsyst VC4 does not model it)

| Item | Loss at rated (kW) | Annual loss (MWh) |
|---|---|---|
| Inverter-to-transformer cables | 19.2 | 33.6 |
| Transformer load loss | 40.0 | 70.1 |
| Transformer no-load loss | 4.2 | 36.8 |
| 33 kV line | 11.9 | 20.9 |
| **Total** | | **161.3 (2.28% of 7,078)** |

Energy delivered at the 33 kV point (before any plant auxiliary use): **6,917 MWh/yr**. The load-factor term (mean P^2 / Prated^2 = 0.2) is an assumption; it can be replaced by the real hourly output from PVsyst.

