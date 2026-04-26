"""
Higgs RG Hunt: At what scale does λ(μ) hit a φ-expression?
============================================================
Mac McLean — Pentagon Physics / Primary Coherence Theory
23 February 2026

Physics:
  SM 1-loop RG equations for λ, y_t, g_3, g_2, g_1
  Initial conditions at μ = m_t (MS-bar)
  Scan for φ-expressions across the full range

The hunting question:
  1. At what energy scale does λ run to a clean φ-expression?
  2. What is M* such that v/M* = φ⁻¹ (or another clean ratio)?
"""

import numpy as np
from scipy.integrate import solve_ivp
from math import sqrt, log, log10, pi

# ─── Constants ───
phi  = (1 + sqrt(5)) / 2      # 1.6180339887...
phi2 = phi**2                   # 2.6180339887...
phi3 = phi**3                   # 4.2360679775...
phi4 = phi**4                   # 6.8541019662...
sqrt5 = sqrt(5)
v_ew = 246.2196                 # GeV (Higgs VEV)
m_H  = 125.25                  # GeV (Higgs mass, PDG 2024)
m_t  = 173.1                   # GeV (top pole mass)

# ─── Tree-level λ at EW scale ───
lam_tree = m_H**2 / (2 * v_ew**2)
print(f"Tree-level λ = m_H²/(2v²) = {lam_tree:.6f}")
print(f"  m_H = {m_H} GeV, v = {v_ew} GeV")
print()

# ─── Initial conditions at μ = m_t (MS-bar, from Buttazzo+ 2013 style) ───
# These include threshold corrections
lam_mt = 0.12604    # Higgs quartic at m_t
yt_mt  = 0.93690    # top Yukawa at m_t  
g3_mt  = 1.1666     # strong coupling at m_t
g2_mt  = 0.64779    # SU(2) coupling at m_t
g1_mt  = 0.35830    # U(1) coupling at m_t (GUT normalisation √(5/3)g')

print("═══════════════════════════════════════════════════")
print("  SM 1-LOOP RG RUNNING OF THE HIGGS QUARTIC λ")
print("═══════════════════════════════════════════════════")
print()
print(f"Initial conditions at μ = m_t = {m_t} GeV:")
print(f"  λ   = {lam_mt}")
print(f"  y_t = {yt_mt}")
print(f"  g_3 = {g3_mt}")
print(f"  g_2 = {g2_mt}")
print(f"  g_1 = {g1_mt}")
print()

# ─── 1-loop beta functions ───
# t = ln(μ/m_t), so μ = m_t × exp(t)
# y = [λ, y_t, g_3, g_2, g_1]

def beta_functions(t, y):
    lam, yt, g3, g2, g1 = y
    
    # Useful combinations
    yt2 = yt**2
    yt4 = yt**4
    g32 = g3**2
    g22 = g2**2
    g12 = g1**2
    lam2 = lam**2
    
    fac = 1.0 / (16 * pi**2)
    
    # β_λ (1-loop)
    b_lam = fac * (
        24*lam2
        - 6*yt4
        + 12*lam*yt2
        - 3*lam*(3*g22 + g12)
        + (3.0/8)*(2*g22**2 + (g22 + g12)**2)
    )
    
    # β_yt (1-loop)
    b_yt = fac * yt * (
        (9.0/2)*yt2
        - 8*g32
        - (9.0/4)*g22
        - (17.0/12)*g12
    )
    
    # β_g3 (1-loop, n_f = 6)
    b_g3 = fac * (-7) * g3**3
    
    # β_g2 (1-loop)
    b_g2 = fac * (-19.0/6) * g2**3
    
    # β_g1 (1-loop, GUT normalisation)
    b_g1 = fac * (41.0/6) * g1**3
    
    return [b_lam, b_yt, b_g3, b_g2, b_g1]

# ─── Solve from m_t upward to Planck scale ───
y0 = [lam_mt, yt_mt, g3_mt, g2_mt, g1_mt]

# t = ln(μ/m_t), range: μ from m_t to ~10^19 GeV
t_max = log(1e19 / m_t)  # ~39
t_min_down = log(50 / m_t)  # down to ~50 GeV

# Solve upward
sol_up = solve_ivp(beta_functions, [0, t_max], y0, 
                   method='RK45', dense_output=True,
                   rtol=1e-10, atol=1e-12,
                   max_step=0.1)

# Solve downward
sol_down = solve_ivp(beta_functions, [0, t_min_down], y0,
                     method='RK45', dense_output=True,
                     rtol=1e-10, atol=1e-12,
                     max_step=0.01)

