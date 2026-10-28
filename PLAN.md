# Work Plan: Project 1 (deadline 30 Nov 2026)

Time budget: about 1–1.5 h on most evenings. Daily aptitude practice and exam preparation come first.

## Before 2 Nov
- [ ] **PVsyst licence check:** licence type and version, whether the manufacturer database has Indian modules (Waaree, Vikram, Websol, Adani, Premier) and 1500 V inverters, and whether the test-report PDF carries a watermark. Save screenshots to `pvsyst/screenshots/`.
- [ ] **Choose the site:** western WB (Purulia, Bankura or Paschim Medinipur) or South 24 Parganas near Falta. The site must be non-agricultural, about 20–25 acres, and near a 33 kV substation. Record the coordinates in `data/site.md`.

Term-II exams: 2–4 Nov (no project work).

## Week 1 (5–11 Nov): site, weather, equipment, string sizing
- [ ] Monthly GHI and temperature from Meteonorm, PVGIS and NASA POWER, entered in `data/weather/weather_comparison.csv`
- [ ] Record minimum and design maximum temperatures added to ASSUMPTIONS.md
- [ ] Module chosen (ALMM List-I check, datasheet in `data/datasheets/`)
- [ ] Inverter chosen, with a justification paragraph (string vs central, DC/AC ratio)
- [ ] `calcs/config/design_inputs.json` filled in and `python calcs/string_sizing.py` run
- [ ] Results cross-checked in `calcs/string_sizing.xlsx`

## Week 2 (12–18 Nov): PVsyst
- [ ] Project, orientation and system set up in PVsyst
- [ ] Row pitch and ground cover ratio chosen (shading vs land trade-off)
- [ ] 3D near-shading scene
- [ ] Simulation run; loss diagram, PR and specific yield recorded
- [ ] P50/P90 uncertainties set (weather year-to-year variability, model, module, etc.)
- [ ] Cross-checked with SAM and PVGIS, and any difference above 3% explained

## Week 3 (19–25 Nov): electrical, drawings, economics (SDP781 on 23 Nov)
- [ ] DC string and DC main cable sizing (voltage drop, ampacity, derating)
- [ ] AC cable, inverter transformer and 33 kV evacuation concept
- [ ] AutoCAD layout and SLD exported to PDF
- [ ] BOQ, capex, LCOE, payback and CO₂ avoided

## Week 4 (26–30 Nov): package and publish
- [ ] 6–8 page PDF report in `report/`
- [ ] README results table filled in; repo made public
- [ ] 15–20 interview questions answered in my own words (`report/interview_qa.md`)
- [ ] LinkedIn Projects entry and one post (loss diagram plus key numbers)
- [ ] Two CV bullets

End-sem exams: 1, 3, 8, 10 and 14 Dec.
