# 5 MWp Solar PV Plant: Design & Energy Yield Assessment (West Bengal)

> **Status: in progress.** Target completion is 30 Nov 2026. This README fills in as each stage is finished. Any number below marked *TBD* has not been calculated yet.

A complete preliminary design package for a 5 MWp ground-mounted, fixed-tilt solar PV plant at a real site in West Bengal, India. It is laid out the way a solar EPC or developer design team would prepare one: site and resource assessment, equipment selection, string sizing, a PVsyst energy-yield simulation with P50/P90, independent cross-checks, electrical sizing, drawings and a basic financial model.

**Author:** Sagnik Kumar Nath, B.Tech Electrical Engineering, IEM Kolkata (2027)

---

## Key results

| Parameter | Value |
|---|---|
| Site (resource location) | Kolkata, 22.57 °N, 88.36 °E (exact plot TBD) |
| Land area | TBD |
| DC capacity / AC capacity | 4,994.6 kWp / 4,000 kW (nominal, derates in heat) |
| DC/AC ratio | 1.249 |
| Module | Waaree ELITE BiN-08-565, N-type TOPCon bifacial (ALMM/DCR status to be verified) |
| Inverter | 16 × Sungrow SG250HX (1500 V string inverter) |
| Modules per string / no. of strings | 26 / 340 (8,840 modules) |
| Tilt / azimuth / row pitch | TBD |
| Annual GHI | 1,730 (PVGIS) / 1,669 (NASA POWER) kWh/m²/yr; Meteonorm TBD |
| P50 energy yield | TBD MWh/yr |
| P90 energy yield (1-year) | TBD MWh/yr |
| Specific yield | TBD kWh/kWp/yr |
| Performance ratio (PR) | TBD % |
| Cross-check vs SAM / PVGIS | TBD % / TBD % |
| Capex / LCOE | TBD ₹ Cr / TBD ₹/kWh |
| CO₂ avoided | TBD t/yr |

---

## Approach

1. **Site and resource:** site selection and justification, plus irradiance from Meteonorm cross-checked against PVGIS and NASA POWER. → [`data/`](data/)
2. **Equipment selection:** an ALMM-listed module and an inverter, with reasoning on DCR/ALMM and string vs central inverters and the DC/AC ratio. → [`data/datasheets/`](data/datasheets/)
3. **Array and string design:** tilt, row pitch, and string sizing (Voc at record minimum temperature, Vmp within the MPPT window, current limits). → [`calcs/`](calcs/)
4. **Energy simulation:** PVsyst with a 3D near-shading scene, loss diagram, PR, and P50/P90. → [`pvsyst/`](pvsyst/)
5. **Cross-checks:** NREL SAM and PVGIS, with any difference above 3% explained.
6. **Electrical sizing:** DC and AC cables (voltage drop, ampacity, derating), DCDB/ACDB, inverter transformer, and the 33 kV evacuation concept.
7. **Drawings:** plant layout and single-line diagram (AutoCAD). → [`drawings/`](drawings/)
8. **BOQ and economics:** capex, LCOE, payback and CO₂ avoided.
9. **Report:** → [`report/`](report/)

Every design assumption, with its value, source and reason, is logged in **[ASSUMPTIONS.md](ASSUMPTIONS.md)**.

## Repository structure

```
data/          site info, weather data comparison, equipment datasheets
calcs/         string sizing (Python + Excel), later cable sizing & economics
pvsyst/        PVsyst project files, exported reports, screenshots
drawings/      layout and SLD (DWG + PDF)
report/        final PDF report, interview Q&A
ASSUMPTIONS.md assumption log (value, source, reason)
PLAN.md        4-week work plan and checklist
```

## Tools

PVsyst (IEM academic licence), NREL SAM, PVGIS, NASA POWER, AutoCAD (Autodesk Education), Python, Excel.

## Run the calculations

```bash
python calcs/fetch_weather.py --lat 22.57 --lon 88.36    # PVGIS + NASA POWER data
python calcs/weather_compare.py                          # irradiance cross-check
python calcs/string_sizing.py                            # uses calcs/config/design_inputs.json
python calcs/string_sizing.py --config calcs/config/example_inputs.json   # worked example
python -m unittest discover calcs/tests
```

No packages beyond the Python 3 standard library are required (the Excel version, `calcs/string_sizing.xlsx`, mirrors the script).

## Limitations

*To be written as the study progresses* (for example: a preliminary design without a topographic survey or soil data, generic grid assumptions, and an academic PVsyst licence).
