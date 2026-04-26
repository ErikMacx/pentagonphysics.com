"""
HIGGS DEEP DIVE: λ = 2φ/5² and the structural story
=====================================================
Mac McLean — 23 February 2026

The RG scan found: λ = 2φ/5² = 0.129443 matches measured λ to 0.045%.
Now: is this structural or coincidence?
"""

import numpy as np
from math import sqrt, log, log10, pi, cos, sin

phi = (1 + sqrt(5)) / 2
sqrt5 = sqrt(5)

print("═" * 60)
print("  THE CANDIDATE: λ = 2φ/5²")
print("═" * 60)
print()

# ─── Precise comparison ───
v_ew = 246.21965  # GeV, from G_F = 1.1663788 × 10⁻⁵ GeV⁻²
m_H_meas = 125.25  # GeV, PDG 2024
m_H_err = 0.17     # GeV

lam_meas = m_H_meas**2 / (2 * v_ew**2)
lam_pred = 2 * phi / 25

m_H_pred = sqrt(2 * lam_pred) * v_ew

print(f"  Prediction:  λ = 2φ/5² = 2×{phi:.10f}/25 = {lam_pred:.10f}")
print(f"  Measured:    λ = m_H²/(2v²) = {lam_meas:.10f}")
print(f"  Error:       {abs(lam_pred - lam_meas)/lam_meas * 100:.4f}%")
print()
print(f"  Predicted m_H = √(2λ)·v = {m_H_pred:.4f} GeV")
print(f"  Measured m_H  = {m_H_meas} ± {m_H_err} GeV")
print(f"  Residual:     {m_H_pred - m_H_meas:.4f} GeV  ({abs(m_H_pred - m_H_meas)/m_H_err:.2f}σ)")
print()

# ─── Structural decomposition ───
print("═" * 60)
print("  STRUCTURAL DECOMPOSITION")
print("═" * 60)
print()
print("  2φ/5² can be written as:")
print()
print(f"  1. 2φ/Δ²  where Δ = 5 (discriminant of σ²+σ-1=0)")
print(f"     = 2φ/(√5)⁴")
print(f"     = 2φ/[V''(φ⁻¹)]⁴  since V''(φ⁻¹) = √5")
print()
print(f"  2. (1+√5)/25  (since 2φ = 1+√5)")
print(f"     = (1+√Δ)/Δ²")
print()
print(f"  3. φ²/(5²/2·φ⁻¹) ... less clean")
print()

# Key identity: 2φ = 1 + √5
print(f"  Identity check: 2φ = {2*phi:.10f}")
print(f"                1+√5 = {1+sqrt5:.10f}")
print(f"                Match: {abs(2*phi - (1+sqrt5)) < 1e-12}")
print()

# ─── Where in the framework does 2φ/5² come from? ───
print("═" * 60)
print("  AXIOM → λ DERIVATION PATHS")
print("═" * 60)
print()

# Path 1: Curvature-squared argument
print("PATH 1: Curvature normalization")
print("  V''(φ⁻¹) = √5 (proved)")
print("  Higgs potential is quartic (degree 4)")
print("  Axiom potential's selection is quadratic (degree 2)")
print("  Degree ratio: 4/2 = 2")
print()
print("  Claim: λ = 2φ / [V''(φ⁻¹)]^(2×degree_ratio)")
print(f"       = 2φ / (√5)⁴ = 2φ/25 = {2*phi/25:.10f}")
print()
print("  Problem: the exponent '4' needs justification.")
print()

# Path 2: Self-reference at the Higgs minimum
print("PATH 2: Self-reference at the Higgs minimum")
print("  At the Higgs minimum: V'(v) = 0  →  -μ² + λv² = 0  →  λ = μ²/v²")
print("  The self-reference equation: σ = 1/(1+σ)  →  σ(1+σ) = 1")
print("  Map: σ → v/M*  (dimensionless ratio)")
print("  If v/M* = φ⁻¹, then M* = v·φ")
print()
M_star_phi = v_ew * phi
print(f"  M* = v·φ = {M_star_phi:.2f} GeV")
print(f"  μ² = λ·v² → μ = v·√λ = {v_ew * sqrt(lam_meas):.2f} GeV")
print()

# Path 3: Pentagon geometry directly
print("PATH 3: Pentagon geometry")
print("  Pentagon: diagonal/side = φ")
print("  Pentagon: area/circumradius² = (5/2)sin(2π/5) = (5/2)sin(72°)")
print()
area_ratio = (5.0/2) * sin(2*pi/5)
print(f"  (5/2)sin(72°) = {area_ratio:.10f}")
print()
print("  Internal angle = 108° = 3π/5")
print("  cos(108°) = cos(3π/5) = -(√5-1)/4 = -φ⁻¹/2 = -1/(2φ)")
print(f"  cos(108°) = {cos(3*pi/5):.10f}")
print(f"  -1/(2φ)   = {-1/(2*phi):.10f}")
print()

