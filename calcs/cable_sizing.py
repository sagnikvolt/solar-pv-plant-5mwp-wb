"""Cable sizing and AC-side losses for the 5 MWp plant (preliminary, desk study).

Scope: DC string cables, inverter-to-transformer LV cables, 2 x 2.5 MVA step-up transformers,
33 kV evacuation line. Every number marked ASSUMPTION is logged in ASSUMPTIONS.md.
Cable ampacity values are typical manufacturer-datasheet figures and must be re-checked against the
actual cable chosen. Run:  python calcs/cable_sizing.py
"""
import math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "calcs", "output", "cable_sizing.md")

# ---- inputs from the design -------------------------------------------------
ISC, IMP, VMP = 13.75, 12.97, 43.56      # module STC (datasheet)
N_SERIES, N_STRINGS = 26, 340
REAR_GAIN = 0.10                          # bifacial current allowance (ASSUMPTION, as in string sizing)
RHO_CU_90C = 0.0225                       # ohm.mm2/m, copper at ~90 C
RHO_AL_90C = 0.0368                       # ohm.mm2/m, aluminium at ~90 C
I_AC_INV = 180.5                          # SG250HX max AC current at 800 V (datasheet, verify)
V_AC = 800.0

lines = ["# Cable sizing and AC-side losses (preliminary)", "",
         "Desk calculation. Ampacities are typical datasheet values, rates and lengths are assumptions (see ASSUMPTIONS.md).", ""]

# ---- 1. DC string cable ------------------------------------------------------
i_design = 1.25 * ISC * (1 + REAR_GAIN)           # IEC 62548 style: 1.25 x Isc, with bifacial allowance
T_MAX, T_REF, T_AMB, GROUP = 120.0, 60.0, 70.0, 0.80   # H1Z2Z2-K 120 C, cable-in-sun ambient 70 C (ASSUMPTION), grouping 0.8
k_t = math.sqrt((T_MAX - T_AMB) / (T_MAX - T_REF))
AMP_REF = {4: 55.0, 6: 70.0, 10: 98.0}              # A at 60 C in free air, typical H1Z2Z2-K datasheet
lines += ["## 1. DC string cables (copper, H1Z2Z2-K type, 1.5 kV DC)", "",
          f"Design current = 1.25 x Isc x (1 + {REAR_GAIN:.0%} rear gain) = **{i_design:.1f} A**. "
          f"Temperature derating {k_t:.2f} (cable at {T_AMB:.0f} C ambient, rated {T_MAX:.0f} C), grouping {GROUP:.2f}.", "",
          "| One-way length (m) | Section (mm2) | Ampacity after derating (A) | Voltage drop at Imp | % of string Vmp | Pass |", "|---|---|---|---|---|---|"]
VD_LIMIT = 1.0
string_vdrop = {}
for L in (40, 70, 100, 130):
    for a in (4, 6, 10):
        iz = AMP_REF[a] * k_t * GROUP
        vd = 2 * L * IMP * RHO_CU_90C / a
        pct = vd / (N_SERIES * VMP) * 100
        if iz >= i_design and pct <= VD_LIMIT:
            string_vdrop[L] = (a, pct)
            lines.append(f"| {L} | **{a}** | {iz:.0f} | {vd:.1f} V | {pct:.2f}% | yes |")
            break
avg_pct = sum(p for _, p in string_vdrop.values()) / len(string_vdrop)
lines += ["", f"Rule used: smallest standard section meeting ampacity and a {VD_LIMIT:.1f}% drop at Imp. "
          "4 mm2 serves strings up to about 70 m, 6 mm2 beyond that. PVsyst uses a 1.5% DC ohmic loss at STC; the string cables stay below it.", ""]

# ---- 2. LV AC cables (inverter -> transformer) -------------------------------
LV_LEN = 80.0   # m, ASSUMPTION: inverters on the array, transformer pads at the block centres
lines += ["## 2. Inverter-to-transformer AC cables (aluminium XLPE, 1.1 kV class, 800 V)", "",
          f"Inverter current {I_AC_INV} A at {V_AC:.0f} V, unity power factor, {LV_LEN:.0f} m run. Ampacity after buried-installation derating 0.80 (ASSUMPTION). Target: drop at rated current at most 0.5%.", "",
          "| Section (mm2) | Resistance at 90 C (ohm/km) | Ampacity after derating (A) | Drop at rated current | Pass |", "|---|---|---|---|---|"]
