"""
Nuclear Eigenvalue Scan
Testing whether the spiral operator's spectrum predicts nuclear properties.

Eric McLean / Pentagon Physics
March 2026
"""

import numpy as np
from itertools import product as iprod

phi = (1 + np.sqrt(5)) / 2
sigma = 1 / phi  # = phi - 1
sqrt5 = np.sqrt(5)
alpha_inv = 137.035999206  # Morel 2020
alpha = 1 / alpha_inv

# ============================================================
# 1. NUCLEAR CHARGE RADIUS: r_0
# ============================================================
# Proton: r_p = 4 * hbar / (m_p * c) = 0.8409 fm (framework)
# Empirical: r_p = 0.8414 fm (muonic hydrogen)
# Nuclear scaling: R = r_0 * A^(1/3)
# Empirical r_0 ≈ 1.25 fm
# Question: what is r_0 / r_p?

r_p_framework = 0.8409  # fm, from 4*hbar/(m_p*c)
r_p_measured = 0.8414   # fm, muonic hydrogen
r_0_empirical = 1.25    # fm (Hofstadter)

ratio_r0_rp = r_0_empirical / r_p_measured
print("=" * 70)
print("1. NUCLEAR CHARGE RADIUS")
print("=" * 70)
print(f"r_p (framework) = {r_p_framework:.4f} fm")
print(f"r_p (measured)   = {r_p_measured:.4f} fm")
print(f"r_0 (empirical)  = {r_0_empirical:.4f} fm")
print(f"r_0 / r_p = {ratio_r0_rp:.6f}")
print(f"phi^(1/2) = {phi**0.5:.6f}")
print(f"3/2 = {3/2:.6f}")
print(f"phi = {phi:.6f}")
print(f"sqrt(5)/phi = {sqrt5/phi:.6f}")
print(f"2/sigma = {2/sigma:.6f}")
print(f"phi^2/sigma = {phi**2/sigma:.6f}")

# Try simple phi expressions for the ratio
print("\nSearching for r_0/r_p expressions:")
best = []
for a in range(-5, 6):
    for b in range(-5, 6):
        for c in range(-3, 4):
            for d in range(-3, 4):
                if a == 0 and b == 0 and c == 0 and d == 0:
                    continue
                try:
                    val = (phi**a) * (np.pi**b) * (sqrt5**c) * (2**d)
                    if 0.1 < val < 10:
                        err = abs(val - ratio_r0_rp) / ratio_r0_rp
                        if err < 0.01:
                            best.append((err, a, b, c, d, val))
                except:
                    pass

best.sort()
for err, a, b, c, d, val in best[:10]:
    terms = []
    if a: terms.append(f"φ^{a}")
    if b: terms.append(f"π^{b}")
    if c: terms.append(f"√5^{c}")
    if d: terms.append(f"2^{d}")
    expr = " × ".join(terms)
    print(f"  {expr} = {val:.6f}  err = {err*100:.4f}%")

# ============================================================
# 2. BETHE-WEIZSACKER COEFFICIENTS
# ============================================================
print("\n" + "=" * 70)
print("2. BETHE-WEIZSACKER COEFFICIENTS")
print("=" * 70)

# Standard values (MeV)
a_V = 15.67   # Volume
a_S = 17.23   # Surface
a_C = 0.714   # Coulomb
a_A = 23.29   # Asymmetry
a_P = 12.0    # Pairing (approximate)

m_p_MeV = 938.272

print(f"\nCoefficients in MeV:")
print(f"  a_V = {a_V}")
print(f"  a_S = {a_S}")
print(f"  a_C = {a_C}")
print(f"  a_A = {a_A}")
print(f"  a_P = {a_P}")

