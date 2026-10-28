"""Row pitch for a fixed-tilt table: no inter-row shading in a chosen winter window.

Geometry: shadow cast by the table top edge onto the ground behind it, measured
along the N-S direction (the direction that matters for the next row).
"""
import math, sys

LAT = 22.57          # Kolkata, deg N
TILT = 20.0          # deg
MOD_L, MOD_W = 2.278, 1.134      # Waaree BiN-08-565 (m), area 2.583 m2
ROWS_HIGH = 2                    # 2 modules in portrait per table
CLEAR = 1.0                      # lowest edge height above ground, m (assumption: flood-prone Bengal sites)

def sun(lat, decl, hour):
    h = math.radians(15 * (hour - 12))
    la, de = math.radians(lat), math.radians(decl)
    sin_el = math.sin(la)*math.sin(de) + math.cos(la)*math.cos(de)*math.cos(h)
    el = math.asin(sin_el)
    az = math.atan2(math.sin(h), math.cos(h)*math.sin(la) - math.tan(de)*math.cos(la))  # from south, +west
    return math.degrees(el), math.degrees(az)

def pitch_for(hour_window, decl=-23.44):
    w = MOD_L * ROWS_HIGH
    t = math.radians(TILT)
    rise = w * math.sin(t)
    foot = w * math.cos(t)
    best = 0
    out = []
    for hr in hour_window:
        el, az = sun(LAT, decl, hr)
        # shadow length along N-S = rise / tan(el) * cos(az)
        sh = rise / math.tan(math.radians(el)) * math.cos(math.radians(az))
        out.append((hr, el, az, foot + sh))
        best = max(best, foot + sh)
    return w, rise, foot, best, out

if __name__ == "__main__":
    for label, win in (("10:00-14:00", [10, 11, 12, 13, 14]), ("09:00-15:00", [9, 10, 11, 12, 13, 14, 15])):
        w, rise, foot, p, out = pitch_for(win)
        print(f"Window {label}: pitch >= {p:.2f} m, GCR = {w/p:.2f}")
    w, rise, foot, p, out = pitch_for([9, 10, 11, 12, 13, 14, 15])
    print(f"Table slope width {w:.3f} m, rise {rise:.3f} m, footprint {foot:.3f} m")
    for r in out:
        print("  hour %4.1f  elev %5.1f  az %6.1f  pitch needed %.2f" % r)