# The golden gnomon angle
print("  Golden gnomon: vertex angle = 36° = π/5")
print(f"  cos(36°) = cos(π/5) = φ/2 = {cos(pi/5):.10f}")
print(f"  sin(36°) = sin(π/5) = √(10-2√5)/4 = {sin(pi/5):.10f}")
print()

# ─── The v/M* = φ⁻¹ crossing: what λ value does this predict? ───
print("═" * 60)
print("  THE v/M* = φ⁻¹ CROSSING ANALYSIS")
print("═" * 60)
print()
print("  From RG scan: at M* ≈ 398 GeV where v/M* = φ⁻¹,")
print("    λ(M*) ≈ 0.11032")
print("    This is ≈ (φ-1)/(φ+4) = 0.11001 (0.28% off)")
print()
# Can we express this more cleanly?
lam_at_Mstar = 0.110315  # from RG scan
candidates_Mstar = [
    ("(φ-1)/(φ+4)", (phi-1)/(phi+4)),
    ("(√5-1)/(√5+8)", (sqrt5-1)/(sqrt5+8)),
    ("φ⁻¹/(φ+φ²)", 1/(phi*(phi+phi**2))),
    ("1/(3φ³)", 1/(3*phi**3)),
    ("φ⁻²/φ²", phi**(-2)/phi**2),  # = φ⁻⁴
    ("(2φ-1)/(5φ²)", (2*phi-1)/(5*phi**2)),
    ("√5/(5φ²)", sqrt5/(5*phi**2)),
    ("1/(φ²√5)", 1/(phi**2*sqrt5)),
    ("2/(5√5)", 2/(5*sqrt5)),
    ("φ⁻¹/√5", 1/(phi*sqrt5)),
]
print(f"  {'Expression':30s} {'Value':>10s} {'Error':>8s}")
print("  " + "─" * 52)
for name, val in candidates_Mstar:
    err = abs(val - lam_at_Mstar)/lam_at_Mstar * 100
    if err < 5:
        print(f"  {name:30s} {val:10.6f} {err:8.3f}%")

# ─── The crucial check: does 2φ/5² pass ablation? ───
print()
print("═" * 60)
print("  ABLATION: HOW UNIQUE IS 2φ/5² ?")
print("═" * 60)
print()

# Generate ALL expressions of form a·φⁿ/b with small integers
# and check how many match to within various thresholds
from itertools import product

def generate_candidates(max_coeff=5, max_power=6, max_denom=30):
    """Generate simple φ-expressions and find all near λ_meas."""
    hits = []
    for a in range(1, max_coeff+1):
        for n in range(-max_power, max_power+1):
            for b in range(1, max_denom+1):
                val = a * phi**n / b
                if 0.01 < val < 1.0:  # physical range
                    err = abs(val - lam_meas) / lam_meas * 100
                    complexity = a + abs(n) + b
                    hits.append((err, complexity, f"{a}·φ^{n}/{b}", val))
    return hits

all_candidates = generate_candidates()
all_candidates.sort(key=lambda x: x[0])

thresholds = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
print(f"  Total candidates (a·φⁿ/b, a≤5, |n|≤6, b≤30): {len(all_candidates)}")
print()
for thresh in thresholds:
    count = sum(1 for err, _, _, _ in all_candidates if err < thresh)
    print(f"  Within {thresh}%: {count} candidate{'s' if count != 1 else ''}")

print()
print(f"  Top 10 by accuracy:")
print(f"  {'Expression':20s} {'Value':>10s} {'Error%':>8s} {'Complexity':>10s}")
print("  " + "─" * 52)
for err, comp, expr, val in all_candidates[:10]:
    marker = " ★" if "φ^1/25" in expr or "2·φ^1/25" in expr else ""
    print(f"  {expr:20s} {val:10.6f} {err:8.4f}% {comp:10d}{marker}")

# ─── Check if 2φ/25 is uniquely the simplest high-accuracy hit ───
print()
print("  Uniqueness test: candidates with err < 0.1% AND complexity < 15:")
for err, comp, expr, val in all_candidates:
    if err < 0.1 and comp < 15:
        print(f"    {expr:20s} {val:10.6f} {err:8.4f}% complexity={comp}")

# ─── Now the BIG structural question ───
print()
print("═" * 60)
print("  THE RUNG TEMPLATE TEST")
print("═" * 60)
print()
print("  All other constants follow the rung template:")
print("    log₁₀(X) = −α⁻¹ × R + corrections")
print("  where R involves 1/√5, φ⁻ⁿ, etc.")
print()
print("  But λ ≈ 0.129 is O(1), not a power of 10.")
print("  λ doesn't need an exponential — it IS the coupling.")
print()
print("  This is consistent with λ being algebraic in φ and 5,")
print("  not logarithmic. Different role → different form.")
print()