print(f"\nRatios between coefficients:")
print(f"  a_S/a_V = {a_S/a_V:.6f}  (φ^(1/4) = {phi**0.25:.6f})")
print(f"  a_A/a_V = {a_A/a_V:.6f}  (phi = {phi:.6f}, 3/2 = {1.5:.6f})")
print(f"  a_A/a_S = {a_A/a_S:.6f}  (φ^(1/2) = {phi**0.5:.6f})")
print(f"  a_V/a_C = {a_V/a_C:.6f}")
print(f"  a_P/a_V = {a_P/a_V:.6f}  (σ = {sigma:.6f})")

print(f"\nCoefficients normalised to m_p:")
for name, val in [("a_V", a_V), ("a_S", a_S), ("a_C", a_C), ("a_A", a_A), ("a_P", a_P)]:
    ratio = val / m_p_MeV
    print(f"  {name}/m_p = {ratio:.8f}")

# Check ratios against phi expressions
print(f"\nKey ratio checks:")
print(f"  a_S/a_V = {a_S/a_V:.6f}")
print(f"    1 + σ/5 = {1 + sigma/5:.6f}  err = {abs(a_S/a_V - (1+sigma/5))/(a_S/a_V)*100:.3f}%")
print(f"    1 + 1/φ^4 = {1 + phi**-4:.6f}  err = {abs(a_S/a_V - (1+phi**-4))/(a_S/a_V)*100:.3f}%")

print(f"\n  a_A/a_V = {a_A/a_V:.6f}")
print(f"    3/2 = {3/2:.6f}  err = {abs(a_A/a_V - 3/2)/(a_A/a_V)*100:.3f}%")
print(f"    φ^(3/4)*π^(-1/4) nah...")
print(f"    (φ+σ²) = {phi+sigma**2:.6f}  err = {abs(a_A/a_V - (phi+sigma**2))/(a_A/a_V)*100:.3f}%")

# a_V in natural units
print(f"\n  a_V/m_p = {a_V/m_p_MeV:.8f}")
print(f"    α/5 = {alpha/5:.8f}  err = {abs(a_V/m_p_MeV - alpha/5)/(a_V/m_p_MeV)*100:.3f}%")
print(f"    α×φ/4 = {alpha*phi/4:.8f}  err = {abs(a_V/m_p_MeV - alpha*phi/4)/(a_V/m_p_MeV)*100:.3f}%")

# ============================================================
# 3. MAGIC NUMBERS
# ============================================================
print("\n" + "=" * 70)
print("3. MAGIC NUMBERS")
print("=" * 70)

magic = [2, 8, 20, 28, 50, 82, 126]
print(f"Standard magic numbers: {magic}")
print(f"Differences: {[magic[i+1]-magic[i] for i in range(len(magic)-1)]}")
print(f"Differences: 6, 12, 8, 22, 32, 44")
print(f"Ratios: {[magic[i+1]/magic[i] for i in range(len(magic)-1)]}")

# Check for patterns with 2I character table dimensions
dims_2I = [1, 2, 2, 3, 3, 4, 4, 5, 6]
print(f"\n2I dimensions: {dims_2I}, sum = {sum(dims_2I)}")

# Cumulative sums of sorted dims
sorted_dims = sorted(dims_2I)
cumsum = np.cumsum(sorted_dims)
print(f"Cumulative sums of dims: {list(cumsum)}")

# Products and combinations of dims
print(f"\nChecking magic numbers against dim products:")
for m in magic:
    matches = []
    for i, d1 in enumerate(dims_2I):
        for j, d2 in enumerate(dims_2I):
            if d1 * d2 == m:
                matches.append(f"dim({d1})×dim({d2})")
            for k, d3 in enumerate(dims_2I):
                if d1 * d2 * d3 == m and len(matches) < 5:
                    pass  # too many
    for i, d1 in enumerate(dims_2I):
        for j, d2 in enumerate(dims_2I):
            if d1 * d2 == m:
                matches.append(f"{d1}×{d2}")
    # Simple phi/integer check
    for n in range(1, 200):
        for a in range(-3, 4):
            if abs(n * phi**a - m) / m < 0.001:
                matches.append(f"{n}×φ^{a}")
    if matches:
        print(f"  {m}: {', '.join(matches[:5])}")
    else:
        print(f"  {m}: no simple match found")

