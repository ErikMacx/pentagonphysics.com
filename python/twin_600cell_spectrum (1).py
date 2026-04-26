"""
twin_600cell_spectrum.py

Reproduces the full eigenvalue spectrum of the twin 600-cell graph Laplacian
described in McLean (2026), "The Other Side of Gravity from the 600-Cell
Laplacian", Section 8 and Appendix A.

Construction:
    - Build the 120 vertices of a single 600-cell as the orbit of the binary
      icosahedral group on the unit 3-sphere in R^4. Three vertex types:
        Type A (8 vertices):  +- e_i for i = 1..4
        Type B (16 vertices): (+-1/2, +-1/2, +-1/2, +-1/2)
        Type C (96 vertices): even permutations of (+-phi/2, +-1/2, +-1/(2*phi), 0)
    - Two vertices are adjacent iff their Euclidean distance equals 1/phi.
      With this rule every vertex has degree 12 and the graph has 720 edges.
    - The 24 type-A and type-B vertices together form a regular 24-cell
      inscribed in the 600-cell. This is the D4 bridge.
    - The twin 600-cell graph is two copies of the single 600-cell sharing
      the 24-vertex D4 bridge: 120 + 120 - 24 = 216 vertices, 1440 edges.
    - The graph Laplacian is L = D - A, where A is the 216 x 216 adjacency
      matrix and D is the diagonal matrix of vertex degrees. L is positive
      semi-definite. Trace(L) = sum of degrees = 2880.

Output:
    The 23 distinct eigenvalues of the 216 x 216 Laplacian, with their
    multiplicities (which sum to 216). Integer eigenvalues are flagged.

Requires:
    NumPy (no other external dependencies).

Run time:
    Approximately one second on a standard laptop.

Author: Eric McLean (Pentagon Physics)
ORCID:  0009-0009-6175-4408
Email:  eric@tcel.com
Date:   April 2026
"""

import numpy as np
from itertools import permutations, product
import math

phi = (1 + math.sqrt(5)) / 2

# === Build the 120 vertices of one 600-cell ===
verts = []
vert_types = []

# Type A: 8 unit basis vectors +/- e_i
for i in range(4):
    for s in [1, -1]:
        v = [0.0] * 4
        v[i] = s
        verts.append(tuple(v))
        vert_types.append('A')

# Type B: 16 half-integer vertices (+/- 1/2, +/- 1/2, +/- 1/2, +/- 1/2)
for signs in product([1, -1], repeat=4):
    verts.append(tuple(s * 0.5 for s in signs))
    vert_types.append('B')

# Type C: 96 even permutations of (+/- phi/2, +/- 1/2, +/- 1/(2*phi), 0)
base = [phi / 2, 0.5, 1 / (2 * phi), 0]

def is_even_perm(p):
    inv = sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
    return inv % 2 == 0

seen = set()
for perm in permutations(range(4)):
    if not is_even_perm(perm):
        continue
    for signs in product([1, -1], repeat=4):
        v = [0.0] * 4
        for k, idx in enumerate(perm):
            v[idx] = signs[k] * base[k]
        v_key = tuple(round(x, 10) for x in v)
        if v_key not in seen:
            seen.add(v_key)
            verts.append(tuple(v))
            vert_types.append('C')

assert len(verts) == 120, f"Expected 120 vertices, got {len(verts)}"

# === Build single 600-cell adjacency at edge distance 1/phi ===
N = 120
verts_np = [np.array(v) for v in verts]
adj = np.zeros((N, N), dtype=int)
for i in range(N):
    for j in range(i + 1, N):
        d = np.linalg.norm(verts_np[i] - verts_np[j])
        if abs(d - 1 / phi) < 1e-9:
            adj[i, j] = 1
            adj[j, i] = 1

# === Identify the 24 D4 bridge vertices (the inscribed 24-cell: types A and B) ===
bridge_idx = [i for i, t in enumerate(vert_types) if t in ('A', 'B')]
non_bridge_idx = [i for i in range(N) if i not in bridge_idx]
assert len(bridge_idx) == 24
assert len(non_bridge_idx) == 96

# === Build the 216-vertex twin graph ===
# Index layout:
#   0..95:    proton non-bridge
#   96..119:  bridge (shared between cells)
#   120..215: neutron non-bridge
M = 216
adj_twin = np.zeros((M, M), dtype=int)

# Map proton vertices to twin indices
proton_map = {oi: k for k, oi in enumerate(non_bridge_idx)}
for k, oi in enumerate(bridge_idx):
    proton_map[oi] = 96 + k

# Map neutron vertices to twin indices (bridge shared with proton)
neutron_map = {oi: 120 + k for k, oi in enumerate(non_bridge_idx)}
for k, oi in enumerate(bridge_idx):
    neutron_map[oi] = 96 + k

# Add proton edges
for i in range(N):
    for j in range(N):
        if adj[i, j]:
            adj_twin[proton_map[i], proton_map[j]] = 1

# Add neutron edges (bridge-to-bridge edges already added above; identical)
for i in range(N):
    for j in range(N):
        if adj[i, j]:
            adj_twin[neutron_map[i], neutron_map[j]] = 1

# === Verify the structure ===
deg = adj_twin.sum(axis=1)
assert np.sum(deg == 12) == 192, f"Expected 192 deg-12 vertices, got {np.sum(deg == 12)}"
assert np.sum(deg == 24) == 24,  f"Expected 24 deg-24 vertices, got {np.sum(deg == 24)}"
assert deg.sum() == 2880,        f"Expected sum of degrees 2880, got {deg.sum()}"

# === Build Laplacian and diagonalise ===
L = np.diag(deg) - adj_twin
assert np.allclose(L, L.T)
assert L.trace() == 2880

eigvals = np.sort(np.linalg.eigvalsh(L))
assert len(eigvals) == 216
assert abs(eigvals.sum() - 2880) < 1e-6

# === Group by distinct eigenvalue (within tolerance) ===
TOL = 1e-6
groups = []
current = [eigvals[0]]
for ev in eigvals[1:]:
    if abs(ev - current[-1]) < TOL:
        current.append(ev)
    else:
        groups.append(current)
        current = [ev]
groups.append(current)

# === Print results ===
print(f"Twin 600-cell graph: {M} vertices, {deg.sum() // 2} edges")
print(f"Degree sequence:     192 vertices of degree 12, 24 vertices of degree 24")
print(f"Trace(L) = {L.trace()}  =  sum of eigenvalues = {eigvals.sum():.4f}")
print()
print(f"Spectrum: {len(groups)} distinct eigenvalues, "
      f"total multiplicity {sum(len(g) for g in groups)}")
print()
print(f"  No.  Eigenvalue           Multiplicity")
print(f"  " + "-" * 50)
for i, g in enumerate(groups, 1):
    val = sum(g) / len(g)
    integer_marker = "  (integer)" if abs(val - round(val)) < 1e-4 else ""
    print(f"  {i:>3}  {val:>14.10f}     {len(g):>3}{integer_marker}")

n_int = sum(len(g) for g in groups
            if abs(sum(g) / len(g) - round(sum(g) / len(g))) < 1e-4)
print()
print(f"Integer-eigenvalue modes: {n_int} ({100 * n_int / M:.1f}% of spectrum)")