AMP_AL = {95: 205, 120: 235, 150: 265, 185: 300, 240: 350, 300: 395}  # A, buried, typical XLPE Al 3x1C
X_LV = 0.08                                                           # ohm/km
chosen_lv = None
for a in AMP_AL:
    r = RHO_AL_90C / a * 1000
    iz = AMP_AL[a] * 0.80
    dv = math.sqrt(3) * I_AC_INV * (LV_LEN / 1000) * r
    pct = dv / V_AC * 100
    ok = iz >= I_AC_INV * 1.0 and pct <= 0.5
    lines.append(f"| {a} | {r:.3f} | {iz:.0f} | {pct:.2f}% | {'yes' if ok else 'no'} |")
    if ok and chosen_lv is None:
        chosen_lv = (a, pct, r)
a_lv, pct_lv, r_lv = chosen_lv
lines += ["", f"Chosen: **{a_lv} mm2 aluminium** (3 single-core per inverter). Loss at rated current {pct_lv:.2f}%.", ""]

# ---- 3. Transformers ---------------------------------------------------------
S_TR, N_TR = 2.5, 2
INV_PER_TR = 8
load_kva = INV_PER_TR * 250
lines += ["## 3. Step-up transformers", "",
          f"2 x {S_TR} MVA, 0.8/33 kV, Dyn11, ONAN, outdoor. Each takes {INV_PER_TR} inverters = {load_kva/1000:.1f} MVA at 30 C rating "
          f"({load_kva/(S_TR*1000):.0%} loading), less in summer when inverters derate (225 kVA at 40 C). Typical losses (ASSUMPTION, check vendor): "
          "no-load 2.1 kW, load loss 20 kW at rated.", ""]

# ---- 4. 33 kV evacuation -----------------------------------------------------
P_MW, V_HV = 4.0, 33.0
i_hv = P_MW * 1000 / (math.sqrt(3) * V_HV)
LEN_KM = 3.0      # ASSUMPTION: distance to the nearest 33/11 kV substation (unknown until the plot is chosen)
R_HV, X_HV = 0.27, 0.40   # ohm/km, ACSR Dog (100 mm2) typical
dv_hv = math.sqrt(3) * i_hv * LEN_KM * R_HV
loss_hv_kw = 3 * i_hv ** 2 * R_HV * LEN_KM / 1000
lines += ["## 4. 33 kV evacuation", "",
          f"Full output {P_MW:.1f} MW at {V_HV:.0f} kV: **{i_hv:.0f} A**. Concept: 33 kV RMU (VCB + metering) at the plant, then a {LEN_KM:.0f} km overhead line "
          f"(ACSR Dog 100 mm2, ampacity about 270 A) to the grid substation. Resistive drop {dv_hv/1000/V_HV*100:.2f}% of 33 kV; loss {loss_hv_kw:.1f} kW at full output. "
          "The line length and the grid substation are placeholders until the plot and the DISCOM feasibility are known.", ""]

# ---- 5. AC-side energy loss (not in PVsyst VC4) ------------------------------
E_VC4 = 7078.053   # MWh at inverter output / energy injected (PVsyst, no AC wiring or transformer loss)
FORM = 0.20        # mean(P^2)/Prated^2 over the year (ASSUMPTION; sets the average I^2R loss)
P_RATED_KW = 4000.0
lv_loss_rated_kw = 16 * 3 * I_AC_INV ** 2 * (LV_LEN / 1000) * r_lv / 1000   # 3-phase: 3 I2R
tr_load_kw = N_TR * 20.0
tr_noload_kw = N_TR * 2.1
mwh_lv = lv_loss_rated_kw * FORM * 8760 / 1000
mwh_trl = tr_load_kw * FORM * 8760 / 1000
mwh_trn = tr_noload_kw * 8760 / 1000
mwh_hv = loss_hv_kw * FORM * 8760 / 1000
total = mwh_lv + mwh_trl + mwh_trn + mwh_hv
E_NET = E_VC4 - total
lines += ["## 5. AC-side energy loss (PVsyst VC4 does not model it)", "",
          "| Item | Loss at rated (kW) | Annual loss (MWh) |", "|---|---|---|",
          f"| Inverter-to-transformer cables | {lv_loss_rated_kw:.1f} | {mwh_lv:.1f} |",
          f"| Transformer load loss | {tr_load_kw:.1f} | {mwh_trl:.1f} |",
          f"| Transformer no-load loss | {tr_noload_kw:.1f} | {mwh_trn:.1f} |",
          f"| 33 kV line | {loss_hv_kw:.1f} | {mwh_hv:.1f} |",
          f"| **Total** | | **{total:.1f} ({total/E_VC4*100:.2f}% of {E_VC4:,.0f})** |", "",
          f"Energy delivered at the 33 kV point (before any plant auxiliary use): **{E_NET:,.0f} MWh/yr**. "
          f"The load-factor term (mean P^2 / Prated^2 = {FORM}) is an assumption; it can be replaced by the real hourly output from PVsyst.", ""]
open(OUT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
with open(OUT.replace("cable_sizing.md", "net_energy.txt"), "w") as f:
    f.write(f"{E_NET:.1f}\n{total:.1f}\n")
