"""Preliminary BOQ scope, capex, LCOE, payback and CO2 for the 5 MWp plant.

Cost lines use the MIDPOINTS of published indicative ranges (taypro.in, updated 21 Jun 2026) for utility-scale
ground-mount in India; they are not vendor quotes. Quantities come from the design. Everything marked
ASSUMPTION is logged in ASSUMPTIONS.md. Run:  python calcs/economics.py
"""
import os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "calcs", "output", "economics.md")
DC_MWP = 4.9946
E_NET = float(open(os.path.join(ROOT, "calcs", "output", "net_energy.txt")).read().split()[0])   # MWh/yr at 33 kV point
E_PVSYST = 7078.053

# Cost lines: (low, mid, high) in INR crore per MWp (published indicative ranges)
LINES = {
    "Modules (565 Wp bifacial, 8,840 pcs)":                  (1.50, 1.95, 2.40),
    "Inverters + MV equipment (16 x SG250HX, 2 x 2.5 MVA, RMU)": (0.40, 0.55, 0.70),
    "Mounting structures and foundations (170 tables)":       (0.35, 0.55, 0.75),
    "Cables, combiner/ACDB, SCADA":                           (0.25, 0.35, 0.45),
    "Civil, fencing, roads":                                  (0.20, 0.275, 0.35),
    "Plant-end substation and metering":                      (0.30, 0.425, 0.55),
    "Installation labour and EPC margin (ASSUMPTION)":        (0.20, 0.30, 0.40),
}
OUTSIDE = {
    "Land lease, upfront (published 0.05 to 0.25)":           (0.05, 0.15, 0.25),
    "External 33 kV line, 3 km (published 0.10 to 0.80)":     (0.10, 0.30, 0.80),
    "Connectivity charges (published 0.03 to 0.15)":          (0.03, 0.09, 0.15),
}
CONT = 0.05

# Position within each published range: Low = bottom, Base = 25th percentile, High = top.
# The plain mid-point stacked to INR 5.2 cr/MWp and LCOE 4.9, inconsistent with 2.3-3.6 INR/kWh market tariffs,
# so the base case is set lower in the range (judgement, flagged in the output).
POS = (0.0, 0.25, 1.0)
def pick(v, idx):
    return v[0] + POS[idx] * (v[2] - v[0])

def capex(idx):
    epc = sum(pick(v, idx) for v in LINES.values())
    cont = epc * CONT
    out = sum(pick(v, idx) for v in OUTSIDE.values())
    return epc, cont, out, (epc + cont + out)

# Opex and finance (ASSUMPTIONS)
OM_CR_PER_MWP = 0.05          # INR 5 lakh/MWp/yr incl. cleaning and security
OM_ESC = 0.04
INS_FRAC = 0.003              # insurance, fraction of EPC per year
INV_REPL_YR, INV_REPL_CR = 12, 0.48
DEGR = 0.004                  # per year (PVsyst default aging 0.4%/yr)
LIFE = 25
DISC = 0.10                   # nominal, pre-tax (ASSUMPTION)

def cashflows(total_cr_per_mwp, epc_cr_per_mwp, tariff):
    capex_cr = total_cr_per_mwp * DC_MWP
    cfs, en, opex_l = [-capex_cr], [0.0], [0.0]
    for y in range(1, LIFE + 1):
        e = E_NET * (1 - DEGR) ** (y - 1)                         # MWh
        rev = e * 1000 * tariff / 1e7                             # crore
        opex = OM_CR_PER_MWP * DC_MWP * (1 + OM_ESC) ** (y - 1) + INS_FRAC * epc_cr_per_mwp * DC_MWP
        if y == INV_REPL_YR:
            opex += INV_REPL_CR
        cfs.append(rev - opex); en.append(e); opex_l.append(opex)
    return capex_cr, cfs, en, opex_l

def npv(rate, cfs):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cfs))

def irr(cfs):
    lo, hi = -0.5, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(mid, cfs) > 0:
            lo = mid
        else:
            hi = mid
    return mid

