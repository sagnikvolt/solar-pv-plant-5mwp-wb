# Verification log

Checked on 28 Oct 2026. Status key: **Verified** = matched to a manufacturer or official document, or recomputed from the repo's own outputs; **Assumption** = my stated choice, logged in `ASSUMPTIONS.md`; **Partly** = source found but with a stated limit; **Open** = not confirmed.

## External facts

| Item | Value used | Source / method | Status |
|---|---|---|---|
| Module STC values, Waaree ELITE BiN-08-565 | Voc 51.90 V, Vmp 43.56 V, Isc 13.75 A, Imp 12.97 A, efficiency 21.87% | Waaree datasheet (waaree.com, BiN-08 565-600 W), read 28 Oct 2026 | Verified |
| Module temperature coefficients and NOCT | Pmax -0.30 %/°C, Voc -0.26 %/°C, Isc +0.046 %/°C, NOCT 43 ± 2 °C | Same datasheet; the 575 W sibling page lists identical coefficients | Verified |
| Module size, cells, system voltage | 2278 × 1134 × 33 mm, 144 half cells, 1500 V | Same datasheet | Verified |
| Module ALMM List-I / DCR status of this exact model | Waaree is a large ALMM-approved maker (reported Dec 2025), but the model-level listing was not found | Press reports only; MNRE list not read | **Open** (check on the MNRE ALMM page) |
| Inverter SG250HX limits | Max DC 1500 V; MPPT 600 to 1500 V; 12 MPPTs; 2 connectors per MPPT; 26 A max input per MPPT (50 A short circuit); 250 kVA at 30 °C, 225 kVA at 40 °C; AC 800 V; 180.5 A; efficiency 99.0% | Sungrow datasheet copy hosted by solarics.de, read 28 Oct 2026 | Verified (third-party copy; confirm latest revision on sungrowpower.com) |
| Grid emission factor | 0.727 tCO2/MWh (weighted average), 0.757 (combined margin), FY 2023-24 | CEA CO2 Baseline Database as reported by SolarQuarter (Jan 2025); the page does not name the version | Partly (version label v20 taken from my earlier note) |
| Capex benchmark | CTUIL revised solar benchmark ₹3.5 crore/MW, land 3 acres/MW | indianinfrastructure.com, 7 Sep 2026; GreentechLead repeats the figure and cites SJVN 1 GW Bikaner at about ₹5.49 crore/MW | Partly (news reports, AC/DC basis not stated) |
| Tariff reference points | ₹2.34 (GUVNL, Mar 2026), ₹3.62 (DVC West Bengal interim, Mar 2025) | News headlines only | Partly (headline level) |
| Cost line ranges | taypro.in ranges | Commercial blog | Assumption (indicative, ±20%) |

## Internal consistency (recomputed)

| Check | Result |
|---|---|
| 8,840 modules × 565 W | 4,994.6 kWp ✓ |
| 340 strings × 26 modules | 8,840 ✓ (192 MPPT inputs: 44 × 1 + 148 × 2 = 340 strings ✓) |
| DC/AC | 4,994.6 / 4,000 = 1.249 ✓ |
| Specific yield | 7,078 / 4,994.6 = 1,417 kWh/kWp ✓ |
| Coldest-day string Voc | 26 × 54.81 V = 1,425 V < 1,500 V ✓ (Voc at 3.4 °C from the verified coefficient) |
| AC-side loss | 161.3 MWh = 2.28% of 7,078 ✓; net 7,078 − 161.3 = 6,916.7 MWh ✓ |
| P90 | σ = √(5.0² + 3.2² + 2.0² + 2.0² + 1.5² + 1.0² + 0.5²) = 6.84%; 7,078 × (1 − 1.2816 × 0.0684) = 6,458 ✓ |
| CO2, year 1 | 6,916.7 × 0.727 = 5,028 t ✓ (5,236 t with 0.757) |
| Capex vs benchmark | Base ₹4.42 crore/MWp lies between the CTUIL ₹3.5 and the SJVN ₹5.49 ✓ |
| Unit tests | `python -m unittest discover calcs/tests`: 4 tests pass |
| Docs vs outputs | README, report, LinkedIn draft and interview Q&A quote the same headline numbers as `calcs/output/` ✓ |

## Not verifiable here
- PVsyst's own simulation output was read from the saved reports, not independently re-run; the SAM/PVGIS cross-check (`calcs/output/crosscheck_sam_pvgis.md`) is the independent test (-4.6% / -6.6% as run).
- Datasheet PDFs are not saved in `data/datasheets/` (the workspace cannot download from those hosts). Download them from the links in `SOURCES.md`.
- Drawings are schematic and have not been reviewed by a practising engineer.
