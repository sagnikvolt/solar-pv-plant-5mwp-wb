# Cross-check: PVsyst vs NREL SAM vs PVGIS (monofacial, preliminary)

| Tool | Irradiance data | GHI (kWh/m2) | Energy, no shading (MWh) | Shading-adjusted (MWh) | PVsyst VC2 vs tool |
|---|---|---|---|---|---|
| NREL SAM PVWatts v8 | ERA5 | 1664 | 7196 | 7033 | -4.6% |
| PVGIS PVcalc | ERA5 | 1730 | 7355 | 7188 | -6.6% |
| SAM scaled to Meteonorm GHI | scaled | 1574 | 6805 | 6651 | +0.9% |

PVsyst VC2 (monofacial, 7.0 m pitch) = 6712 MWh. SAM and PVGIS use a flat 10% system loss (soiling 3, mismatch 2, ohmic 0.9, LID 0.5, inverter ~2.7, availability 1) and no shading; the PVsyst near-shading loss (2.26%) is deducted from them for a like-for-like comparison.

Unscaled, the gap is more than 3% (-4.6% to -6.6%). Most of it is the irradiance database: the ERA5 TMY has 1664 kWh/m2 GHI against Meteonorm's 1574 (+5.7%), and PVGIS's multi-year ERA5 figure is higher still. Scaling SAM to the Meteonorm GHI brings it within 0.9% of PVsyst.

Limits: SAM and PVGIS share the ERA5 irradiance, so they are not independent of each other. This check validates the model chain, not the choice of irradiance source. PVWatts is a simpler model than PVsyst (no module-level bifacial, one loss factor).
