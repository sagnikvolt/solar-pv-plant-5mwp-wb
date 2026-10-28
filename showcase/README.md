# Showcase assets (LinkedIn and portfolio)

Everything here is meant to be shown publicly. Items marked **PRELIMINARY** come from the baseline run (VC0) and must be replaced once shading and losses are done.

| Asset | File | Status |
|---|---|---|
| Irradiance source comparison (Meteonorm vs NASA POWER vs PVGIS) | `images/irradiance_comparison.png` | Final data |
| String design summary (Voc, Vmp and current checks) | `images/string_design_summary.png` | Final data |
| PVsyst loss diagram, VC0 baseline | `images/pvsyst_loss_diagram_VC0_baseline.png` | **PRELIMINARY.** No near shading, no soiling. Raw export clips the title and right-hand labels: redo for the final |
| PVsyst simulation report, VC0 baseline (6 pages) | `pvsyst_report_VC0_baseline_PRELIMINARY.pdf` | **PRELIMINARY** |

Regenerate the two charts with `python calcs/make_showcase_charts.py`.

## Still to capture
- [ ] Final loss diagram after 3D shading, soiling and the loss review
- [ ] PVsyst results dashboard (monthly energy, PR)
- [ ] 3D near-shading scene screenshot
- [ ] System overview screenshot
- [ ] Final PVsyst report PDF with P50/P90
- [ ] Plant layout and single-line diagram (PDF/PNG from AutoCAD)
- [ ] SAM / PVGIS cross-check chart
- [ ] LinkedIn post cover image (loss diagram plus key numbers)

## Honest caveats to carry into any post
- The baseline PR of 85.2% is optimistic and will fall.
- Irradiance sources differ by up to 10%; Meteonorm, the lowest, is used.
- Module ALMM/DCR status is not yet verified.
- The PVsyst licence bar read "0 days remaining" on 28 Oct 2026.
