# Interview Q&A: draft answers

**DRAFT written by Claude from this project's numbers. Rewrite every answer in your own words before an interview**, and only keep what you can explain and defend. Numbers come from `README.md`, `ASSUMPTIONS.md` and `calcs/output/`. Answers 16, 17 and 20 are general engineering knowledge, not project results.

**1. Walk me through your plant design in two minutes.**
A 5 MWp (4,994.6 kWp) fixed-tilt ground-mount plant using Kolkata's climate. 8,840 Waaree 565 Wp bifacial TOPCon modules in 340 strings of 26, on 16 Sungrow SG250HX string inverters (4 MW AC, DC/AC 1.25). Tilt 20°, south-facing, row pitch 8.0 m. Energy comes from PVsyst with a 3D shading scene: 7,078 MWh/yr, 1,417 kWh/kWp, PR 85.6%. Two transformers of 2.5 MVA step up to 33 kV, and about 2.3% is lost on the AC side, leaving roughly 6,917 MWh/yr at the grid point. P90 is 6,458 MWh/yr from an assumed uncertainty budget.

**2. How did you decide the number of modules per string? Which temperature did you use and why?**
The string must stay under 1,500 V at the coldest temperature and above the inverter's 600 V MPPT minimum at the hottest. I used the record minimum ambient of 3.4 °C (NASA POWER) for Voc: 54.81 V per module, so 27 modules is the limit. I chose 26 because 27 would reach 1,480 V, only 20 V (1.3%) under 1,500 V, whereas 26 gives 1,425 V (5% margin). (With my first module choice, a 580 W class module, 27 reached 1,497 V.) At the hot end I used a cell temperature of 75.8 °C (NOCT model at 47 °C ambient).

**3. Why does Voc go up in cold weather? What happens if a string exceeds 1500 V?**
Silicon's bandgap widens and recombination falls as temperature drops, so Voc rises (about 0.26%/°C for this module). Above the rated system voltage the inverter input and module insulation are over-stressed: damage, a safety hazard and a voided warranty.

**4. What is a performance ratio? What was yours, and what drives it down?**
PR is the energy delivered divided by the energy an ideal plant would give for the same irradiation: it removes the effect of the weather. Mine is 85.6%. It is pulled down by temperature, shading, soiling, mismatch, cable and inverter losses. It is high partly because bifacial gain (about 4.4%) offsets some of those losses, and partly because the AC-side losses are not in the PVsyst figure. Including them, it would be about 83.7% (my arithmetic).

**5. Explain the biggest losses in your loss diagram.**
From the VC4 PVsyst loss diagram: temperature 5.59% is the largest, then soiling 3.00% (my assumption), module and string mismatch 2.05%, IAM (reflection at the glass) 2.01%, near shading 1.75%, inverter efficiency 1.61% and inverter clipping 1.22% (from the 1.25 DC/AC ratio), unavailability 1.01%, and DC wiring 0.93%. Bifaciality adds energy back (rear irradiance, 113 kWh/m²). The exported diagram image in `showcase/images/` is preliminary and clipped at the edges.

**6. What is the difference between P50 and P90? Where does the uncertainty come from?**
P50 is the yield exceeded 50% of the time, P90 exceeded 90% of the time (what lenders use). I combined independent uncertainties by root-sum-square: data source 5.0%, interannual 3.2%, transposition 2.0%, PV model 2.0%, module 1.5%, soiling 1.0%, availability 0.5%. That gives 6.84%, so P90 = P50 × (1 − 1.2816 × 0.0684) = 6,458 MWh/yr. The percentages are my assumptions, not measured.

**7. Why did you pick a string (or central) inverter?**
At 5 MW with 340 strings, string inverters give many MPPTs (192 inputs), so partial shading or mismatch hurts less, plant availability is higher because one failure takes out 250 kW, not the whole plant, and they are easier to service. Central inverters have a lower cost per kW but need combiner boxes and a single point of failure.

**8. What DC/AC ratio did you choose, and what is the trade-off?**
1.249. A higher ratio gives more energy in the mornings and evenings and during cloud, at the price of clipping at midday and extra DC cost. The ratio also depends on inverter derating: the SG250HX gives 250 kVA at 30 °C but 225 kVA at 40 °C.

**9. What are ALMM and DCR, and why do they matter for module choice in India?**
ALMM is MNRE's approved list of module manufacturers: projects in government schemes and many tenders must use listed modules. DCR means the module cells are made in India, required for certain subsidies and schemes. **I have not yet verified this module's status**; check the MNRE site before quoting it.

