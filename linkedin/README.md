# LinkedIn and CV text (drafts)

Edit into your own voice. Post only after the AutoCAD drawings are added and the repo is public (about 30 Nov). Do not claim anything marked "to verify".

## 1. Projects entry

**Title:** 5 MWp Ground-Mount Solar PV Plant: Design and Energy Yield Assessment (West Bengal)
**Dates:** Oct 2026 to Nov 2026
**Associated with:** IEM Kolkata
**Skills to tag:** PVsyst, Solar PV system design, Energy yield assessment, AutoCAD, Python, NREL SAM, Cable sizing

**Description:**
Designed a 5 MWp fixed-tilt, bifacial ground-mount solar plant using Kolkata's climate data, the way an EPC design team would prepare a preliminary package.
- Selected 565 Wp N-type TOPCon bifacial modules and 250 kW string inverters; sized strings against record temperatures (26 modules per string, 340 strings, DC/AC 1.25) with a Python tool and Excel version.
- Simulated in PVsyst with a 3D shading scene and a row-pitch sweep (6.4 to 9.0 m): 7,078 MWh/yr, 1,417 kWh/kWp, PR 85.6%; P90 6,458 MWh/yr from an assumed uncertainty budget.
- Cross-checked against NREL SAM and PVGIS; the 4.6% gap came from the irradiance database, and fell to +0.9% after scaling to the same irradiance.
- Sized DC and AC cables, transformers and the 33 kV connection concept; estimated about 5,000 t CO2 avoided per year.
- Everything is documented with an assumption log. Preliminary design: no site survey, indicative costs.

**Link:** github.com/sagnikvolt/solar-pv-plant-5mwp-wb (add once public)

## 2. Post draft

> I spent the last few weeks designing a 5 MWp solar plant from scratch, to learn what an EPC design team actually does.
>
> The setup: 8,840 bifacial modules, 16 string inverters, Kolkata's climate, fixed tilt 20°.
>
> Three things I learned:
> 1. Row spacing is a trade-off, not a number. Going from 6.4 m to 9.0 m pitch added about 2.6% energy but needed 39% more land. I picked 8.0 m.
> 2. Different weather databases disagree. Kolkata's yearly irradiation is 1,574 (Meteonorm), 1,669 (NASA POWER) or 1,730 (PVGIS) kWh/m². My SAM check was 4.6% above PVsyst until I scaled it to the same irradiance, then +0.9%. The model was fine; the data source wasn't.
> 3. String sizing is set by the coldest morning. At 3.4 °C a 27-module string came within 3 V of the 1,500 V limit, so I used 26.
>
> Result: 7,078 MWh/yr, PR 85.6%, P90 6,458 MWh/yr (assuming a 6.8% uncertainty). Layout and single-line diagram are next.
>
> Everything, including every assumption and where I'm unsure, is in the repo: [link]
>
> I'm looking for graduate engineer roles in solar (design, projects or O&M) in West Bengal. Feedback from anyone who does this for real is very welcome.
>
> #solar #pvsyst #renewableenergy #westbengal

Numbers behind the post: pitch sweep `calcs/output/pitch_sweep.md` (energy 6,938 to 7,121 MWh = +2.6%; footprint 3.20 to 4.45 ha = +39%). Image to attach: `showcase/images/row_pitch_tradeoff.png` or the loss diagram.

## 3. CV bullets

- Designed and simulated a 5 MWp bifacial solar plant (8,840 modules, 16 string inverters) in PVsyst with 3D shading; achieved 7,078 MWh/yr at PR 85.6% and cross-checked against NREL SAM and PVGIS (gap explained to +0.9%).
- Sized strings, DC/AC cables, transformers and 33 kV evacuation to IEC practice, built a Python/Excel string-sizing tool, and documented every assumption in a public GitHub repository.

## 4. Things to verify before posting
- Module ALMM/DCR status (MNRE site).
- Capex and LCOE are not in the post because the cost model is unreconciled.
- The repo is private until about 30 Nov; add the link only when public.
