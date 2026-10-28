"""P50/P90 annual energy from a PVsyst P50 result and a stated uncertainty budget.

The uncertainty components below are ENGINEERING ASSUMPTIONS (see ASSUMPTIONS.md),
not PVsyst outputs. Components are treated as independent and normally distributed,
so they combine as the root sum of squares (RSS).
"""
import math, json, sys

P50_MWH = float(sys.argv[1]) if len(sys.argv) > 1 else 7006.164   # PVsyst VC1 annual E_Grid
Z90 = 1.2816  # one-sided 90% exceedance

# name: (sigma %, is interannual)
BUDGET = {
    "Irradiance data source (Meteonorm vs PVGIS vs NASA POWER spread)": (5.0, False),
    "Interannual GHI variability (Meteonorm, PVsyst)":               (3.2, True),
    "Transposition and bifacial model":                              (2.0, False),
    "PV performance model (temperature, low-light, IAM)":            (2.0, False),
    "Module data and degradation behaviour":                         (1.5, False),
    "Soiling assumption":                                            (1.0, False),
    "Availability assumption":                                       (0.5, False),
}

def combine(include_interannual=True, years=1):
    tot = 0.0
    for name, (s, inter) in BUDGET.items():
        if inter:
            if include_interannual:
                tot += (s / math.sqrt(years)) ** 2
        else:
            tot += s ** 2
    return math.sqrt(tot)

rows = []
for label, years in (("1-year", 1), ("10-year", 10)):
    sig = combine(True, years)
    p90 = P50_MWH * (1 - Z90 * sig / 100)
    rows.append((label, sig, p90, p90 / P50_MWH))

out = ["# P50 / P90 energy estimate (preliminary)", "",
       f"P50 = PVsyst variant VC1 annual energy injected = **{P50_MWH:,.0f} MWh/yr**", "",
       "| Uncertainty component | σ (%) |", "|---|---|"]
for name, (s, _) in BUDGET.items():
    out.append(f"| {name} | {s:.1f} |")
out += ["", "| Case | Combined σ (%) | P90 (MWh/yr) | P90 / P50 |", "|---|---|---|---|"]
for label, sig, p90, ratio in rows:
    out.append(f"| {label} | {sig:.2f} | {p90:,.0f} | {ratio:.3f} |")
out += ["", "Method: RSS of independent components, P90 = P50 × (1 − 1.2816 σ). "
        "The 10-year case divides the interannual component by √10.",
        "All σ values are assumptions, to be revisited; the largest (data source, 5%) reflects the spread "
        "between the three irradiance datasets (1,574 to 1,730 kWh/m²)."]
text = "\n".join(out)
print(text)
open("calcs/output/p50_p90.md", "w").write(text + "\n")