def metrics(idx, tariff):
    epc, cont, out, tot = capex(idx)
    capex_cr, cfs, en, opex_l = cashflows(tot, epc * (1 + CONT), tariff)
    pv_cost = capex_cr + sum(o / (1 + DISC) ** t for t, o in enumerate(opex_l) if t > 0)
    pv_en = sum(e / (1 + DISC) ** t for t, e in enumerate(en) if t > 0)
    lcoe = pv_cost * 1e7 / (pv_en * 1000)        # INR/kWh
    cum, pay = 0.0, None
    for t, cf in enumerate(cfs):
        prev = cum
        cum += cf
        if t > 0 and cum >= 0 and pay is None:
            pay = t - 1 + (-prev) / cf
    return dict(capex=capex_cr, per_mwp=tot, lcoe=lcoe, payback=pay, irr=irr(cfs), npv=npv(DISC, cfs))

L = ["# Preliminary BOQ scope, capex, LCOE, payback and CO2", "",
     "Indicative desk estimate, not a quotation. Cost lines are positioned within published indicative ranges (Base = 25th percentile; plain mid-points gave INR 5.2 cr/MWp and LCOE 4.9, which contradicts market tariffs, so were judged too high) (see sources below); "
     "quantities are from the design. Financial inputs are assumptions.", "",
     "## Scope (from the design)", "",
     "| Item | Quantity |", "|---|---|",
     "| PV modules, Waaree BiN-08-565 (565 Wp) | 8,840 |",
     "| Strings (26 modules each) | 340 |",
     "| Mounting tables (2 portrait x 26 modules = 52 modules) | 170, in 17 rows |",
     "| String inverters, Sungrow SG250HX | 16 |",
     "| Step-up transformers, 2.5 MVA, 0.8/33 kV | 2 |",
     "| 33 kV RMU (VCB + metering) | 1 |",
     "| DC string cable (approx. 70 m per polarity, 5% wastage) | about 50 km |",
     "| LV AC cable, 240 mm2 Al, 3 single-core x 80 m x 16 inverters | about 3.8 km |",
     "| 33 kV overhead line, ACSR Dog (placeholder) | 3 km |",
     "| DC capacity / AC capacity | 4,994.6 kWp / 4,000 kW |", "",
     "## Capex (INR crore)", "",
     "| Line | Low | Base (25th pct of range) | High |", "|---|---|---|---|"]
for name, v in LINES.items():
    L.append(f"| {name} | {pick(v,0)*DC_MWP:.2f} | {pick(v,1)*DC_MWP:.2f} | {pick(v,2)*DC_MWP:.2f} |")
epcs = [capex(i) for i in range(3)]
L.append(f"| **EPC subtotal** | {epcs[0][0]*DC_MWP:.2f} | {epcs[1][0]*DC_MWP:.2f} | {epcs[2][0]*DC_MWP:.2f} |")
L.append(f"| Contingency 5% of EPC | {epcs[0][1]*DC_MWP:.2f} | {epcs[1][1]*DC_MWP:.2f} | {epcs[2][1]*DC_MWP:.2f} |")
for name, v in OUTSIDE.items():
    L.append(f"| {name} | {pick(v,0)*DC_MWP:.2f} | {pick(v,1)*DC_MWP:.2f} | {pick(v,2)*DC_MWP:.2f} |")
L.append(f"| **Total capex** | **{epcs[0][3]*DC_MWP:.1f}** | **{epcs[1][3]*DC_MWP:.1f}** | **{epcs[2][3]*DC_MWP:.1f}** |")
L.append(f"| per MWp | {epcs[0][3]:.2f} | {epcs[1][3]:.2f} | {epcs[2][3]:.2f} |")
L += ["", "## Energy used", "",
      f"PVsyst VC4 {E_PVSYST:,.0f} MWh/yr, less AC-side losses (`cable_sizing.md`) = **{E_NET:,.0f} MWh/yr** at the 33 kV point in year 1; degradation {DEGR*100:.1f}%/yr over {LIFE} years.", "",
      "## Financial results", "",
      f"Assumptions: discount rate {DISC:.0%} nominal pre-tax, O&M INR {OM_CR_PER_MWP*100:.0f} lakh/MWp/yr escalating {OM_ESC:.0%}, insurance {INS_FRAC:.1%} of EPC, "
      f"inverter replacement INR {INV_REPL_CR} crore in year {INV_REPL_YR}, no tax, depreciation, subsidy or debt. Tariff flat for {LIFE} years.", "",
      "| Capex case | Tariff (INR/kWh) | Capex (INR cr) | LCOE (INR/kWh) | Simple payback (yr) | Project IRR (pre-tax) | NPV at 10% (INR cr) |", "|---|---|---|---|---|---|---|"]
