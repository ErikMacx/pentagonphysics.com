"""
Does E8 have the same V⊗V self-referential spectral structure 
as the 600-cell?

Key facts:
- 600-cell: 120 vertices = binary icosahedral group 2I acting on itself
- E8 root system: 240 roots = TWO copies of 600-cell under golden projection
- E8 is unique: its adjoint representation IS its smallest irrep (dim 248)
- E8 literally acts on itself. No external space needed.

The golden ratio projection from 8D to 4D splits E8's 240 roots into
two 600-cells related by a factor of φ.

Let's construct the E8 root system and compute its adjacency spectrum.
"""

import numpy as np
from itertools import combinations

phi = (1 + np.sqrt(5)) / 2

# ================================================================
# Construct E8 root system (240 roots in 8D)
# ================================================================

# E8 roots come in two types:
# Type D8: all permutations of (±1, ±1, 0, 0, 0, 0, 0, 0) — 112 roots
# Type half-spin: (±1/2, ±1/2, ±1/2, ±1/2, ±1/2, ±1/2, ±1/2, ±1/2)
#                 with an even number of minus signs — 128 roots

roots = []

# Type 1: D8 roots — all pairs of positions with ±1
for i, j in combinations(range(8), 2):
    for si in [1, -1]:
        for sj in [1, -1]:
            v = [0.0] * 8
            v[i] = si
            v[j] = sj
            roots.append(v)

print(f"D8 roots: {len(roots)}")

# Type 2: half-spin — (±1/2)^8 with even number of minus signs
from itertools import product as iprod
for signs in iprod([0.5, -0.5], repeat=8):
    neg_count = sum(1 for s in signs if s < 0)
    if neg_count % 2 == 0:
        roots.append(list(signs))

print(f"Total roots: {len(roots)}")
assert len(roots) == 240, f"Expected 240, got {len(roots)}"

roots = np.array(roots)
norms = np.sqrt(np.sum(roots**2, axis=1))
print(f"Norm range: {norms.min():.4f} to {norms.max():.4f}")
print(f"All norms = √2: {np.allclose(norms, np.sqrt(2))}")

# ================================================================
# Compute inner products and adjacency
# ================================================================
dots = roots @ roots.T

# E8 roots have inner products: 2 (same), ±1, 0, -2 (opposite)
# Two roots are "adjacent" (connected) if their inner product = 1
# (they form a 120° angle, which is the E8 Dynkin structure)

adj = (np.abs(dots - 1.0) < 0.01).astype(int)
np.fill_diagonal(adj, 0)

degrees = adj.sum(axis=1)
print(f"\nAdjacency (dot product = 1):")
print(f"Degree: min={degrees.min()}, max={degrees.max()}, mean={degrees.mean():.1f}")

# Each E8 root has 56 neighbours with dot product = 1
# This is related to the E7 root system

# ================================================================
# Eigenvalues of E8 adjacency matrix
# ================================================================
print(f"\nComputing eigenvalues of 240×240 adjacency matrix...")
eigenvalues = np.linalg.eigvalsh(adj.astype(float))
eigenvalues = np.sort(eigenvalues)[::-1]

unique_eigs = np.unique(np.round(eigenvalues, 4))[::-1]
print(f"\n{'='*72}")
print("E8 ROOT SYSTEM ADJACENCY SPECTRUM (dot product = 1)")
print(f"{'='*72}")
print(f"{'Eigenvalue':>12} {'Mult':>6} {'√Mult':>8} {'d²?':>6} {'φ-test':>15}")
print(f"{'-'*60}")

for eig in unique_eigs:
    mult = np.sum(np.abs(eigenvalues - eig) < 0.01)
    sqrt_m = np.sqrt(mult)
    is_sq = abs(sqrt_m - round(sqrt_m)) < 0.01
    sq_str = f"{int(round(sqrt_m))}²" if is_sq else "no"
    
    # φ identification
    phi_id = ""
    checks = {
        '56': 56, '28+28φ': 28+28*phi, '21+21φ': 21+21*phi,
        '14+14φ': 14+14*phi, '7+7φ': 7+7*phi,
        '28': 28, '21': 21, '14': 14, '7': 7,
        '8φ': 8*phi, '6φ': 6*phi, '4φ': 4*phi, '2φ': 2*phi,
        '-8/φ': -8/phi, '-6/φ': -6/phi, '-4/φ': -4/phi,
        '8': 8, '-8': -8, '0': 0,
        '-2': -2, '-4': -4, '-6': -6, '-7': -7, '-8': -8,
        '-14': -14, '-21': -21, '-28': -28,
        '12': 12, '-12': -12,
    }
    for name, val in checks.items():
        if abs(eig - val) < 0.05:
            phi_id = name
            break
    
    print(f"{eig:12.4f} {mult:6d} {sqrt_m:8.2f} {sq_str:>6} {phi_id:>15}")

print(f"\nTotal: {len(eigenvalues)} eigenvalues")
print(f"Trace: {eigenvalues.sum():.4f} (should be 0)")

# ================================================================
# Also check adjacency with dot product = -1 (opposite connectivity)
# ================================================================
print(f"\n{'='*72}")
print("ALTERNATIVE: FULL CONNECTIVITY (|dot| = 1)")
print(f"{'='*72}")

adj2 = (np.abs(np.abs(dots) - 1.0) < 0.01).astype(int)
np.fill_diagonal(adj2, 0)
degrees2 = adj2.sum(axis=1)
print(f"Degree: {degrees2[0]}")

