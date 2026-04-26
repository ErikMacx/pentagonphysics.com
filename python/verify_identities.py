"""
Verify the algebraic identities and dig deeper into the magic number pattern.
"""
import numpy as np
from sympy import sqrt, Rational, simplify, symbols, cos, pi

phi_exact = (1 + sqrt(5)) / 2
sigma_exact = 1 / phi_exact

print("=" * 70)
print("IDENTITY CHECK: σ²√5 = √5/φ² = 1 - 1/φ⁴")
print("=" * 70)

expr1 = sigma_exact**2 * sqrt(5)
expr2 = sqrt(5) / phi_exact**2  
expr3 = 1 - 1/phi_exact**4

print(f"σ²√5     = {simplify(expr1)}")
print(f"√5/φ²    = {simplify(expr2)}")
print(f"1 - 1/φ⁴ = {simplify(expr3)}")
print(f"Are σ²√5 and 1-1/φ⁴ equal? {simplify(expr1 - expr3) == 0}")
print()

# Expand manually
# σ² = 1/φ² = (3-√5)/2  
# σ²√5 = √5(3-√5)/2 = (3√5-5)/2
# 1 - 1/φ⁴ = 1 - (7-3√5)/2 = (2-7+3√5)/2 = (-5+3√5)/2 = (3√5-5)/2
print("Manual: σ²√5 = (3√5-5)/2")
print("Manual: 1-1/φ⁴ = (3√5-5)/2")
print("IDENTICAL. Same expression, two routes.")

print()
print("=" * 70)
print("MAGIC NUMBERS: DEEP STRUCTURE")
print("=" * 70)

print("\nFirst four magic numbers from 2I dimensions:")
print("  2  = 1 × 2 = dim(1) × dim(2)")
print("  8  = 2 × 4 = dim(2) × dim(4)")
print("  20 = 4 × 5 = dim(4) × dim(5)")
print("  28 = dim(so(8)) = n(n-1)/2 for n=8")
print()
print("Pattern for first three: consecutive dim products")
print("  dim(1)×dim(2), dim(2)×dim(4), dim(4)×dim(5)")
print("  Each uses the NEXT dimension in the table")
print()

# Check: 28 as cumulative
print("Cumulative check:")
print(f"  2 = 2")
print(f"  2 + 6 = 8")
print(f"  8 + 12 = 20")
print(f"  20 + 8 = 28  (spin-orbit breaks HO degeneracy)")
print(f"  28 + 22 = 50")
print(f"  50 + 32 = 82")
print(f"  82 + 44 = 126")
print()
print("Shell degeneracies: 2, 6, 12, 8, 22, 32, 44")
print("These are 2(2l+1) for each subshell")

# 50 decomposition  
print(f"\n50 = 2 × 25 = 2 × 5²")
print(f"   = 2 × discriminant²")
print(f"   = dim(2) × Δ²")
print(f"   or: 50 = |2I|/2 - 10 = 60 - 10")

# 82 decomposition
print(f"\n82 = 2+8+20+28+24")
print(f"   = (first four magic) + |24-cell vertices|")
print(f"   But 2+8+20+28 = 58, not 82. Let me recheck...")
print(f"   2+8+20+28 = {2+8+20+28}")
print(f"   58+24 = {58+24}")
print(f"   CONFIRMED: 82 = Σ(first 4 magic) + 24")

# 126
print(f"\n126 = |2I| + 6 = 120 + dim(6)")
print(f"    = |symmetry group| + highest dim irrep")
print(f"    or: 126 = 82 + 44")
print(f"    44 = 120 - 82 + 6? No, 44 = 4×11")
print(f"    44 = 2 × 22 = 2 × (28-6)")

# Alternative: triangular numbers
print(f"\nTriangular number check:")
for n in range(1, 20):
    t = n*(n+1)//2
    if t in [2, 8, 20, 28, 50, 82, 126]:
        print(f"  T({n}) = {t} ✓ MAGIC")

