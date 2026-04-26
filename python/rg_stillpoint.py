#!/usr/bin/env python3
"""
Electroweak Stillpoint Test
============================
Test whether φ-boundary conditions at a single scale μ* reproduce 
observed electroweak parameters at M_Z under Standard Model RG running.

Stillpoint conditions:
  sin²θ_W(μ*) = φ⁻³
  g₂(μ*) = 2φ/5
  λ(μ*) = 2φ/25
  g₁²(μ*) = g₂²(μ*) × sin²θ_W/(1 - sin²θ_W) → g₁² = λ = 2φ/25

SM 1-loop and 2-loop β-functions for g₁, g₂, g₃, y_t, λ.
Convention: g₁ is U(1)_Y coupling (NOT GUT normalized).
"""

import numpy as np
from scipy.integrate import solve_ivp

phi = (1 + np.sqrt(5)) / 2

# ============================================================
# MEASURED VALUES AT M_Z (PDG 2024 / standard references)
# ============================================================
MZ = 91.1876  # GeV
mt_pole = 172.69  # GeV (top pole mass)
mH = 125.25  # GeV

# At M_Z in MS-bar:
alpha_em_MZ = 1/127.951  # electromagnetic coupling at M_Z
sin2_theta_W_MZ = 0.23122  # MS-bar at M_Z
alpha_s_MZ = 0.1179  # strong coupling at M_Z

# Derived gauge couplings at M_Z
e_MZ = np.sqrt(4 * np.pi * alpha_em_MZ)
g2_MZ = e_MZ / np.sqrt(sin2_theta_W_MZ)
g1_MZ = e_MZ / np.sqrt(1 - sin2_theta_W_MZ)
g3_MZ = np.sqrt(4 * np.pi * alpha_s_MZ)

# Top Yukawa at M_Z (approximate from pole mass)
v = 246.22  # GeV
yt_MZ = np.sqrt(2) * mt_pole / v  # ~0.994

# Higgs quartic at M_Z (tree-level proxy)
lambda_MZ = mH**2 / (2 * v**2)  # ~0.1294

print("=" * 70)
print("MEASURED VALUES AT M_Z = 91.19 GeV")
print("=" * 70)
print(f"  g₁(MZ)  = {g1_MZ:.6f}     [U(1)_Y coupling]")
print(f"  g₂(MZ)  = {g2_MZ:.6f}     [SU(2)_L coupling]")
print(f"  g₃(MZ)  = {g3_MZ:.6f}     [SU(3)_c coupling]")
print(f"  y_t(MZ) = {yt_MZ:.6f}     [top Yukawa]")
print(f"  λ(MZ)   = {lambda_MZ:.6f}     [Higgs quartic, tree-level]")
print(f"  sin²θ_W = {sin2_theta_W_MZ:.5f}")
print(f"  g₁²(MZ) = {g1_MZ**2:.6f}")

# ============================================================
# PHI VALUES (stillpoint boundary conditions)
# ============================================================
sin2_phi = phi**(-3)
g2_phi = 2 * phi / 5
g1_sq_phi = g2_phi**2 * sin2_phi / (1 - sin2_phi)
g1_phi = np.sqrt(g1_sq_phi)
lambda_phi = 2 * phi / 25

print(f"\n{'=' * 70}")
print(f"PHI STILLPOINT CONDITIONS")
print(f"{'=' * 70}")
print(f"  sin²θ_W* = φ⁻³ = {sin2_phi:.6f}")
print(f"  g₂*      = 2φ/5 = {g2_phi:.6f}")
print(f"  g₁*      = √(g₂²·s²/(1-s²)) = {g1_phi:.6f}")
print(f"  g₁²*     = {g1_sq_phi:.6f}")
print(f"  λ*       = 2φ/25 = {lambda_phi:.6f}")
print(f"  g₁² = λ? {abs(g1_sq_phi - lambda_phi)/lambda_phi*100:.4f}% difference")

# ============================================================
# STANDARD MODEL β-FUNCTIONS (1-loop)
# ============================================================
# t = ln(μ/μ₀), dt = d(ln μ)
# Convention: dX/dt = β_X / (16π²)
# 
# For U(1)_Y (not GUT normalized):
#   β_g1 = (41/6) g₁³    [with factor (3/5) for GUT → Y conversion already handled]
# Actually let me be precise.
#
# Standard 1-loop with nG=3 generations, nH=1 Higgs doublet:
# Using hypercharge coupling g' = g₁ (not GUT normalized g₁^GUT = √(5/3) g')
#
# dg'/dt = g'³/(16π²) × (1/6 × 2nH + 20/9 × nG) = g'³/(16π²) × (1/3 + 20/3) = g'³/(16π²) × (41/6)  ← Wait
#
# Let me use the standard result directly:
# b₁ = 41/10  (GUT normalized)
# b₂ = -19/6
# b₃ = -7
#
# For hypercharge g' (not GUT):  dg'/dt = g'³/(16π²) × 41/6
# For SU(2):                     dg₂/dt = g₂³/(16π²) × (-19/6)
# For SU(3):                     dg₃/dt = g₃³/(16π²) × (-7)

