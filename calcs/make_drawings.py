"""Generate preliminary plant layout and single-line diagram (DXF) from the design numbers.

Run: python calcs/make_drawings.py
Outputs (drawings/): SPV5-DWG-01-Layout-R0.dxf/.png/.pdf, SPV5-DWG-02-SLD-R0.dxf/.png/.pdf
The drawings are schematic: inverter and transformer symbols are enlarged and the yard position is a placeholder.
"""
import math, os
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "drawings")
os.makedirs(OUT, exist_ok=True)

# ---- design numbers (from calcs/ and ASSUMPTIONS.md)
N_ROWS, TABLES_PER_ROW = 17, 10
ROW_LEN = 300.02          # m, 260 modules per row
PITCH = 8.0
TABLE_DEPTH = 4.58 * math.cos(math.radians(20))   # plan depth, m
TABLE_W = ROW_LEN / TABLES_PER_ROW
ARRAY_H = (N_ROWS - 1) * PITCH + TABLE_DEPTH
DATE = "28-10-2026"

def new_doc():
    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.M
    for name, col in [("BOUNDARY", 1), ("ARRAY", 5), ("ROAD", 8), ("CABLE_LV", 6), ("EQUIP", 84),
                      ("TEXT", 7), ("FRAME", 7), ("DIM", 7), ("GRID", 4), ("HV", 1), ("DC", 5)]:
        doc.layers.add(name, color=col)
    return doc

def txt(msp, s, x, y, h=3.0, layer="TEXT", align="LEFT", rot=0):
    t = msp.add_text(s, dxfattribs={"height": h, "layer": layer, "rotation": rot})
    t.set_placement((x, y), align=getattr(ezdxf.enums.TextEntityAlignment, align))
    return t

def rect(msp, x0, y0, x1, y1, layer="EQUIP"):
    return msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": layer})

def line(msp, a, b, layer="EQUIP"):
    return msp.add_line(a, b, dxfattribs={"layer": layer})

def title_block(msp, x1, y0, w, no, title, scale_note, h=3.0):
    """Title block, bottom-right corner at (x1, y0)."""
    x0 = x1 - w
    rows = [("PROJECT", "5 MWp ground-mount solar PV plant, West Bengal (resource site: Kolkata)"),
            ("DESCRIPTION", title), ("DRAWING NO.", no), ("SCALE", scale_note),
            ("DRAWN / DATE", f"Sagnik Kumar Nath / {DATE}"),
            ("STATUS", "PRELIMINARY, NOT FOR CONSTRUCTION")]
    rh = h * 2.2
    rect(msp, x0, y0, x1, y0 + rh * len(rows), "FRAME")
    for i, (k, v) in enumerate(rows):
        yy = y0 + rh * (len(rows) - 1 - i)
        if i: line(msp, (x0, yy + rh), (x1, yy + rh), "FRAME")
        txt(msp, k, x0 + 1.5, yy + rh * 0.3, h * 0.75)
        txt(msp, v, x0 + 30 * h / 3.0, yy + rh * 0.3, h * 0.85)
    line(msp, (x0 + 28 * h / 3.0, y0), (x0 + 28 * h / 3.0, y0 + rh * len(rows)), "FRAME")

