# Showcase assets (LinkedIn and portfolio)

Everything here is meant to be shown publicly. Items marked **PRELIMINARY** come from the baseline run (VC0) and must be replaced once shading and losses are done.

| Asset | File | Status |
|---|---|---|
| Irradiance source comparison (Meteonorm vs NASA POWER vs PVGIS) | `images/irradiance_comparison.png` | Final data |
| String design summary (Voc, Vmp and current checks) | `images/string_design_summary.png` | Final data |
| PVsyst loss diagram, VC0 baseline | `images/pvsyst_loss_diagram_VC0_baseline.png` | **PRELIMINARY.** No near shading, no soiling. Raw export clips the title and right-hand labels: redo for the final |
| PVsyst simulation report, VC0 baseline (6 pages) | `pvsyst_report_VC0_baseline_PRELIMINARY.pdf` | **PRELIMINARY**, superseded by VC1 |
| PVsyst loss diagram, VC1 (bifacial, shading, soiling) | `images/pvsyst_loss_diagram_VC1_bifacial_shaded.png` | **PRELIMINARY.** Raw export clips edges, and its title still says "Base case" (renamed afterwards): redo for the final |
| 3D shading scene, 17 rows, 8,840 modules | `images/pvsyst_3d_scene_VC1.jpg` | Working capture, low resolution (876×589) |
| PVsyst simulation report, VC1 (8 pages) | `pvsyst_report_VC1_bifacial_shaded_PRELIMINARY.pdf` | **PRELIMINARY**, superseded by VC4 |
| PVsyst loss diagram, VC4 (adopted 8.0 m pitch) | `images/pvsyst_loss_diagram_VC4_pitch8m.png` | **PRELIMINARY.** Raw export clips right-hand labels |
| PVsyst simulation report, VC4 (8 pages) | `pvsyst_report_VC4_pitch8m_PRELIMINARY.pdf` | **PRELIMINARY** (current design) |
| Row pitch trade-off chart | `images/row_pitch_tradeoff.png` | Final data, from the PVsyst sweep |

| Proof-of-work screenshots (PVsyst project window, results dashboard, 3D scene, AutoCAD layout) | `proof/*.png` | Real screenshots, 28 Oct 2026; account name blurred |
| Plant layout drawing | `../drawings/SPV5-DWG-01-Layout-R0.png` / `.pdf` | R0, schematic |
| Single-line diagram | `../drawings/SPV5-DWG-02-SLD-R0.png` / `.pdf` | R0, schematic |
| Loss steps chart (clean, VC4) | `images/loss_steps_VC4_clean.png` | Redrawn from the PVsyst report numbers; preliminary |
| Monthly energy and PR (VC4) | `images/monthly_energy_pr_VC4.png` | From the PVsyst report table; preliminary |
| Draft design report (8 pages) | `../report/5MWp_solar_design_report_DRAFT.pdf` | DRAFT, drawings to be added |
| LinkedIn entry, post, CV bullets | `../linkedin/README.md` | Drafts, post after drawings and repo public |

Regenerate the charts with `python calcs/make_showcase_charts.py`.

## Still to capture
- [x] Clean loss diagram (redrawn from report numbers: `images/loss_steps_VC4_clean.png`)
- [x] Monthly energy and PR (`images/monthly_energy_pr_VC4.png`; PVsyst's own dashboard screenshot not captured)
- [ ] System overview screenshot
- [ ] Final PVsyst report PDF with P50/P90
- [x] Plant layout and single-line diagram (PDF/PNG in `drawings/`)
- [ ] LinkedIn post cover image (loss diagram plus key numbers)

## Honest caveats to carry into any post
- The baseline PR of 85.2% is optimistic and will fall.
- Irradiance sources differ by up to 10%; Meteonorm, the lowest, is used.
- Module ALMM/DCR status is not yet verified.
- The PVsyst licence bar read "0 days remaining" on 28 Oct 2026.