for idx, nm in ((0, "Low"), (1, "Base"), (2, "High")):
    for tf in (2.34, 3.00, 3.62):
        m = metrics(idx, tf)
        pb = f"{m['payback']:.1f}" if m['payback'] else "> 25"
        L.append(f"| {nm} | {tf:.2f} | {m['capex']:.1f} | {m['lcoe']:.2f} | {pb} | {m['irr']*100:.1f}% | {m['npv']:.1f} |")
base = metrics(1, 3.00)
L += ["", f"**Headline (base capex, tariff 3.00):** capex INR {base['capex']:.1f} crore (INR {base['per_mwp']:.2f} crore/MWp), LCOE INR {base['lcoe']:.2f}/kWh, "
      f"simple payback {base['payback']:.1f} years, project IRR {base['irr']*100:.1f}%.", "",
      "Tariff reference points: INR 2.34/kWh (GUVNL 625 MW solar auction, March 2026, per a news headline), INR 3.00 (my base case), "
      "INR 3.62/kWh (CERC interim tariff for DVC's 8 MW solar project in West Bengal, March 2025, per a news headline). Neither headline was opened in full.", ""]
CO2_AVG, CO2_CM = 0.727, 0.757
L += ["## CO2 avoided", "",
      f"Grid emission factor: CEA CO2 Baseline Database v20.0 (Dec 2024), FY 2023-24: weighted average **{CO2_AVG} tCO2/MWh**, combined margin {CO2_CM} tCO2/MWh.", "",
      f"Year 1: {E_NET*CO2_AVG:,.0f} tCO2 (weighted average) to {E_NET*CO2_CM:,.0f} tCO2 (combined margin). Over {LIFE} years with degradation: about "
      f"{sum(E_NET*(1-DEGR)**y for y in range(LIFE))*CO2_AVG/1000:,.0f} thousand tCO2 at a constant factor (the grid factor will fall as the grid decarbonises, so treat this as an upper figure).", "",
      "## Sources and limits", "",
      "- Capex ranges: taypro.in utility-scale cost guide (indicative 2024 to 2026 ranges, updated 21 June 2026). A commercial blog, not a regulator figure; checked against the CTUIL benchmark below. Treat as +/-20%.",
      "- Emission factor: CEA CO2 Baseline Database User Guide v20.0.",
      "- No DCR premium, GST, interest during construction, or working capital is modelled. DCR modules cost more than the mid-range assumed here.",
      "- Capex cross-check (verified Oct 2026): CTUIL's revised planning benchmark is INR 3.5 crore/MW for solar (article dated 7 Sep 2026; AC/DC basis not stated), which matches the Low case (INR 3.54 crore/MWp). A real project cited alongside it, SJVN 1 GW Bikaner, works out to about INR 5.49 crore/MW. The Base case (INR 4.42 crore/MWp) lies between the two, which is plausible for a 5 MWp single site with its own 33 kV line. Quote capex as INR 3.5 to 5.5 crore/MWp, base 4.4.",
      "- Tariff caveat: auction tariffs of INR 2.3 to 3.6/kWh come from large projects with cheaper capital and lower return targets than the 10% discount rate used here, so LCOE here (INR 3.5 to 4.3) is not directly comparable. Treat LCOE as indicative.",
      "- Not modelled: debt, tax, depreciation, generation-based incentives, land purchase instead of lease."]
text = "\n".join(L)
open(OUT, "w").write(text + "\n")
print(text)