print("RG integration complete.")
print()

# ─── φ-expression targets ───
targets = {
    "φ⁻⁴ = (7−3√5)/2":      phi**(-4),     # 0.14590
    "1/(2φ³)  [= α_s!]":     1/(2*phi3),    # 0.11803
    "φ⁻²/2":                  1/(2*phi2),    # 0.19098
    "1/φ⁴":                   1/phi4,        # 0.14590
    "1/(5φ)":                 1/(5*phi),     # 0.12361
    "φ⁻²/√5":                1/(phi2*sqrt5),# 0.17082
    "(√5−2)":                 sqrt5 - 2,     # 0.23607
    "1/(2√5)":                1/(2*sqrt5),   # 0.22361
    "φ⁻¹/5":                  1/(5*phi),     # 0.12361
    "2/(5φ²)":                2/(5*phi2),    # 0.15279
    "(3−√5)/4":               (3-sqrt5)/4,   # 0.19098
    "1/(φ²+5)":               1/(phi2+5),    # 0.13150
    "φ⁻³":                    phi**(-3),     # 0.23607
    "φ/(2·5)":                phi/10,        # 0.16180
    "5/(φ⁵·π²)":             5/(phi**5*pi**2),
    "1/(φ²π)":               1/(phi2*pi),   # 0.12159
    "1/(2φ²+1)":             1/(2*phi2+1),  # 0.15956
    "√5/(φ⁴+φ²)":           sqrt5/(phi4+phi2),
    "1/(2φ⁴−1)":            1/(2*phi4-1),   
    "φ⁻²·(1−φ⁻²)":         (1/phi2)*(1 - 1/phi2),
    "(√5−1)/(2·5)":          (sqrt5-1)/10,  # = φ⁻¹/5
    "2φ⁻⁵":                  2*phi**(-5),   # 0.18034
    "1/φ⁵":                   phi**(-5),     # 0.09017
    "1/(5+φ⁻¹)":            1/(5 + 1/phi),  # 0.17798
    "1/(3φ²)":               1/(3*phi2),    # 0.12733  ← CLOSE!
    "φ⁻²·π/(4π+1)":         (1/phi2)*pi/(4*pi+1),
    "√5/φ⁵":                 sqrt5/phi**5,  # 0.20165
}

# Add some compound expressions
targets["2/(φ⁴+φ²+5)"]   = 2/(phi4 + phi2 + 5)  
targets["1/(φ³+φ)"]        = 1/(phi3 + phi)
targets["(φ−1)/(φ+4)"]     = (phi-1)/(phi+4)
targets["(φ²−2)/φ³"]       = (phi2-2)/phi3
targets["φ/(φ³+8)"]        = phi/(phi3+8)

# Sort by value for display
sorted_targets = sorted(targets.items(), key=lambda x: x[1])

print("═══════════════════════════════════════════════════")
print("  φ-EXPRESSION TARGETS")
print("═══════════════════════════════════════════════════")
for name, val in sorted_targets:
    if 0.05 < val < 0.30:  # relevant range
        print(f"  {name:30s} = {val:.6f}")
print()

# ─── Scan for crossings ───
print("═══════════════════════════════════════════════════")
print("  SCANNING FOR λ(μ) = φ-EXPRESSION CROSSINGS")
print("═══════════════════════════════════════════════════")
print()

# Build fine grid
t_vals_up = np.linspace(0, t_max, 100000)
lam_vals_up = sol_up.sol(t_vals_up)[0]

t_vals_down = np.linspace(0, t_min_down, 10000)
lam_vals_down = sol_down.sol(t_vals_down)[0]

# Combine (reversed down + up)
t_all = np.concatenate([t_vals_down[::-1], t_vals_up[1:]])
lam_all = np.concatenate([lam_vals_down[::-1], lam_vals_up[1:]])
mu_all = m_t * np.exp(t_all)

# Find crossings for each target
crossings = []
for name, target_val in sorted_targets:
    if target_val < lam_all.min() or target_val > lam_all.max():
        continue
    # Find sign changes
    diff = lam_all - target_val
    for i in range(len(diff)-1):
        if diff[i] * diff[i+1] < 0:
            # Linear interpolation
            frac = abs(diff[i]) / (abs(diff[i]) + abs(diff[i+1]))
            mu_cross = mu_all[i] + frac * (mu_all[i+1] - mu_all[i])
            t_cross = t_all[i] + frac * (t_all[i+1] - t_all[i])
            crossings.append((name, target_val, mu_cross, t_cross))

# Sort by closeness of target to measured λ
crossings.sort(key=lambda x: x[2])

