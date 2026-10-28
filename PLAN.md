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
- [x] Row pitch: sweep 6.4 / 7 / 8 / 9 m run, **8.0 m adopted** (`calcs/output/pitch_sweep.md`)
- [x] 3D near-shading scene (17 sheds, 8,840 modules) and bifacial model
- [x] Simulation run (VC1); loss diagram, PR and specific yield recorded
- [x] P50/P90 uncertainty budget set (`calcs/p50_p90.py`); **assumptions to review**
- [x] Cross-checked with SAM and PVGIS; gap above 3% explained by irradiance source (`calcs/output/crosscheck_sam_pvgis.md`)

## Week 3 (19–25 Nov): electrical, drawings, economics (SDP781 on 23 Nov)
- [x] DC string and DC main cable sizing (voltage drop, ampacity, derating)
- [x] AC cable, inverter transformer and 33 kV evacuation concept
- [ ] AutoCAD layout and SLD exported to PDF
- [x] BOQ, capex, LCOE, payback and CO₂ avoided (indicative; costs need a real benchmark)

## Week 4 (26–30 Nov): package and publish
- [x] 6–8 page PDF report in `report/` (draft; AutoCAD drawings to be added)
- [ ] README results table filled in; repo made public
- [ ] 15–20 interview questions: drafts written; rewrite in my own words (`report/interview_qa.md`)
- [x] LinkedIn Projects entry and one post drafted in `linkedin/` (post after drawings)
- [x] Two CV bullets drafted in `linkedin/`

End-sem exams: 1, 3, 8, 10 and 14 Dec.
