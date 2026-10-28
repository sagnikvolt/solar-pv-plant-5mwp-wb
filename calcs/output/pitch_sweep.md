# Row pitch trade-off (PVsyst, bifacial, 20 deg tilt, same losses)

Array footprint = row length x (16 x pitch + table depth projected on the ground). It excludes roads, fencing, inverter pads and the substation.

| Pitch (m) | GCR | Variant | Energy (MWh/yr) | kWh/kWp | PR | Footprint (ha) | ha per MWp | Energy vs previous row | Footprint vs previous row |
|---|---|---|---|---|---|---|---|---|---|
| 6.4 | 72% | VC3 | 6938 | 1389 | 0.840 | 3.20 | 0.64 |  |  |
| 7.0 | 66% | VC1 | 7006 | 1403 | 0.848 | 3.49 | 0.70 | +1.0% | +9.0% |
| 8.0 | 58% | VC4 | 7078 | 1417 | 0.856 | 3.97 | 0.79 | +1.0% | +13.8% |
| 9.0 | 51% | VC5 | 7121 | 1426 | 0.862 | 4.45 | 0.89 | +0.6% | +12.1% |

Reading: each step from 6.4 to 9.0 m gains less energy for more land. 7.0 to 8.0 m gains +1.0% energy for +14% footprint, 8.0 to 9.0 m only +0.6% for +12.1%. **8.0 m is adopted** as the balance point; land cost and the real plot shape could still move it.