# Shell model: 2, 6, 12, 8, 22, 32, 44 (j+1/2 degeneracies)
# Harmonic oscillator shells: 2, 6, 12, 20, 30, 42, 56
ho_shells = [2, 6, 12, 20, 30, 42, 56]
ho_cumsum = list(np.cumsum(ho_shells))
print(f"\nHarmonic oscillator cumulative: {ho_cumsum}")
print(f"vs magic:                       {magic}")
print(f"Magic deviates at shell 4 (28 vs 40) due to spin-orbit splitting")

# ============================================================
# 4. DEUTERON MAGNETIC MOMENT
# ============================================================
print("\n" + "=" * 70)
print("4. DEUTERON MAGNETIC MOMENT")
print("=" * 70)

mu_p = 2.7928473446  # nuclear magnetons
mu_n = -1.9130427001
mu_d_measured = 0.8574382308  # nuclear magnetons

mu_d_naive = mu_p + mu_n
deficit = mu_d_measured - mu_d_naive
print(f"μ_p = {mu_p:.6f} μ_N")
print(f"μ_n = {mu_n:.6f} μ_N")
print(f"μ_p + μ_n = {mu_d_naive:.6f} μ_N")
print(f"μ_d (measured) = {mu_d_measured:.6f} μ_N")
print(f"deficit = {deficit:.6f} μ_N ({deficit/mu_d_measured*100:.2f}%)")

# Framework prediction for mu_p
mu_p_framework = 3 - sigma/3
mu_n_framework = -2 * (1 - sigma/3)
mu_d_framework_naive = mu_p_framework + mu_n_framework
print(f"\nFramework:")
print(f"  μ_p = 3 - σ/3 = {mu_p_framework:.6f}")
print(f"  μ_n = -2(1 - σ/3) = {mu_n_framework:.6f}")
print(f"  μ_p + μ_n (framework) = {mu_d_framework_naive:.6f}")

# What correction do we need for the deuteron?
print(f"\n  Needed correction: {mu_d_measured - mu_d_framework_naive:.6f}")
print(f"  As fraction of mu_d: {(mu_d_measured - mu_d_framework_naive)/mu_d_measured:.6f}")

# Try phi corrections
for name, val in [
    ("σ/30", sigma/30),
    ("σ²/6", sigma**2/6),
    ("1/(5φ³)", 1/(5*phi**3)),
    ("-σ²/5", -sigma**2/5),
    ("σ/(3φ²)", sigma/(3*phi**2)),
    ("φ⁻⁴", phi**-4),
    ("-σ/5", -sigma/5),
]:
    pred = mu_d_framework_naive + val
    err = abs(pred - mu_d_measured) / mu_d_measured * 100
    print(f"  {mu_d_framework_naive:.4f} + {name} = {pred:.6f}, err = {err:.3f}%")

# Direct phi expression for mu_d
print(f"\nDirect expressions for μ_d:")
for name, val in [
    ("σ/σ = 1.0 nope", 1.0),
    ("3σ", 3*sigma),
    ("φ/2", phi/2),
    ("σ + σ²/3", sigma + sigma**2/3),
    ("1 - σ/5", 1 - sigma/5),
    ("(3-σ/3) + (-2+2σ/3)", mu_p_framework + mu_n_framework),
    ("1 - σ/φ³", 1 - sigma/phi**3),
    ("σ²×√5", sigma**2 * sqrt5),
    ("φ²/3", phi**2/3),
    ("5σ/3 - σ²", 5*sigma/3 - sigma**2),
    ("(5-σ)/5", (5-sigma)/5),
]:
    err = abs(val - mu_d_measured) / mu_d_measured * 100
    if err < 2:
        print(f"  {name} = {val:.6f}, err = {err:.3f}%")

