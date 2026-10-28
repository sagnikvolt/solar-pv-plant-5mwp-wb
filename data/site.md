# Site

| Item | Value |
|---|---|
| Project location | Kolkata, West Bengal |
| Coordinates used for resource data | 22.57 °N, 88.36 °E |
| Elevation | 15 m (PVGIS) |
| Climate | Tropical wet-and-dry; monsoon (Jun–Sep) cuts irradiance, summer peaks Mar–May |
| Annual GHI | 1,730 kWh/m² (PVGIS-ERA5, 2005–2020); 1,669 kWh/m² (NASA POWER) |
| Record minimum ambient | 3.4 °C (9 Jan 2013, NASA POWER gridded) |
| Record maximum ambient | 46.9 °C (30 Apr 2024, NASA POWER gridded) |
| Usable land | TBD: a 5 MWp fixed-tilt plant needs about 20–25 acres |
| Plot and nearest 33 kV substation | TBD (to be confirmed on Google Earth) |

## Open point: where in "Kolkata"
Kolkata city itself has no 20–25 acre open plots, so the project uses Kolkata's climate and coordinates as the resource site. The physical plot still has to be pinned down. Options:
1. A plot on the metropolitan fringe (South 24 Parganas / Howrah / Hooghly outskirts), where the weather data is essentially the same.
2. A rooftop or brownfield variant at a smaller capacity.

Whichever you choose, record the exact plot coordinates and the substation here, and re-run `python calcs/fetch_weather.py --lat <lat> --lon <lon>` if it is more than about 25 km away.

## Why Kolkata
Home city, and a resource of about 1,730 kWh/m²/yr, roughly 4% lower than the Bankura/Purulia belt (about 1,803 kWh/m²/yr in PVGIS). That difference is mentioned in the report as a site-selection trade-off.

## Screenshots
*Google Earth view with the plant boundary and substation marked (save in `data/`).*
