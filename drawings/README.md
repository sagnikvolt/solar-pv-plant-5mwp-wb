# Drawings

| No. | Drawing | DWG | DXF | PDF / PNG | Status |
|---|---|---|---|---|---|
| 01 | Plant layout (17 rows, 170 tables, 16 inverters, 2 transformers, yard, fence) | `SPV5-DWG-01-Layout-R0.dwg` | `.dxf` | `.pdf`, `.png` | R0, preliminary and schematic |
| 02 | Single-line diagram (PV, inverters, LV panel, 2 x 2.5 MVA transformers, 33 kV RMU, grid) | `SPV5-DWG-02-SLD-R0.dwg` | `.dxf` | `.pdf`, `.png` | R0, preliminary and schematic |

## How these were made
`python calcs/make_drawings.py` builds both drawings from the design numbers with Python (`ezdxf`) and writes the DXF, PDF and PNG. The DXF files were then opened in AutoCAD 2027 (education licence) and saved as AutoCAD 2018 DWG. The PDF/PNG files come from the Python render, not from an AutoCAD plot, so they carry no education-licence plot stamp. The DWG files do carry AutoCAD's education marking.

## What is schematic or missing
- Inverter, transformer and yard symbols are enlarged, and the yard position and 33 kV route are placeholders.
- String-to-inverter assignment and cable routes are indicative only. Cable lengths in `calcs/cable_sizing.py` are not taken from this layout.
- The single-line diagram omits earthing, lightning protection, auxiliary supply, SCADA and DC isolation detail.
- Not checked by a practising engineer.

Naming: `SPV5-DWG-01-Layout-R0.dwg` (R0 becomes R1 on each revision).