# Tetrahedral?
print(f"\nTetrahedral number check:")
for n in range(1, 20):
    t = n*(n+1)*(n+2)//6
    if t in [2, 8, 20, 28, 50, 82, 126]:
        print(f"  Tet({n}) = {t} ✓ MAGIC")

print()
print("=" * 70)
print("DEUTERON: PHYSICAL INTERPRETATION")
print("=" * 70)
print()
print("μ_d = σ²√5 = √5/φ² = (3√5-5)/2")
print()
print("Physical reading:")
print("σ² = the impedance SQUARED = the power reflection coefficient")
print("√5 = the discriminant = the fundamental arithmetic invariant")
print()
print("The deuteron magnetic moment is the discriminant")
print("scaled by the power reflection at the Galois boundary.")
print()
print("Or equivalently: 1 - 1/φ⁴")
print("= 1 minus the fourth-order attenuation")
print("= what remains after four sections of the impedance ladder")
print()
print("The deuteron has 2 nucleons. Each nucleon is an 18-mode cavity.")
print("But the deuteron isn't 2×18 = 36 independent modes.")
print("It's a BOUND state. The binding reduces the effective mode count.")
print("The magnetic moment measures what's left after binding.")
print()
phi_f = (1+np.sqrt(5))/2
mu_d_pred = np.sqrt(5)/phi_f**2
mu_d_meas = 0.8574382308
print(f"Prediction:  σ²√5 = {mu_d_pred:.7f} μ_N")
print(f"Measurement: μ_d  = {mu_d_meas:.7f} μ_N")
print(f"Error: {abs(mu_d_pred-mu_d_meas)/mu_d_meas*100:.3f}%")
print(f"This is 0.39%. Not as tight as μ_p (0.04%) but")
print(f"still sub-percent with zero free parameters.")

print()
print("=" * 70)
print("ABLATION: DEUTERON")
print("=" * 70)
# How many simple phi/sqrt5 expressions give 0.39% or better?
target = 0.8574382308
count = 0
hits = []
for a in range(-6, 7):
    for b in range(-4, 5):
        for c in range(-4, 5):
            try:
                val = phi_f**a * np.sqrt(5)**b * 2**c
                if 0.1 < val < 10:
                    err = abs(val - target)/target
                    if err < 0.0039:
                        count += 1
                        hits.append((err, a, b, c, val))
            except:
                pass
hits.sort()
print(f"Expressions φ^a × √5^b × 2^c within 0.39% of μ_d:")
print(f"Total: {count} out of search space")
for err, a, b, c, val in hits[:5]:
    terms = []
    if a: terms.append(f"φ^{a}")
    if b: terms.append(f"√5^{b}")
    if c: terms.append(f"2^{c}")
    print(f"  {' × '.join(terms)} = {val:.7f}  err = {err*100:.4f}%")

print()
print("=" * 70)
print("ABLATION: n-p MASS DIFFERENCE")
print("=" * 70)
target_np = 2.530978  # (m_n-m_p)/m_e
count = 0
hits = []
for a in range(-6, 7):
    for b in range(-4, 5):
        for c in range(-4, 5):
            try:
                val = phi_f**a * np.sqrt(5)**b * 2**c
                if 0.5 < val < 10:
                    err = abs(val - target_np)/target_np
                    if err < 0.0052:  # 0.52%
                        count += 1
                        hits.append((err, a, b, c, val))
            except:
                pass
hits.sort()
print(f"Expressions φ^a × √5^b × 2^c within 0.52% of (m_n-m_p)/m_e:")
print(f"Total: {count}")
for err, a, b, c, val in hits[:5]:
    terms = []
    if a: terms.append(f"φ^{a}")
    if b: terms.append(f"√5^{b}")
    if c: terms.append(f"2^{c}")
    print(f"  {' × '.join(terms)} = {val:.7f}  err = {err*100:.4f}%")

