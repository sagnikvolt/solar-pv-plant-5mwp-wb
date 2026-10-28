# String Sizing Results
_Generated 2026-10-28 by `calcs/string_sizing.py`_

**Module:** Generic 550 Wp mono PERC (example)  |  **Inverter:** Generic 1500 V, 250 kW string inverter (example)

## Temperatures
- Min cell temperature (record min ambient): 3.0 °C
- Max cell temperature (NOCT model, 1000 W/m²): 76.2 °C
- Vmp coefficient: γ(Pmax) used as β(Vmp) approximation

## Per-module values
| Quantity | Value |
|---|---|
| Voc at min temp | 52.76 V |
| Vmp at max temp | 34.38 V |
| Vmp at min temp | 45.13 V |
| Isc at max temp (incl. bifacial gain) | 14.34 A |
| 1.25 × Isc (cable/fuse sizing basis) | 17.93 A |

## String length
- Max modules (DC voltage limit): **28**
- Min modules (MPPT min voltage, hot): **15**
- Max modules before MPPT max (cold): 33
- **Chosen: 28 modules/string** → Voc,max 1477 V, Vmp range 963–1264 V

## Plant configuration
| Quantity | Value |
|---|---|
| String power | 15.40 kWp |
| Number of strings | 325 |
| Number of modules | 9100 |
| DC capacity | 5005.0 kWp |
| Inverters | 16 × 250 kW = 4000 kW |
| DC/AC ratio | 1.251 |
| Strings per inverter (max allowed) | 21 (36) |

## Checks
| Check | Result |
|---|---|
| Voc_cold x N <= Vdc_max | PASS |
| Vmp_hot x N >= Vmppt_min | PASS |
| Vmp_cold x N <= Vmppt_max | PASS |
| Strings/inverter within MPPT current limit | PASS |
| N within feasible range | PASS |
