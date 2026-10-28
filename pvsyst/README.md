# PVsyst

PVsyst 7.4 workspace: `PVsyst7.0_Data/` in the project root (selected as the PVsyst *user workspace*), so the project files live in the repo.

| Item | File |
|---|---|
| Project | `PVsyst7.0_Data/Projects/SPV5_Kolkata_5MWp_Project.PRJ` |
| Variant VC0 | `PVsyst7.0_Data/Projects/SPV5_Kolkata_5MWp_Project.VC0` |
| Variant VC1 | `PVsyst7.0_Data/Projects/SPV5_Kolkata_5MWp_Project.VC1` |
| Reports, loss diagrams, 3D scene picture | `../showcase/` |
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
| VC1 | Bifacial (albedo 0.25), 3D shed scene at 7.0 m pitch, linear near shading, free-standing thermal model, soiling 3%, LID 0.5%, unavailability 1% | 7,006 MWh | 1,403 kWh/kWp | 0.848 | Near shading -2.26%, soiling -3.0%, rear irradiance +6.5% of front. Unavailability placed randomly (3 periods, 3.7 days), so June looks low |

## Next
- [x] Bifacial system settings, 3D scene, loss review, report PDF and loss diagram (VC1)
- [ ] Pitch sweep (6.4 / 8 / 9 m) and a monofacial run to quantify bifacial gain
- [ ] Module-string (electrical) shading with table partitions
- [ ] Monthly soiling values; fix unavailability periods
- [ ] Multi-MPPT warning: 44 inputs carry 1 string and 148 carry 2 (PVsyst suggests disabling the multi-MPPT option)
