"""
String sizing and array configuration for the 5 MWp plant.

Checks performed (IEC 62548 practice):
  1. Max string Voc at record-minimum cell temperature  <= inverter max DC voltage (hard limit)
  2. Min string Vmp at hot cell temperature             >= inverter MPPT min voltage
  3. Max string Vmp at cold cell temperature            <= inverter MPPT max voltage (else clipping/derate)
  4. Parallel strings per MPPT limited by the MPPT's max short-circuit current
  5. Plant block: number of strings, inverters and actual DC/AC ratio

Usage:
    python calcs/string_sizing.py [--config calcs/config/design_inputs.json]

All inputs come from the JSON config. Values marked null must be filled in from
datasheets / site data before the script will run.
"""
import argparse
import json
import math
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(HERE, "config", "design_inputs.json")
OUTPUT_DIR = os.path.join(HERE, "output")


# ---------------------------------------------------------------- helpers
def load_config(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    missing = []
    for section in ("module", "inverter", "site", "design"):
        for key, val in cfg[section].items():
            if key.startswith("_"):
                continue
            if val is None and not key.endswith("_optional"):
                missing.append(f"{section}.{key}")
    if missing:
        sys.exit("Fill these values in the config first:\n  " + "\n  ".join(missing))
    return cfg


def temp_adjust(value_stc, coeff_pct_per_c, t_cell):
    """Linear temperature correction from STC (25 °C)."""
    return value_stc * (1 + coeff_pct_per_c / 100.0 * (t_cell - 25.0))


def cell_temp_noct(t_amb, noct, irradiance=1000.0):
    """NOCT model: Tcell = Tamb + (NOCT - 20)/800 * G."""
    return t_amb + (noct - 20.0) / 800.0 * irradiance


# ---------------------------------------------------------------- core
def size_strings(cfg):
    m, inv, site, d = cfg["module"], cfg["inverter"], cfg["site"], cfg["design"]

    beta_vmp = m.get("beta_Vmp_pct_per_C_optional")
    vmp_coeff_note = "datasheet β(Vmp)"
    if beta_vmp is None:
        beta_vmp = m["gamma_Pmax_pct_per_C"]
        vmp_coeff_note = "γ(Pmax) used as β(Vmp) approximation"

    t_cell_min = site["T_amb_record_min_C"]                      # dawn: cell ≈ ambient
    t_cell_max = cell_temp_noct(site["T_amb_design_max_C"], m["NOCT_C"])

    voc_cold = temp_adjust(m["Voc_V"], m["beta_Voc_pct_per_C"], t_cell_min)
    vmp_hot = temp_adjust(m["Vmp_V"], beta_vmp, t_cell_max)
    vmp_cold = temp_adjust(m["Vmp_V"], beta_vmp, t_cell_min)
    isc_hot = temp_adjust(m["Isc_A"], m["alpha_Isc_pct_per_C"], t_cell_max)
    isc_design = isc_hot * (1 + d["bifacial_rear_gain_frac"])

    n_max_voltage = math.floor(inv["Vdc_max_V"] / voc_cold)
    n_min_mppt = math.ceil(inv["Vmppt_min_V"] / vmp_hot)
    n_max_mppt = math.floor(inv["Vmppt_max_V"] / vmp_cold)

    n_chosen = d.get("modules_per_string_optional") or n_max_voltage
    strings_per_mppt_max = math.floor(inv["Isc_max_per_MPPT_A"] / isc_design)
    strings_per_inv_max = strings_per_mppt_max * inv["n_MPPT"]

    string_kwp = n_chosen * m["Pmax_W"] / 1000.0
    n_strings = round(d["target_DC_kWp"] / string_kwp)
    dc_kwp = n_strings * string_kwp
    n_inverters = max(1, round(dc_kwp / (inv["Pac_kW"] * d["target_DC_AC_ratio"])))
    ac_kw = n_inverters * inv["Pac_kW"]
    strings_per_inv = math.ceil(n_strings / n_inverters)

    checks = {
        "Voc_cold x N <= Vdc_max": n_chosen * voc_cold <= inv["Vdc_max_V"],
        "Vmp_hot x N >= Vmppt_min": n_chosen * vmp_hot >= inv["Vmppt_min_V"],
        "Vmp_cold x N <= Vmppt_max": n_chosen * vmp_cold <= inv["Vmppt_max_V"],
        "Strings/inverter within MPPT current limit": strings_per_inv <= strings_per_inv_max,
        "N within feasible range": n_min_mppt <= n_chosen <= n_max_voltage,
    }

    return {
        "inputs_note": vmp_coeff_note,
        "T_cell_min_C": t_cell_min,
        "T_cell_max_C": t_cell_max,
        "Voc_cold_V": voc_cold,
        "Vmp_hot_V": vmp_hot,
        "Vmp_cold_V": vmp_cold,
        "Isc_hot_A": isc_hot,
        "Isc_design_A": isc_design,
        "Isc_x1.25_for_cable_fuse_A": isc_design * 1.25,
        "N_max_voltage": n_max_voltage,
        "N_min_mppt": n_min_mppt,
        "N_max_mppt": n_max_mppt,
        "N_chosen": n_chosen,
        "String_Voc_cold_V": n_chosen * voc_cold,
        "String_Vmp_hot_V": n_chosen * vmp_hot,
        "String_Vmp_cold_V": n_chosen * vmp_cold,
        "Strings_per_MPPT_max": strings_per_mppt_max,
        "Strings_per_inverter_max": strings_per_inv_max,
        "String_kWp": string_kwp,
        "N_strings": n_strings,
        "N_modules": n_strings * n_chosen,
        "DC_kWp": dc_kwp,
        "N_inverters": n_inverters,
        "AC_kW": ac_kw,
        "DC_AC_ratio": dc_kwp / ac_kw,
        "Strings_per_inverter": strings_per_inv,
        "checks": checks,
    }


def to_markdown(cfg, r):
    m, inv = cfg["module"], cfg["inverter"]
    ok = lambda b: "PASS" if b else "**FAIL**"
    lines = [
        "# String Sizing Results",
        f"_Generated {date.today().isoformat()} by `calcs/string_sizing.py`_\n",
        f"**Module:** {m['model']}  |  **Inverter:** {inv['model']}\n",
        "## Temperatures",
        f"- Min cell temperature (record min ambient): {r['T_cell_min_C']:.1f} °C",
        f"- Max cell temperature (NOCT model, 1000 W/m²): {r['T_cell_max_C']:.1f} °C",
        f"- Vmp coefficient: {r['inputs_note']}\n",
        "## Per-module values",
        "| Quantity | Value |", "|---|---|",
        f"| Voc at min temp | {r['Voc_cold_V']:.2f} V |",
        f"| Vmp at max temp | {r['Vmp_hot_V']:.2f} V |",
        f"| Vmp at min temp | {r['Vmp_cold_V']:.2f} V |",
        f"| Isc at max temp (incl. bifacial gain) | {r['Isc_design_A']:.2f} A |",
        f"| 1.25 × Isc (cable/fuse sizing basis) | {r['Isc_x1.25_for_cable_fuse_A']:.2f} A |\n",
        "## String length",
        f"- Max modules (DC voltage limit): **{r['N_max_voltage']}**",
        f"- Min modules (MPPT min voltage, hot): **{r['N_min_mppt']}**",
        f"- Max modules before MPPT max (cold): {r['N_max_mppt']}",
        f"- **Chosen: {r['N_chosen']} modules/string** → Voc,max {r['String_Voc_cold_V']:.0f} V, "
        f"Vmp range {r['String_Vmp_hot_V']:.0f}–{r['String_Vmp_cold_V']:.0f} V\n",
        "## Plant configuration",
        "| Quantity | Value |", "|---|---|",
        f"| String power | {r['String_kWp']:.2f} kWp |",
        f"| Number of strings | {r['N_strings']} |",
        f"| Number of modules | {r['N_modules']} |",
        f"| DC capacity | {r['DC_kWp']:.1f} kWp |",
        f"| Inverters | {r['N_inverters']} × {inv['Pac_kW']} kW = {r['AC_kW']:.0f} kW |",
        f"| DC/AC ratio | {r['DC_AC_ratio']:.3f} |",
        f"| Strings per inverter (max allowed) | {r['Strings_per_inverter']} ({r['Strings_per_inverter_max']}) |\n",
        "## Checks",
        "| Check | Result |", "|---|---|",
    ]
    lines += [f"| {k} | {ok(v)} |" for k, v in r["checks"].items()]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    args = ap.parse_args()
    cfg = load_config(args.config)
    r = size_strings(cfg)
    md = to_markdown(cfg, r)
    print(md)
    stem = os.path.splitext(os.path.basename(args.config))[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"string_sizing_{stem}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Saved -> {os.path.relpath(out)}")
    if not all(r["checks"].values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
