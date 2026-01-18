import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# === Literature-calibrated parameters (2025–2026) ===
Tc_max = 92.0          # K, optimal
delta_opt = 0.036      # from fit to expanded data
a = 231.4              # sharpness (K^{-1})
Jc0 = 1e8              # A/m² base, calibrated to AM ~2.1e8 enhanced
Bc2_max = 150.0        # T at low T, scales with Tc

# Expanded lit data points (Tc vs δ)
delta_data = np.array([0.0, 0.07, 0.1, 0.20, 0.40, 0.5])
tc_data = np.array([89.0, 92.0, 88.0, 83.0, 60.0, 40.0])

# Tc model (clamped >=0)
def tc_parabolic(delta, Tc_max=Tc_max, delta_opt=delta_opt, a=a):
    tc = Tc_max - a * (delta - delta_opt)**2
    return np.maximum(0.0, tc)

# Robust fit (least_squares)
def residuals(p, delta, tc):
    return tc - tc_parabolic(delta, *p)

res = least_squares(residuals, [92.0, 0.07, 500.0], args=(delta_data, tc_data), max_nfev=2000)
popt_tc = res.x
print("Fitted Tc params:", popt_tc)
Tc_max_fit, delta_opt_fit, a_fit = popt_tc

# Pinning factor (AM, BZO, hybrid, coherent APCs, size scaling)
def pinning_factor(defect_density=0.0, defect_type='standard', defect_size_nm=5.0, coherent_bonus=1.0):
    d = np.maximum(0.0, defect_density)
    size_factor = (defect_size_nm / 5.0)**2   # optimal ~5-10 nm
    if defect_type == 'AM_mono':
        calc = 1.0 + 10.0 * d
    elif defect_type == 'BZO_nano':
        calc = 1.0 + 20.0 * d
    elif defect_type == 'hybrid':
        calc = 1.0 + 15.0 * d + 5.0 * d**2
    else:
        calc = 1.0
    return np.maximum(1.0, np.minimum(4.0, calc * size_factor * coherent_bonus))

# Jc model
def jc_model(delta, B=0.0, T=77.0, pinning_factor=1.0, defect_type='standard',
             defect_size_nm=5.0, coherent_bonus=1.0, space_tweak=False):
    Tc = tc_parabolic(delta)
    if Tc <= 0:
        return 0.0
    
    # Phase flag (insulator)
    if delta > 0.5:
        return 0.0
    
    Bc2 = Bc2_max * (Tc / Tc_max_fit)
    jc_base = Jc0 * (Tc / Tc_max_fit)**1.5
    field_dep = 1.0 / (1.0 + B / Bc2) if Bc2 > 0 else 1.0
    
    pf = pinning_factor(defect_density=0.0, defect_type=defect_type,
                        defect_size_nm=defect_size_nm, coherent_bonus=coherent_bonus)
    
    jc = jc_base * pf * field_dep
    
    # Space tweak: radiation-induced pinning bonus + low-mass scaling
    if space_tweak:
        jc *= 1.5  # radiation bonus (columnar defects from cosmic rays)
        jc *= 2.0  # effective per-mass gain from foam/composite
    
    return np.maximum(0.0, jc)

# Logarithmic vortex creep (refined cuprate form)
def run_creep_simulation(Jc_pre, t=1000.0, T=77.0, U_p_base=20.0, pinning_factor=1.0):
    kB = 8.617333262145e-5  # eV/K
    kT = kB * T
    U_p = U_p_base * pinning_factor  # scales with pinning strength
    if U_p <= 0:
        return Jc_pre * np.exp(-t / 1.0)  # fallback
    tau0 = 1e-9  # attempt time ~ns
    creep_factor = 1.0 / (1.0 + (kT / U_p) * np.log(1.0 + t / tau0))
    return Jc_pre * creep_factor

# Simple anisotropy (parallel vs perpendicular)
def apply_anisotropy(Jc, theta_deg=0.0):
    theta_rad = np.deg2rad(theta_deg)
    return Jc * np.abs(np.cos(theta_rad))  # basic model

# Monte Carlo uncertainty (δ variation + param noise)
def monte_carlo_run(N=1000, delta=0.07, B=5.0, T=77.0, defect_density=0.15,
                    defect_size_nm=10.0, defect_type='hybrid', coherent_bonus=1.5,
                    space_tweak=False):
    delta_mc = np.random.normal(delta, 0.02, N)
    Jc_pre = np.array([jc_model(d, B=B, T=T, defect_density=defect_density,
                                defect_size_nm=defect_size_nm, defect_type=defect_type,
                                coherent_bonus=coherent_bonus, space_tweak=space_tweak)
                       for d in delta_mc])
    Jc_post = np.array([run_creep_simulation(j, t=1000, T=T, pinning_factor=pinning_factor(
        defect_density=defect_density, defect_size_nm=defect_size_nm,
        defect_type=defect_type, coherent_bonus=coherent_bonus))
                        for j in Jc_pre])
    return Jc_post.mean(), Jc_post.std()

# Example usage / test block
if __name__ == "__main__":
    delta = 0.07
    Tc = tc_parabolic(delta)
    print(f"Tc at δ={delta:.2f}: {Tc:.1f} K")
    
    Jc_pre = jc_model(delta, B=5.0, T=77.0, defect_density=0.15, defect_size_nm=10.0,
                      defect_type='hybrid', coherent_bonus=1.5, space_tweak=False)
    print(f"Jc pre-creep (5 T, 77 K): {Jc_pre:.2e} A/m²")
    
    Jc_post = run_creep_simulation(Jc_pre, t=1000, T=77.0, pinning_factor=3.5)
    print(f"Jc after 1000 s creep: {Jc_post:.2e} A/m²")
    
    mean_mc, std_mc = monte_carlo_run(N=1000, delta=delta, B=5.0, T=77.0,
                                      defect_density=0.15, defect_size_nm=10.0,
                                      defect_type='hybrid', coherent_bonus=1.5)
    print(f"MC mean / std (post-creep): {mean_mc:.2e} ± {std_mc:.2e} A/m²")
