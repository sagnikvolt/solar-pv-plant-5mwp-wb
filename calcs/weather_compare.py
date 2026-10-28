"""
Compare monthly GHI from Meteonorm, PVGIS and NASA POWER for the site.

Fill data/weather/weather_comparison.csv with MONTHLY TOTALS in kWh/m²/month.
(NASA POWER gives daily averages in kWh/m²/day, so multiply by the 'days' column first.)

Usage:  python calcs/weather_compare.py
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "weather", "weather_comparison.csv")
OUT = os.path.join(ROOT, "calcs", "output", "weather_comparison.md")
SOURCES = [("Meteonorm", "meteonorm_GHI_kWh_m2"),
           ("PVGIS", "pvgis_GHI_kWh_m2"),
           ("NASA POWER", "nasa_power_GHI_kWh_m2")]


def main():
    with open(CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    totals = {}
    for name, col in SOURCES:
        vals = [r[col] for r in rows]
        if all(v.strip() for v in vals):
            totals[name] = sum(float(v) for v in vals)
    if not totals:
        sys.exit("No complete GHI column found in " + os.path.relpath(CSV))

    base_name = "Meteonorm" if "Meteonorm" in totals else next(iter(totals))
    base = totals[base_name]
    lines = ["# Irradiance cross-check", "",
             f"| Source | Annual GHI (kWh/m²/yr) | Δ vs {base_name} |", "|---|---|---|"]
    for name, tot in totals.items():
        lines.append(f"| {name} | {tot:,.0f} | {100 * (tot - base) / base:+.1f}% |")
    lines += ["", "_Explain any difference above ~3% in the report (data period, satellite vs. "
              "ground-station interpolation, spatial resolution)._"]
    md = "\n".join(lines) + "\n"
    print(md)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)


if __name__ == "__main__":
    main()
