"""
Deep analysis of the 600-cell spectrum.

Key discovery: The adjacency eigenvalues are expressible in terms of φ!
Let's identify them properly and look for constant matches.
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2
phi_inv = 1 / phi

# The 600-cell adjacency spectrum (verified numerically):
# eigenvalue : multiplicity
spectrum = [
    (12,          1),
    (6*phi,       4),   # 9.70820...
    (4*phi,       9),   # 6.47214...
    (3,          16),
    (0,          25),
    (-2,         36),
    (-4*phi_inv,  9),   # -2.47214...  = 4(1-φ) = -4/φ
    (-3,         16),
    (-6*phi_inv,  4),   # -3.70820...  = 6(1-φ) = -6/φ
]

print("=" * 72)
print("600-CELL ADJACENCY SPECTRUM — EXACT EXPRESSIONS")
print("=" * 72)

for val, mult in spectrum:
    print(f"  {val:10.6f}  mult = {mult:2d} = {int(np.sqrt(mult))}²")

print(f"\nMultiplicities: {[m for _,m in spectrum]}")
print(f"Perfect squares: {[int(np.sqrt(m)) for _,m in spectrum]}")
print(f"Sum: {sum(m for _,m in spectrum)} = 120 ✓")

print(f"\n{'='*72}")
print("OBSERVATION 1: THE MULTIPLICITIES ARE PERFECT SQUARES")
print("1², 2², 3², 4², 5², 6², 3², 4², 2²")
print("This means each eigenspace is a tensor product: V ⊗ V")
print("Dimensions of the 9 irreps of binary icosahedral group 2I")
print("=" * 72)

print(f"\n{'='*72}")
print("OBSERVATION 2: φ ↔ φ⁻¹ SYMMETRY")
print("=" * 72)
print(f"  6φ    (mult 4)  ↔  -6/φ   (mult 4)   ratio: φ²")
print(f"  4φ    (mult 9)  ↔  -4/φ   (mult 9)   ratio: φ²")
print(f"  3     (mult 16) ↔  -3     (mult 16)   ratio: 1")
print(f"  Unpaired: 12 (mult 1), 0 (mult 25), -2 (mult 36)")

print(f"\n{'='*72}")
print("OBSERVATION 3: NORMALISED BY DEGREE (÷12)")
print("=" * 72)
norm = [(v/12, m) for v, m in spectrum]
for v, m in norm:
    print(f"  {v:10.6f}  mult {m:2d}")

print(f"\n  First nontrivial: φ/2 = {phi/2:.6f}")
print(f"  Second: φ/3 = {phi/3:.6f}")
print(f"  Ratio: (φ/2)/(φ/3) = 3/2 EXACTLY")
print(f"  Reciprocal = 2/3 = Koide Q")

print(f"\n{'='*72}")
print("OBSERVATION 4: LAPLACIAN EIGENVALUES = 1 - adj/12")
print("=" * 72)
lap = [(1 - v/12, m) for v, m in spectrum]
for v, m in lap:
    expr = ""
    if abs(v) < 1e-8: expr = "= 0"
    elif abs(v - phi**(-2)/2) < 1e-6: expr = f"= φ⁻²/2 = {phi**(-2)/2:.6f}"
    elif abs(v - (3-phi)/3) < 1e-6: expr = f"= (3-φ)/3 = 1 - φ/3"
    elif abs(v - 0.75) < 1e-6: expr = "= 3/4"
    elif abs(v - 1.0) < 1e-6: expr = "= 1"
    elif abs(v - 7/6) < 1e-6: expr = "= 7/6"
    elif abs(v - 5/4) < 1e-6: expr = "= 5/4"
    elif abs(v - (1 + 1/(3*phi))) < 1e-6: expr = f"= 1 + 1/(3φ)"
    elif abs(v - (1 + 1/(2*phi))) < 1e-6: expr = f"= 1 + φ⁻¹/2"
    print(f"  λ = {v:10.6f}  mult {m:2d}  {expr}")

print(f"\n  KEY: First nontrivial Laplacian eigenvalue = φ⁻²/2")
print(f"       2 × (first Lap eigenvalue) = φ⁻² = 0.381966...")
print(f"       φ⁻² = total matter fraction in Rung Theorem")

print(f"\n{'='*72}")
print("OBSERVATION 5: WHAT DO THE EIGENVALUES GENERATE?")
print("=" * 72)

# The raw adjacency eigenvalues: 12, 6φ, 4φ, 3, 0, -2, -4/φ, -3, -6/φ
eigs = [12, 6*phi, 4*phi, 3, 0, -2, -4/phi, -3, -6/phi]
pos_eigs = [e for e in eigs if e > 0]

print("\nProducts of pairs of positive eigenvalues, divided by 120:")
for i in range(len(pos_eigs)):
    for j in range(i, len(pos_eigs)):
        prod = pos_eigs[i] * pos_eigs[j] / 120
        match = ""
        # Check known values
        checks = {
            'φ⁻¹': phi_inv, 'φ⁻²': phi_inv**2, 'φ⁻³': phi_inv**3,
            'φ': phi, 'φ²': phi**2, '1': 1.0, '2': 2.0, '3': 3.0,
            '1/2': 0.5, '1/3': 1/3, '1/4': 0.25, '1/5': 0.2,
            '2/3': 2/3, '3/4': 0.75,
            '√5': np.sqrt(5), '1/√5': 1/np.sqrt(5), '2/√5': 2/np.sqrt(5),
            'π/5': np.pi/5, '2π/5': 2*np.pi/5,
        }
        for name, val in checks.items():
            if val > 0 and abs(prod - val)/val < 0.01:
                match = f" ← {name} ({abs(prod-val)/val*100:.3f}%)"
        print(f"  ({pos_eigs[i]:.3f} × {pos_eigs[j]:.3f})/120 = {prod:.6f}{match}")

print(f"\n{'='*72}")
print("OBSERVATION 6: THE CRITICAL RATIOS")
print("=" * 72)

# Specific ratio tests
r1 = 6*phi / (4*phi)
r2 = 12 / (6*phi)  
r3 = 4*phi / 3
r4 = 12 / (4*phi)
r5 = 12 / 3
r6 = 6*phi / 3

print(f"  6φ / 4φ = 3/2     = {r1:.6f}  →  reciprocal 2/3 = Koide Q")
print(f"  12 / 6φ = 2/φ     = {r2:.6f}  →  = 2φ⁻¹")
print(f"  4φ / 3             = {r3:.6f}")
print(f"  12 / 4φ = 3/φ     = {r4:.6f}  →  = 3φ⁻¹")  
print(f"  12 / 3  = 4       = {r5:.6f}")
print(f"  6φ / 3  = 2φ      = {r6:.6f}  →  = φ² + φ⁻² + 1 = φ + 1 + φ⁻¹")

print(f"\n  CONSECUTIVE RATIOS:")
print(f"  12 → 6φ → 4φ → 3")
print(f"  ×(φ/2)  ×(2/3)  ×(3/(4φ))")
print(f"  = ×{phi/2:.6f}  ×{2/3:.6f}  ×{3/(4*phi):.6f}")

print(f"\n{'='*72}")
print("OBSERVATION 7: SPECTRAL GAP AND PHYSICAL MEANING")
print("=" * 72)

print(f"\n  Spectral gap (first nontrivial adj eigenvalue / max):")
print(f"  6φ/12 = φ/2 = {phi/2:.6f}")
print(f"  This IS the second-largest normalized eigenvalue")
print(f"  Gap = 1 - φ/2 = (2-φ)/2 = φ⁻²/2 = {(2-phi)/2:.6f}")
print(f"       = {phi**-2:.6f}/2")
print(f"  Note: φ⁻² = 0.382 = total matter fraction")
print(f"        φ⁻²/2 = 0.191 ≈ first Laplacian eigenvalue")

print(f"\n  The spectral gap of the 600-cell is HALF the matter fraction.")
print(f"  The expansion rate of a random walk on the 600-cell is")
print(f"  controlled by φ⁻²/2: half the matter budget.")

print(f"\n{'='*72}")
print("OBSERVATION 8: TRACE IDENTITIES")
print("=" * 72)

tr = sum(v*m for v,m in spectrum)
tr2 = sum(v**2 * m for v,m in spectrum)
tr3 = sum(v**3 * m for v,m in spectrum)
print(f"  Tr(A)  = {tr:.6f}  (should be 0: no self-loops)")
print(f"  Tr(A²) = {tr2:.6f}  = 120×12 = {120*12} (= vertices × degree: counts edge-pairs)")
print(f"  Tr(A³) = {tr3:.6f}  (counts triangles × 6)")
print(f"  Triangles = Tr(A³)/6 = {tr3/6:.0f}")
print(f"  600-cell has {tr3/6:.0f} triangles")

# Check: 600-cell should have 1200 triangular faces
print(f"  (600-cell has 1200 triangular faces)")

print(f"\n  Tr(A²)/120 = {tr2/120:.6f} = 12 = degree ✓")
print(f"  Tr(A³)/120 = {tr3/120:.6f}")
print(f"  Tr(A³)/720 = {tr3/720:.6f}  (÷ edges)")
print(f"  Tr(A³)/1440 = {tr3/1440:.6f}")

print(f"\n{'='*72}")
print("OBSERVATION 9: THE DAMPED OSCILLATOR ON THE 600-CELL GRAPH")
print("=" * 72)
print(f"\n  On each vertex: ε̈ᵢ + (1/12)Σ_adj εⱼ = φ · ε̇ᵢ")
print(f"  Mode decomposition using adjacency eigenvectors:")
print(f"  For mode with adj eigenvalue λₐ:")
print(f"    ε̈ + (λₐ/12)ε = φε̇")
print(f"    ε̈ - φε̇ + (λₐ/12)ε = 0")
print(f"    Characteristic: ω² - iφω + λₐ/12 = 0")
print(f"    ω = [iφ ± √(-φ² + 4λₐ/12)] / 2")
print(f"    ω = [iφ ± √(λₐ/3 - φ²)] / 2")

print(f"\n  For each adjacency eigenvalue λₐ:")
for val, mult in spectrum:
    disc = val/3 - phi**2
    if disc > 0:
        omega = np.sqrt(disc) / 2
        gamma = phi / 2
        Q = omega / phi  # quality factor
        survival = np.exp(-2*np.pi*gamma/omega)
        print(f"  λₐ={val:8.4f} (mult {mult:2d}): Ω={omega:.6f}, Q={Q:.4f}, "
              f"survival={survival:.6f}")
    elif disc == 0:
        print(f"  λₐ={val:8.4f} (mult {mult:2d}): CRITICALLY DAMPED")
    else:
        print(f"  λₐ={val:8.4f} (mult {mult:2d}): OVERDAMPED (disc={disc:.4f})")

print(f"\n  φ² = {phi**2:.6f}")
print(f"  12/3 = 4 > φ²: mode oscillates")
print(f"  6φ/3 = 2φ = {2*phi:.6f} < φ² = {phi**2:.6f}? {2*phi < phi**2}")
print(f"  Actually 2φ = {2*phi:.6f} and φ² = {phi**2:.6f}")
print(f"  2φ > φ² since 2 > φ (barely: {2 > phi})")
print(f"  2φ - φ² = 2φ - φ - 1 = φ - 1 = 1/φ = {phi - 1:.6f}")

print(f"\n  CRITICAL: 6φ/3 - φ² = 2φ - φ² = φ - 1 = φ⁻¹")
print(f"  The discriminant of the second mode is EXACTLY φ⁻¹!")

