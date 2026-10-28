"""Workflow diagram: how the 5 MWp design was produced, step by step. Run: python calcs/make_workflow_diagram.py"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "showcase", "images", "workflow_overview.png")

NAVY, ORANGE, INK, GREY = "#14213d", "#e07a1f", "#1b1b1b", "#5b6270"
steps = [
    ("1", "Site and weather", "Kolkata; Meteonorm, NASA POWER and PVGIS compared", "Python"),
    ("2", "Equipment", "565 Wp bifacial module, 250 kVA string inverter (datasheets)", "Datasheets"),
    ("3", "String sizing", "26 modules per string; 1,500 V and MPPT limits checked", "Python + Excel"),
    ("4", "Row pitch sweep", "6.4 to 9.0 m; 8.0 m chosen", "PVsyst"),
    ("5", "Yield simulation", "Bifacial, 3D shading, losses: 7,078 MWh/yr", "PVsyst 7.4"),
    ("6", "Uncertainty", "P50 and P90 from an assumed error budget", "Python"),
    ("7", "Independent check", "SAM and PVGIS compared with PVsyst", "Python (SAM)"),
    ("8", "Electrical design", "Cables, transformers, 33 kV; 6,917 MWh/yr delivered", "Python"),
    ("9", "Drawings", "Site layout and single-line diagram", "Python + AutoCAD 2027"),
    ("10", "Economics and CO2", "Indicative cost range, LCOE, tonnes of CO2 avoided", "Python"),
    ("11", "Report and checks", "8-page report; every number logged in VERIFICATION.md", "Python, Chromium"),
]
fig, ax = plt.subplots(figsize=(14, 9.2), dpi=160)
ax.set_xlim(0, 14); ax.set_ylim(0, 9.2); ax.axis("off")
fig.patch.set_facecolor("white")
ax.text(0.4, 8.75, "How the 5 MWp plant design was built", fontsize=22, fontweight="bold", color=NAVY, va="center")
ax.text(0.4, 8.3, "Each step uses the output of the one before it. All scripts and files are in this repository.", fontsize=12, color=GREY, va="center")
cols = 2; per = 6
for i, (n, title, desc, tool) in enumerate(steps):
    c = i // per; r = i % per
    x = 0.4 + c * 6.8; y = 7.2 - r * 1.2
    ax.add_patch(FancyBboxPatch((x, y - 0.45), 6.4, 1.0, boxstyle="round,pad=0.02,rounding_size=0.12", fc="#f4f6fb", ec=NAVY, lw=1.2))
    ax.add_patch(plt.Circle((x + 0.5, y + 0.05), 0.34, fc=ORANGE, ec="none"))
    ax.text(x + 0.5, y + 0.05, n, ha="center", va="center", fontsize=13, fontweight="bold", color="white")
    ax.text(x + 1.0, y + 0.25, title, fontsize=13, fontweight="bold", color=NAVY, va="center")
    ax.text(x + 1.0, y - 0.1, desc, fontsize=9.5, color=INK, va="center")
    ax.text(x + 6.3, y + 0.25, tool, fontsize=8.5, color=ORANGE, va="center", ha="right", fontweight="bold")
ax.text(0.4, 0.25, "Preliminary design for learning and portfolio use. Not a bankable report.", fontsize=10, color=GREY, style="italic")
fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print(OUT)
