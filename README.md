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
