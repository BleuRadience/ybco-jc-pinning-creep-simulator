# YBCO Jc + Pinning + Creep Simulator (Calibrated to 2025–2026 Literature)

This open-source Python tool simulates the critical temperature (Tc) dome, critical current density (Jc), vortex creep behavior, pinning enhancements (additive manufacturing monocrystalline, BZO nanoparticles, hybrid, coherent APCs), anisotropy, overdoped regimes, and basic space-hardening features in YBCO (YBa₂Cu₃O₇₋δ).

**Key Features**
- Empirical Tc parabolic dome with phase flags (insulator at δ > 0.5, pseudogap suppression underdoped)
- Jc model with field dependence, defect size scaling, anisotropy, and coherent pinning bonus
- Logarithmic vortex creep with U_p scaling for mitigation (reduces relative fade 40–50% in high-pinning regimes)
- Monte Carlo uncertainty, error propagation, and multi-objective defect optimization
- Space mode (radiation hardening + low-mass scaling for foam/composite applications)
- Calibrated to 2025–2026 literature (AM monocrystalline benchmarks, coherent APCs, electrochemical overdoping, TcSUH-related studies)

**Installation**
```bash
pip install -r requirements.txt

Quick Example

Pythonimport numpy as np
from ybco_simulator import tc_parabolic, jc_model, pinning_factor, run_creep_simulation

delta = 0.07
Tc = tc_parabolic(delta, Tc_max=92.0, delta_opt=0.036, a=231.4)
pinning = pinning_factor(defect_density=0.15, defect_size_nm=10, defect_type='hybrid', coherent_bonus=1.5)
Jc = jc_model(delta, B=5.0, T=77.0, pinning_factor=pinning)
print(f"Tc: {Tc:.1f} K | Jc (pre-creep): {Jc:.2e} A/m²")

# Creep example
Jc_after_creep = run_creep_simulation(Jc, t=1000, T=77.0, U_p_factor=3.5)
print(f"Jc after 1000 s creep: {Jc_after_creep:.2e} A/m²")

Literature Calibration References

Additive-manufactured monocrystalline YBCO (Nature Communications 2025)
Coherent artificial pinning centers (BaHfO₃/BaZrO₃, 2025–2026 papers)
Overdoped YBCO via electrochemical oxidation
TcSUH thin-film and pinning studies

Disclaimer
This is a simulation tool only. Results are predictive, based on public literature, and require experimental validation. No warranty expressed or implied.
License
MIT License – see LICENSE file.

Citation
DOI available on Zenodo (after upload).
Developed by Cassandra (@BleuRadience, Houston, TX) with iterative assistance from AI.

Contact
Open to questions, forks, or collaborations.