# Actually, the standard coefficients for dαᵢ/dt = bᵢ αᵢ²/(2π):
# With α₁ = (5/3)g'²/(4π), α₂ = g₂²/(4π), α₃ = g₃²/(4π)
# b₁ = 41/10, b₂ = -19/6, b₃ = -7

# For couplings directly:
# d(g'²)/dt = g'⁴/(8π²) × 41/6
# d(g₂²)/dt = g₂⁴/(8π²) × (-19/6)
# d(g₃²)/dt = g₃⁴/(8π²) × (-7)

def beta_1loop(t, y, mu0):
    """1-loop SM beta functions.
    y = [g1, g2, g3, yt, lam]
    g1 = U(1)_Y hypercharge coupling (not GUT normalized)
    """
    g1, g2, g3, yt, lam = y
    pi2_16 = 16 * np.pi**2
    
    # 1-loop gauge β-functions
    # dg/dt = b × g³ / (16π²)
    b1 = 41.0/6.0    # U(1)_Y
    b2 = -19.0/6.0   # SU(2)
    b3 = -7.0         # SU(3)
    
    dg1 = b1 * g1**3 / pi2_16
    dg2 = b2 * g2**3 / pi2_16
    dg3 = b3 * g3**3 / pi2_16
    
    # Top Yukawa 1-loop
    # dyt/dt = yt/(16π²) × (9/2 yt² - 17/12 g1² - 9/4 g2² - 8 g3²)
    dyt = yt / pi2_16 * (9.0/2 * yt**2 - 17.0/12 * g1**2 - 9.0/4 * g2**2 - 8 * g3**2)
    
    # Higgs quartic 1-loop
    # dλ/dt = 1/(16π²) × [24λ² - λ(3g1² + 9g2²) + 3/8(g1⁴ + 2g1²g2² + 3g2⁴) + 12λyt² - 12yt⁴]
    # Note: some references include additional terms
    dlam = (1.0 / pi2_16) * (
        24 * lam**2
        - lam * (3 * g1**2 + 9 * g2**2)
        + 3.0/8 * (g1**4 + 2 * g1**2 * g2**2 + 3 * g2**4)
        + 12 * lam * yt**2
        - 12 * yt**4
    )
    
    return [dg1, dg2, dg3, dyt, dlam]


# ============================================================
# SCAN: For each μ*, set φ-conditions, run to M_Z, compare
# ============================================================
print(f"\n{'=' * 70}")
print(f"RG RUNNING: SCANNING μ* FROM 100 TO 400 GeV")
print(f"{'=' * 70}")

mu_stars = np.linspace(100, 400, 301)
results = []

for mu_star in mu_stars:
    # At μ*, set g₁ and g₂ from φ-conditions
    g1_star = g1_phi
    g2_star = g2_phi
    lam_star = lambda_phi
    
    # For g₃ and y_t at μ*, we need to run them FROM M_Z TO μ*
    # First run g3 and yt from MZ to mu_star
    t_span_up = (0, np.log(mu_star / MZ))
    y0_up = [g1_MZ, g2_MZ, g3_MZ, yt_MZ, lambda_MZ]
    
    sol_up = solve_ivp(beta_1loop, t_span_up, y0_up, args=(MZ,),
                       method='RK45', rtol=1e-10, atol=1e-12,
                       dense_output=True)
    
    if sol_up.success:
        g3_star = sol_up.y[2, -1]  # g₃ at μ*
        yt_star = sol_up.y[3, -1]  # y_t at μ*
    else:
        continue
    
    # Now run FROM μ* TO M_Z with φ-conditions for g1, g2, λ
    # but measured g3, yt
    t_span_down = (0, np.log(MZ / mu_star))  # negative since MZ < mu_star
    y0_down = [g1_star, g2_star, g3_star, yt_star, lam_star]
    
    sol_down = solve_ivp(beta_1loop, t_span_down, y0_down, args=(mu_star,),
                         method='RK45', rtol=1e-10, atol=1e-12,
                         dense_output=True)
    
    if sol_down.success:
        g1_pred = sol_down.y[0, -1]
        g2_pred = sol_down.y[1, -1]
        g3_pred = sol_down.y[2, -1]
        yt_pred = sol_down.y[3, -1]
        lam_pred = sol_down.y[4, -1]
        
        sin2_pred = g1_pred**2 / (g1_pred**2 + g2_pred**2)
        
        results.append({
            'mu': mu_star,
            'g1': g1_pred,
            'g2': g2_pred,
            'g3': g3_pred,
            'yt': yt_pred,
            'lam': lam_pred,
            'sin2': sin2_pred,
            'g1_err': (g1_pred - g1_MZ) / g1_MZ * 100,
            'g2_err': (g2_pred - g2_MZ) / g2_MZ * 100,
            'sin2_err': (sin2_pred - sin2_theta_W_MZ) / sin2_theta_W_MZ * 100,
            'lam_err': (lam_pred - lambda_MZ) / lambda_MZ * 100,
        })

