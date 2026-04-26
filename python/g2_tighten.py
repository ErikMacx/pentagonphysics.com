"""
TIGHTENING g₂ = 2φ/5
=====================
Mac McLean — 23 February 2026

The scan found v/M_W ≈ 5/φ → g₂ = 2φ/5 at 0.87%.
Question: is this tree-level? MS-bar at some scale? 
Does the running help or hurt?

Key fact: g₂ RUNS. It increases at low energies.
The MS-bar value at M_Z is g₂(M_Z) = 0.6518.
The on-shell M_W gives g₂ ≈ 0.6529 (includes radiative corrections).

2φ/5 = 0.64721. That's BELOW both values.
So either:
  (a) g₂ = 2φ/5 at a HIGHER scale (where g₂ is smaller), or
  (b) the formula needs a small correction, or
  (c) g₂ isn't exactly 2φ/5

Let's find out.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from math import sqrt, log, log10, pi, asin, acos

phi = (1 + sqrt(5)) / 2
sqrt5 = sqrt(5)
alpha_inv = 137.035999206
v_ew = 246.2196
m_H = 125.25
M_W = 80.377
M_Z = 91.1876
m_t = 173.1

# ─── Precise experimental values ───
# MS-bar couplings at M_Z (PDG 2024)
g1_MZ = 0.35760    # U(1)_Y, GUT normalization √(5/3)g'
g2_MZ = 0.65184     # SU(2)_L
g3_MZ = 1.2210      # SU(3)_C  → α_s(M_Z) = g3²/(4π) = 0.1179

# On-shell quantities
sin2_thetaW_onshell = 1 - M_W**2/M_Z**2  # = 0.2231
sin2_thetaW_MSbar = 0.23122  # at M_Z

print("═" * 65)
print("  g₂ = 2φ/5 ?  — ELECTROWEAK COUPLING INVESTIGATION")
print("═" * 65)
print()

g2_target = 2*phi/5
print(f"  Target: g₂ = 2φ/5 = {g2_target:.8f}")
print(f"  MS-bar at M_Z: g₂ = {g2_MZ:.8f}")
print(f"  Difference: {(g2_target - g2_MZ)/g2_MZ*100:+.3f}%")
print()

# ─── RG running of g₂ (1-loop) ───
# β_g2 = -(19/6)g₂³/(16π²)  [SM with 1 Higgs doublet, 3 generations]
# g₂ DECREASES going up in energy (asymptotic freedom-like for SU(2))

def beta_g2_1loop(t, g2):
    return [-(19.0/6) * g2[0]**3 / (16 * pi**2)]

# Solve from M_Z upward
y0 = [g2_MZ]
t_max = log(1e16 / M_Z)

sol = solve_ivp(beta_g2_1loop, [0, t_max], y0,
                method='RK45', dense_output=True, rtol=1e-12, atol=1e-14)

# Find where g₂(μ) = 2φ/5
def g2_minus_target(t):
    return sol.sol(t)[0] - g2_target

# g₂ decreases upward, so we're looking for a crossing above M_Z
try:
    t_cross = brentq(g2_minus_target, 0, t_max, xtol=1e-14)
    mu_cross = M_Z * np.exp(t_cross)
    print(f"  g₂(μ) = 2φ/5 at μ = {mu_cross:.2f} GeV")
    print(f"  log₁₀(μ) = {log10(mu_cross):.4f}")
    print()
    
    # What is this scale?
    print(f"  Compare:")
    print(f"    M_Z   = {M_Z} GeV")
    print(f"    m_H   = {m_H} GeV")
    print(f"    m_t   = {m_t} GeV")
    print(f"    v     = {v_ew} GeV")
    print(f"    vφ    = {v_ew*phi:.1f} GeV")
    print()
    
    # Ratios
    for name, scale in [("M_Z", M_Z), ("m_H", m_H), ("m_t", m_t), 
                         ("v", v_ew), ("M_W", M_W)]:
        r = mu_cross / scale
        print(f"    μ/{name:4s} = {r:.6f}", end="")
        for rname, rval in [("φ", phi), ("√φ", sqrt(phi)), ("φ²", phi**2),
                             ("√5", sqrt5), ("5/φ", 5/phi), ("π/φ", pi/phi),
                             ("2", 2.0), ("φ+1", phi+1), ("3", 3.0),
                             ("5/2", 2.5), ("φ³/π", phi**3/pi)]:
            if abs(r - rval)/rval < 0.03:
                print(f"  ≈ {rname} ({rval:.4f}, err: {abs(r-rval)/rval*100:.2f}%)", end="")
        print()
    print()
except:
    print("  No crossing found — g₂ may not reach 2φ/5 at 1-loop")

# ─── Full 1-loop with all three gauge couplings ───
print("═" * 65)
print("  FULL 1-LOOP RG: ALL GAUGE COUPLINGS")
print("═" * 65)
print()

def beta_gauge(t, y):
    g1, g2, g3 = y
    fac = 1/(16*pi**2)
    b1 = fac * (41.0/6) * g1**3     # U(1), GUT norm
    b2 = fac * (-19.0/6) * g2**3    # SU(2)
    b3 = fac * (-7.0) * g3**3       # SU(3)
    return [b1, b2, b3]

y0_full = [g1_MZ, g2_MZ, g3_MZ]
sol_full = solve_ivp(beta_gauge, [0, log(1e19/M_Z)], y0_full,
                     method='RK45', dense_output=True, rtol=1e-12, atol=1e-14)

# Also solve downward
sol_down = solve_ivp(beta_gauge, [0, log(10/M_Z)], y0_full,
                     method='RK45', dense_output=True, rtol=1e-12, atol=1e-14)

print(f"  {'μ (GeV)':>14s} {'log₁₀μ':>8s} {'g₁':>10s} {'g₂':>10s} {'g₃':>10s} {'sin²θ_W':>10s}")
print("  " + "─" * 65)

scales = [10, 50, M_Z, m_H, m_t, v_ew, 300, 500, 1000, 5000, 
          1e4, 1e5, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16]

for mu in scales:
    t = log(mu / M_Z)
    if t >= 0:
        vals = sol_full.sol(t)
    else:
        vals = sol_down.sol(t)
    g1, g2, g3 = vals
    sin2 = g1**2 / (g1**2 + g2**2)  # GUT normalization
    
    marker = ""
    if abs(g2 - 2*phi/5) / g2 < 0.005:
        marker = f"  ← g₂ ≈ 2φ/5 = {2*phi/5:.6f}"
    if abs(sin2 - phi**(-3)) / sin2 < 0.03:
        marker += f"  ← sin²θ ≈ φ⁻³"
    
    print(f"  {mu:14.1f} {log10(mu):8.3f} {g1:10.6f} {g2:10.6f} {g3:10.6f} {sin2:10.6f}{marker}")

print()

# ─── Where does g₂ = 2φ/5 exactly? ───
print("═" * 65)
print("  EXACT CROSSING: g₂(μ) = 2φ/5")
print("═" * 65)
print()

def g2_full_minus_target(t):
    return sol_full.sol(t)[1] - 2*phi/5

try:
    t_cross = brentq(g2_full_minus_target, 0, log(1e19/M_Z), xtol=1e-14)
    mu_cross = M_Z * np.exp(t_cross)
    g_vals = sol_full.sol(t_cross)
    g1_at, g2_at, g3_at = g_vals
    sin2_at = g1_at**2 / (g1_at**2 + g2_at**2)
    
    print(f"  g₂ = 2φ/5 at μ = {mu_cross:.2f} GeV  (log₁₀ = {log10(mu_cross):.4f})")
    print(f"  At this scale:")
    print(f"    g₁ = {g1_at:.6f}")
    print(f"    g₂ = {g2_at:.6f}  (= 2φ/5 = {2*phi/5:.6f} ✓)")
    print(f"    g₃ = {g3_at:.6f}")
    print(f"    sin²θ_W = {sin2_at:.6f}")
    print(f"    α₂ = g₂²/(4π) = {g2_at**2/(4*pi):.6f}")
    print(f"    α₃ = g₃²/(4π) = {g3_at**2/(4*pi):.6f}")
    print()
    
    # Check g₃ and g₁ for φ-expressions at this scale
    print(f"  Are g₁ and g₃ also φ-expressions at μ = {mu_cross:.0f} GeV?")
    print()
    
    for name, val, meas in [("g₁", g1_at, ""), ("g₃", g3_at, "")]:
        print(f"  {name} = {val:.6f}")
        candidates = [
            ("φ⁻¹", 1/phi), ("φ⁻²", 1/phi**2), ("1/√5", 1/sqrt5),
            ("2/5", 0.4), ("√5/5", sqrt5/5), ("φ/π", phi/pi),
            ("1/√φ", 1/sqrt(phi)), ("2/√5", 2/sqrt5),
            ("√(2/5)", sqrt(2/5)), ("φ²/π", phi**2/pi),
            ("√5/φ", sqrt5/phi), ("√5/2", sqrt5/2),
            ("2φ/π", 2*phi/pi), ("5/(2π)", 5/(2*pi)),
            ("3/π", 3/pi), ("φ/√π", phi/sqrt(pi)),
            ("(√5+1)/5", (sqrt5+1)/5), ("√(φ/π)", sqrt(phi/pi)),
        ]
        for cname, cval in candidates:
            err = abs(val - cval)/val * 100
            if err < 3:
                print(f"    ≈ {cname:15s} = {cval:.6f}  (err: {err:.3f}%)")
        print()
    
    # Check α_s at this scale
    alpha_s_at = g3_at**2 / (4*pi)
    print(f"  α_s at μ = {mu_cross:.0f} GeV: {alpha_s_at:.6f}")
    for cname, cval in [("φ⁻³/2", phi**(-3)/2), ("1/(3φ²)", 1/(3*phi**2)),
                         ("1/(2φ³)", 1/(2*phi**3)), ("φ⁻⁴", phi**(-4)),
                         ("1/(5φ)", 1/(5*phi)), ("√5/(5φ²)", sqrt5/(5*phi**2))]:
        err = abs(alpha_s_at - cval)/alpha_s_at*100
        if err < 5:
            print(f"    ≈ {cname:15s} = {cval:.6f}  (err: {err:.3f}%)")
    
except Exception as e:
    print(f"  Error: {e}")

# ─── Alternative: g₂ = 2φ/5 at m_t or v ───
print()
print("═" * 65)
print("  g₂ AT KEY PHYSICAL SCALES")
print("═" * 65)
print()

for name, mu in [("M_Z", M_Z), ("m_H", m_H), ("m_t", m_t), ("v", v_ew)]:
    t = log(mu / M_Z)
    if t >= 0:
        vals = sol_full.sol(t)
    else:
        vals = sol_down.sol(t)
    g1, g2, g3 = vals
    sin2 = g1**2 / (g1**2 + g2**2)
    err_g2 = (g2 - 2*phi/5)/g2 * 100
    
    print(f"  μ = {name:4s} = {mu:8.2f} GeV:")
    print(f"    g₂ = {g2:.6f}  (2φ/5 = {2*phi/5:.6f}, err: {err_g2:+.3f}%)")
    
    # What IS g₂ at this scale as a φ-expression?
    for cname, cval in [("2φ/5", 2*phi/5), ("φ/√(φ+1)", phi/sqrt(phi+1)),
                         ("√(φ/π)", sqrt(phi/pi)*sqrt(pi)*phi/sqrt(phi)/phi*g2), # nah
                         ("(√5+1)/5", (sqrt5+1)/5), 
                         ("2(√5+1)/10", 2*(sqrt5+1)/10),  # = 2φ/5
                         ]:
        pass  # skip redundant
    print()

# ─── THE REAL TEST: Is there a SINGLE scale where ALL three are φ-expressions? ───
print("═" * 65)
print("  GRAND TEST: ALL COUPLINGS AS φ-EXPRESSIONS AT ONE SCALE?")
print("═" * 65)
print()

# Scan for scales where g₂ is closest to 2φ/5
# and check what g₁ and g₃ are
t_fine = np.linspace(0, log(1e6/M_Z), 100000)
g2_fine = np.array([sol_full.sol(t)[1] for t in t_fine])
mu_fine = M_Z * np.exp(t_fine)

# At the g₂ = 2φ/5 scale, check systematic φ-expression search for g₁ and g₃
t_g2cross = brentq(g2_full_minus_target, 0, log(1e19/M_Z))
g_at_cross = sol_full.sol(t_g2cross)
g1_c, g2_c, g3_c = g_at_cross
mu_c = M_Z * np.exp(t_g2cross)

print(f"  At μ = {mu_c:.1f} GeV (where g₂ = 2φ/5):")
print()

# Systematic search for g₁
print(f"  g₁ = {g1_c:.8f}")
results_g1 = []
for a in range(1, 6):
    for n in range(-6, 7):
        for b in range(1, 26):
            for p in range(0, 3):
                val = a * phi**n / (b * pi**p)
                if 0.3 < val < 0.5:
                    err = abs(val - g1_c) / g1_c * 100
                    if err < 1:
                        expr = f"{a}·φ^{n}/({b}·π^{p})"
                        results_g1.append((err, expr, val))

results_g1.sort()
print(f"  Best φ-expressions for g₁ (within 1%):")
for err, expr, val in results_g1[:10]:
    print(f"    {expr:30s} = {val:.6f}  (err: {err:.4f}%)")

print()

# Systematic search for g₃  
print(f"  g₃ = {g3_c:.8f}")
results_g3 = []
for a in range(1, 6):
    for n in range(-6, 7):
        for b in range(1, 26):
            for p in range(0, 3):
                val = a * phi**n / (b * pi**p)
                if 0.5 < val < 1.5:
                    err = abs(val - g3_c) / g3_c * 100
                    if err < 1:
                        expr = f"{a}·φ^{n}/({b}·π^{p})"
                        results_g3.append((err, expr, val))

results_g3.sort()
print(f"  Best φ-expressions for g₃ (within 1%):")
for err, expr, val in results_g3[:10]:
    print(f"    {expr:30s} = {val:.6f}  (err: {err:.4f}%)")

print()

# ─── sin²θ_W running ───
print("═" * 65)
print("  sin²θ_W RUNNING: WHERE DOES IT HIT φ⁻³?")
print("═" * 65)
print()

def sin2_minus_phi3(t):
    vals = sol_full.sol(t)
    g1, g2, g3 = vals
    return g1**2 / (g1**2 + g2**2) - phi**(-3)

# sin²θ increases with energy (g₁ grows, g₂ shrinks)
# At M_Z: sin²θ ≈ 0.231, target φ⁻³ = 0.236
# So we need to go UP in energy
try:
    t_sin2 = brentq(sin2_minus_phi3, 0, log(1e19/M_Z))
    mu_sin2 = M_Z * np.exp(t_sin2)
    g_at_sin2 = sol_full.sol(t_sin2)
    
    print(f"  sin²θ_W = φ⁻³ at μ = {mu_sin2:.1f} GeV  (log₁₀ = {log10(mu_sin2):.3f})")
    print(f"  At this scale:")
    print(f"    g₁ = {g_at_sin2[0]:.6f}")
    print(f"    g₂ = {g_at_sin2[1]:.6f}")
    print(f"    g₃ = {g_at_sin2[2]:.6f}")
    
    # Is g₂ also a φ-expression here?
    g2_here = g_at_sin2[1]
    print(f"    g₂ err from 2φ/5: {abs(g2_here - 2*phi/5)/g2_here*100:.3f}%")
    
    # How far apart are the two scales?
    print(f"\n  Scale separation:")
    print(f"    g₂ = 2φ/5 at {mu_c:.0f} GeV")
    print(f"    sin²θ = φ⁻³ at {mu_sin2:.0f} GeV")
    print(f"    Ratio: {mu_sin2/mu_c:.2f}")
    
except Exception as e:
    print(f"  Error: {e}")

print()

# ─── The M_W prediction chain ───
print("═" * 65)
print("  M_W PREDICTION FROM g₂ = 2φ/5")
print("═" * 65)
print()

# Tree level: M_W = g₂v/2
# But g₂ runs, so we need to specify the scale
# The physical M_W includes radiative corrections

# Option A: g₂ = 2φ/5 is the TREE-LEVEL (low-energy) value
M_W_tree = (2*phi/5) * v_ew / 2
print(f"  Option A: g₂(tree) = 2φ/5")
print(f"    M_W = g₂v/2 = {M_W_tree:.4f} GeV")
print(f"    Measured: {M_W} GeV")
print(f"    Error: {abs(M_W_tree - M_W)/M_W*100:.3f}%")
print()

# Option B: Use g₂(M_Z) and accept the 0.7% offset
# The SM radiative correction to M_W is:
# M_W = M_W^tree × (1 + Δr)^{-1/2}
# where Δr ≈ 0.0361 (dominated by top loop)
# M_W^tree = g₂(M_Z) × v / 2 = 0.65184 × 246.22 / 2 = 80.22 GeV
# With Δr: M_W = 80.22 / √(1-0.0361) = 80.22 / 0.9817 = 81.7... nah

# Actually the tree-level relation gives M_W from the on-shell scheme:
# G_F/(√2) = g₂²/(8M_W²) → M_W² = g₂²v²/4
# v is defined from G_F, so M_W = g₂v/2 at tree level
# The difference between g₂v/2 and measured M_W is the radiative correction

M_W_from_g2MZ = g2_MZ * v_ew / 2
print(f"  g₂(M_Z) × v/2 = {M_W_from_g2MZ:.4f} GeV")
print(f"  Measured M_W   = {M_W:.3f} GeV")
print(f"  Difference (radiative corrections): {M_W - M_W_from_g2MZ:.4f} GeV ({(M_W - M_W_from_g2MZ)/M_W*100:.3f}%)")
print()

# So if g₂ = 2φ/5 at tree level:
# M_W^tree = (2φ/5)(v/2) = vφ/5 = 79.678 GeV
# Radiative correction needs to add ~0.7 GeV (0.87%)
# This is LARGER than the SM radiative correction from g₂(M_Z)

print("  The SM radiative correction to M_W is ~0.2% from g₂(M_Z)")
print("  If g₂ = 2φ/5, we need a ~0.87% correction")
print("  This means either:")
print("    (a) g₂ = 2φ/5 isn't exact at tree level")
print("    (b) The correction mechanism differs from SM")
print("    (c) g₂ = 2φ/5 holds at a different scale")
print()

# ─── The ratio g₂²/g₁² ───
print("═" * 65)
print("  COUPLING RATIOS")
print("═" * 65)
print()

g2_over_g1_MZ = g2_MZ / g1_MZ
print(f"  g₂/g₁ at M_Z = {g2_over_g1_MZ:.6f}")

for name, val in [("φ", phi), ("√5", sqrt5), ("2", 2.0), ("√(φ³)", sqrt(phi**3)),
                   ("√(2φ)", sqrt(2*phi)), ("π/√5", pi/sqrt5), 
                   ("5/π", 5/pi), ("φπ/3", phi*pi/3),
                   ("√(φπ)", sqrt(phi*pi)), ("3/√5", 3/sqrt5)]:
    err = abs(g2_over_g1_MZ - val)/g2_over_g1_MZ * 100
    if err < 5:
        print(f"    ≈ {name:15s} = {val:.6f}  (err: {err:.3f}%)")

print()

# g₂²/g₁² 
ratio_sq = g2_MZ**2 / g1_MZ**2
print(f"  g₂²/g₁² at M_Z = {ratio_sq:.6f}")
for name, val in [("φ²", phi**2), ("3", 3.0), ("5/φ", 5/phi), 
                   ("φ+2", phi+2), ("π", pi), ("φ³/φ", phi**2),
                   ("10/3", 10/3), ("2φ+1", 2*phi+1)]:
    err = abs(ratio_sq - val)/ratio_sq * 100
    if err < 5:
        print(f"    ≈ {name:15s} = {val:.6f}  (err: {err:.3f}%)")

print()

# sin²θ_W = g₁²/(g₁²+g₂²) = 1/(1 + g₂²/g₁²)
# If sin²θ_W = φ⁻³, then g₂²/g₁² = 1/φ⁻³ - 1 = φ³ - 1
target_ratio = phi**3 - 1
print(f"  If sin²θ_W = φ⁻³: g₂²/g₁² = φ³ - 1 = {target_ratio:.6f}")
print(f"  Measured:          g₂²/g₁² = {ratio_sq:.6f}")
print(f"  Error: {abs(ratio_sq - target_ratio)/ratio_sq*100:.3f}%")
print()

# φ³ - 1 = φ² + φ - 1 = 2φ (using φ²=φ+1) ... wait
# φ³ = φ² × φ = (φ+1)φ = φ² + φ = 2φ + 1
# φ³ - 1 = 2φ = √5 + 1 = 3.236...
print(f"  φ³ - 1 = 2φ = {phi**3 - 1:.6f} = {2*phi:.6f}  ✓")
print(f"  So: g₂²/g₁² = 2φ at the scale where sin²θ_W = φ⁻³")
print()

# If g₂ = 2φ/5 AND g₂²/g₁² = 2φ, then:
# g₁² = g₂²/(2φ) = (2φ/5)²/(2φ) = 4φ²/(25·2φ) = 2φ/25 = λ!
g1_from_chain = sqrt(g2_target**2 / (2*phi))
print("═" * 65)
print("  ★ KEY DISCOVERY: g₁² = g₂²/(2φ) = 4φ²/(50φ) = 2φ/25 = λ !")
print("═" * 65)
print()
print(f"  If g₂ = 2φ/5 and g₂²/g₁² = 2φ:")
print(f"    g₁² = (2φ/5)² / (2φ) = 4φ²/(25·2φ) = 2φ/25")
print(f"    g₁² = {g2_target**2/(2*phi):.8f}")
print(f"    But 2φ/25 = λ = {2*phi/25:.8f}")
print(f"    g₁ = √(2φ/25) = {sqrt(2*phi/25):.8f}")
print(f"    g₁ measured at M_Z = {g1_MZ:.8f}")
print(f"    Error: {abs(g1_from_chain - g1_MZ)/g1_MZ*100:.3f}%")
print()
print("  THIS IS EXTRAORDINARY:")
print("  g₁² = λ_Higgs = 2φ/5²")
print()
print("  The U(1) coupling squared equals the Higgs quartic!")
print("  Both are 2φ/25. Same formula. Different sector.")
print()

# Is this a known SM relation? Let's check numerically at M_Z
print(f"  At M_Z:")
print(f"    g₁² = {g1_MZ**2:.6f}")
print(f"    λ(m_t) = 0.12604")
print(f"    λ(tree) = {m_H**2/(2*v_ew**2):.6f}")
print(f"    g₁²/λ(tree) = {g1_MZ**2/(m_H**2/(2*v_ew**2)):.6f}")
print()

# Not exactly equal in the SM, but close!
# The relation g₁² ≈ λ would hold at the specific scale where
# both are equal to 2φ/25

# At what scale does g₁² = λ in the SM?
# g₁ increases, λ decreases going up
# They must cross somewhere

print("═" * 65)
print("  WHERE DOES g₁² = λ IN THE SM?")
print("═" * 65)
print()

# Need to run λ and g₁ together
def beta_all(t, y):
    lam, yt, g3, g2, g1 = y
    yt2, yt4 = yt**2, yt**4
    g32, g22, g12 = g3**2, g2**2, g1**2
    fac = 1/(16*pi**2)
    b_lam = fac * (24*lam**2 - 6*yt4 + 12*lam*yt2 
                   - 3*lam*(3*g22 + g12) + (3.0/8)*(2*g22**2 + (g22+g12)**2))
    b_yt = fac * yt * ((9.0/2)*yt2 - 8*g32 - (9.0/4)*g22 - (17.0/12)*g12)
    b_g3 = fac * (-7) * g3**3
    b_g2 = fac * (-19.0/6) * g2**3
    b_g1 = fac * (41.0/6) * g1**3
    return [b_lam, b_yt, b_g3, b_g2, b_g1]

# Initial at m_t
y0_all = [0.12604, 0.93690, 1.1666, 0.64779, 0.35830]
sol_all = solve_ivp(beta_all, [0, log(1e19/m_t)], y0_all,
                    method='RK45', dense_output=True, rtol=1e-10, atol=1e-12)

# Also downward
sol_all_down = solve_ivp(beta_all, [0, log(50/m_t)], y0_all,
                         method='RK45', dense_output=True, rtol=1e-10, atol=1e-12)

def g1sq_minus_lam(t):
    vals = sol_all.sol(t)
    lam, yt, g3, g2, g1 = vals
    return g1**2 - lam

# Check endpoints
vals_0 = sol_all.sol(0)
vals_end = sol_all.sol(log(1e19/m_t))
print(f"  At m_t: g₁² = {vals_0[4]**2:.6f}, λ = {vals_0[0]:.6f}, diff = {vals_0[4]**2 - vals_0[0]:+.6f}")
print(f"  At 10¹⁹: g₁² = {vals_end[4]**2:.6f}, λ = {vals_end[0]:.6f}, diff = {vals_end[4]**2 - vals_end[0]:+.6f}")

try:
    t_equal = brentq(g1sq_minus_lam, 0, log(1e8/m_t))
    mu_equal = m_t * np.exp(t_equal)
    vals_eq = sol_all.sol(t_equal)
    lam_eq, yt_eq, g3_eq, g2_eq, g1_eq = vals_eq
    
    print(f"\n  g₁² = λ at μ = {mu_equal:.1f} GeV  (log₁₀ = {log10(mu_equal):.3f})")
    print(f"    g₁² = λ = {g1_eq**2:.6f}")
    print(f"    g₁ = {g1_eq:.6f}")
    print(f"    g₂ = {g2_eq:.6f}  (2φ/5 = {2*phi/5:.6f}, err: {abs(g2_eq-2*phi/5)/g2_eq*100:.3f}%)")
    print(f"    g₃ = {g3_eq:.6f}")
    print(f"    y_t = {yt_eq:.6f}")
    print()
    
    # Is g₁² = λ = 2φ/25 at this scale?
    print(f"    g₁² = {g1_eq**2:.6f}")
    print(f"    2φ/25 = {2*phi/25:.6f}")
    print(f"    Error from 2φ/25: {abs(g1_eq**2 - 2*phi/25)/(2*phi/25)*100:.3f}%")
    print()
    
    # How close to m_H?
    print(f"    μ/m_H = {mu_equal/m_H:.4f}")
    print(f"    μ/M_Z = {mu_equal/M_Z:.4f}")
    print(f"    μ/m_t = {mu_equal/m_t:.4f}")
    
except Exception as e:
    print(f"  Error finding crossing: {e}")
    # Let's see the profile
    t_scan = np.linspace(0, log(1e8/m_t), 10000)
    for t in t_scan[::500]:
        vals = sol_all.sol(t)
        mu = m_t * np.exp(t)
        print(f"    μ={mu:.0f}: g₁²={vals[4]**2:.6f}, λ={vals[0]:.6f}, diff={vals[4]**2-vals[0]:+.6f}")

print()
print("═" * 65)
print("  SUMMARY")
print("═" * 65)