# Display
print(f"{'φ-expression':35s} {'target':>10s} {'μ (GeV)':>14s} {'log₁₀μ':>8s} {'v/μ':>10s}")
print("─" * 85)
for name, val, mu_cross, t_cross in crossings:
    log_mu = log10(mu_cross)
    v_over_mu = v_ew / mu_cross if mu_cross > 0 else float('inf')
    marker = ""
    # Check if v/μ is a φ-expression
    for ratio_name, ratio_val in [("φ⁻¹", 1/phi), ("φ⁻²", 1/phi2), 
                                    ("1/√5", 1/sqrt5), ("2/√5", 2/sqrt5),
                                    ("φ⁻³", 1/phi3), ("1/5", 0.2),
                                    ("1", 1.0), ("φ", phi)]:
        if abs(v_over_mu - ratio_val) / ratio_val < 0.05:
            marker = f"  ← v/μ ≈ {ratio_name} ({ratio_val:.4f})"
            break
    print(f"  {name:33s} {val:10.6f} {mu_cross:14.2f} {log_mu:8.3f} {v_over_mu:10.6f}{marker}")

print()

# ─── Detailed profile of λ vs scale ───
print("═══════════════════════════════════════════════════")
print("  λ(μ) PROFILE AT KEY SCALES")
print("═══════════════════════════════════════════════════")
print()

key_scales = [50, 80, 91.2, 125.25, 173.1, 246, 500, 1000, 5000, 
              1e4, 1e5, 1e6, 1e8, 1e10, 1e12, 1e14, 1e16, 1e18, 1e19]

print(f"{'μ (GeV)':>14s} {'log₁₀μ':>8s} {'λ(μ)':>10s} {'y_t(μ)':>8s} {'g_3(μ)':>8s}")
print("─" * 55)
for mu in key_scales:
    t = log(mu / m_t)
    if t >= 0 and t <= t_max:
        vals = sol_up.sol(t)
    elif t < 0 and t >= t_min_down:
        vals = sol_down.sol(t)
    else:
        continue
    lam_val, yt_val, g3_val, g2_val, g1_val = vals
    print(f"  {mu:12.1f} {log10(mu):8.3f} {lam_val:10.6f} {yt_val:8.5f} {g3_val:8.5f}")

print()

# ─── The critical question: where does λ vanish? ───
# Find the scale where λ = 0 (instability boundary)
diff_zero = lam_vals_up
for i in range(len(diff_zero)-1):
    if diff_zero[i] * diff_zero[i+1] < 0:
        frac = abs(diff_zero[i]) / (abs(diff_zero[i]) + abs(diff_zero[i+1]))
        t_zero = t_vals_up[i] + frac * (t_vals_up[i+1] - t_vals_up[i])
        mu_zero = m_t * np.exp(t_zero)
        print(f"λ(μ) = 0 at μ = {mu_zero:.3e} GeV  (log₁₀ = {log10(mu_zero):.2f})")
        print(f"  This is the SM vacuum instability scale")
        break

# Find the minimum of λ
i_min = np.argmin(lam_vals_up)
t_min = t_vals_up[i_min]
mu_min = m_t * np.exp(t_min)
lam_min = lam_vals_up[i_min]
print(f"Minimum λ = {lam_min:.6f} at μ = {mu_min:.3e} GeV  (log₁₀ = {log10(mu_min):.2f})")
print()

# ─── v/M* analysis ───
print("═══════════════════════════════════════════════════")
print("  v/M* RATIO ANALYSIS")
print("═══════════════════════════════════════════════════")
print()
print("What scale M* gives v/M* = φ-expression?")
print()

ratio_targets = {
    "φ⁻¹ = 0.61803":    1/phi,
    "φ⁻² = 0.38197":    1/phi2,
    "1/√5 = 0.44721":   1/sqrt5,
    "2/√5 = 0.89443":   2/sqrt5,
    "φ⁻³ = 0.23607":    1/phi3,
    "1/5  = 0.20000":   0.2,
}

