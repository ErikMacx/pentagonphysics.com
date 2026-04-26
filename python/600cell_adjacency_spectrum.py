"""
Adjacency spectrum of the 600-cell graph.

Constructs the 120 vertices of the 600-cell as unit quaternions
(elements of the binary icosahedral group 2I), computes the
120x120 adjacency matrix, and reports the eigenvalues with
multiplicities.

Requires: numpy
Runtime:  ~10 seconds

Eric McLean · eric@tcel.com · ORCID 0009-0009-6175-4408
March 2026
"""

import numpy as np
from itertools import product as iprod

phi = (1 + np.sqrt(5)) / 2


def even_permutations(vals):
    """Return the 12 even permutations of a 4-tuple."""
    a, b, c, d = vals
    return [
        (a, b, c, d), (a, c, d, b), (a, d, b, c),
        (b, a, d, c), (b, c, a, d), (b, d, c, a),
        (c, a, b, d), (c, b, d, a), (c, d, a, b),
        (d, a, c, b), (d, b, a, c), (d, c, b, a),
    ]


def make_600cell_vertices():
    """
    Construct the 120 vertices of the 600-cell as unit quaternions.

    Three families:
      8 vertices  — permutations of (±1, 0, 0, 0)
      16 vertices — (±½, ±½, ±½, ±½)
      96 vertices — even permutations of (±φ/2, ±½, ±1/(2φ), 0)
                    with all sign combinations on nonzero entries
    """
    verts = set()

    # Family 1: 8 vertices
    for i in range(4):
        for s in [1.0, -1.0]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = s
            verts.add(tuple(round(x, 10) for x in v))

    # Family 2: 16 vertices
    for signs in iprod([0.5, -0.5], repeat=4):
        verts.add(tuple(round(x, 10) for x in signs))

    # Family 3: 96 vertices
    base = [phi / 2, 0.5, 1 / (2 * phi), 0.0]
    for perm in even_permutations(base):
        nonzero = [i for i in range(4) if abs(perm[i]) > 1e-10]
        for signs in iprod([1, -1], repeat=len(nonzero)):
            v = list(perm)
            for idx, s in zip(nonzero, signs):
                v[idx] *= s
            verts.add(tuple(round(x, 10) for x in v))

    return np.array(list(verts))


# ── Construct vertices ──────────────────────────────────────────

vertices = make_600cell_vertices()
n = len(vertices)
assert n == 120, f"Expected 120 vertices, got {n}"
norms = np.sqrt(np.sum(vertices**2, axis=1))
assert np.allclose(norms, 1.0), "Not all vertices are unit quaternions"

# ── Build adjacency matrix ──────────────────────────────────────
# Two vertices of the unit-circumradius 600-cell are adjacent
# iff their dot product equals φ/2  (angular distance π/5).

dots = vertices @ vertices.T
adj = (np.abs(dots - phi / 2) < 1e-6).astype(int)
np.fill_diagonal(adj, 0)

degrees = adj.sum(axis=1)
assert np.all(degrees == 12), "Expected regular graph of degree 12"

# ── Eigenvalues ─────────────────────────────────────────────────

eigenvalues = np.linalg.eigvalsh(adj.astype(float))
eigenvalues = np.sort(eigenvalues)[::-1]

unique_eigs = np.unique(np.round(eigenvalues, 5))[::-1]

print("=" * 64)
print("ADJACENCY SPECTRUM OF THE 600-CELL")
print("=" * 64)
print(f"\nVertices: {n}   Degree: 12   Edges: {int(adj.sum()) // 2}")
print(f"\n{'Eigenvalue':>11}  {'Exact':>8}  {'Mult':>5}  {'d':>3}  {'d²':>4}")
print("-" * 42)

# Identify exact forms
exact_forms = {
    12:            '12',
    6 * phi:       '6φ',
    4 * phi:       '4φ',
    3:             '3',
    0:             '0',
    -2:            '−2',
    -4 / phi:      '−4/φ',
    -3:            '−3',
    -6 / phi:      '−6/φ',
}

for eig in unique_eigs:
    mult = int(np.sum(np.abs(eigenvalues - eig) < 0.01))
    d = int(round(np.sqrt(mult)))

    name = ''
    for val, label in exact_forms.items():
        if abs(eig - val) < 0.01:
            name = label
            break

    print(f"  {eig:+10.5f}   {name:>6}  {mult:5d}  {d:3d}  {d}²")

print(f"\nSum of multiplicities: {sum(int(np.sum(np.abs(eigenvalues - e) < 0.01)) for e in unique_eigs)}")
print(f"Trace  Tr(A)  = {eigenvalues.sum():.6f}  (should be 0)")

# ── Key invariants ──────────────────────────────────────────────

print(f"\n{'=' * 64}")
print("SPECTRAL INVARIANTS")
print("=" * 64)

# Eigenvalue ratio
r = (6 * phi) / (4 * phi)
print(f"\n  6φ / 4φ  =  {r:.1f}")
print(f"  Reciprocal =  {1/r:.10f}   (Koide Q = 2/3)")

# Spectral gap
gap = 1 - phi / 2
print(f"\n  Spectral gap  =  1 − φ/2  =  {gap:.10f}")
print(f"  2 × gap       =  φ⁻²     =  {2*gap:.10f}")

# Trace of A³
eig_vals = list(exact_forms.keys())
eig_mults = [1, 4, 9, 16, 25, 36, 9, 16, 4]
tr3 = sum(v**3 * m for v, m in zip(eig_vals, eig_mults))
print(f"\n  Tr(A³) / 1440 =  {tr3 / 1440:.1f}")

# Irrep dimensions and Coxeter number
irrep_dims = [1, 2, 2, 3, 3, 4, 4, 5, 6]
print(f"\n  2I irrep dimensions:  {irrep_dims}")
print(f"  Sum  = {sum(irrep_dims)}   (Coxeter number of E8)")
print(f"  Σd²  = {sum(d**2 for d in irrep_dims)}   (order of 2I)")

# φ ↔ φ⁻¹ pairing
print(f"\n  Conjugate pairs (ratio φ² = {phi**2:.6f}):")
print(f"    6φ  ↔  −6/φ   :  6φ × 6/φ = 36  =  6²")
print(f"    4φ  ↔  −4/φ   :  4φ × 4/φ = 16  =  4²")
print(f"    3   ↔  −3     :  3 × 3    =  9  =  3²")

# 248 decomposition
print(f"\n  E8:  248 = 2 × Σd²  +  2² + 2²")
print(f"           = 2 × {sum(d**2 for d in irrep_dims)}  +  8")
print(f"           = {2 * sum(d**2 for d in irrep_dims) + 8}")