# ============================================================
# 5. BINDING ENERGY PER NUCLEON AT KEY ELEMENTS
# ============================================================
print("\n" + "=" * 70)
print("5. BINDING ENERGY PATTERN")
print("=" * 70)

# B/A in MeV for key nuclei
be_data = {
    'H-2': (2, 1.112),
    'He-4': (4, 7.074),
    'C-12': (12, 7.680),
    'O-16': (16, 7.976),
    'Fe-56': (56, 8.790),
    'Ni-62': (62, 8.795),
    'Sn-120': (120, 8.505),
    'Pb-208': (208, 7.867),
    'U-238': (238, 7.570),
}

print(f"\nBinding energy per nucleon (MeV):")
print(f"{'Nucleus':<10} {'A':>4} {'B/A':>8} {'B/A / m_p':>12}")
for name, (A, BA) in be_data.items():
    print(f"{name:<10} {A:>4} {BA:>8.3f} {BA/m_p_MeV:>12.8f}")

# The peak is at Fe-56/Ni-62, B/A ≈ 8.79 MeV
# B/A_max / m_p = 8.79/938.27 = 0.009369
peak_BA = 8.795
ratio_peak = peak_BA / m_p_MeV
print(f"\nPeak B/A = {peak_BA} MeV")
print(f"Peak B/A / m_p = {ratio_peak:.8f}")
print(f"α/φ = {alpha/phi:.8f}  err = {abs(ratio_peak - alpha/phi)/ratio_peak*100:.3f}%")
print(f"α²×φ×5 = {alpha**2*phi*5:.8f}")
print(f"α/(2σ) = {alpha/(2*sigma):.8f}  err = {abs(ratio_peak - alpha/(2*sigma))/ratio_peak*100:.3f}%")
print(f"α×φ²/5 = {alpha*phi**2/5:.8f}")
print(f"α/√5 = {alpha/sqrt5:.8f}")

# He-4 binding energy is special: most tightly bound light nucleus
he4_BA = 7.074
he4_ratio = he4_BA / m_p_MeV
print(f"\nHe-4 B/A / m_p = {he4_ratio:.8f}")

# ============================================================
# 6. NUCLEAR MAGNETIC MOMENTS ACROSS TABLE
# ============================================================
print("\n" + "=" * 70)
print("6. NUCLEAR MAGNETIC MOMENTS (odd-A nuclei)")
print("=" * 70)

# Measured magnetic moments of key odd-A nuclei (in nuclear magnetons)
moments = {
    'H-1': (1, 1, 2.7928),     # proton
    'H-3': (3, 1, 2.9790),     # tritium
    'He-3': (3, 2, -2.1276),   # helium-3
    'Li-7': (7, 3, 3.2564),    # lithium
    'B-11': (11, 5, 2.6886),   # boron
    'N-15': (15, 7, -0.2832),  # nitrogen
    'F-19': (19, 9, 2.6289),   # fluorine
    'Na-23': (23, 11, 2.2175), # sodium
    'Al-27': (27, 13, 3.6415), # aluminium
    'P-31': (31, 15, 1.1316),  # phosphorus
}

print(f"{'Nucleus':<8} {'A':>3} {'Z':>3} {'μ (μ_N)':>10} {'μ/μ_p':>10}")
for name, (A, Z, mu) in moments.items():
    print(f"{name:<8} {A:>3} {Z:>3} {mu:>10.4f} {mu/mu_p:>10.4f}")

# Schmidt lines: single-particle predictions
# For proton paper: mu_p = 3 - sigma/3
# Check if corrections scale with A or Z
print(f"\nMagnetic moment / proton moment ratios:")
print(f"  H-3/H-1 = {moments['H-3'][2]/mu_p:.6f}  (three nucleons, paired n+n+p)")
print(f"  He-3/H-1 = {moments['He-3'][2]/mu_p:.6f}  (three nucleons, paired p+p+n)")
print(f"  He-3 has unpaired neutron: μ_He3/μ_n = {moments['He-3'][2]/mu_n:.6f}")

