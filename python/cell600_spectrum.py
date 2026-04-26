"""
Test 2: The 600-cell itself.

If the constants are eigenvalues, they're eigenvalues of 
an operator on the 600-cell graph, not the continuous S³.

The 600-cell has 120 vertices, each connected to 12 neighbours.
Its adjacency matrix A is 120×120 with known spectrum.

The eigenvalues of the adjacency matrix of the 600-cell are:
  12, 3+3φ, 3+3φ, ..., -3φ, ..., 3-3φ, ...
  
More precisely, they come from the representation theory of 
the binary icosahedral group 2I (order 120).

Let's construct it and compute the actual spectrum.
"""

import numpy as np
from itertools import product

phi = (1 + np.sqrt(5)) / 2
psi = (np.sqrt(5) - 1) / 2  # = 1/phi = phi - 1

# Construct 600-cell vertices
# 120 vertices on S³, using quaternion representation
# The vertices of the 600-cell with unit circumradius are:

vertices = []

# 8 vertices: all permutations of (±1, 0, 0, 0)
for i in range(4):
    for s in [1, -1]:
        v = [0, 0, 0, 0]
        v[i] = s
        vertices.append(tuple(v))

# 16 vertices: (±1/2, ±1/2, ±1/2, ±1/2)
for signs in product([0.5, -0.5], repeat=4):
    vertices.append(tuple(signs))

# 96 vertices: even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
# Need all even permutations of the four coordinates
half_phi = phi / 2
half = 0.5
half_psi = psi / 2  # = 1/(2φ)

# Generate all even permutations of (a, b, c, d)
def even_perms(vals):
    """Generate all even permutations of 4 values."""
    a, b, c, d = vals
    # The 12 even permutations of 4 elements
    perms = [
        (a, b, c, d), (a, c, d, b), (a, d, b, c),
        (b, a, d, c), (b, c, a, d), (b, d, c, a),
        (c, a, b, d), (c, b, d, a), (c, d, a, b),
        (d, a, c, b), (d, b, a, c), (d, c, b, a),
    ]
    return perms

base = [half_phi, half, half_psi, 0.0]
for perm in even_perms(base):
    for s0 in [1, -1]:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                v = (s0 * perm[0], s1 * perm[1], s2 * perm[2], perm[3])
                # Only include if the sign changes preserve the even perm structure
                # Actually, all sign combinations of nonzero coords
                # But we need to handle the zero specially
                pass

# More reliable method: use the known quaternion group elements
# The 120 elements of the binary icosahedral group 2I as unit quaternions

def make_600cell_vertices():
    verts = set()
    
    # Type 1: 8 vertices — permutations of (±1, 0, 0, 0)
    for i in range(4):
        for s in [1, -1]:
            v = [0.0] * 4
            v[i] = s
            verts.add(tuple(round(x, 10) for x in v))
    
    # Type 2: 16 vertices — (±½, ±½, ±½, ±½)
    for s0 in [-1, 1]:
        for s1 in [-1, 1]:
            for s2 in [-1, 1]:
                for s3 in [-1, 1]:
                    v = (s0*0.5, s1*0.5, s2*0.5, s3*0.5)
                    verts.add(tuple(round(x, 10) for x in v))
    
    # Type 3: 96 vertices — even permutations of (±φ/2, ±1/2, ±1/(2φ), 0)
    hp = phi / 2
    h = 0.5
    hq = 1 / (2 * phi)
    
    base_vals = [hp, h, hq, 0.0]
    
    for perm in even_perms(base_vals):
        # For each even permutation, apply all sign combinations
        # to the nonzero coordinates
        nonzero_indices = [i for i in range(4) if perm[i] != 0.0]
        zero_indices = [i for i in range(4) if perm[i] == 0.0]
        
        n_nonzero = len(nonzero_indices)
        for signs in product([1, -1], repeat=n_nonzero):
            v = list(perm)
            for idx, s in zip(nonzero_indices, signs):
                v[idx] *= s
            verts.add(tuple(round(x, 10) for x in v))
    
    return list(verts)

vertices = make_600cell_vertices()
print(f"Number of vertices: {len(vertices)}")

if len(vertices) != 120:
    print(f"WARNING: Expected 120, got {len(vertices)}. Adjusting...")
    # If we got duplicates or extras, let's verify norms
    verts_array = np.array(vertices)
    norms = np.sqrt(np.sum(verts_array**2, axis=1))
    print(f"Norms range: {norms.min():.6f} to {norms.max():.6f}")
    # Keep only unit norm vertices
    unit_mask = np.abs(norms - 1.0) < 0.01
    verts_array = verts_array[unit_mask]
    print(f"After unit filter: {len(verts_array)}")
    vertices = [tuple(v) for v in verts_array]

verts = np.array(vertices)
n = len(verts)
print(f"Working with {n} vertices")

# Compute all pairwise dot products
dots = verts @ verts.T

# In the 600-cell, two vertices are connected by an edge 
# iff their dot product = φ/2 (angular distance = π/5)
# Edge length = 1/φ for unit circumradius

edge_threshold = phi / 2
adj = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i+1, n):
        if abs(dots[i, j] - edge_threshold) < 0.001:
            adj[i, j] = 1
            adj[j, i] = 1

degrees = adj.sum(axis=1)
print(f"Degree distribution: min={degrees.min()}, max={degrees.max()}, mean={degrees.mean():.1f}")
print(f"Expected: each vertex has 12 neighbours")

