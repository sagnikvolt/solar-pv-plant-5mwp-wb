# Preliminary BOQ scope, capex, LCOE, payback and CO2

Indicative desk estimate, not a quotation. Cost lines are positioned within published indicative ranges (Base = 25th percentile; plain mid-points gave INR 5.2 cr/MWp and LCOE 4.9, which contradicts market tariffs, so were judged too high) (see sources below); quantities are from the design. Financial inputs are assumptions.

## Scope (from the design)

| Item | Quantity |
|---|---|
| PV modules, Waaree BiN-08-565 (565 Wp) | 8,840 |
| Strings (26 modules each) | 340 |
| Mounting tables (2 portrait x 26 modules = 52 modules) | 170, in 17 rows |
| String inverters, Sungrow SG250HX | 16 |
| Step-up transformers, 2.5 MVA, 0.8/33 kV | 2 |
| 33 kV RMU (VCB + metering) | 1 |
| DC string cable (approx. 70 m per polarity, 5% wastage) | about 50 km |
| LV AC cable, 240 mm2 Al, 3 single-core x 80 m x 16 inverters | about 3.8 km |
| 33 kV overhead line, ACSR Dog (placeholder) | 3 km |
| DC capacity / AC capacity | 4,994.6 kWp / 4,000 kW |

## Capex (INR crore)

| Line | Low | Base (25th pct of range) | High |
|---|---|---|---|
| Modules (565 Wp bifacial, 8,840 pcs) | 7.49 | 8.62 | 11.99 |
| Inverters + MV equipment (16 x SG250HX, 2 x 2.5 MVA, RMU) | 2.00 | 2.37 | 3.50 |
| Mounting structures and foundations (170 tables) | 1.75 | 2.25 | 3.75 |
| Cables, combiner/ACDB, SCADA | 1.25 | 1.50 | 2.25 |
| Civil, fencing, roads | 1.00 | 1.19 | 1.75 |
| Plant-end substation and metering | 1.50 | 1.81 | 2.75 |
| Installation labour and EPC margin (ASSUMPTION) | 1.00 | 1.25 | 2.00 |
| **EPC subtotal** | 15.98 | 18.98 | 27.97 |
| Contingency 5% of EPC | 0.80 | 0.95 | 1.40 |
| Land lease, upfront (published 0.05 to 0.25) | 0.25 | 0.50 | 1.25 |
| External 33 kV line, 3 km (published 0.10 to 0.80) | 0.50 | 1.37 | 4.00 |
| Connectivity charges (published 0.03 to 0.15) | 0.15 | 0.30 | 0.75 |
| **Total capex** | **17.7** | **22.1** | **35.4** |
| per MWp | 3.54 | 4.42 | 7.08 |

## Energy used

PVsyst VC4 7,078 MWh/yr, less AC-side losses (`cable_sizing.md`) = **6,917 MWh/yr** at the 33 kV point in year 1; degradation 0.4%/yr over 25 years.

## Financial results

Assumptions: discount rate 10% nominal pre-tax, O&M INR 5 lakh/MWp/yr escalating 4%, insurance 0.3% of EPC, inverter replacement INR 0.48 crore in year 12, no tax, depreciation, subsidy or debt. Tariff flat for 25 years.

| Capex case | Tariff (INR/kWh) | Capex (INR cr) | LCOE (INR/kWh) | Simple payback (yr) | Project IRR (pre-tax) | NPV at 10% (INR cr) |
|---|---|---|---|---|---|---|
| Low | 2.34 | 17.7 | 3.52 | 15.3 | 3.7% | -7.2 |
| Low | 3.00 | 17.7 | 3.52 | 10.5 | 7.4% | -3.1 |
| Low | 3.62 | 17.7 | 3.52 | 8.3 | 10.5% | 0.6 |
| Base | 2.34 | 22.1 | 4.25 | 20.0 | 1.5% | -11.7 |
| Base | 3.00 | 22.1 | 4.25 | 13.8 | 4.8% | -7.6 |
| Base | 3.62 | 22.1 | 4.25 | 10.6 | 7.5% | -3.9 |
| High | 2.34 | 35.4 | 6.47 | > 25 | -2.6% | -25.2 |
| High | 3.00 | 35.4 | 6.47 | 24.1 | 0.2% | -21.2 |
| High | 3.62 | 35.4 | 6.47 | 18.2 | 2.4% | -17.4 |

**Headline (base capex, tariff 3.00):** capex INR 22.1 crore (INR 4.42 crore/MWp), LCOE INR 4.25/kWh, simple payback 13.8 years, project IRR 4.8%.

Tariff reference points: INR 2.34/kWh (GUVNL 625 MW solar auction, March 2026, per a news headline), INR 3.00 (my base case), INR 3.62/kWh (CERC interim tariff for DVC's 8 MW solar project in West Bengal, March 2025, per a news headline). Neither headline was opened in full.

## CO2 avoided

Grid emission factor: CEA CO2 Baseline Database v20.0 (Dec 2024), FY 2023-24: weighted average **0.727 tCO2/MWh**, combined margin 0.757 tCO2/MWh.

Year 1: 5,028 tCO2 (weighted average) to 5,236 tCO2 (combined margin). Over 25 years with degradation: about 120 thousand tCO2 at a constant factor (the grid factor will fall as the grid decarbonises, so treat this as an upper figure).

## Sources and limits

- Capex ranges: taypro.in utility-scale cost guide (indicative 2024 to 2026 ranges, updated 21 June 2026). A commercial blog, not a regulator figure; checked against the CTUIL benchmark below. Treat as +/-20%.
- Emission factor: CEA CO2 Baseline Database User Guide v20.0.
- No DCR premium, GST, interest during construction, or working capital is modelled. DCR modules cost more than the mid-range assumed here.
- Capex cross-check (verified Oct 2026): CTUIL's revised planning benchmark is INR 3.5 crore/MW for solar (article dated 7 Sep 2026; AC/DC basis not stated), which matches the Low case (INR 3.54 crore/MWp). A real project cited alongside it, SJVN 1 GW Bikaner, works out to about INR 5.49 crore/MW. The Base case (INR 4.42 crore/MWp) lies between the two, which is plausible for a 5 MWp single site with its own 33 kV line. Quote capex as INR 3.5 to 5.5 crore/MWp, base 4.4.
- Tariff caveat: auction tariffs of INR 2.3 to 3.6/kWh come from large projects with cheaper capital and lower return targets than the 10% discount rate used here, so LCOE here (INR 3.5 to 4.3) is not directly comparable. Treat LCOE as indicative.
- Not modelled: debt, tax, depreciation, generation-based incentives, land purchase instead of lease.