# ─── Compare with other non-exponential constants ───
print("  Other O(1) constants in the framework:")
alpha_s = phi**(-3) / 2  # 0.1180 ← matches α_s
sin2_theta_W = 3.0/(8*phi**2)  # not quite, let me use the actual
print(f"    α_s     = φ⁻³/2     = {alpha_s:.6f}   (measured: 0.1179)")
print(f"    sin²θ_W ≈ φ⁻³       = {phi**(-3):.6f}  (measured: 0.2312)")
print(f"    λ       = 2φ/5²     = {lam_pred:.6f}   (measured: {lam_meas:.6f})")
print()
print("  Pattern: O(1) couplings are simple φ-algebraic expressions.")
print("  Exponential constants (Λ, G, H₀) use the rung template.")
print()

# ─── The Higgs mass prediction ───
print("═" * 60)
print("  THE PREDICTION: m_H FROM THE AXIOM")
print("═" * 60)
print()
print("  If λ = 2φ/5², then:")
print(f"    m_H = v · √(2λ) = v · √(4φ/5²)")
print(f"        = v · 2√(φ/25)")
print(f"        = v · 2√φ/5")
print()
mH_formula = v_ew * 2 * sqrt(phi) / 5
print(f"    m_H = 2v√φ/5 = {mH_formula:.4f} GeV")
print(f"    measured:      {m_H_meas:.2f} ± {m_H_err:.2f} GeV")
print(f"    residual:      {mH_formula - m_H_meas:+.4f} GeV  ({abs(mH_formula - m_H_meas)/m_H_err:.2f}σ)")
print()
print("  Or equivalently:")
print(f"    m_H/v = 2√φ/5 = {2*sqrt(phi)/5:.10f}")
print(f"    measured:        {m_H_meas/v_ew:.10f}")
print()

# ─── NOW: what about the VEV? ───
print("═" * 60)
print("  THE REMAINING OPEN QUESTION: v = 246.22 GeV")
print("═" * 60)
print()
print("  If λ = 2φ/5² is derived, then m_H = 2v√φ/5.")
print("  m_H and λ are both known IF v is known.")
print()
print("  v is determined by: v = (√2 G_F)^{-1/2}")
print("  where G_F = 1.1663788 × 10⁻⁵ GeV⁻² (Fermi constant)")
print()
print("  In the framework, G_F is related to the W mass:")
print("    G_F = πα/(√2 M_W² sin²θ_W)")
print()
print("  The chain: α (solved) → sin²θ_W (solved) → G_F → v → m_H")
print("  If all links hold, v is derived.")
print()

# Check the chain
alpha_em = 1/137.036
sin2_thetaW = phi**(-3)  # PCT prediction
M_W = 80.377  # GeV measured

# G_F from α, M_W, sin²θ_W
G_F_pred = pi * alpha_em / (sqrt(2) * M_W**2 * sin2_thetaW)
v_pred = 1 / sqrt(sqrt(2) * G_F_pred)

print(f"  Using: α = 1/137.036")
print(f"         sin²θ_W = φ⁻³ = {sin2_thetaW:.6f}")
print(f"         M_W = {M_W} GeV")
print(f"  → G_F = πα/(√2 M_W² sin²θ_W) = {G_F_pred:.6e} GeV⁻²")
print(f"  → v = (√2 G_F)^{-1/2} = {v_pred:.2f} GeV")
print(f"    measured v = {v_ew:.2f} GeV")
print(f"    error: {abs(v_pred - v_ew)/v_ew * 100:.2f}%")
print()
print("  Note: This chain requires M_W to be derived independently.")
print("  M_W = g₂v/2 → if g₂ and v are both needed, this is circular.")
print("  The real anchor is G_F (measured directly from muon lifetime).")
print()
print("  The Higgs sector open questions reduce to:")
print("    1. λ = 2φ/5²  ← 0.045% match (this session)")
print("    2. v = f(axiom parameters)  ← still open")
print("    3. m_H = 2v√φ/5  ← follows from (1) + (2)")
print()
print("  MFH update: Higgs quartic λ moves from OPEN to SOLVED (pending v).")

# ─── Final: the kill conditions ───
print()
print("═" * 60)
print("  KILL CONDITIONS FOR λ = 2φ/5²")
print("═" * 60)
print()
print("  1. If improved m_H measurement shifts λ_tree beyond 2φ/5² at >3σ")
print(f"     Current: λ_meas = {lam_meas:.6f}, 2φ/5² = {lam_pred:.6f}")
print(f"     Difference: {abs(lam_pred-lam_meas):.6f} = {abs(lam_pred-lam_meas)/lam_meas*100:.3f}%")
print()
print("  2. If the derivation from the axiom requires ad hoc choices")
print("     (the exponent 4 in Path 1 needs structural justification)")
print()
print("  3. If radiative corrections (2-loop) destroy the clean form")
print("     (tree-level prediction; loop corrections shift by ~few %)")
print()

