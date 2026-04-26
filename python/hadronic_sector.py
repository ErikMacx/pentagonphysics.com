"""
What does the character table need to specify for the hadronic sector?
Not quark masses. Hadron observables.
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
sigma = phi - 1

# ============================================================
# THE HADRONIC OBSERVABLES
# ============================================================
print("="*80)
print("THE HADRONIC OBSERVABLES: What we actually measure")
print("="*80)

# All in MeV
m_p = 938.272
m_n = 939.565
m_e = 0.51100
m_pi0 = 134.977
m_pipm = 139.570
m_K0 = 497.611
m_Kpm = 493.677
m_D0 = 1864.84
m_Dpm = 1869.66
m_B0 = 5279.66
m_Bpm = 5279.34
m_t = 172690  # top: quasi-observable

print(f"\n  LIGHT HADRONS:")
print(f"  m_p = {m_p} MeV (proton)")
print(f"  m_n = {m_n} MeV (neutron)")
print(f"  m_π⁰ = {m_pi0} MeV (neutral pion)")
print(f"  m_π± = {m_pipm} MeV (charged pion)")
print(f"  m_K⁰ = {m_K0} MeV (neutral kaon)")
print(f"  m_K± = {m_Kpm} MeV (charged kaon)")

print(f"\n  HEAVY FLAVOUR:")
print(f"  m_D⁰ = {m_D0} MeV (charm meson)")
print(f"  m_B⁰ = {m_B0} MeV (bottom meson)")
print(f"  m_t = {m_t} MeV (top quark — decays before confining)")

# ============================================================
# KEY RATIOS
# ============================================================
print(f"\n{'='*80}")
print("DIMENSIONLESS RATIOS: The table's natural variables")
print("="*80)

ratios = {
    'm_π⁰/m_p': m_pi0/m_p,
    'm_K/m_π': m_K0/m_pi0,
    'm_D/m_K': m_D0/m_K0,
    'm_B/m_D': m_B0/m_D0,
    'm_t/m_B': m_t/m_B0,
    '(m_n-m_p)/m_e': (m_n-m_p)/m_e,
    'm_π±/m_π⁰': m_pipm/m_pi0,
    'm_K/m_p': m_K0/m_p,
    'm_p/m_e': m_p/m_e,
}

print(f"\n  {'Ratio':<16} {'Value':>10}  Table candidates")
print("  " + "-"*70)

def find_table_match(val, tol=0.02):
    """Find character table expressions matching val"""
    matches = []
    
    # n/m dimension ratios
    for n in range(1, 50):
        for m in range(1, 50):
            if abs(n/m - val)/val < tol:
                matches.append(f"{n}/{m} = {n/m:.4f}")
    
    # φ powers × dimension
    for d in [1,2,3,4,5,6]:
        for p in range(-8, 9):
            if p == 0: continue
            v = d * phi**p
            if abs(v - val)/val < tol:
                matches.append(f"{d}·φ^{p} = {v:.4f}")
    
    # π powers × dimension / dimension
    for d1 in [1,2,3,4,5,6]:
        for d2 in [1,2,3,4,5,6]:
            for p in range(1, 7):
                v = d1 * np.pi**p / d2
                if abs(v - val)/val < tol:
                    matches.append(f"{d1}·π^{p}/{d2} = {v:.4f}")

    # √5 expressions
    s5 = np.sqrt(5)
    for d in [1,2,3,4,5,6]:
        for m in [1,2,3,4,5,6]:
            v = d * s5 / m
            if abs(v - val)/val < tol:
                matches.append(f"{d}√5/{m} = {v:.4f}")
    
    # (d1 + φ^a) / d2
    for d1 in range(-6, 7):
        for d2 in [1,2,3,4,5,6]:
            for a in range(-4, 5):
                if a == 0: continue
                v = (d1 + phi**a) / d2
                if v > 0 and abs(v - val)/val < tol:
                    matches.append(f"({d1}+φ^{a})/{d2} = {v:.4f}")

    return matches[:5]

for name, val in ratios.items():
    matches = find_table_match(val)
    mstr = matches[0] if matches else "—"
    print(f"  {name:<16} {val:>10.4f}  {mstr}")
    for m in matches[1:3]:
        print(f"  {'':16} {'':>10}  {m}")

# ============================================================
# THE PION: The most important hadron
# ============================================================
print(f"\n{'='*80}")
print("THE PION: Can we derive m_π/m_p from the table?")
print("="*80)

ratio_pi_p = m_pi0 / m_p
print(f"\n  m_π⁰/m_p = {ratio_pi_p:.6f}")

# The pion mass from chiral perturbation theory:
# m_π² ≈ (m_u + m_d) × B₀, where B₀ ≈ -<qq>/f_π²
# But we don't want quark masses! Can the table get here directly?

# Key observation: 1/7 is close
print(f"  1/7 = 1/(d4+d3) = {1/7:.6f}  error: {abs(1/7-ratio_pi_p)/ratio_pi_p*100:.2f}%")
print(f"  σ/φ³ = σ⁴ = {sigma**4:.6f}  error: {abs(sigma**4-ratio_pi_p)/ratio_pi_p*100:.2f}%")
print(f"  φ⁻⁴/σ = {phi**(-4)/sigma:.6f}")

# Let's be more systematic
print(f"\n  Systematic search (< 1% error):")
for expr, val_e, name_e in [
    (1/(4+3), 1/7, "1/(d4+d3)"),
    (sigma**4, sigma**4, "σ⁴"),
    (1/(2*phi**3), 1/(2*phi**3), "1/(d2·φ³)"),
    (sigma**3/phi, sigma**3/phi, "σ³/φ"),
    (3/(2*phi**5), 3/(2*phi**5), "d3/(d2·φ⁵)"),
    (1/(phi**4+phi**2), 1/(phi**4+phi**2), "1/(φ⁴+φ²)"),
    (sigma**2/(phi+1), sigma**2/(phi+1), "σ²/φ²"),
    (sigma**2/phi**2, sigma**2/phi**2, "σ²/φ² = σ⁴"),
    (2/(3*phi**3), 2/(3*phi**3), "d2/(d3·φ³)"),
    (phi**(-2) / phi, phi**(-3), "φ⁻³"),
    (1/(3+4), 1/7, "1/(d3+d4) = 1/7"),
    (sigma/(2+3), sigma/5, "σ/d5"),
    (sigma/phi**2, sigma/phi**2, "σ/φ² = σ³"),
]:
    err = abs(val_e - ratio_pi_p)/ratio_pi_p * 100
    if err < 2:
        print(f"    {name_e:<25} = {val_e:.6f}  error: {err:.3f}%")

# ============================================================
# THE FLAVOUR LADDER: K/π, D/K, B/D, t/B
# ============================================================
print(f"\n{'='*80}")
print("THE FLAVOUR LADDER: Ratios between successive thresholds")
print("="*80)

ladder = [
    ("m_K/m_π", m_K0/m_pi0, "strange/light"),
    ("m_D/m_K", m_D0/m_K0, "charm/strange"),
    ("m_B/m_D", m_B0/m_D0, "bottom/charm"),
    ("m_t/m_B", m_t/m_B0, "top/bottom"),
]

print(f"\n  {'Step':<12} {'Ratio':>8}  {'Log ratio':>10}  Table match")
print("  " + "-"*60)

for name, val, desc in ladder:
    log_val = np.log(val) / np.log(phi)  # log base φ
    matches = find_table_match(val, tol=0.03)
    mstr = matches[0] if matches else "—"
    print(f"  {name:<12} {val:>8.3f}  {log_val:>8.3f}·ln φ  {mstr}")

print(f"\n  Log-φ of each step:")
for name, val, desc in ladder:
    log_val = np.log(val) / np.log(phi)
    print(f"    {name}: log_φ = {log_val:.3f}")

print(f"\n  Sum of log-φ steps = log_φ(m_t/m_π) = {np.log(m_t/m_pi0)/np.log(phi):.3f}")

# ============================================================
# THE PROTON AND PION: What's already known
# ============================================================
print(f"\n{'='*80}")
print("WHAT THE TABLE ALREADY KNOWS ABOUT HADRONS")
print("="*80)

print(f"""
  DERIVED (published):
  ✓ m_p/m_e = 6π⁵ + π⁵/[φ⁷(π⁵−1)] = 1836.153  (0.005 ppm)
  ✓ (m_n-m_p)/m_e = 2.531                         (exact match)
  ✓ αs(MZ) = φ⁻³/2 = 0.1180                      (0.11%)
  ✓ θ_QCD = 0                                      (exact)
  ✓ CKM angles (draft)
  
  NOT YET DERIVED:
  ? m_π/m_p = 0.14386  ≈  1/7 = 1/(d4+d3)         (0.7%)
  ? m_K/m_π = 3.686    ≈  ?
  ? m_D/m_K = 3.749    ≈  ?
  ? m_B/m_D = 2.830    ≈  ?
  ? m_t      = 172.69 GeV  (quasi-observable)

  NOTE: m_π/m_p ≈ 1/7 = 1/(d4+d3) is 0.7% off.
  If this is real, the pion mass is determined by the sum of the 
  d=4 and d=3 dimensions — the boundary representations.
  The pion is the Goldstone boson of chiral symmetry breaking.
  Chiral symmetry maps to the d=3 representation (flavour triplet).
  The d=4 boundary enters through the Koide phase.
  The pion mass IS the boundary: 1/(d4+d3) = the inverse of the 
  representations that separate the local and non-local sectors.
