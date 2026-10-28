# PVsyst

PVsyst 7.4 workspace: `PVsyst7.0_Data/` in the project root (selected as the PVsyst *user workspace*), so the project files live in the repo.

| Item | File |
|---|---|
| Project | `PVsyst7.0_Data/Projects/SPV5_Kolkata_5MWp_Project.PRJ` |
| Variant VC0 | `PVsyst7.0_Data/Projects/SPV5_Kolkata_5MWp_Project.VC0` |
| Site (Meteonorm 8.1) | `PVsyst7.0_Data/Sites/Kolkata_MN81.SIT` |
| Weather | `PVsyst7.0_Data/Meteo/Kolkata_MN81_SYN.MET` |
| Custom module | `PVsyst7.0_Data/ComposPV/PVmodules/Waaree_Energies_BiN-08-565.PAN` |

## Notes
- The licence screen showed "LICENSED" but also "licence will expire soon, 0 days remaining" (28 Oct 2026). Check this before relying on PVsyst. Exported PDF reports may carry restrictions or a watermark.
- The Waaree list in PVsyst's database holds only older WSMD models, so the BiN-08-565 `.PAN` was created from the datasheet.
- No manufacturer-database problem for the inverter: SG250-HX is included.

## Simulation variants
| Variant | Change | Annual energy | Specific yield | PR | Notes |
|---|---|---|---|---|---|
| VC0 | Base: 20° tilt, no near shading, default losses, bifacial settings not yet defined | 7,041 MWh | 1,410 kWh/kWp | 0.852 | **Preliminary baseline.** Optimistic: no shading, soiling or measured losses, and bifacial gain not yet modelled |

## Next
- [ ] Bifacial system settings (albedo, pitch, height)
- [ ] Row pitch and 3D near-shading scene
- [ ] Soiling, LID, mismatch, ohmic and availability losses reviewed
- [ ] P50/P90
- [ ] Export report PDF and loss diagram