# =============================== 01 LAYOUT ===============================
def layout_drawing():
    doc = new_doc(); msp = doc.modelspace()
    FX0, FX1, FY0, FY1 = -35, 420, -95, 227
    rect(msp, FX0, FY0, FX1, FY1, "FRAME")
    rect(msp, FX0 + 3, FY0 + 3, FX1 - 3, FY1 - 3, "FRAME")

    # rows of tables
    for r in range(N_ROWS):
        y = r * PITCH
        for t in range(TABLES_PER_ROW):
            x = t * TABLE_W
            rect(msp, x + 0.15, y, x + TABLE_W - 0.15, y + TABLE_DEPTH, "ARRAY")
        txt(msp, f"R{r+1}", -5.3, y + 1.0, 2.0)
    # inverters (symbol enlarged) at east end of rows 1-16, LV trench, access road
    TRENCH_X = ROW_LEN + 8
    inv_pos = []
    for r in range(16):
        yc = r * PITCH + TABLE_DEPTH / 2
        rect(msp, ROW_LEN + 1.5, yc - 1.0, ROW_LEN + 4.5, yc + 1.0, "EQUIP")
        line(msp, (ROW_LEN + 4.5, yc), (TRENCH_X, yc), "CABLE_LV")
        txt(msp, f"INV{r+1}", ROW_LEN + 1.6, yc + 1.2, 1.4)
        inv_pos.append(yc)
    line(msp, (TRENCH_X, inv_pos[0]), (TRENCH_X, inv_pos[-1]), "CABLE_LV")
    # substation yard (placeholder position)
    YX0, YX1, YY0, YY1 = 320, 376, 12, 128
    rect(msp, YX0, YY0, YX1, YY1, "BOUNDARY")
    txt(msp, "SUBSTATION YARD", YX0, YY1 + 3, 3)
    txt(msp, "(placeholder position)", YX0 + 2, YY1 - 4, 1.9)
    for name, yc in (("TR1 2.5 MVA", 30), ("TR2 2.5 MVA", 94)):
        rect(msp, YX0 + 6, yc - 5, YX0 + 20, yc + 5, "EQUIP")
        txt(msp, name, YX0 + 4, yc + 7, 2.2)
        txt(msp, "0.8/33 kV Dyn11", YX0 + 4, yc - 9, 1.9)
    rect(msp, YX0 + 32, 52, YX0 + 44, 72, "EQUIP"); txt(msp, "33 kV RMU", YX0 + 31, 74, 2.2)
    txt(msp, "(VCB + metering)", YX0 + 36, 48.5, 1.9)
    rect(msp, YX0 + 26, 104, YX0 + 52, 118, "EQUIP"); txt(msp, "CONTROL ROOM", YX0 + 26, 120, 2.0)
    txt(msp, "SCADA / LV panels", YX0 + 28, 110, 1.9)
    # LV trench (two halves) and taps to transformers
    line(msp, (TRENCH_X, inv_pos[0]), (TRENCH_X, inv_pos[7]), "CABLE_LV")
    line(msp, (TRENCH_X, inv_pos[8]), (TRENCH_X, inv_pos[15]), "CABLE_LV")
    line(msp, (TRENCH_X, 30), (YX0 + 6, 30), "CABLE_LV")
    line(msp, (TRENCH_X, 94), (YX0 + 6, 94), "CABLE_LV")
    # HV links
    line(msp, (YX0 + 20, 30), (YX0 + 32, 57), "HV"); line(msp, (YX0 + 20, 94), (YX0 + 32, 67), "HV")
    line(msp, (YX0 + 44, 62), (YX1 + 24, 62), "HV")
    txt(msp, "33 kV O/H line", YX1 + 9, 65, 1.9); txt(msp, "to grid (3 km, TBD)", YX1 + 9, 57.5, 1.9)
    # road loop and fence
    FEN = (-12, -12, YX1 + 8, ARRAY_H + 12)
    rect(msp, *FEN, "BOUNDARY")
    for xs, ys, xe, ye in [(-6, -6, 312, -6), (312, -6, 312, ARRAY_H + 6), (312, ARRAY_H + 6, -6, ARRAY_H + 6), (-6, ARRAY_H + 6, -6, -6)]:
        msp.add_line((xs, ys), (xe, ye), dxfattribs={"layer": "ROAD", "linetype": "DASHED"})
    txt(msp, "4 m internal road (centreline, indicative)", 80, -9.5, 2.2, "ROAD")
    txt(msp, "GATE", 312, -10, 2.2); line(msp, (306, -12), (318, -12), "BOUNDARY")
    # dimensions (simple, drawn by hand)
    def dim_h(x0, x1, y, label):
        line(msp, (x0, y), (x1, y), "DIM"); line(msp, (x0, y - 1.5), (x0, y + 1.5), "DIM"); line(msp, (x1, y - 1.5), (x1, y + 1.5), "DIM")
        txt(msp, label, (x0 + x1) / 2, y + 1.5, 2.4, "DIM", "BOTTOM_CENTER")
    def dim_v(x, y0, y1, label):
        line(msp, (x, y0), (x, y1), "DIM"); line(msp, (x - 1.5, y0), (x + 1.5, y0), "DIM"); line(msp, (x - 1.5, y1), (x + 1.5, y1), "DIM")
        txt(msp, label, x - 1.5, (y0 + y1) / 2, 2.4, "DIM", "BOTTOM_CENTER", 90)
    dim_h(0, ROW_LEN, ARRAY_H + 19, f"{ROW_LEN:.1f} m (10 tables x 26 modules)")
    dim_v(-20, 0, PITCH, "8.0 m pitch")
    dim_v(-20, 0, ARRAY_H, f"{ARRAY_H:.1f} m")
    fence_w, fence_h = FEN[2] - FEN[0], FEN[3] - FEN[1]
    area_ha = fence_w * fence_h / 1e4
    txt(msp, f"Fence {fence_w:.0f} m x {fence_h:.0f} m = {area_ha:.1f} ha ({area_ha*2.471:.1f} acres), schematic", FEN[0], FEN[3] + 2.5, 2.6, "BOUNDARY")
    # north arrow
    msp.add_lwpolyline([(-24, 170), (-21, 170 + 14), (-18, 170), (-21, 173)], close=True, dxfattribs={"layer": "TEXT"})
    txt(msp, "N", -22.2, 187, 4)
    # header
    txt(msp, "5 MWp SOLAR PV PLANT: PRELIMINARY PLANT LAYOUT (PLAN)", 0, 215, 6)
    txt(msp, "Fixed tilt 20 deg, azimuth 0 deg (south), pitch 8.0 m, GCR 58%. Schematic: inverter, transformer and yard symbols are enlarged / placeholders.", 0, 208, 2.6)
    # key data (bottom left)
    kd = ["KEY DATA",
          "DC 4,994.6 kWp (8,840 x 565 Wp bifacial) / AC 4,000 kW (16 x SG250HX)",
          "17 rows x 10 tables = 170 tables (2 portrait x 26 modules = 52 modules each)",
          "340 strings of 26 modules (2 strings per table)",
          "Array footprint 300.0 m x 132.3 m = 3.97 ha (excl. roads, yard, fence)",
          "2 x 2.5 MVA 0.8/33 kV transformers: TR1 takes INV1-8, TR2 takes INV9-16",
          "PVsyst VC4: 7,078 MWh/yr; 6,917 MWh/yr at 33 kV point after AC losses",
          "Strings-to-inverter assignment and cable routes are indicative (not yet designed)"]
    for i, s in enumerate(kd):
        txt(msp, s, -30, -26 - 4.2 * i, 2.6 if i else 3.2)
    # legend
    lg = [("ARRAY", "PV table (2 portrait modules x 26)"), ("EQUIP", "Inverter / transformer / RMU (schematic)"),
          ("CABLE_LV", "LV AC cable (240 mm2 Al, 800 V)"), ("HV", "33 kV link"), ("ROAD", "Internal road (indicative)"),
          ("BOUNDARY", "Fence line / yard boundary")]
    txt(msp, "LEGEND", 135, -26, 3.2)
    cols = {"ARRAY": 5, "EQUIP": 84, "CABLE_LV": 6, "HV": 1, "ROAD": 8, "BOUNDARY": 1}
    for i, (ly, d) in enumerate(lg):
        y = -32 - 4.6 * i
        line(msp, (135, y + 1), (145, y + 1), ly)
        txt(msp, d, 148, y, 2.6)
    # scale bar 50 m
    line(msp, (135, -66), (185, -66), "TEXT"); line(msp, (135, -68), (135, -64), "TEXT"); line(msp, (185, -68), (185, -64), "TEXT")
    txt(msp, "0", 134, -72, 2.4); txt(msp, "50 m", 183, -72, 2.4)
    title_block(msp, FX1 - 3, FY0 + 3, 170, "SPV5-DWG-01-Layout-R0", "Plant layout (plan)", "As plotted on A3 (see scale bar)")
    return doc