for name, ratio in sorted(ratio_targets.items(), key=lambda x: x[1]):
    M_star = v_ew / ratio
    t_star = log(M_star / m_t)
    if 0 <= t_star <= t_max:
        vals = sol_up.sol(t_star)
    elif t_min_down <= t_star < 0:
        vals = sol_down.sol(t_star)
    else:
        print(f"  v/M* = {name:20s}  →  M* = {M_star:.2f} GeV  (outside range)")
        continue
    lam_at_Mstar = vals[0]
    yt_at_Mstar = vals[1]
    print(f"  v/M* = {name:20s}  →  M* = {M_star:10.2f} GeV  →  λ(M*) = {lam_at_Mstar:.6f}  y_t(M*) = {yt_at_Mstar:.5f}")
    
    # Check if λ(M*) is a φ-expression
    for lam_name, lam_target in sorted_targets:
        if abs(lam_at_Mstar - lam_target) / max(abs(lam_at_Mstar), 1e-10) < 0.02:
            print(f"         ↑ λ(M*) ≈ {lam_name} = {lam_target:.6f}  (err: {abs(lam_at_Mstar-lam_target)/lam_at_Mstar*100:.2f}%)")

print()

# ─── Special investigation: 1/(3φ²) ───
val_target = 1/(3*phi2)
print("═══════════════════════════════════════════════════")
print(f"  SPECIAL: λ = 1/(3φ²) = {val_target:.6f}")
print("═══════════════════════════════════════════════════")
print()
print(f"  Measured λ(m_t)  = {lam_mt:.6f}")
print(f"  Target 1/(3φ²)   = {val_target:.6f}")
print(f"  Difference       = {(lam_mt - val_target)/lam_mt*100:.2f}%")
print()
# Is this close enough to be interesting?
# What scale does λ actually hit 1/(3φ²)?
for name, val, mu_cross, t_cross in crossings:
    if "1/(3φ²)" in name:
        print(f"  λ crosses 1/(3φ²) at μ = {mu_cross:.1f} GeV  (log₁₀ = {log10(mu_cross):.3f})")

# ─── The m_H prediction test ───
print()
print("═══════════════════════════════════════════════════")
print("  IF λ WERE EXACTLY A φ-EXPRESSION AT EW SCALE")
print("═══════════════════════════════════════════════════")
print()
print("  m_H = √(2λ) × v")
print()
for name, val in sorted_targets:
    if 0.10 < val < 0.20:
        m_H_pred = sqrt(2 * val) * v_ew
        err = (m_H_pred - m_H) / m_H * 100
        marker = " ★" if abs(err) < 1.0 else ""
        print(f"  λ = {name:30s} = {val:.6f}  →  m_H = {m_H_pred:.2f} GeV  ({err:+.2f}%){marker}")

print()

# ─── Deep structural test: λ = m²/(2v²) where m² connects to √5 ───
print("═══════════════════════════════════════════════════")
print("  STRUCTURAL: m_H² / v² AND φ-RELATIONS")
print("═══════════════════════════════════════════════════")
print()
ratio_mH_v = m_H / v_ew
ratio_mH2_v2 = m_H**2 / v_ew**2
print(f"  m_H/v     = {ratio_mH_v:.6f}")
print(f"  m_H²/v²   = {ratio_mH2_v2:.6f}  (= 2λ)")
print(f"  2λ        = {2*lam_tree:.6f}")
print()

# Check against φ-expressions
for name, val in [("1/√5", 1/sqrt5), ("2/√5", 2/sqrt5), ("φ⁻¹", 1/phi),
                   ("φ⁻²", 1/phi2), ("1/2", 0.5), ("φ/π", phi/pi),
                   ("1/φ√5", 1/(phi*sqrt5)), ("2/φ²", 2/phi2),
                   ("√5/φ³", sqrt5/phi3), ("1/π", 1/pi),
                   ("φ²/5", phi2/5), ("(√5-1)/5", (sqrt5-1)/5)]:
    err = (ratio_mH_v - val) / ratio_mH_v * 100
    if abs(err) < 10:
        print(f"  m_H/v ≈ {name:15s} = {val:.6f}  (err: {err:+.2f}%)")

print()
for name, val in [("1/√5", 1/sqrt5), ("2/√5", 2/sqrt5), ("φ⁻²", 1/phi2),
                   ("1/φ³", 1/phi3), ("2/(5φ)", 2/(5*phi)), ("φ²/5", phi2/5),
                   ("2/φ⁴", 2/phi4), ("1/φ²√5", 1/(phi2*sqrt5))]:
    err = (ratio_mH2_v2 - val) / ratio_mH2_v2 * 100
    if abs(err) < 15:
        print(f"  m_H²/v² ≈ {name:15s} = {val:.6f}  (err: {err:+.2f}%)")

