"""
Fetch monthly irradiance and temperature data for the site from two free sources
and write data/weather/weather_comparison.csv (PVGIS + NASA POWER columns).
The Meteonorm columns are left for you to copy from PVsyst's Meteonorm import.

Sources
  PVGIS v5.3 MRcalc  : monthly GHI, 2005-2020 average (ERA5-based radiation database)
  NASA POWER         : climatology GHI (ALLSKY_SFC_SW_DWN) and T2M, plus DAILY T2M_MIN/T2M_MAX
                       2001-2025 to find record extremes for string sizing

Usage:  python calcs/fetch_weather.py --lat 23.15 --lon 87.00
"""
import argparse
import calendar
import csv
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(ROOT, "data", "weather", "weather_comparison.csv")
OUT_EXT = os.path.join(ROOT, "data", "weather", "temperature_extremes.json")
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
NAMES = [m.title() for m in MONTHS]


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    a = ap.parse_args()

    pv = get("https://re.jrc.ec.europa.eu/api/v5_3/MRcalc?lat=%s&lon=%s&horirrad=1&avtemp=1"
             "&outputformat=json&startyear=2005&endyear=2020" % (a.lat, a.lon))
    rows = pv["outputs"]["monthly"]
    elev = pv["inputs"]["location"]["elevation"]
    pv_g = [sum(r["H(h)_m"] for r in rows if r["month"] == m) / 16 for m in range(1, 13)]

    nc = get("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters="
             "ALLSKY_SFC_SW_DWN,T2M&community=RE&longitude=%s&latitude=%s&format=JSON" % (a.lon, a.lat))
    p = nc["properties"]["parameter"]
    days = [calendar.monthrange(2023, i + 1)[1] for i in range(12)]   # non-leap
    nasa_g = [p["ALLSKY_SFC_SW_DWN"][m] * days[i] for i, m in enumerate(MONTHS)]  # kWh/m2/day -> /month
    nasa_t = [p["T2M"][m] for m in MONTHS]

    nd = get("https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M_MIN,T2M_MAX"
             "&community=RE&longitude=%s&latitude=%s&start=20010101&end=20251231&format=JSON" % (a.lon, a.lat))
    d = nd["properties"]["parameter"]
    tmin = min((v, k) for k, v in d["T2M_MIN"].items() if v > -900)
    tmax = max((v, k) for k, v in d["T2M_MAX"].items() if v > -900)

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", "days", "meteonorm_GHI_kWh_m2", "pvgis_GHI_kWh_m2", "nasa_power_GHI_kWh_m2",
                    "meteonorm_Tamb_C", "nasa_power_Tamb_C"])
        for i in range(12):
            w.writerow([NAMES[i], days[i], "", round(pv_g[i], 1), round(nasa_g[i], 1), "", round(nasa_t[i], 1)])
    with open(OUT_EXT, "w", encoding="utf-8") as f:
        json.dump({"lat": a.lat, "lon": a.lon, "elevation_m": elev,
                   "record_min_C": tmin[0], "record_min_date": tmin[1],
                   "record_max_C": tmax[0], "record_max_date": tmax[1],
                   "source": "NASA POWER daily T2M_MIN/T2M_MAX 2001-2025 (gridded; station extremes can be a little more extreme)"},
                  f, indent=2)
    print("PVGIS annual GHI %.0f | NASA POWER %.0f kWh/m2/yr" % (sum(pv_g), sum(nasa_g)))
    print("Record min %.1f C (%s) | record max %.1f C (%s) | elevation %s m"
          % (tmin[0], tmin[1], tmax[0], tmax[1], elev))


if __name__ == "__main__":
    main()