# =============================== 02 SLD ===============================
def sld_drawing():
    doc = new_doc(); msp = doc.modelspace()
    W, H = 420, 297
    rect(msp, 0, 0, W, H, "FRAME"); rect(msp, 5, 5, W - 5, H - 5, "FRAME")
    txt(msp, "5 MWp SOLAR PV PLANT: SINGLE-LINE DIAGRAM (PRELIMINARY)", 12, 276, 6)
    txt(msp, "Two identical 2 MW blocks (INV1-8 + TR1, INV9-16 + TR2) join at the 33 kV RMU. Ratings are design values, not vendor-confirmed.", 12, 268, 2.6)

    def block(yc, inv_label, tr_label):
        # PV array
        rect(msp, 12, yc - 18, 62, yc + 18)
        txt(msp, "PV ARRAY", 14, yc + 12, 3.2)
        txt(msp, f"{inv_label[1]} strings x 26 modules", 14, yc + 6, 2.4)
        txt(msp, "565 Wp bifacial, Voc,max 1425 V", 14, yc + 1, 2.2)
        txt(msp, "DC 1500 V max", 14, yc - 4, 2.2)
        txt(msp, f"{inv_label[2]} kWp", 14, yc - 10, 2.4)
        # DC cable
        line(msp, (62, yc), (88, yc), "DC")
        txt(msp, "DC string cable", 63, yc + 8, 2.0); txt(msp, "H1Z2Z2-K Cu", 63, yc + 4.5, 2.0); txt(msp, "4 to 10 mm2", 63, yc + 1.2, 2.0)
        # inverters
        rect(msp, 88, yc - 18, 138, yc + 18)
        txt(msp, "8 x INVERTER", 90, yc + 12, 3.2)
        txt(msp, "Sungrow SG250HX", 90, yc + 6, 2.4)
        txt(msp, "250 kVA (30 C), 800 V AC", 90, yc + 1, 2.2)
        txt(msp, "12 MPPT, 180.5 A each", 90, yc - 4, 2.2)
        txt(msp, inv_label[0], 90, yc - 10, 2.4)
        # LV cable to LV panel
        line(msp, (138, yc), (172, yc), "CABLE_LV")
        txt(msp, "3 x 1C 240 mm2 Al XLPE", 139, yc + 7, 2.0); txt(msp, "1.1 kV, 80 m, drop 0.48%", 139, yc + 3.5, 2.0)
        # LV panel with MCCB per inverter
        rect(msp, 172, yc - 14, 205, yc + 14)
        txt(msp, "LV AC PANEL", 174, yc + 8, 2.6); txt(msp, "MCCB per inverter", 174, yc + 3, 2.0)
        txt(msp, "(>= 226 A, to select)", 174, yc - 1.5, 1.8); txt(msp, "800 V busbar", 174, yc - 6, 2.0)
        line(msp, (205, yc), (225, yc), "CABLE_LV")
        # transformer symbol
        cx = 238
        msp.add_circle((cx - 4, yc), 8, dxfattribs={"layer": "EQUIP"}); msp.add_circle((cx + 4, yc), 8, dxfattribs={"layer": "EQUIP"})
        line(msp, (225, yc), (cx - 12, yc), "CABLE_LV"); line(msp, (cx + 12, yc), (262, yc), "HV")
        txt(msp, tr_label, 222, yc - 16, 2.6)
        txt(msp, "2.5 MVA, 0.8/33 kV", 222, yc - 21, 2.2); txt(msp, "Dyn11, ONAN", 222, yc - 25, 2.2)
        # breaker symbol (VCB) on 33 kV side
        rect(msp, 262, yc - 3, 272, yc + 3, "HV"); line(msp, (262, yc - 3), (272, yc + 3), "HV"); line(msp, (262, yc + 3), (272, yc - 3), "HV")
        txt(msp, "VCB", 263, yc + 5, 2.0)
        line(msp, (272, yc), (290, yc), "HV")

    block(200, ("INV1 to INV8", 170, "2,497.3"), "TR1")
    block(110, ("INV9 to INV16", 170, "2,497.3"), "TR2")
    # 33 kV bus
    line(msp, (290, 110), (290, 200), "HV")
    line(msp, (290, 155), (325, 155), "HV")
    rect(msp, 325, 140, 365, 170, "EQUIP")
    txt(msp, "33 kV RMU", 328, 163, 3.0); txt(msp, "Incomer VCB, CT, PT", 327, 157, 2.0)
    txt(msp, "Energy meter (net)", 327, 152, 2.0); txt(msp, "Protection relay", 327, 147, 2.0)
    line(msp, (365, 155), (395, 155), "HV")
    txt(msp, "33 kV O/H line", 366, 163, 2.2); txt(msp, "ACSR Dog, 3 km", 366, 159, 2.0); txt(msp, "(length placeholder)", 366, 148, 1.9)
    rect(msp, 395, 135, 412, 175, "GRID"); txt(msp, "GRID", 397, 158, 3.0); txt(msp, "SUBSTN", 396, 153, 2.4); txt(msp, "(DISCOM", 396, 148, 2.0); txt(msp, "TBC)", 397, 144, 2.0)
    # notes
    notes = ["NOTES",
             "1. DC/AC ratio 1.249; 340 strings (148 MPPT inputs with 2 strings, 44 with 1) across 16 inverters.",
             "2. Net energy at 33 kV point 6,917 MWh/yr after 2.28% AC-side losses (cables, transformers, 33 kV line).",
             "3. Not yet shown: auxiliary supply, SCADA/communication, weather station, earthing and lightning protection,",
             "    surge protection devices, DC isolation detail. Add before any construction use.",
             "4. MCCB/relay ratings and cable lengths are to be confirmed with the final layout and vendor data."]
    for i, s in enumerate(notes):
        txt(msp, s, 12, 70 - 5 * i, 3.0 if i == 0 else 2.4)
    lg = [("DC", "DC (1500 V max)"), ("CABLE_LV", "LV AC (800 V)"), ("HV", "33 kV")]
    txt(msp, "LEGEND", 12, 38, 3)
    for i, (ly, d) in enumerate(lg):
        line(msp, (12, 33 - 5 * i + 1), (24, 33 - 5 * i + 1), ly); txt(msp, d, 27, 33 - 5 * i, 2.4)
    title_block(msp, W - 8, 8, 160, "SPV5-DWG-02-SLD-R0", "Single-line diagram", "Not to scale")
    return doc

def export(doc, stem, w_mm=420, h_mm=297):
    dxf = os.path.join(OUT, stem + ".dxf")
    doc.saveas(dxf)
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out, config=Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR)).draw_layout(doc.modelspace(), finalize=True)
    ax.set_facecolor("white"); fig.patch.set_facecolor("white")
    # draw in black on white
    for pdf_png in (".png", ".pdf"):
        fig.savefig(os.path.join(OUT, stem + pdf_png), dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", dxf)

if __name__ == "__main__":
    export(layout_drawing(), "SPV5-DWG-01-Layout-R0")
    export(sld_drawing(), "SPV5-DWG-02-SLD-R0")