""")

# Check: if m_π = m_p / 7 exactly, what does that predict?
m_pi_pred = m_p / 7
print(f"  If m_π = m_p/(d4+d3):")
print(f"    Predicted: {m_pi_pred:.3f} MeV")
print(f"    Measured:  {m_pi0:.3f} MeV")
print(f"    Error:     {abs(m_pi_pred-m_pi0)/m_pi0*100:.2f}%")

# The isospin splitting
print(f"\n  Isospin splitting m_π±/m_π⁰ = {m_pipm/m_pi0:.5f}")
print(f"  This is electromagnetic, proportional to α.")
print(f"  (m_π± - m_π⁰)/m_π⁰ = {(m_pipm-m_pi0)/m_pi0:.5f}")
print(f"  ≈ α/3? = {1/(3*137.036):.5f}")
print(f"  Actual/predicted = {(m_pipm-m_pi0)/m_pi0 / (1/(3*137.036)):.2f}")
print(f"  Not α/3. But the splitting is electromagnetic in origin.")

# ============================================================
# THE REAL OPEN FRONTIER
# ============================================================
print(f"\n{'='*80}")
print("THE REAL OPEN FRONTIER: Recount")
print("="*80)

print(f"""
  What the SM calls "6 quark masses" maps to these observables:

  1. m_π/m_p ≈ 1/(d4+d3) = 1/7                   ← DERIVABLE?
  2. m_K/m_π ≈ 3.686                               ← strangeness scale  
  3. m_D/m_K ≈ 3.749                               ← charm scale
  4. m_B/m_D ≈ 2.830                               ← bottom scale
  5. m_t ≈ 172.69 GeV                              ← top (quasi-observable)

  Of these, (1) may already be determined by the table (1/7 at 0.7%).
  And (2)-(4) form a LADDER. If the ladder has a pattern, 
  maybe one number determines the whole sequence.

  The ladder ratios: 3.686, 3.749, 2.830, 32.71
  Are these related? 
  
  K/π ≈ D/K ≈ 3.7. The first two steps are nearly equal!
  Only B/D drops and t/B jumps.
  
  3.7 ≈ φ³ - 1 = {phi**3 - 1:.3f}? No, φ³ = {phi**3:.3f}.
  3.7 ≈ 2φ + σ = {2*phi + sigma:.3f}? = {2*phi+sigma:.4f}.
  3.7 ≈ (d4+d3-d2·σ) = {4+3-2*sigma:.4f}? = {7-2*sigma:.4f}. Nah.
  3.7 ≈ d5·σ + d3·σ = {5*sigma + 3*sigma:.4f}? No.
  3.7 ≈ φ² + 1 = {phi**2+1:.4f}? = φ² + 1 = φ + 2 = 3.618. Off by 1.8%.
  
  m_K/m_π ≈ φ + 2 = φ² + 1?
  {m_K0/m_pi0:.4f} vs {phi+2:.4f} error: {abs(m_K0/m_pi0-(phi+2))/(m_K0/m_pi0)*100:.2f}%
  
  Hmm, 1.8%. In the false-positive danger zone.
  
  Let me check: m_K/m_π = {m_K0/m_pi0:.6f}
  
  Best rational: 29/8 = {29/8:.6f}, error {abs(29/8 - m_K0/m_pi0)/(m_K0/m_pi0)*100:.3f}%
  
  This is exploratory. Not a result. But the territory is mapped.
""")

