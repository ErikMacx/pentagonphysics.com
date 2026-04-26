"""
Compute the WIDTH of the recombination era and the distribution shape.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

phi = (1 + np.sqrt(5)) / 2
sigma = 1 / phi
alpha = 1 / 137.035999207
m_e_eV = 0.51099895e6
E_H = alpha**2 * m_e_eV / 2
eta = 6.104e-10
zeta3 = 1.20206
T_CMB = 2.725

# PP cosmology
H0_PP = 70.5
Omega_L = phi**(-1)
Omega_m = 1 - Omega_L
H0_SI = H0_PP * 1e3 / 3.0857e22

def saha_x(T_eV):
    """Return ionization fraction x at temperature T."""
    # Saha: x²/(1-x) = (1/n_b) × (m_e T/(2π))^(3/2) × exp(-E_H/T)
    # n_b = η × 2ζ(3)/π² × T³
    n_b_coeff = eta * 2 * zeta3 / np.pi**2  # × T³
    rhs_coeff = (m_e_eV / (2 * np.pi))**(1.5)  # × T^(3/2) × exp(-E_H/T)
    
    # x²/(1-x) = rhs_coeff × T^(3/2) × exp(-E_H/T) / (n_b_coeff × T³)
    # = rhs_coeff / n_b_coeff × T^(-3/2) × exp(-E_H/T)
    K = rhs_coeff / n_b_coeff * T_eV**(-1.5) * np.exp(-E_H / T_eV)
    
    # x²/(1-x) = K → x² + Kx - K = 0 → x = (-K + √(K²+4K))/2
    x = (-K + np.sqrt(K**2 + 4*K)) / 2
    return min(max(x, 0), 1)

def T_to_z(T_eV):
    return T_eV * 11604.5 / T_CMB - 1

def z_to_t(z):
    """Time at redshift z using PP cosmology."""
    a = 1 / (1 + z)
    def integ(a_val):
        return 1.0 / (a_val * np.sqrt(Omega_m / a_val**3 + Omega_L))
    result, _ = quad(integ, 1e-10, a)
    return result / H0_SI / (365.25 * 24 * 3600)  # years

# Compute ionization fraction vs temperature/redshift
print("=" * 70)
print("RECOMBINATION PROFILE")
print("=" * 70)

print(f"\n{'T (eV)':>8} {'z':>7} {'x (ion frac)':>12} {'t (kyr)':>10}")
print("-" * 42)

T_range = np.linspace(0.45, 0.15, 30)
results = []
for T in T_range:
    x = saha_x(T)
    z = T_to_z(T)
    if z > 0:
        t = z_to_t(z)
        results.append((T, z, x, t))
        if abs(x - 0.9) < 0.05 or abs(x - 0.5) < 0.05 or abs(x - 0.1) < 0.05 or abs(x - 0.01) < 0.02:
            print(f"{T:8.4f} {z:7.0f} {x:12.4f} {t/1000:10.1f}")

# Find specific ionization fractions
print(f"\nKey thresholds:")
for x_target, label in [(0.99, "1% recombined"), (0.90, "10% recombined"), 
                          (0.50, "50% recombined"), (0.10, "90% recombined"),
                          (0.01, "99% recombined")]:
    def resid(T):
        return saha_x(T) - x_target
    try:
        T_found = brentq(resid, 0.15, 0.50)
        z_found = T_to_z(T_found)
        t_found = z_to_t(z_found)
        print(f"  x = {x_target:.2f} ({label:16s}): T = {T_found:.4f} eV, z = {z_found:.0f}, t = {t_found/1000:.1f} kyr")
    except:
        print(f"  x = {x_target:.2f}: could not solve")

# Width
def find_x_T(x_target):
    def resid(T):
        return saha_x(T) - x_target
    return brentq(resid, 0.15, 0.50)

T_90 = find_x_T(0.90)
T_10 = find_x_T(0.10)
z_90 = T_to_z(T_90)
z_10 = T_to_z(T_10)
t_90 = z_to_t(z_90)
t_10 = z_to_t(z_10)

print(f"\nRecombination width (10% to 90%):")
print(f"  Δz = {z_90 - z_10:.0f}")
print(f"  Δt = {(t_10 - t_90)/1000:.1f} kyr")
print(f"  From z = {z_90:.0f} to z = {z_10:.0f}")
print(f"  From t = {t_90/1000:.1f} kyr to t = {t_10/1000:.1f} kyr")

# 1% to 99% width
T_99 = find_x_T(0.99)
T_01 = find_x_T(0.01)
z_99 = T_to_z(T_99)
z_01 = T_to_z(T_01)
t_99 = z_to_t(z_99)
t_01 = z_to_t(z_01)

print(f"\nFull width (1% to 99%):")
print(f"  Δz = {z_99 - z_01:.0f}")
print(f"  Δt = {(t_01 - t_99)/1000:.1f} kyr")
print(f"  From z = {z_99:.0f} to z = {z_01:.0f}")
print(f"  From t = {t_99/1000:.1f} kyr to t = {t_01/1000:.1f} kyr")

# Planck comparison
print(f"\nPlanck 2018 values for comparison:")
print(f"  z_rec = 1089.80 (defined at x ≈ 0.5)")
print(f"  Δz_rec = 194.57 (width of last scattering surface)")
print(f"  This Δz is the optical depth width, not exactly Saha 10-90%")

# ============================================================
# PARAMETER SWEEP TABLE
# ============================================================
print(f"\n{'='*70}")
print(f"PARAMETER SENSITIVITY TABLE")
print(f"{'='*70}")

print(f"\n{'H₀':>6} {'Ω_Λ':>8} {'z_rec':>6} {'t_rec (kyr)':>12} {'Source':>20}")
print(f"{'-'*6} {'-'*8} {'-'*6} {'-'*12} {'-'*20}")

# Use Peebles T_rec = 0.2603 eV for fair comparison
T_peebles = 0.2603
z_peebles = T_to_z(T_peebles)

configs = [
    (67.36, 0.685, "Planck 2018 ΛCDM"),
    (67.36, 0.618, "Planck H₀ + PP Ω_Λ"),
    (70.5,  0.685, "PP H₀ + Planck Ω_Λ"),
    (70.5,  0.618, "Full PP attractor"),
    (73.04, 0.685, "SHoES H₀ + Planck Ω_Λ"),
    (73.04, 0.618, "SHoES H₀ + PP Ω_Λ"),
    (69.8,  0.685, "TDCOSMO H₀ + Planck Ω_Λ"),
    (69.8,  0.618, "TDCOSMO H₀ + PP Ω_Λ"),
]

a_peebles = 1 / (1 + z_peebles)

for H0, OmL, label in configs:
    OmM = 1 - OmL
    H0_si = H0 * 1e3 / 3.0857e22
    def integ(a):
        return 1.0 / (a * np.sqrt(OmM / a**3 + OmL))
    result, _ = quad(integ, 1e-10, a_peebles)
    t_yr = result / H0_si / (365.25 * 24 * 3600)
    print(f"{H0:6.2f} {OmL:8.3f} {z_peebles:6.0f} {t_yr/1000:12.1f} {label:>20}")

