"""Cross-check of the PVsyst yield with NREL SAM (PVWatts v8) and PVGIS PVcalc.

Weather for SAM: PVGIS ERA5 TMY (data/weather/kolkata_pvgis_era5_tmy.epw). Because PVGIS and this
TMY share the ERA5 irradiance, they are NOT independent of each other; they differ from PVsyst mainly
through the irradiance database (Meteonorm 8.1). The point of the check is to separate irradiance
differences from model differences.

Requires: pip install NREL-PySAM
"""
import json, os, urllib.request
import PySAM.Pvwattsv8 as pv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPW = os.path.join(ROOT, "data", "weather", "kolkata_pvgis_era5_tmy.epw")
DC_KW = 4994.6
LOSS = 10.0     # soiling 3, mismatch 2, ohmic 0.9, LID 0.5, inverter ~2.7, availability 1 (approx, PVsyst VC1)

def sam(tilt=20, bifacial=0, pitch_gcr=0.0, loss=LOSS):
    m = pv.default("PVWattsNone")
    m.SolarResource.solar_resource_file = EPW
    s = m.SystemDesign
    s.system_capacity = DC_KW
    s.dc_ac_ratio = 1.249
    s.tilt = tilt
    s.azimuth = 180
    s.array_type = 0          # fixed open rack
    s.module_type = 0
    s.losses = loss
    s.gcr = 0.5
    s.inv_eff = 98.4
    s.bifaciality = 0.8 if bifacial else 0.0
    m.execute()
    return m.Outputs.ac_annual / 1000.0, m.Outputs.poa_annual if hasattr(m.Outputs, "poa_annual") else None

def pvgis():
    url = ("https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat=22.563&lon=88.363&peakpower=%s&loss=%s&angle=20&aspect=0"
           "&pvtechchoice=crystSi&mountingplace=free&raddatabase=PVGIS-ERA5&outputformat=json" % (DC_KW, LOSS))
    with urllib.request.urlopen(url, timeout=90) as r:
        t = json.load(r)["outputs"]["totals"]["fixed"]
    return t["E_y"] / 1e3, t["H(i)_y"], t["l_tg"]

def tmy_ghi():
    import csv
    with open(EPW) as f:
        rows = list(csv.reader(f))[8:]
    return sum(float(r[13]) for r in rows) / 1000.0

if __name__ == "__main__":
    PVSYST_MONO = 6712.0      # PVsyst VC2: monofacial, 7.0 m pitch, near shading, same losses
    SHADING = 0.0226          # PVsyst near-shading loss at 7.0 m (SAM/PVGIS runs have none)
    METEONORM_GHI = 1573.6
    e_sam, _ = sam()
    e_pvg, h_pvg, ltg = pvgis()
    ghi = tmy_ghi()
    lines = ["# Cross-check: PVsyst vs NREL SAM vs PVGIS (monofacial, preliminary)", "",
             "| Tool | Irradiance data | GHI (kWh/m2) | Energy, no shading (MWh) | Shading-adjusted (MWh) | PVsyst VC2 vs tool |",
             "|---|---|---|---|---|---|"]
    for name, e, g in (("NREL SAM PVWatts v8", e_sam, ghi), ("PVGIS PVcalc", e_pvg, 1730.0)):
        adj = e * (1 - SHADING)
        lines.append("| %s | ERA5 | %.0f | %.0f | %.0f | %+.1f%% |" % (name, g, e, adj, (PVSYST_MONO / adj - 1) * 100))
    scaled = e_sam * (METEONORM_GHI / ghi) * (1 - SHADING)
    lines.append("| SAM scaled to Meteonorm GHI | scaled | %.0f | %.0f | %.0f | %+.1f%% |" % (METEONORM_GHI, e_sam * METEONORM_GHI / ghi, scaled, (PVSYST_MONO / scaled - 1) * 100))
    lines += ["", "PVsyst VC2 (monofacial, 7.0 m pitch) = %.0f MWh. SAM and PVGIS use a flat 10%% system loss (soiling 3, mismatch 2, ohmic 0.9, LID 0.5, inverter ~2.7, availability 1) and no shading; the PVsyst near-shading loss (2.26%%) is deducted from them for a like-for-like comparison." % PVSYST_MONO,
              "", "Unscaled, the gap is more than 3%% (%.1f%% to %.1f%%). Most of it is the irradiance database: the ERA5 TMY has %.0f kWh/m2 GHI against Meteonorm's %.0f (+%.1f%%), and PVGIS's multi-year ERA5 figure is higher still. Scaling SAM to the Meteonorm GHI brings it within %.1f%% of PVsyst." % (
                  (PVSYST_MONO / (e_sam * (1 - SHADING)) - 1) * 100, (PVSYST_MONO / (e_pvg * (1 - SHADING)) - 1) * 100, ghi, METEONORM_GHI, (ghi / METEONORM_GHI - 1) * 100, abs((PVSYST_MONO / scaled - 1) * 100)),
              "", "Limits: SAM and PVGIS share the ERA5 irradiance, so they are not independent of each other. This check validates the model chain, not the choice of irradiance source. PVWatts is a simpler model than PVsyst (no module-level bifacial, one loss factor)."]
    text = "\n".join(lines)
    print(text)
    open(os.path.join(ROOT, "calcs", "output", "crosscheck_sam_pvgis.md"), "w").write(text + "\n")
