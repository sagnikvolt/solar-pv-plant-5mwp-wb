# Assumptions Log

Every design input that isn't a direct measurement goes here. Each row needs a **source** and a **reason**. When a value changes, update it and note the change in the last column.

| # | Area | Assumption | Value | Source | Reason / note | Changed? |
|---|---|---|---|---|---|---|
| 1 | Plant | DC capacity | 5.0 MWp (design: 4,994.6 kWp) | Project scope | Typical single-feeder 33 kV ground-mount size; actual capacity is set by whole strings | |
| 2 | Plant | Target DC/AC ratio | 1.25 (actual 1.249) | Industry practice | Balance clipping vs. inverter cost; to be tested in PVsyst | |
| 3 | Site | Location | Kolkata, 22.57 °N, 88.36 °E, 15 m | Project choice | Resource site; exact plot TBD (see `data/site.md`) | 28 Oct: changed from Bankura to Kolkata |
| 4 | Site | Record minimum ambient | 3.4 °C | NASA POWER daily T2M_MIN, 2001–2025 | Sets maximum string Voc. Gridded value; a station may read slightly lower | |
| 5 | Site | Design maximum ambient | 47 °C | NASA POWER daily T2M_MAX (46.9 °C) rounded up | Sets minimum string Vmp (MPPT window) | |
| 6 | Irradiance | Annual GHI | Meteonorm 8.1 (1991–2012): **1,573.6**; NASA POWER: 1,669 (+6.1%); PVGIS-ERA5 (2005–2020): 1,730 (+10.0%) kWh/m² | PVsyst Meteonorm import; NASA POWER; PVGIS v5.3 | Spread far above the 3% threshold. Meteonorm is the lowest and the most conservative; it is the basis of the PVsyst simulation. Causes to investigate for the report: different averaging periods, satellite vs. interpolated ground data, and aerosol treatment. Year-to-year GHI variability (Meteonorm): 3.2% | |
| 7 | Module | Model and class | Waaree ELITE BiN-08-565 (565 W) | Waaree datasheet WEL/E&PD/565-600/144/BiN-08/HC/09/03.01.2025 (see `data/datasheets/SOURCES.md`) | N-type TOPCon, bifacial, 144 half-cut cells. **ALMM List-I and DCR status not yet verified** | 28 Oct: 580 W class rejected, see #14 |
| 8 | Module | STC values | Voc 51.9 V, Vmp 43.56 V, Isc 13.75 A, Imp 12.97 A | Same datasheet | | |
| 9 | Module | Temperature coefficients | β(Voc) −0.26 %/°C, α(Isc) +0.046 %/°C, γ(Pmax) −0.30 %/°C; NOCT 43 °C | Same datasheet | The datasheet gives no β(Vmp) | |
| 10 | Inverter | Model | Sungrow SG250HX | Sungrow datasheet v1.22 (© 2019; see SOURCES.md) | 1500 V string inverter, 12 MPPTs, 250 kVA at 30 °C. **Derates to 225 kVA at 40 °C and 200 kVA at 50 °C**: PVsyst must model this for Kolkata summers | |
| 11 | Inverter | Limits used | Vdc max 1500 V; MPPT 600–1500 V; 2 string inputs per MPPT; 26 A operating and 50 A Isc per MPPT | Same datasheet | Newer datasheet revisions may state a lower MPPT minimum voltage; 600 V is conservative | |
| 12 | Design | Cell temperature model | Tcell = Tamb + (NOCT − 20)/800 × 1000 | IEC 61215 NOCT convention | Used for hot-condition Vmp and Isc (75.8 °C) | |
| 13 | Design | Vmp temperature coefficient | γ(Pmax) = −0.30 %/°C used as β(Vmp) | Common approximation | PVsyst's model derives −0.33 %/°C, so −0.30 slightly overstates hot Vmp. No effect on the design: the minimum string is 17 modules and 26 are used | |
| 14 | Design | String length | 26 modules (maximum allowed is 27) | `calcs/output/` | At 27, string Voc reaches 1,497 V, only 3 V below the 1,500 V limit, so one module was dropped for a 5% margin. See `iteration1_580W_27mod_FAILED.md` | Iteration 2 |
| 15 | Design | Module class | 565 W instead of 580 W | `calcs/output/` | With the 580 W class, two strings on one MPPT draw 26.36 A, above the inverter's 26 A limit. The 565 W class gives 25.94 A | Iteration 2 |
| 16 | Design | Bifacial rear gain (current only) | 10% | Engineering assumption | Conservative input for current checks only; PVsyst computes the real gain | |
| 17 | Site | Albedo | TBD (PVsyst default until set in the bifacial settings) | PVsyst default / literature | Matters for bifacial gain | |
| 18 | Losses | Soiling | TBD | | | |
| 19 | PVsyst | Weather file | Kolkata_MN81_SYN.MET (Meteonorm 8.1, synthetic hourly) | PVsyst, 28 Oct 2026 | Coordinates picked from PVsyst's map: 22.563 °N, 88.363 °E, 11 m, UTC+5.5 | |
| 20 | PVsyst | Orientation | Fixed tilt 20°, azimuth 0° (south) | PVsyst quick optimisation | Transposition factor 1.06; 0.1% below the optimum (30° would be 0.6% below). Lower tilt also shortens row pitch | |
| 21 | PVsyst | Module file | Waaree_Energies_BiN-08-565.PAN, created by hand from the datasheet | Datasheet values (see #7–9) | Not in PVsyst's Waaree list (older WSMD models only). Created from the WSMD-545 template; Pmax temp. coefficient set to −0.30 %/°C and bifaciality 0.80. PVsyst's one-diode model derives Voc −0.25 %/°C and Vmp −0.33 %/°C (my hand calc used −0.30 for Vmp, so PVsyst is slightly more conservative on Vmp). Rsh/Rs are PVsyst defaults, not from the datasheet | |
| 22 | PVsyst | Inverter | Sungrow SG250-HX from PVsyst's database | PVsyst database (since 2022) | The database entry lists the MPPT range as 500–1450 V; datasheet v1.22 says 600–1500 V. Both are satisfied by the 26-module string (Vmp 960–1206 V) | |
| 23 | PVsyst | Array | 26 modules in series, 340 strings, 16 inverters (192 MPPT inputs) | `calcs/string_sizing.py` | PVsyst confirms 8,840 modules, 4,995 kWp, 4,000 kWac, ratio 1.249, Voc at −10 °C 1,465 V. 44 MPPT inputs get 1 string and 148 get 2 | |