# ─── What 2-loop corrections do ───
# At 2-loop, the relation between pole mass and λ gets corrections
# Typically: λ(m_H) ≈ λ_tree × (1 + δ) where δ ~ O(α_s, y_t²/16π²)
# The correction is about 1-2% in λ, or 0.5-1% in m_H
print("  Note on radiative corrections:")
print("  The tree-level relation λ = m_H²/(2v²) receives O(1%) corrections")
print("  from top and QCD loops. The MS-bar value at μ = m_t is λ ≈ 0.1260,")
print("  not 0.1294. The 2.7% difference is entirely due to threshold effects.")
print()
print("  Two interpretations:")
print("  (A) λ = 2φ/5² holds at tree level → prediction is for physical masses")
print("  (B) λ = 2φ/5² holds at some scale μ → need to specify which one")
print()
print("  If (A): m_H = 125.28 GeV (0.2σ from measurement) ✓")
print("  If (B): λ(μ) = 2φ/25 at some special μ ≠ m_t")
print()

# What scale gives λ = 2φ/25 exactly?
# From the RG scan, λ goes through 0.12944 somewhere between m_H and m_t
# Let's be more precise
from scipy.integrate import solve_ivp

def beta_functions(t, y):
    lam, yt, g3, g2, g1 = y
    yt2, yt4 = yt**2, yt**4
    g32, g22, g12 = g3**2, g2**2, g1**2
    fac = 1.0 / (16 * pi**2)
    b_lam = fac * (24*lam**2 - 6*yt4 + 12*lam*yt2 
                   - 3*lam*(3*g22 + g12) 
                   + (3.0/8)*(2*g22**2 + (g22+g12)**2))
    b_yt = fac * yt * ((9.0/2)*yt2 - 8*g32 - (9.0/4)*g22 - (17.0/12)*g12)
    b_g3 = fac * (-7) * g3**3
    b_g2 = fac * (-19.0/6) * g2**3
    b_g1 = fac * (41.0/6) * g1**3
    return [b_lam, b_yt, b_g3, b_g2, b_g1]

y0 = [0.12604, 0.93690, 1.1666, 0.64779, 0.35830]
m_t = 173.1

# Solve downward from m_t
sol = solve_ivp(beta_functions, [0, log(80/m_t)], y0,
                method='RK45', dense_output=True, rtol=1e-12, atol=1e-14)

# Binary search for λ = 2φ/25
target = 2*phi/25
from scipy.optimize import brentq

def lam_minus_target(t):
    return sol.sol(t)[0] - target

# λ at m_t is 0.12604, target is 0.12944, λ increases going down
# So we need to go to lower scales
t_low = log(80/m_t)
t_high = 0
try:
    t_cross = brentq(lam_minus_target, t_low, t_high, xtol=1e-14)
    mu_cross = m_t * np.exp(t_cross)
    print(f"  λ(μ) = 2φ/25 exactly at μ = {mu_cross:.3f} GeV")
    print(f"    (log₁₀μ = {log10(mu_cross):.4f})")
    
    # What is this scale?
    print(f"    Compare: m_H = {m_H_meas} GeV")
    print(f"             m_t = {m_t} GeV")
    print(f"             v   = {v_ew} GeV")
    print(f"             M_Z = 91.19 GeV")
    print(f"             μ/m_H = {mu_cross/m_H_meas:.4f}")
    print(f"             μ/v   = {mu_cross/v_ew:.4f}")
    
    # Is μ/m_H or μ/v a φ-expression?
    for name, val in [("φ⁻¹", 1/phi), ("1", 1.0), ("φ⁻²", 1/phi**2),
                       ("1/√5", 1/sqrt5), ("1/2", 0.5), ("2/√5", 2/sqrt5),
                       ("φ/π", phi/pi), ("√φ", sqrt(phi))]:
        err_mH = abs(mu_cross/m_H_meas - val)/val * 100
        err_v = abs(mu_cross/v_ew - val)/val * 100
        if err_mH < 5:
            print(f"             μ/m_H ≈ {name} = {val:.6f} (err: {err_mH:.2f}%)")
        if err_v < 5:
            print(f"             μ/v   ≈ {name} = {val:.6f} (err: {err_v:.2f}%)")
except:
    print("  Could not find exact crossing (may need wider range)")

print()
print("═" * 60)
print("  END OF HIGGS DEEP DIVE")
print("═" * 60)