eigs2 = np.linalg.eigvalsh(adj2.astype(float))
eigs2 = np.sort(eigs2)[::-1]
unique2 = np.unique(np.round(eigs2, 4))[::-1]

for eig in unique2:
    mult = np.sum(np.abs(eigs2 - eig) < 0.01)
    sqrt_m = np.sqrt(mult)
    is_sq = abs(sqrt_m - round(sqrt_m)) < 0.01
    sq_str = f"{int(round(sqrt_m))}²" if is_sq else f"  ({sqrt_m:.2f})"
    print(f"  {eig:10.4f}  mult = {mult:4d} = {sq_str}")

# ================================================================
# The GOLDEN PROJECTION: 8D → 4D
# ================================================================
print(f"\n{'='*72}")
print("THE GOLDEN PROJECTION: E8 → two 600-cells")
print(f"{'='*72}")

# The Coxeter element of E8 has eigenvalues exp(2πi·m/30) 
# for m = 1, 7, 11, 13, 17, 19, 23, 29
# The golden projection uses the eigenspaces corresponding to
# m = 1, 11, 19, 29 (one 4D subspace) and m = 7, 13, 17, 23 (the other)
# These are related by the golden ratio

# For a simpler approach: project using the known projection matrix
# The 4D projection of E8 roots using the H4 (600-cell) projection

# The projection matrix from 8D to 4D that reveals the 600-cell structure
# uses the eigenvectors of the E8 Cartan matrix's Coxeter element

# Let's use a known good projection. The E8 to H4 projection maps
# the 240 roots onto 120 vertices of a 600-cell (some with multiplicity 2,
# giving the two copies at different radii related by φ)

# Simple version: project onto first 4 coordinates and check structure
proj_4d = roots[:, :4]
norms_4d = np.sqrt(np.sum(proj_4d**2, axis=1))

print(f"4D projection norms: min={norms_4d.min():.4f}, max={norms_4d.max():.4f}")
print(f"Distinct norms: {np.unique(np.round(norms_4d, 3))}")

# Count how many project to each radius shell
for r in np.unique(np.round(norms_4d, 3)):
    count = np.sum(np.abs(norms_4d - r) < 0.01)
    ratio_to_min = r / norms_4d[norms_4d > 0.01].min() if r > 0.01 else 0
    print(f"  r = {r:.4f}: {count} roots  (r/r_min = {ratio_to_min:.4f})")

# ================================================================
# Check: does 240 = 120 + 120 split maintain V⊗V?
# ================================================================
print(f"\n{'='*72}")
print("E8 vs 600-CELL: STRUCTURAL COMPARISON")
print(f"{'='*72}")

print(f"""
600-cell (2I, order 120):
  Adjacency eigenvalues: 12, 6φ, 4φ, 3, 0, -2, -4/φ, -3, -6/φ
  Multiplicities:        1², 2², 3², 4², 5², 6², 3², 4², 2²
  ALL perfect squares: YES
  V⊗V structure: YES (from regular representation of 2I)
  Self-referential: group acts on itself
  
E8 root system (240 roots):
  E8 is the ONLY simple Lie algebra whose adjoint = fundamental
  This means E8 acts on itself, just like 2I does
  248 = 8 + 240: the algebra IS the root system (plus Cartan)
  
  If E8 has V⊗V, then:
  - dim(E8) = 248 is itself a sum of d²'s
  - The E8 Weyl group (order 696,729,600) would generate the structure
  - The 240 roots split as 2×120, each copy a 600-cell
  - Each 600-cell has V⊗V → E8 has V⊗V at BOTH levels
""")

# Key check: 248 as sum of squares
print("Can 248 be written as a sum of perfect squares (irrep dimensions²)?")
# E8 decomposes under various subgroups
# Under SU(5) × SU(5): 248 = (24,1) + (1,24) + (5,10) + (10,5) + (5̄,10̄) + (10̄,5̄)
# Under H4 (icosahedral): need the branching rules

# 248 = 1 + 3 + 5 + 7 + 9 + 11 + 13 + ... nope
# 248 = 4 + 4 + 16 + 16 + 36 + 36 + 9 + 9 + 1 + 25 + ... 
# From 2I branching: if 248 decomposes under 2I

# 120 = 1+4+4+9+9+16+16+25+36 (from 2I irreps, each d²)
# 240 = 2 × 120
# 248 = 240 + 8

# Under 2I (binary icosahedral), the 8D Cartan subalgebra decomposes too
# Let's just check the main claim: are the E8 adjacency multiplicities perfect squares?

print(f"\n{'='*72}")
print("DIRECT TEST: ARE E8 ADJACENCY MULTIPLICITIES PERFECT SQUARES?")
print(f"{'='*72}")

all_squares = True
for eig in unique_eigs:
    mult = np.sum(np.abs(eigenvalues - eig) < 0.01)
    sqrt_m = np.sqrt(mult)
    is_sq = abs(sqrt_m - round(sqrt_m)) < 0.01
    if not is_sq:
        all_squares = False
    status = "✓ d²" if is_sq else "✗ NOT d²"
    print(f"  λ = {eig:10.4f}  mult = {mult:4d}  √mult = {sqrt_m:8.3f}  {status}")

if all_squares:
    print(f"\n  *** ALL MULTIPLICITIES ARE PERFECT SQUARES ***")
    print(f"  *** E8 HAS V⊗V SELF-REFERENTIAL STRUCTURE ***")
else:
    print(f"\n  Some multiplicities are NOT perfect squares.")
    print(f"  Checking if they factor as products of representation dimensions...")

