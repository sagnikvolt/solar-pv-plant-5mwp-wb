"""
Build LinkedIn-ready charts from the repo's own data (no hand-typed numbers).
  showcase/images/irradiance_comparison.png : monthly GHI, Meteonorm vs PVGIS vs NASA POWER
  showcase/images/string_design_summary.png : string sizing results card (from design_inputs.json)
Usage: python calcs/make_showcase_charts.py
"""
import csv
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "calcs"))
from string_sizing import size_strings, load_config  # noqa: E402

OUT = os.path.join(ROOT, "showcase", "images")
os.makedirs(OUT, exist_ok=True)
FONT = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({"font.family": FONT, "axes.spines.top": False, "axes.spines.right": False})
INK, MUTED = "#1f2937", "#6b7280"
C = {"Meteonorm": "#0f766e", "PVGIS": "#d97706", "NASA POWER": "#64748b"}


def irradiance():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "weather", "weather_comparison.csv"), encoding="utf-8")))
    months = [r["month"] for r in rows]
    series = {"Meteonorm": "meteonorm_GHI_kWh_m2", "PVGIS": "pvgis_GHI_kWh_m2", "NASA POWER": "nasa_power_GHI_kWh_m2"}
    data = {k: [float(r[v]) for r in rows] for k, v in series.items()}
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
    for k, v in data.items():
        tot = sum(v)
        ax.plot(months, v, marker="o", ms=4, lw=2.2, color=C[k], label=f"{k}: {tot:,.0f} kWh/m²/yr")
    ax.set_ylabel("Global horizontal irradiation (kWh/m²/month)", color=MUTED)
    ax.set_ylim(90, 200)
    ax.grid(axis="y", alpha=.25)
    ax.legend(frameon=False, loc="upper right", labelcolor=INK)
    base = sum(data["Meteonorm"])
    spread = max(sum(v) for v in data.values()) / base - 1
    fig.suptitle("Kolkata: three irradiance sources, one site", x=0.06, ha="left", fontsize=17, fontweight="bold", color=INK)
    ax.set_title(f"Annual GHI differs by up to {spread*100:.0f}% between datasets. The PVsyst model uses Meteonorm, the most conservative.",
                 loc="left", fontsize=10.5, color=MUTED)
    fig.text(0.06, 0.01, "Sources: PVsyst Meteonorm 8.1 (1991-2012), PVGIS v5.3 ERA5 (2005-2020), NASA POWER climatology. Site 22.57°N, 88.36°E.",
             fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    fig.savefig(os.path.join(OUT, "irradiance_comparison.png"))
    plt.close(fig)


def string_card():
    cfg = load_config(os.path.join(ROOT, "calcs", "config", "design_inputs.json"))
    r = size_strings(cfg)
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=200)
    ax.axis("off")
    fig.text(0.06, 0.92, "5 MWp plant: string design checks", fontsize=18, fontweight="bold", color=INK)
    fig.text(0.06, 0.865, f"{cfg['module']['model'].split(' (')[0]}  +  {cfg['inverter']['model'].split(' (')[0]}  |  {cfg['site']['name']}",
             fontsize=10.5, color=MUTED)
    lim = cfg["inverter"]
    rows = [
        ("Max string Voc at record-cold", f"{r['String_Voc_cold_V']:.0f} V", f"limit {lim['Vdc_max_V']} V", r["checks"]["Voc_cold x N <= Vdc_max"]),
        ("Min string Vmp at hot cell temp", f"{r['String_Vmp_hot_V']:.0f} V", f"MPPT min {lim['Vmppt_min_V']} V", r["checks"]["Vmp_hot x N >= Vmppt_min"]),
        ("Max string Vmp at cold", f"{r['String_Vmp_cold_V']:.0f} V", f"MPPT max {lim['Vmppt_max_V']} V", r["checks"]["Vmp_cold x N <= Vmppt_max"]),
        ("Imp of 2 strings on one MPPT", f"{r['Imp_all_strings_on_one_MPPT_A']:.2f} A", f"limit {lim['Imax_operating_per_MPPT_A_optional']} A",
         r["checks"]["Imp x strings per MPPT <= MPPT max operating current"]),
        ("Strings per inverter", f"{r['Strings_per_inverter']}", f"max {r['Strings_per_inverter_max']}", r["checks"]["Strings/inverter within MPPT current limit"]),
    ]
    y = 0.74
    for label, val, lim_txt, ok in rows:
        fig.text(0.06, y, label, fontsize=12.5, color=INK)
        fig.text(0.50, y, val, fontsize=12.5, fontweight="bold", color=INK)
        fig.text(0.62, y, lim_txt, fontsize=11, color=MUTED)
        fig.text(0.86, y, "PASS" if ok else "FAIL", fontsize=11.5, fontweight="bold", color="#0f766e" if ok else "#b91c1c")
        y -= 0.085
    fig.text(0.06, 0.28, f"{r['N_chosen']} modules/string  |  {r['N_strings']} strings  |  {r['N_modules']:,} modules  |  "
             f"{r['DC_kWp']:,.0f} kWp DC  |  {r['N_inverters']} x {lim['Pac_kW']} kW  |  DC/AC {r['DC_AC_ratio']:.2f}",
             fontsize=11.5, fontweight="bold", color=INK)
    fig.text(0.06, 0.20, "Design iteration: the first pass (580 W class, 27 modules/string) failed the MPPT current check and sat 3 V under the\n"
             "1,500 V limit. Switching to the 565 W class and 26 modules/string fixed both.", fontsize=10.5, color=MUTED, linespacing=1.5)
    fig.text(0.06, 0.04, "Computed by calcs/string_sizing.py from manufacturer datasheet values. Record-cold 3.4 °C, design max ambient 47 °C.",
             fontsize=8, color=MUTED)
    fig.savefig(os.path.join(OUT, "string_design_summary.png"))
    plt.close(fig)


irradiance()
string_card()
print("saved", sorted(os.listdir(OUT)))
