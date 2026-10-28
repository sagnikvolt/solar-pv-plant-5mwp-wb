# 5 MWp Solar PV Plant: Design & Energy Yield Assessment (West Bengal)

> **Status: in progress (about 85%).** Done: site, equipment, strings, PVsyst yield and P50/P90, cross-check, cable sizing, indicative economics, layout and single-line drawings, draft 8-page report. Still to do: plot and substation choice, a reconciled cost benchmark, my own rewrite of the interview answers. Target completion is 30 Nov 2026. Any number marked *TBD* has not been calculated yet.

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
| Tilt / azimuth / row pitch | 20° / 0° (south) / 8.0 m (GCR 58%), chosen from a 4-pitch sweep |
| Annual GHI | 1,574 (Meteonorm 8.1, used in PVsyst) / 1,669 (NASA POWER) / 1,730 (PVGIS) kWh/m²/yr |
| Energy, PVsyst VC4 (bifacial, 3D shading, losses; preliminary) | 7,078 MWh/yr |
| P50 energy yield | 7,078 MWh/yr (preliminary) |
| P90 energy yield (1-year) | 6,458 MWh/yr (assumed uncertainty budget) |
| Specific yield | 1,417 kWh/kWp/yr |
| Performance ratio | 85.6% (bifacial gain of about 4.4% offsets shading, soiling and availability) |
| Cross-check vs SAM / PVGIS | -4.6% / -6.6% as run; +0.9% vs SAM once scaled to Meteonorm irradiance (see `calcs/output/crosscheck_sam_pvgis.md`) |
| Energy at 33 kV point | 6,917 MWh/yr (after 2.28% AC-side losses, `calcs/output/cable_sizing.md`) |
| Capex / LCOE (indicative) | ₹3.5 to 4.4 crore/MWp, LCOE ₹3.5 to 4.3/kWh. Does not reconcile with auction tariffs; see `calcs/output/economics.md` |
| CO₂ avoided | about 5,030 t/yr (CEA average factor 0.727 t/MWh) |

---

## Approach

1. **Site and resource:** site selection and justification, plus irradiance from Meteonorm cross-checked against PVGIS and NASA POWER. → [`data/`](data/)
2. **Equipment selection:** an ALMM-listed module and an inverter, with reasoning on DCR/ALMM and string vs central inverters and the DC/AC ratio. → [`data/datasheets/`](data/datasheets/)
3. **Array and string design:** tilt, row pitch, and string sizing (Voc at record minimum temperature, Vmp within the MPPT window, current limits). → [`calcs/`](calcs/)
4. **Energy simulation:** PVsyst with a 3D near-shading scene, loss diagram, PR, and P50/P90. → [`pvsyst/`](pvsyst/)
5. **Cross-checks:** NREL SAM and PVGIS, with any difference above 3% explained.
6. **Electrical sizing:** DC and AC cables (voltage drop, ampacity, derating), DCDB/ACDB, inverter transformer, and the 33 kV evacuation concept.
7. **Drawings:** plant layout and single-line diagram, generated in Python and saved as DWG in AutoCAD. → [`drawings/`](drawings/)
8. **BOQ and economics:** capex, LCOE, payback and CO₂ avoided.
9. **Report:** → [`report/`](report/)

Every design assumption, with its value, source and reason, is logged in **[ASSUMPTIONS.md](ASSUMPTIONS.md)**.

## Repository structure

```
data/          site info, weather data comparison, equipment datasheets
calcs/         string sizing (Python + Excel), later cable sizing & economics
pvsyst/        PVsyst project files, exported reports, screenshots
drawings/      layout and single-line diagram (DWG, DXF, PDF, PNG)
report/        draft PDF report (report.html is its source), interview Q&A drafts
linkedin/      LinkedIn Projects entry, post draft, CV bullets
showcase/      images and PDFs meant for public posting
ASSUMPTIONS.md assumption log (value, source, reason)
PLAN.md        4-week work plan and checklist
```

## Tools

PVsyst (IEM academic licence), NREL SAM, PVGIS, NASA POWER, Python (including `ezdxf` for drawings), AutoCAD 2027 (Autodesk Education licence, used to open and save the DWG files), Excel.

## Run the calculations

```bash
python calcs/fetch_weather.py --lat 22.57 --lon 88.36    # PVGIS + NASA POWER data
python calcs/weather_compare.py                          # irradiance cross-check
python calcs/string_sizing.py                            # uses calcs/config/design_inputs.json
python calcs/string_sizing.py --config calcs/config/example_inputs.json   # worked example
python calcs/cable_sizing.py                            # cable sizing and AC-side losses
python calcs/economics.py                               # BOQ scope, capex, LCOE, CO2 (needs cable_sizing first)
python calcs/make_drawings.py                           # layout and SLD (needs ezdxf, matplotlib)
python calcs/make_report.py                             # report/report.html to PDF (needs Playwright)
python -m unittest discover calcs/tests
```

The string sizing needs only the Python 3 standard library; the cross-check scripts need PySAM and requests, and the report build needs Playwright (the Excel version, `calcs/string_sizing.xlsx`, mirrors the script).

## Limitations

- Preliminary design: no topographic survey, soil or flood data, and no DISCOM feasibility. The plot, land area and 33 kV substation are not fixed.
- P50/P90 uses an assumed uncertainty budget, not measured values.
- Costs are indicative and do not reconcile with market tariffs; quote them only as a range.
- Module-string shading and monthly soiling are not modelled; PVsyst warns about unequal MPPT string counts.
- Module ALMM/DCR status is unverified.
- PVsyst is used under an academic licence.
- Drawings are schematic (symbols enlarged, yard and 33 kV route are placeholders) and not checked by a practising engineer.
