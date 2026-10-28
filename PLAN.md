# Work Plan: Project 1 (deadline 30 Nov 2026)

Time budget: about 1–1.5 h on most evenings. Daily aptitude practice and exam preparation come first.

## Before 2 Nov
- [x] ~~PVsyst licence check~~ skipped by decision (28 Oct); note any watermark when the first report is produced
- [x] **Site chosen: Kolkata** (22.57 N, 88.36 E). Still open: exact plot and 33 kV substation (see `data/site.md`)

Term-II exams: 2–4 Nov (no project work).

## Week 1 (5–11 Nov): site, weather, equipment, string sizing
- [x] PVGIS and NASA POWER monthly GHI and temperature done (Meteonorm to come from PVsyst), entered in `data/weather/weather_comparison.csv`
- [x] Record minimum and design maximum temperatures added to ASSUMPTIONS.md
- [x] Module chosen: Waaree BiN-08-565. **Still to do: ALMM List-I check and save the PDF in `data/datasheets/`**
- [x] Inverter chosen: Sungrow SG250HX. **Still to do: write your justification paragraph (string vs central, DC/AC ratio)**
- [x] `calcs/config/design_inputs.json` filled in and string sizing run (all checks pass)
- [x] Results cross-checked in `calcs/string_sizing.xlsx` (Excel and Python agree)

## Week 2 (12–18 Nov): PVsyst
- [x] Project, orientation and system set up in PVsyst (done 28 Oct; VC0 baseline run)
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