# Find best μ* (minimize total error)
if results:
    for r in results:
        r['total_err'] = np.sqrt(r['g1_err']**2 + r['g2_err']**2 + r['sin2_err']**2 + r['lam_err']**2)
    
    best = min(results, key=lambda x: x['total_err'])
    
    print(f"\n--- BEST OVERALL FIT: μ* = {best['mu']:.1f} GeV ---")
    print(f"  g₁(MZ) predicted: {best['g1']:.6f}  measured: {g1_MZ:.6f}  error: {best['g1_err']:+.3f}%")
    print(f"  g₂(MZ) predicted: {best['g2']:.6f}  measured: {g2_MZ:.6f}  error: {best['g2_err']:+.3f}%")
    print(f"  sin²θ_W predicted: {best['sin2']:.5f}  measured: {sin2_theta_W_MZ:.5f}  error: {best['sin2_err']:+.3f}%")
    print(f"  λ(MZ)  predicted: {best['lam']:.6f}  measured: {lambda_MZ:.6f}  error: {best['lam_err']:+.3f}%")
    print(f"  Combined RMS error: {best['total_err']:.3f}%")
    
    # Also show results at specific interesting scales
    print(f"\n--- RESULTS AT KEY SCALES ---")
    for target_mu in [147, 160, 175, 193, 200, 248, 300]:
        closest = min(results, key=lambda x: abs(x['mu'] - target_mu))
        if abs(closest['mu'] - target_mu) < 2:
            print(f"\n  μ* = {closest['mu']:.0f} GeV:")
            print(f"    g₁(MZ): {closest['g1_err']:+.3f}%    g₂(MZ): {closest['g2_err']:+.3f}%")
            print(f"    sin²θ_W: {closest['sin2_err']:+.3f}%    λ: {closest['lam_err']:+.3f}%")
            print(f"    RMS: {closest['total_err']:.3f}%")
    
    # Find best for each individual quantity
    print(f"\n--- INDIVIDUAL BEST SCALES ---")
    best_g1 = min(results, key=lambda x: abs(x['g1_err']))
    best_g2 = min(results, key=lambda x: abs(x['g2_err']))
    best_sin2 = min(results, key=lambda x: abs(x['sin2_err']))
    best_lam = min(results, key=lambda x: abs(x['lam_err']))
    
    print(f"  g₁ crosses φ-value at μ ≈ {best_g1['mu']:.0f} GeV (error: {best_g1['g1_err']:+.4f}%)")
    print(f"  g₂ crosses φ-value at μ ≈ {best_g2['mu']:.0f} GeV (error: {best_g2['g2_err']:+.4f}%)")
    print(f"  sin²θ_W crosses φ⁻³ at μ ≈ {best_sin2['mu']:.0f} GeV (error: {best_sin2['sin2_err']:+.4f}%)")
    print(f"  λ crosses 2φ/25 at μ ≈ {best_lam['mu']:.0f} GeV (error: {best_lam['lam_err']:+.4f}%)")
    
    # The paper claims ~147, ~193, ~248 GeV for λ, g₂, sin²θ_W
    
    print(f"\n{'=' * 70}")
    print(f"THE KEY QUESTION: Does a single μ* work?")
    print(f"{'=' * 70}")
    
    # Check: at the best μ*, what are the individual errors?
    print(f"\n  At best combined μ* = {best['mu']:.0f} GeV:")
    print(f"    g₁:     {best['g1_err']:+.3f}%")
    print(f"    g₂:     {best['g2_err']:+.3f}%")
    print(f"    sin²θ_W: {best['sin2_err']:+.3f}%")
    print(f"    λ:       {best['lam_err']:+.3f}%")
    
    # Compare: what does standard running give from MZ values?
    print(f"\n  For context, the φ-values differ from MZ values by:")
    print(f"    g₁: {(g1_phi - g1_MZ)/g1_MZ * 100:+.3f}%")
    print(f"    g₂: {(g2_phi - g2_MZ)/g2_MZ * 100:+.3f}%")
    print(f"    sin²θ_W: {(sin2_phi - sin2_theta_W_MZ)/sin2_theta_W_MZ * 100:+.3f}%")
    print(f"    λ: {(lambda_phi - lambda_MZ)/lambda_MZ * 100:+.3f}%")

