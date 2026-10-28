"""
Build LinkedIn-ready charts from the repo's own data (no hand-typed numbers).
  showcase/images/irradiance_comparison.png : monthly GHI, Meteonorm vs PVGIS vs NASA POWER
  showcase/images/string_design_summary.png : string sizing results card (from design_inputs.json)
  showcase/images/row_pitch_tradeoff.png    : energy vs land for 4 row pitches (from calcs/output/pitch_sweep.md)
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


def pitch_chart():
    rows = []
    for line in open(os.path.join(ROOT, "calcs", "output", "pitch_sweep.md"), encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        try:
            rows.append((float(c[0]), float(c[3]), float(c[6])))
        except (ValueError, IndexError):
            continue
    pitch = [r[0] for r in rows]
    en = [r[1] for r in rows]
    ha = [r[2] for r in rows]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10, 5.6), dpi=200, gridspec_kw={"width_ratios": [1.25, 1]})
    labels = [f"{p:.1f} m" for p in pitch]
    cols = ["#0f766e" if p == 8.0 else "#94a3b8" for p in pitch]
    bars = ax.bar(labels, en, color=cols, width=0.6)
    ax.set_ylim(6700, 7200)
    ax.set_ylabel("Annual energy (MWh), axis starts at 6,700", color=MUTED)
    for b_, e in zip(bars, en):
        ax.text(b_.get_x() + b_.get_width() / 2, e + 6, f"{e:,.0f}", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_xlabel("Row pitch", color=MUTED)
    cols2 = ["#b45309" if p == 8.0 else "#fcd9a8" for p in pitch]
    bars2 = ax2.bar(labels, ha, color=cols2, width=0.6)
    ax2.set_ylim(0, 5)
    ax2.set_ylabel("Array footprint (ha)", color=MUTED)
    ax2.set_xlabel("Row pitch", color=MUTED)
    for b_, h in zip(bars2, ha):
        ax2.text(b_.get_x() + b_.get_width() / 2, h + 0.07, f"{h:.2f}", ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.grid(axis="y", alpha=.2)
    ax2.grid(axis="y", alpha=.2)
    fig.suptitle("Row pitch: more energy, but more land", x=0.06, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.06, 0.885, "Bifacial 20° fixed tilt, Kolkata. Gains flatten above 8 m, so 8.0 m (highlighted) is adopted.", fontsize=10.5, color=MUTED)
    fig.text(0.06, 0.01, "PVsyst 7.4 simulations VC3, VC1, VC4, VC5. Footprint excludes roads, fencing and substation. Preliminary.", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.87))
    fig.savefig(os.path.join(OUT, "row_pitch_tradeoff.png"))
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
pitch_chart()
print("saved", sorted(os.listdir(OUT)))

# ---- PVsyst VC4 numbers, copied from showcase/pvsyst_report_VC4_pitch8m_PRELIMINARY.pdf (page 5 and 7)
VC4_MONTHLY = [  # month, E_Grid kWh, PR
    ("Jan", 602898, .893), ("Feb", 584978, .876), ("Mar", 712927, .853), ("Apr", 709930, .847),
    ("May", 695431, .852), ("Jun", 491910, .785), ("Jul", 521809, .865), ("Aug", 524042, .857),
    ("Sep", 524913, .856), ("Oct", 571700, .861), ("Nov", 582257, .874), ("Dec", 555258, .860)]
VC4_LOSSES = [  # step, % (applied in sequence to the array nominal energy 8,179,891 kWh)
    ("Irradiance level", .77), ("Temperature", 5.59), ("LID", .50), ("Mismatch (modules, strings)", 2.05),
    ("Mismatch (rear side)", .55), ("DC wiring", .93), ("Inverter efficiency", 1.61),
    ("Inverter clipping (over nominal power)", 1.22), ("Unavailability", 1.01)]

def loss_waterfall():
    e = 8179.891
    start = e
    steps = []
    for name, pct in VC4_LOSSES:
        loss = e * pct / 100
        steps.append((name, pct, e - loss, loss))
        e -= loss
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=200)
    names = ["Array nominal energy (at STC)"] + [s[0] for s in steps] + ["Energy injected into grid"]
    y = list(range(len(names)))[::-1]
    ax.barh(y[0], start, color="#94a3b8", height=0.62)
    ax.text(start + 20, y[0], f"{start:,.0f} MWh", va="center", fontsize=10.5, fontweight="bold", color=INK)
    for yi, (name, pct, left, loss) in zip(y[1:-1], steps):
        ax.barh(yi, loss, left=left, color="#b45309", height=0.62)
        ax.text(start + 20, yi, f"-{loss:,.0f} MWh  ({pct:.2f}%)", va="center", fontsize=10, color=INK)
    ax.barh(y[-1], 7078.053, color="#0f766e", height=0.62)
    ax.text(7078.053 + 20, y[-1], "7,078 MWh", va="center", fontsize=10.5, fontweight="bold", color=INK)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=10, color=INK)
    ax.set_xlim(6800, 8900); ax.set_xlabel("Annual energy (MWh), axis starts at 6,800", color=MUTED)
    ax.grid(axis="x", alpha=.2)
    fig.suptitle("Where the energy goes: PVsyst VC4 loss steps", x=0.04, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.04, 0.9, "Bifacial 20° fixed tilt, 8.0 m pitch, Kolkata. Optical steps (shading, soiling, bifacial gain) are already inside the array nominal energy.", fontsize=9.5, color=MUTED)
    fig.text(0.04, 0.012, "Step sizes are my arithmetic from PVsyst's percentages (rounding within about 1 MWh). Preliminary; AC-side losses (about 2.3%) are not in PVsyst.", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.89))
    fig.savefig(os.path.join(OUT, "loss_steps_VC4_clean.png"))

def monthly_chart():
    m = [r[0] for r in VC4_MONTHLY]; en = [r[1] / 1000 for r in VC4_MONTHLY]; pr = [r[2] for r in VC4_MONTHLY]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.5, 5), dpi=200, gridspec_kw={"width_ratios": [1.35, 1]})
    cols = ["#99c9c4" if x == "Jun" else "#0f766e" for x in m]
    bars = ax.bar(m, en, color=cols, width=0.65)
    for b_, v in zip(bars, en):
        ax.text(b_.get_x() + b_.get_width() / 2, v + 8, f"{v:,.0f}", ha="center", fontsize=8.5, color=INK)
    ax.set_ylim(0, 800); ax.set_ylabel("Energy injected into grid (MWh)", color=MUTED); ax.grid(axis="y", alpha=.2)
    ax.set_title("Monthly energy", loc="left", fontsize=12, fontweight="bold", color=INK)
    ax2.plot(m, pr, color="#b45309", marker="o", markersize=6, linewidth=2)
    ax2.set_ylim(0.75, 0.92); ax2.set_ylabel("Performance ratio, axis starts at 0.75", color=MUTED); ax2.grid(axis="y", alpha=.2)
    ax2.set_title("Monthly performance ratio", loc="left", fontsize=12, fontweight="bold", color=INK)
    ax2.annotate("June: random 3.7-day\nunavailability period", xy=(5, pr[5]), xytext=(5.6, 0.775), fontsize=8.5, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=MUTED))
    plt.setp(ax2.get_xticklabels(), fontsize=8.5)
    fig.suptitle("Plant output by month: 7,078 MWh/yr, PR 85.6%", x=0.04, ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.04, 0.012, "PVsyst 7.4 VC4 (bifacial, 8.0 m pitch), Meteonorm 8.1 Kolkata. The June dip is an artefact of how PVsyst places unavailability; annual total is unaffected. Preliminary.", fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.92))
    fig.savefig(os.path.join(OUT, "monthly_energy_pr_VC4.png"))

loss_waterfall()
monthly_chart()
