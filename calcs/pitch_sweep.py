"""Row pitch trade-off from the PVsyst runs (VC3, VC1, VC4, VC5): yield vs land."""
import os
ROW_LEN, ROWS, TABLE_DEPTH = 300.02, 17, 4.58
TILT = 20
import math
# pitch: (variant, energy MWh, specific kWh/kWp, PR)
RUNS = {6.4: ("VC3", 6938, 1389, 0.840), 7.0: ("VC1", 7006, 1403, 0.848),
        8.0: ("VC4", 7078, 1417, 0.856), 9.0: ("VC5", 7121, 1426, 0.862)}
DC_MWP = 4.9946
out = ["# Row pitch trade-off (PVsyst, bifacial, 20 deg tilt, same losses)", "",
       "Array footprint = row length x (16 x pitch + table depth projected on the ground). It excludes roads, "
       "fencing, inverter pads and the substation.", "",
       "| Pitch (m) | GCR | Variant | Energy (MWh/yr) | kWh/kWp | PR | Footprint (ha) | ha per MWp | Energy vs previous row | Footprint vs previous row |",
       "|---|---|---|---|---|---|---|---|---|---|"]
prev = None
for p, (v, e, sy, pr) in sorted(RUNS.items()):
    area = ROW_LEN * ((ROWS - 1) * p + TABLE_DEPTH * math.cos(math.radians(TILT))) / 1e4
    gcr = 4.62 / p * 100
    de = "" if prev is None else "%+.1f%%" % ((e / prev[0] - 1) * 100)
    da = "" if prev is None else "%+.1f%%" % ((area / prev[1] - 1) * 100)
    out.append("| %.1f | %.0f%% | %s | %d | %d | %.3f | %.2f | %.2f | %s | %s |" % (p, gcr, v, e, sy, pr, area, area / DC_MWP, de, da))
    prev = (e, area)
out += ["", "Reading: each step from 6.4 to 9.0 m gains less energy for more land. 7.0 to 8.0 m gains +1.0% energy for +14% footprint, "
        "8.0 to 9.0 m only +0.6% for +12.1%. **8.0 m is adopted** as the balance point; land cost and the real plot shape could still move it."]
text = "\n".join(out)
print(text)
open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "calcs", "output", "pitch_sweep.md"), "w").write(text + "\n")