# ============================================================
# 7. NUCLEAR RADII vs A^(1/3) — does φ appear?
# ============================================================
print("\n" + "=" * 70)
print("7. CHARGE RADII vs FRAMEWORK")
print("=" * 70)

# Measured RMS charge radii (fm)
radii = {
    'H-1': (1, 0.8414),
    'H-2': (2, 2.1421),
    'He-4': (4, 1.6755),
    'C-12': (12, 2.4702),
    'O-16': (16, 2.6991),
    'Ca-40': (40, 3.4776),
    'Ca-48': (48, 3.4771),  # famous: same radius as Ca-40!
    'Ni-58': (58, 3.775),
    'Sn-120': (120, 4.6519),
    'Pb-208': (208, 5.5012),
}

print(f"{'Nucleus':<8} {'A':>4} {'r (fm)':>8} {'r/r_p':>8} {'r/A^(1/3)':>10}")
for name, (A, r) in radii.items():
    print(f"{name:<8} {A:>4} {r:>8.4f} {r/r_p_measured:>8.4f} {r/A**(1/3):>10.4f}")

# r_0 from fit
r0_vals = [r / A**(1/3) for name, (A, r) in radii.items() if A > 10]
r0_mean = np.mean(r0_vals)
print(f"\nMean r_0 (A > 10) = {r0_mean:.4f} fm")
print(f"r_0 / r_p = {r0_mean / r_p_measured:.6f}")
print(f"φ^(1/2) = {phi**0.5:.6f}")
print(f"3/2 = 1.500000")
print(f"2/√φ = {2/phi**0.5:.6f}")
print(f"φ²/σ² ... nah")

# ============================================================
# 8. THE 12/7 PATTERN IN NUCLEAR PHYSICS
# ============================================================
print("\n" + "=" * 70)
print("8. THE 12/7 RATIO")
print("=" * 70)

# 12/7 appears in gravity: alpha_G = alpha^18 * 12/7
# Does it appear anywhere else in nuclear physics?

# Ratio of neutron to proton magnetic moments
mu_ratio = abs(mu_n / mu_p)
print(f"|μ_n/μ_p| = {mu_ratio:.6f}")
print(f"2/3 = {2/3:.6f}")
print(f"12/7 × σ/3 = {12/7 * sigma/3:.6f}")
print(f"σ × √(12/7) = {sigma * np.sqrt(12/7):.6f}")

# Proton-neutron mass difference
m_n_MeV = 939.565
dm = m_n_MeV - m_p_MeV
print(f"\nm_n - m_p = {dm:.3f} MeV")
print(f"(m_n - m_p) / m_e = {dm/0.511:.4f}")
print(f"2√φ × m_e = {2*phi**0.5 * 0.511:.4f} MeV")
print(f"  err = {abs(dm - 2*phi**0.5*0.511)/dm*100:.2f}%")

# ============================================================
# 9. Ca-40 vs Ca-48: THE ISOTOPE SHAPE TEST
# ============================================================
print("\n" + "=" * 70)
print("9. CALCIUM ISOTOPES (eigenfunction shape)")
print("=" * 70)
print("Ca-40 (Z=20, N=20): doubly magic, spherical")
print("Ca-48 (Z=20, N=28): doubly magic, spherical")
print(f"Charge radii: Ca-40 = 3.4776 fm, Ca-48 = 3.4771 fm")
print(f"IDENTICAL within 0.01% despite 8 extra neutrons!")
print(f"This is a classic eigenvalue signature: both are at magic-number")
print(f"closed shells, so the eigenfunction shape doesn't change.")
print(f"8 extra neutrons add mass but don't change the shape.")
print(f"8 = |Q_8| = m_B²/m_D² ... coincidence?")

