# String Sizing Results
_Generated 2026-10-28 by `calcs/string_sizing.py`_

**Module:** Waaree ELITE BiN-08-580 (N-type TOPCon, bifacial, 144 half-cut cells)  |  **Inverter:** Sungrow SG250HX (datasheet v1.22)

## Temperatures
- Min cell temperature (record min ambient): 3.4 °C
- Max cell temperature (NOCT model, 1000 W/m²): 75.8 °C
- Vmp coefficient: γ(Pmax) used as β(Vmp) approximation

## Per-module values
| Quantity | Value |
|---|---|
| Voc at min temp | 55.45 V |
| Vmp at max temp | 37.31 V |
| Vmp at min temp | 46.86 V |
| Isc at max temp (incl. bifacial gain) | 15.68 A |
| 1.25 × Isc (cable/fuse sizing basis) | 19.60 A |

## String length
- Max modules (DC voltage limit): **27**
- Min modules (MPPT min voltage, hot): **17**
- Max modules before MPPT max (cold): 32
- **Chosen: 27 modules/string** → Voc,max 1497 V, Vmp range 1007–1265 V

## Plant configuration
| Quantity | Value |
|---|---|
| String power | 15.66 kWp |
| Number of strings | 319 |
| Number of modules | 8613 |
| DC capacity | 4995.5 kWp |
| Inverters | 16 × 250 kW = 4000 kW |
| DC/AC ratio | 1.249 |
| Strings per inverter (max allowed) | 20 (24) |
| Imp per string / all strings on one MPPT | 13.18 A / 26.36 A (limit 26 A) |

## Checks
| Check | Result |
|---|---|
| Voc_cold x N <= Vdc_max | PASS |
| Vmp_hot x N >= Vmppt_min | PASS |
| Vmp_cold x N <= Vmppt_max | PASS |
| Strings/inverter within MPPT current limit | PASS |
| Imp x strings per MPPT <= MPPT max operating current | **FAIL** |
| N within feasible range | PASS |
