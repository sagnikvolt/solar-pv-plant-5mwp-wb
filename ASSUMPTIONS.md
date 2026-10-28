# Assumptions Log

Every design input that isn't a direct measurement goes here. Interviewers probe these, so each row needs a **source** and a **reason**. When a value changes, update it here and note the change in the last column.

| # | Area | Assumption | Value | Source | Reason / note | Changed? |
|---|---|---|---|---|---|---|
| 1 | Plant | DC capacity | 5.0 MWp | Project scope | Typical size for a single-feeder 33 kV ground-mount plant | |
| 2 | Plant | Target DC/AC ratio | 1.2–1.3 (TBD) | Industry practice, check in PVsyst | Balance inverter clipping vs. inverter cost | |
| 3 | Site | Location / coordinates | TBD | Google Earth | | |
| 4 | Site | Record minimum ambient temperature | TBD °C | IMD / NASA POWER | Sets the maximum string Voc (1500 V limit) | |
| 5 | Site | Design maximum ambient temperature | TBD °C | IMD / NASA POWER | Sets the minimum string Vmp (MPPT window) | |
| 6 | Site | Albedo | TBD | PVsyst default / literature | | |
| 7 | Losses | Soiling | TBD % | | | |
| 8 | Equipment | Module | TBD | ALMM List-I | | |
| 9 | Equipment | Inverter | TBD | | | |
| 10 | Design | Cell temperature model | Tcell = Tamb + (NOCT − 20)/800 × 1000 | IEC 61215 NOCT convention | Used for hot-condition Vmp and Isc | |
| 11 | Design | Vmp temperature coefficient | ≈ γ(Pmax) unless the datasheet gives β(Vmp) | Common approximation | Slightly conservative for the minimum string length | |
| 12 | Design | Cell temperature at record minimum ambient | = Tamb,min | Conservative | At dawn the cells are at ambient temperature, and Voc is highest | |