# ─── The GPT Route C key object: dimensionless curvature ───
print()
print("═══════════════════════════════════════════════════")
print("  GPT ROUTE C: DIMENSIONLESS CURVATURE INVARIANTS")
print("═══════════════════════════════════════════════════")
print()
print("  V''(v)/μ² at the minimum:")
print(f"    C₁ = V''(v)/μ² = m_H²/μ² = 2 (tree-level, exact from form)")
print(f"    C₂ = V''(v)/(λv²) = 2 (tree-level)")
print(f"    C₃ = V''(v)·v²/|V(v)| = m_H²·v²/(λv⁴/4) = 4m_H²/(λv²) = 8")
print()
print("  None of these are √5 in the plain quartic.")
print("  BUT: the axiom potential V(σ) = σ³/3 + σ²/2 − σ gives V''(φ⁻¹) = √5")
print("  The dimensionless curvature IS √5 — at the axiom level.")
print()
print("  Route C claim: √5 encodes the selection equation's curvature,")
print("  not the literal potential's curvature.")
print()

# ─── The λ = 0.129 puzzle: what if λ is determined by the axiom? ───
print("═══════════════════════════════════════════════════")
print("  THE λ PUZZLE: STRUCTURAL CANDIDATES")
print("═══════════════════════════════════════════════════")
print()

# The measured value
lam_EW = lam_tree  # 0.12941

# Systematic search of simple φ-π expressions
import itertools

results = []
# Form: a·φ^n / (b·π^m · 5^k)  with small integers
for a in range(1, 6):
    for n in range(-6, 7):
        for b in range(1, 11):
            for m in range(0, 4):
                for k in range(0, 3):
                    val = a * phi**n / (b * pi**m * 5**k)
                    if 0.125 < val < 0.135:  # within ~5% of measured
                        err = abs(val - lam_EW) / lam_EW * 100
                        complexity = abs(a) + abs(n) + abs(b) + abs(m) + abs(k)
                        expr = f"{a}·φ^{n}/({b}·π^{m}·5^{k})"
                        results.append((err, complexity, expr, val))

# Also check forms like (a·φ^n + b·φ^m) / c
for a in range(-3, 4):
    for n in range(-5, 5):
        for b in range(-3, 4):
            for m in range(-5, 5):
                if a == 0 and b == 0: continue
                for c in range(1, 20):
                    val = (a*phi**n + b*phi**m) / c
                    if 0.125 < val < 0.135:
                        err = abs(val - lam_EW) / lam_EW * 100
                        complexity = abs(a) + abs(n) + abs(b) + abs(m) + abs(c)
                        expr = f"({a}·φ^{n}+{b}·φ^{m})/{c}"
                        if complexity < 15:
                            results.append((err, complexity, expr, val))

results.sort(key=lambda x: (x[0], x[1]))

print(f"  Measured λ = {lam_EW:.6f}")
print(f"  {'Expression':40s} {'Value':>10s} {'Error%':>8s} {'Complexity':>10s}")
print("  " + "─" * 72)
seen = set()
count = 0
for err, comp, expr, val in results:
    val_key = round(val, 7)
    if val_key in seen:
        continue
    seen.add(val_key)
    print(f"  {expr:40s} {val:10.6f} {err:8.4f}% {comp:10d}")
    count += 1
    if count >= 25:
        break

print()

# ─── Check the specific candidate: m_H² = 2v²·λ with λ = f(φ) ───
# If m_H = v·√(2λ), and we know v ≈ 246 GeV, then:
#   m_H/v = √(2λ) ≈ 0.5087
# What is 0.5087 as a φ-expression?
print("═══════════════════════════════════════════════════")
print("  m_H/v = √(2λ) ANALYSIS")
print("═══════════════════════════════════════════════════")
print()
r = m_H / v_ew
print(f"  m_H/v = {r:.6f}")
print(f"  (m_H/v)² = 2λ = {r**2:.6f}")
print()
# Close φ-expressions for r ≈ 0.5087
candidates_r = [
    ("1/2", 0.5),
    ("φ⁻¹/√(φ+1)", 1/(phi*sqrt(phi+1))),
    ("1/(φ+φ⁻¹)", 1/(phi + 1/phi)),
    ("1/√(φ³)", 1/sqrt(phi3)),
    ("φ/π", phi/pi),
    ("√(φ/π²)", sqrt(phi/pi**2)),
    ("(√5-1)/π", (sqrt5-1)/pi),
    ("√(1/φ³)", phi**(-1.5)),
    ("√5/(2φ²)", sqrt5/(2*phi2)),
]
for name, val in candidates_r:
    err = (r - val)/r * 100
    if abs(err) < 5:
        print(f"  m_H/v ≈ {name:25s} = {val:.6f}  (err: {err:+.3f}%)")

print()
print("═══════════════════════════════════════════════════")
print("  SUMMARY: WHAT THE RG SCAN REVEALS")
print("═══════════════════════════════════════════════════")