**10. How did you choose the tilt angle and row pitch?**
PVsyst's quick optimisation put 20° within 0.1% of the best transposition (30° would be 0.6% below), and a lower tilt also allows a shorter row pitch. For pitch, 6.4 m is the minimum for no shading from 9:00 to 15:00 on 21 December. I ran 6.4, 7.0, 8.0 and 9.0 m: energy rose 6,938 → 7,121 MWh but land rose 3.20 → 4.45 ha. I adopted 8.0 m as the point where the gain per extra hectare drops off.

**11. How do Meteonorm, PVGIS and NASA POWER differ? Which did you trust and why?**
Annual GHI at Kolkata: Meteonorm 1,574, NASA POWER 1,669, PVGIS 1,730 kWh/m². They use different satellite/reanalysis sources and periods. I used Meteonorm because it is the lowest, so the estimate is conservative, and it is PVsyst's native source. The spread of up to 10% is why the data source is the largest term in the P90 budget.

**12. How did your PVsyst result compare with SAM? What caused the difference?**
PVsyst's monofacial case came out 4.6% and 6.6% below SAM and PVGIS after removing shading. Scaling SAM's irradiance to the Meteonorm level brought the gap to 0.9%, so the gap is the irradiance database, not the model. Caveat: SAM and PVGIS both use ERA5, so they don't independently validate the irradiance choice.

**13. How do you size a DC string cable? Why use 1.25 × Isc?**
Design current = 1.25 × Isc (the safety factor for irradiance above 1,000 W/m²) × 1.10 for bifacial rear gain = 18.9 A. Then derate for temperature (0.91) and grouping (0.80), choose the cross-section that carries it, and check voltage drop. Result: 4 mm² copper up to about 70 m.

**14. What is the voltage drop limit you used for DC and AC cables?**
DC string cables: 1.0% at Imp. Inverter-to-transformer AC cables: 0.5% at rated current, which needed 240 mm² aluminium (185 mm² gave 0.62%).

**15. How is the plant evacuated to the grid? What equipment sits between the inverter and the 33 kV line?**
Inverter (800 V AC) → LV cable → 2.5 MVA 0.8/33 kV Dyn11 transformer (8 inverters each) → 33 kV RMU with vacuum circuit breaker and metering → overhead line (3 km ACSR Dog, a placeholder) → grid substation. The plot and the substation are not fixed yet.

**16. What earthing does a solar plant need (DC side, AC side, lightning)?** *(general knowledge, not in this design yet)*
Equipotential bonding of module frames and structures to an earth grid; separate system earthing for the transformer neutral and LV side; an earth grid with enough electrodes to keep resistance low (commonly below 1 Ω for a plant this size, check the project specification); lightning protection with air terminals and surge protection devices on the DC and AC sides. The single-line diagram I will draw shows the earthing concept, not its detailed design.

**17. How does soiling affect yield, and how would you decide on a cleaning schedule?** *(general knowledge, plus my 3% assumption)*
Dust blocks light and reduces output. I assumed a flat 3%. A real schedule compares the cleaning cost against the energy value of the soiling loss, using measured soiling-station data. Monsoon rain cleans modules from June to September, so cleaning matters most in the dry season.

**18. What is bifacial gain, and would bifacial modules make sense at your site?**
Bifacial modules collect light on the rear. PVsyst gave +4.4% for this design (7,006 vs 6,712 MWh at 7.0 m), with ground albedo 0.25 and 1.0 m clearance. Wider row pitch and a higher albedo increase it. Whether it pays depends on the extra module cost; I did not model that trade-off.

**19. How did you estimate LCOE? What is the biggest cost driver?**
Capex from published indicative cost ranges and the BOQ quantities, plus O&M, insurance and one inverter replacement, discounted at 10% over 25 years with 0.4%/yr degradation. Modules are the largest line (about 40%). The numbers are indicative: my lowest-cost case gives ₹3.5/kWh, above recent auction tariffs of ₹2.3 to 3.6, so I treat it as a range, not a result.

**20. What would you do differently with a real topographic survey and soil report?** *(general knowledge)*
Lay out rows to the real terrain and shading, choose foundations (piles or ballast) from the soil data, size drainage for West Bengal monsoon flooding, confirm the plot's land area and the real 33 kV connection point, and replace placeholder cable lengths with measured ones.