# Compute eigenvalues of adjacency matrix
eigenvalues = np.linalg.eigvalsh(adj.astype(float))
eigenvalues = np.sort(eigenvalues)[::-1]  # descending

# Get unique eigenvalues (with multiplicities)
unique_eigs, counts = np.unique(np.round(eigenvalues, 6), return_counts=True)
unique_eigs = unique_eigs[::-1]
counts = counts[::-1]

print(f"\n{'='*72}")
print("ADJACENCY MATRIX SPECTRUM OF THE 600-CELL")
print(f"{'='*72}")
print(f"{'Eigenvalue':>12} {'Multiplicity':>12} {'φ-expression':>20} {'As φ power':>12}")
print(f"{'-'*72}")

for eig, mult in zip(unique_eigs, counts):
    # Try to identify in terms of φ
    phi_expr = ""
    log_phi_val = ""
    
    # Check known values
    checks = {
        '12': 12,
        '3+3φ': 3 + 3*phi,
        '3φ': 3*phi,
        '2+2φ': 2 + 2*phi,
        '1+φ': 1 + phi,
        'φ': phi,
        '2': 2.0,
        '1': 1.0,
        '0': 0.0,
        '-1': -1.0,
        '-φ': -phi,
        '-(1+φ)': -(1+phi),
        '-2': -2.0,
        '3-3φ': 3 - 3*phi,
        '-3': -3.0,
        '-3φ': -3*phi,
        '-(3+3φ)': -(3+3*phi),
        '2φ-2': 2*phi-2,
        '2-2φ': 2-2*phi,
        'φ-2': phi-2,
        '2φ': 2*phi,
        '-2φ': -2*phi,
        '5': 5.0,
        '-5': -5.0,
        'φ²': phi**2,
        '-φ²': -phi**2,
        '√5': np.sqrt(5),
        '-√5': -np.sqrt(5),
        '2√5': 2*np.sqrt(5),
        '3': 3.0,
        '1+2φ': 1+2*phi,
        '2+φ': 2+phi,
    }
    
    for name, val in checks.items():
        if abs(eig - val) < 0.01:
            phi_expr = name
            break
    
    if eig > 0.001:
        lp = np.log(eig) / np.log(phi)
        log_phi_val = f"{lp:.4f}"
    elif eig < -0.001:
        log_phi_val = f"neg"
    else:
        log_phi_val = "0"
    
    print(f"{eig:12.6f} {mult:12d} {phi_expr:>20} {log_phi_val:>12}")

print(f"\nTotal eigenvalue count: {sum(counts)} (should be {n})")
print(f"Trace (sum of eigenvalues): {eigenvalues.sum():.6f} (should be 0)")

# Now: the NORMALISED Laplacian = I - D^{-1}A
# where D = degree matrix (all 12s for regular graph)
print(f"\n{'='*72}")
print("NORMALISED LAPLACIAN SPECTRUM")
print(f"{'='*72}")

lap_eigs = 1.0 - eigenvalues / 12.0
for eig, mult in zip(unique_eigs, counts):
    lap = 1.0 - eig / 12.0
    print(f"  Adj eig = {eig:8.4f}  →  Lap eig = {lap:8.6f}  (mult {mult})")

# Key test: ratios of Laplacian eigenvalues
print(f"\n{'='*72}")
print("KEY RATIOS AND MATCHES")
print(f"{'='*72}")

# Collect positive unique laplacian eigenvalues
lap_unique = sorted(set(np.round(1.0 - eigenvalues/12.0, 8)))
lap_unique = [x for x in lap_unique if x > 0.001]

print("\nPositive Laplacian eigenvalues:")
targets = {
    'φ⁻¹': 1/phi,
    'φ⁻²': 1/phi**2,
    'φ⁻³': 1/phi**3,
    'φ⁻⁴': 1/phi**4,
    'φ⁻⁵': 1/phi**5,
    'φ⁻⁶': 1/phi**6,
    '1/3': 1/3,
    '2/3': 2/3,
    '1/√5': 1/np.sqrt(5),
    '2/√5': 2/np.sqrt(5),
    '1/5': 0.2,
    '2/5': 0.4,
    '1/12': 1/12,
    '1/45': 1/45,
    '2φ/25': 2*phi/25,
    'sin²θ_W=φ⁻³': phi**(-3),
}

for lv in lap_unique:
    match = ""
    for name, val in targets.items():
        if abs(lv - val) / max(val, 0.001) < 0.03:
            match = f" ← MATCH: {name} ({abs(lv-val)/val*100:.2f}%)"
    print(f"  {lv:.8f}{match}")

# Adjacency eigenvalue ratios
print(f"\n{'='*72}")
print("ADJACENCY EIGENVALUE RATIOS")  
print(f"{'='*72}")

pos_eigs = sorted([e for e in unique_eigs if e > 0.1], reverse=True)
for i in range(len(pos_eigs)):
    for j in range(i+1, len(pos_eigs)):
        ratio = pos_eigs[i] / pos_eigs[j]
        match = ""
        for name, val in targets.items():
            if abs(ratio - val) / val < 0.03:
                match = f" ← {name}"
        if abs(ratio - phi) / phi < 0.03:
            match = " ← φ!"
        if abs(ratio - phi**2) / phi**2 < 0.03:
            match = " ← φ²!"
        if match or ratio < 5:
            print(f"  {pos_eigs[i]:.4f} / {pos_eigs[j]:.4f} = {ratio:.6f}{match}")

