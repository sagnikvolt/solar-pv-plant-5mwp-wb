# Assumptions Log

Every design input that isn't a direct measurement goes here. Each row needs a **source** and a **reason**. When a value changes, update it and note the change in the last column.

| # | Area | Assumption | Value | Source | Reason / note | Changed? |
|---|---|---|---|---|---|---|
| 1 | Plant | DC capacity | 5.0 MWp (design: 4,994.6 kWp) | Project scope | Typical single-feeder 33 kV ground-mount size; actual capacity is set by whole strings | |
| 2 | Plant | Target DC/AC ratio | 1.25 (actual 1.249) | Industry practice | Balance clipping vs. inverter cost; to be tested in PVsyst | |
| 3 | Site | Location | Kolkata, 22.57 °N, 88.36 °E, 15 m | Project choice | Resource site; exact plot TBD (see `data/site.md`) | 28 Oct: changed from Bankura to Kolkata |
| 4 | Site | Record minimum ambient | 3.4 °C | NASA POWER daily T2M_MIN, 2001–2025 | Sets maximum string Voc. Gridded value; a station may read slightly lower | |
| 5 | Site | Design maximum ambient | 47 °C | NASA POWER daily T2M_MAX (46.9 °C) rounded up | Sets minimum string Vmp (MPPT window) | |
| 6 | Irradiance | Annual GHI | 1,730 kWh/m² (PVGIS) / 1,669 (NASA) | PVGIS v5.3 ERA5 2005–2020; NASA POWER | NASA is 3.5% lower, above the 3% review threshold; to be discussed in the report. Meteonorm to be added from PVsyst | |
| 7 | Module | Model and class | Waaree ELITE BiN-08-565 (565 W) | Waaree datasheet WEL/E&PD/565-600/144/BiN-08/HC/09/03.01.2025 (see `data/datasheets/SOURCES.md`) | N-type TOPCon, bifacial, 144 half-cut cells. **ALMM List-I and DCR status not yet verified** | 28 Oct: 580 W class rejected, see #14 |
| 8 | Module | STC values | Voc 51.9 V, Vmp 43.56 V, Isc 13.75 A, Imp 12.97 A | Same datasheet | | |
| 9 | Module | Temperature coefficients | β(Voc) −0.26 %/°C, α(Isc) +0.046 %/°C, γ(Pmax) −0.30 %/°C; NOCT 43 °C | Same datasheet | The datasheet gives no β(Vmp) | |
| 10 | Inverter | Model | Sungrow SG250HX | Sungrow datasheet v1.22 (© 2019; see SOURCES.md) | 1500 V string inverter, 12 MPPTs, 250 kVA at 30 °C. **Derates to 225 kVA at 40 °C and 200 kVA at 50 °C**: PVsyst must model this for Kolkata summers | |
| 11 | Inverter | Limits used | Vdc max 1500 V; MPPT 600–1500 V; 2 string inputs per MPPT; 26 A operating and 50 A Isc per MPPT | Same datasheet | Newer datasheet revisions may state a lower MPPT minimum voltage; 600 V is conservative | |
| 12 | Design | Cell temperature model | Tcell = Tamb + (NOCT − 20)/800 × 1000 | IEC 61215 NOCT convention | Used for hot-condition Vmp and Isc (75.8 °C) | |
| 13 | Design | Vmp temperature coefficient | γ(Pmax) = −0.30 %/°C used as β(Vmp) | Common approximation | Slightly conservative for the minimum string length | |
| 14 | Design | String length | 26 modules (maximum allowed is 27) | `calcs/output/` | At 27, string Voc reaches 1,497 V, only 3 V below the 1,500 V limit, so one module was dropped for a 5% margin. See `iteration1_580W_27mod_FAILED.md` | Iteration 2 |
| 15 | Design | Module class | 565 W instead of 580 W | `calcs/output/` | With the 580 W class, two strings on one MPPT draw 26.36 A, above the inverter's 26 A limit. The 565 W class gives 25.94 A | Iteration 2 |
| 16 | Design | Bifacial rear gain (current only) | 10% | Engineering assumption | Conservative input for current checks only; PVsyst computes the real gain | |
| 17 | Site | Albedo | TBD | PVsyst default / literature | | |
| 18 | Losses | Soiling | TBD | | | |
