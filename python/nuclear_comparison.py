#!/usr/bin/env python3
"""
Nuclear Physics vs 600-Cell Eigenvalue Framework
Systematic Comparison and Ablation Testing

Eric McLean, Independent Researcher, Cyprus
ORCID: 0009-0009-6175-4408
"""

import numpy as np
from itertools import product as iterproduct
import json

phi = (1 + np.sqrt(5)) / 2
sqrt5 = np.sqrt(5)

# ============================================================
# 600-CELL SPECTRUM (exact)
# ============================================================
eigenvalues_exact = {
    '12': (12, 1),
    '3+3√5': (3 + 3*sqrt5, 4),
    '2+2√5': (2 + 2*sqrt5, 9),
    '3': (3, 16),
    '0': (0, 25),
    '-2': (-2, 36),
    '2-2√5': (2 - 2*sqrt5, 9),
    '-3': (-3, 16),
    '3-3√5': (3 - 3*sqrt5, 4),
}

evals_sorted = sorted([(v, m) for v, m in eigenvalues_exact.values()], reverse=True)
print("=" * 80)
print("600-CELL ADJACENCY SPECTRUM")
print("=" * 80)
for val, mult in evals_sorted:
    print(f"  λ = {val:10.4f}  mult = {mult:3d}  ({int(np.sqrt(mult))}²)")

# Eigenvalue gaps (from largest down)
evals_only = [v for v, m in evals_sorted]
gaps = []
for i in range(len(evals_only) - 1):
    gap = evals_only[i] - evals_only[i+1]
    gaps.append(gap)
    
print("\nEigenvalue gaps (descending):")
for i, g in enumerate(gaps):
    print(f"  Gap {i}: {evals_only[i]:.4f} → {evals_only[i+1]:.4f} = {g:.4f}")

# ============================================================
# ABLATION ENGINE
# ============================================================
def generate_phi_expressions(a_range=(-4, 5), b_range=(-4, 5), n_range=(1, 13), m_range=(1, 13)):
    """Generate all expressions phi^a * sqrt(5)^b * n / m"""
    expressions = []
    for a in range(a_range[0], a_range[1]):
        for b in range(b_range[0], b_range[1]):
            for n in range(n_range[0], n_range[1]):
                for m in range(m_range[0], m_range[1]):
                    val = (phi**a) * (sqrt5**b) * n / m
                    if 0.01 < abs(val) < 100 and np.isfinite(val):
                        expressions.append((val, f"φ^{a}·√5^{b}·{n}/{m}"))
    # Remove duplicates close to each other
    expressions.sort(key=lambda x: x[0])
    return expressions

def ablation_test(target, tolerance_pct, expressions=None):
    """
    For a given target value, count how many expressions in the search space
    fall within tolerance_pct of the target. Return rank of best match.
    """
    if expressions is None:
        expressions = generate_phi_expressions()
    
    tol = abs(target) * tolerance_pct / 100.0
    matches = []
    for val, expr in expressions:
        if abs(val - target) <= tol:
            err = abs(val - target) / abs(target) * 100
            matches.append((err, val, expr))
    
    matches.sort()
    total_search = len(expressions)
    return matches, total_search

# Pre-generate expression library
print("\n\nGenerating ablation search space...")
all_expressions = generate_phi_expressions()
print(f"Search space size: {len(all_expressions)} expressions")

# Also generate a simpler search space for ratios near 1
simple_expressions = []
for a in range(-6, 7):
    for b in range(-3, 4):
        val = phi**a * sqrt5**b
        if 0.01 < abs(val) < 100:
            simple_expressions.append((val, f"φ^{a}·√5^{b}"))
        for n in range(2, 13):
            val2 = phi**a * sqrt5**b / n
            if 0.01 < abs(val2) < 100:
                simple_expressions.append((val2, f"φ^{a}·√5^{b}/{n}"))
            val3 = phi**a * sqrt5**b * n
            if 0.01 < abs(val3) < 100:
                simple_expressions.append((val3, f"φ^{a}·√5^{b}·{n}"))

print(f"Simple search space: {len(simple_expressions)} expressions")

# ============================================================
# TASK 2a: BINDING ENERGY RATIOS TO IRON PEAK
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2a: BINDING ENERGY PER NUCLEON RATIOS TO Fe-56")
print("=" * 80)

# AME2020 / NUBASE2020 values for B/A in MeV
# Source: Wang et al., Chinese Physics C 45 (2021) 030003
binding_energies = {
    # (Z, A, symbol): B/A in MeV
    'H-2': 1.112283,
    'H-3': 2.827266,
    'He-3': 2.572681,
    'He-4': 7.073915,
    'Li-6': 5.332331,
    'Li-7': 5.606291,
    'Be-9': 6.462668,
    'B-10': 6.475083,
    'B-11': 6.927732,
    'C-12': 7.680144,
    'C-13': 7.469849,
    'N-14': 7.475614,
    'N-15': 7.699459,
    'O-16': 7.976206,
    'O-18': 7.767097,
    'F-19': 7.779015,
    'Ne-20': 8.032240,
    'Na-23': 8.111493,
    'Mg-24': 8.260709,
    'Al-27': 8.331553,
    'Si-28': 8.447744,
    'P-31': 8.481167,
    'S-32': 8.493129,
    'Cl-35': 8.520278,
    'Ar-36': 8.519909,
    'Ar-40': 8.595259,
    'K-39': 8.557025,
    'Ca-40': 8.551301,
    'Ca-48': 8.666507,
    'Ti-48': 8.722903,
    'V-51': 8.742042,
    'Cr-52': 8.775953,
    'Mn-55': 8.764818,
    'Fe-56': 8.790323,
    'Co-59': 8.768028,
    'Ni-58': 8.732032,
    'Ni-62': 8.794553,  # Highest B/A
    'Cu-63': 8.752113,
    'Zn-64': 8.735636,
    'Zn-68': 8.682559,
    'Ge-72': 8.731736,
    'Se-80': 8.710591,
    'Kr-84': 8.717014,
    'Sr-88': 8.732560,
    'Zr-90': 8.709920,
    'Mo-98': 8.635048,
    'Sn-120': 8.504876,
    'Xe-132': 8.413762,
    'Ba-138': 8.393753,
    'Ce-140': 8.376283,
    'Nd-142': 8.346200,
    'Sm-152': 8.244055,
    'Gd-158': 8.183780,
    'Dy-164': 8.139850,
    'Er-168': 8.105560,
    'Yb-174': 8.060930,
    'Hf-180': 8.024720,
    'W-184': 7.998250,
    'Os-192': 7.944550,
    'Pt-198': 7.907140,
    'Au-197': 7.915660,
    'Pb-208': 7.867895,
    'Bi-209': 7.847989,
    'Th-232': 7.615040,
    'U-235': 7.590907,
    'U-238': 7.570119,
}

BA_Fe56 = binding_energies['Fe-56']

print(f"\nB/A(Fe-56) = {BA_Fe56:.6f} MeV (AME2020)")
print(f"B/A(Ni-62) = {binding_energies['Ni-62']:.6f} MeV (true maximum)")

print(f"\n{'Nucleus':<10} {'B/A':>10} {'Ratio':>10} {'Best φ-expr':>25} {'Error%':>10} {'Rank':>6} {'Search':>8}")
print("-" * 90)

results_2a = []
for nucleus, ba in sorted(binding_energies.items(), key=lambda x: -x[1]):
    ratio = ba / BA_Fe56
    matches, total = ablation_test(ratio, 2.0, all_expressions)
    if matches:
        best_err, best_val, best_expr = matches[0]
        rank = 1
        # Count how many are within same tolerance as best match
        best_tol = best_err
        within_same = sum(1 for e, v, x in matches if e <= max(best_tol * 2, 0.5))
        results_2a.append((nucleus, ba, ratio, best_expr, best_err, within_same, total))
        if best_err < 1.0:  # Only show sub-1% matches
            print(f"{nucleus:<10} {ba:10.6f} {ratio:10.6f} {best_expr:>25} {best_err:10.4f} {within_same:6d} {total:8d}")

# Specific checks from the prompt
print("\n\nSPECIFIC CHECKS FROM PROMPT:")
specific_checks = [
    ('He-4', phi/2, 'φ/2'),
    ('C-12', phi**2/3, 'φ²/3'),
    ('N-14', 1 - 1/phi**4, '1-1/φ⁴'),
    ('Li-6', 1/phi, '1/φ'),
]

for nucleus, predicted, label in specific_checks:
    actual = binding_energies[nucleus] / BA_Fe56
    err = abs(actual - predicted) / actual * 100
    # Full ablation
    matches, total = ablation_test(actual, err * 1.5, all_expressions)
    rank_count = len(matches)
    print(f"\n  {nucleus}: actual ratio = {actual:.6f}")
    print(f"    {label} = {predicted:.6f}, error = {err:.4f}%")
    print(f"    Ablation: {rank_count} expressions within {err*1.5:.2f}% tolerance (search space {total})")
    if matches:
        print(f"    Top 5 matches:")
        for e, v, x in matches[:5]:
            print(f"      {x}: {v:.6f} (error {e:.4f}%)")

# ============================================================
# TASK 2b: Pb-208 EXCITATION SPECTRUM vs 600-CELL GAPS
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2b: Pb-208 EXCITATION SPECTRUM vs 600-CELL GAPS")
print("=" * 80)

# Pb-208 excitation energies (MeV) from NNDC
# Source: Evaluated Nuclear Structure Data File (ENSDF)
pb208_states = [
    (2.615, '3⁻'),
    (3.198, '5⁻'),
    (3.475, '2⁺'),
    (3.709, '4⁺'),
    (3.920, '4⁻'),
    (3.961, '6⁺'),
    (4.037, '2⁺'),
    (4.086, '7⁻'),
    (4.180, '5⁻'),
    (4.323, '4⁺'),
]

E1 = pb208_states[0][0]  # First excited state

# 600-cell gaps (from largest eigenvalue down)
cell_gaps = [
    12 - (3 + 3*sqrt5),           # gap0 = 2.292
    (3 + 3*sqrt5) - (2 + 2*sqrt5), # gap1 = 1 + √5 = 3.236
    (2 + 2*sqrt5) - 3,             # gap2 = 2√5-1 = 3.472
    3 - 0,                          # gap3 = 3
    0 - (-2),                       # gap4 = 2
    (-2) - (2 - 2*sqrt5),          # gap5 = 2√5-4 = 0.472
    (2 - 2*sqrt5) - (-3),          # gap6 = 5 - 2√5 = 0.528
    (-3) - (3 - 3*sqrt5),          # gap7 = 3√5-6 = 0.708
]

print("\n600-cell eigenvalue gaps:")
for i, g in enumerate(cell_gaps):
    print(f"  Gap {i}: {g:.4f}")

# Gap ratios
gap_ratios = []
for i in range(len(cell_gaps)):
    for j in range(len(cell_gaps)):
        if i != j and cell_gaps[j] != 0:
            gap_ratios.append((cell_gaps[i]/cell_gaps[j], f"gap{i}/gap{j}"))

print(f"\n{'Ratio E/E1':>12} {'State':>6} {'Best gap ratio':>20} {'Gap ratio val':>14} {'Error%':>10}")
print("-" * 75)

for energy, spin in pb208_states[1:]:
    ratio = energy / E1
    # Test against gap ratios
    best_match = None
    best_err = 999
    for gr, glabel in gap_ratios:
        if gr > 0:
            err = abs(ratio - gr) / ratio * 100
            if err < best_err:
                best_err = err
                best_match = (gr, glabel)
    
    # Also test against simple φ-expressions
    phi_matches, _ = ablation_test(ratio, 2.0, simple_expressions)
    
    print(f"{ratio:12.4f} {spin:>6} {best_match[1]:>20} {best_match[0]:14.4f} {best_err:10.4f}%")
    if phi_matches and phi_matches[0][0] < best_err:
        print(f"{'':12} {'':>6} {'φ-expr: ' + phi_matches[0][2]:>20} {phi_matches[0][1]:14.4f} {phi_matches[0][0]:10.4f}%")

# Full ablation on specific matches from prompt
print("\n\nABLATION ON SPECIFIC Pb-208 MATCHES:")
specific_pb = [
    ('E(4⁺)/E(3⁻)', 3.709/2.615, 'gap₁/gap₀ approx'),
    ('E(4⁻)/E(3⁻)', 3.920/2.615, '3/2'),
    ('E(5⁻@4.18)/E(3⁻)', 4.180/2.615, 'φ'),
]

for label, target, claim in specific_pb:
    print(f"\n  {label} = {target:.4f} (claimed ≈ {claim})")
    matches, total = ablation_test(target, 2.0, all_expressions)
    print(f"  Ablation: {len(matches)} expressions within 2% (search space {total})")
    if matches:
        for e, v, x in matches[:5]:
            print(f"    {x}: {v:.6f} (error {e:.4f}%)")

# ============================================================
# TASK 2b EXTENDED: Other doubly-magic nuclei
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2b EXTENDED: OTHER DOUBLY-MAGIC NUCLEI")
print("=" * 80)

# O-16 excitation spectrum (MeV) from NNDC/ENSDF
o16_states = [
    (6.049, '0⁺'),
    (6.130, '3⁻'),
    (6.917, '2⁺'),
    (7.117, '1⁻'),
    (8.872, '2⁻'),
    (9.585, '1⁻'),
    (9.845, '2⁺'),
    (10.356, '4⁺'),
]

# Ca-40 excitation spectrum (MeV)
ca40_states = [
    (3.353, '0⁺'),
    (3.737, '3⁻'),
    (3.904, '2⁺'),
    (4.491, '5⁻'),
    (5.213, '2⁺'),
    (5.249, '4⁺'),
    (5.614, '4⁻'),
    (5.903, '0⁺'),
]

# Ca-48 excitation spectrum (MeV)
ca48_states = [
    (3.832, '2⁺'),
    (4.283, '3⁻'),
    (4.507, '4⁺'),
    (5.146, '2⁺'),
    (5.370, '5⁻'),
]

# Sn-132 (limited data)
sn132_states = [
    (4.041, '2⁺'),
    (4.352, '4⁺'),
    (4.416, '7⁻'),
    (4.715, '3⁻'),
    (4.831, '6⁺'),
]

for name, states in [('O-16', o16_states), ('Ca-40', ca40_states), 
                      ('Ca-48', ca48_states), ('Sn-132', sn132_states)]:
    if len(states) < 2:
        continue
    E1_local = states[0][0]
    print(f"\n{name} excitation ratios (to first excited state at {E1_local:.3f} MeV):")
    print(f"  {'Ratio':>10} {'State':>6} {'Best φ-expr':>25} {'Error%':>10} {'Rank/Total':>15}")
    for energy, spin in states[1:]:
        ratio = energy / E1_local
        matches, total = ablation_test(ratio, 2.0, simple_expressions)
        if matches:
            print(f"  {ratio:10.4f} {spin:>6} {matches[0][2]:>25} {matches[0][0]:10.4f} {len(matches):>6}/{total}")

# ============================================================
# TASK 2c: BETHE-WEIZSACKER PARAMETER RATIOS
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2c: BETHE-WEIZSACKER PARAMETER RATIOS")
print("=" * 80)

# BW parameters - multiple sources for comparison
# Source 1: Rohlf (1994) - widely used textbook values
bw_rohlf = {
    'a_V': 15.75,
    'a_S': 17.80,
    'a_C': 0.711,
    'a_A': 23.70,
    'a_P': 11.18,
}

# Source 2: Krane (1987) 
bw_krane = {
    'a_V': 15.56,
    'a_S': 17.23,
    'a_C': 0.697,
    'a_A': 23.29,
    'a_P': 12.00,
}

# Source 3: Myers-Swiatecki (1966) droplet model
bw_myers = {
    'a_V': 15.68,
    'a_S': 18.56,
    'a_C': 0.717,
    'a_A': 28.10,
    'a_P': 11.00,
}

for src_name, bw in [('Rohlf 1994', bw_rohlf), ('Krane 1987', bw_krane), ('Myers-Swiatecki', bw_myers)]:
    print(f"\n{src_name}:")
    params = list(bw.keys())
    print(f"  {'Ratio':<15} {'Value':>10} {'Best φ-expr':>25} {'Error%':>10} {'Matches@2%':>12}")
    for i in range(len(params)):
        for j in range(len(params)):
            if i != j:
                ratio = bw[params[i]] / bw[params[j]]
                label = f"{params[i]}/{params[j]}"
                matches, total = ablation_test(ratio, 2.0, all_expressions)
                if matches and matches[0][0] < 1.0:
                    print(f"  {label:<15} {ratio:10.4f} {matches[0][2]:>25} {matches[0][0]:10.4f} {len(matches):>12}")

# Special check: a_A/a_V vs 3/2
print("\n\nSPECIFIC CHECK: a_A/a_V vs 3/2 = dim(3)/dim(2)")
for src_name, bw in [('Rohlf 1994', bw_rohlf), ('Krane 1987', bw_krane), ('Myers-Swiatecki', bw_myers)]:
    ratio = bw['a_A'] / bw['a_V']
    err = abs(ratio - 1.5) / ratio * 100
    print(f"  {src_name}: a_A/a_V = {ratio:.4f}, error from 3/2 = {err:.2f}%")

# Check eigenvalue ratio connection
print("\n\nEigenvalue ratio check: (3+3√5)/(2+2√5) = 3/2 exactly")
print(f"  (3+3√5)/(2+2√5) = {(3+3*sqrt5)/(2+2*sqrt5):.10f}")
print(f"  This is exact: 3(1+√5) / 2(1+√5) = 3/2")

# ============================================================
# TASK 2d: MAGIC NUMBERS FROM THE OPERATOR
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2d: MAGIC NUMBERS FROM CHARACTER TABLE DECOMPOSITION")
print("=" * 80)

# 2I character table dimensions
dims_2I = [1, 2, 2, 3, 3, 4, 4, 5, 6]  # dimensions of irreps
group_invariants = {
    '|2I|': 120,
    '|I|': 60,
    '24-cell': 24,
    'Δ=5': 5,
    'dim total': sum(dims_2I),  # 30
}

magic_numbers = [2, 8, 20, 28, 50, 82, 126]

# Proposed decompositions
decompositions = {
    2: "dim(1) × dim(2) = 1 × 2",
    8: "dim(2) × dim(4) = 2 × 4",
    20: "dim(4) × dim(5) = 4 × 5",
    28: "dim(so(8)) = dim(D₄ Lie algebra)",
    50: "dim(2) × Δ² = 2 × 25",
    82: "Σ(2,8,20,28) + 24 = 58 + 24",
    126: "|2I| + dim(6) = 120 + 6",
}

print("\nMagic number decompositions:")
for mn in magic_numbers:
    print(f"  {mn:>4} = {decompositions[mn]}")

# ABLATION: How many integers in [1, 200] can be decomposed?
print("\n\nABLATION: Reachable integers from 2I building blocks")

# Building blocks: products, sums, and simple combinations of dims and invariants
all_blocks = dims_2I + list(group_invariants.values())
# Also add squares of dims
all_blocks_sq = [d**2 for d in dims_2I]

reachable = set()

# Method 1: Products of two dims
for d1 in dims_2I:
    for d2 in dims_2I:
        reachable.add(d1 * d2)

# Method 2: Sums of two dims
for d1 in dims_2I:
    for d2 in dims_2I:
        reachable.add(d1 + d2)

# Method 3: Products of three dims
for d1 in dims_2I:
    for d2 in dims_2I:
        for d3 in dims_2I:
            reachable.add(d1 * d2 * d3)

# Method 4: dim * dim_squared
for d1 in dims_2I:
    for d2 in dims_2I:
        reachable.add(d1 * d2**2)

# Method 5: Sums of products
for d1 in dims_2I:
    for d2 in dims_2I:
        for d3 in dims_2I:
            reachable.add(d1 * d2 + d3)

# Method 6: Group invariants ± dims/products
for inv in group_invariants.values():
    for d in dims_2I:
        reachable.add(inv + d)
        reachable.add(inv - d)
        reachable.add(inv * d)
    for d1 in dims_2I:
        for d2 in dims_2I:
            reachable.add(inv + d1 * d2)
            reachable.add(inv - d1 * d2)

# Method 7: Sums of first k magic numbers + invariant
partial_sums = []
s = 0
for m in magic_numbers:
    s += m
    partial_sums.append(s)
    for inv_val in list(group_invariants.values()) + dims_2I:
        reachable.add(s + inv_val)
        reachable.add(s - inv_val)

reachable_in_range = sorted([x for x in reachable if 1 <= x <= 200])
magic_set = set(magic_numbers)
magic_hit = magic_set.intersection(reachable)

print(f"  Reachable integers in [1, 200]: {len(reachable_in_range)} / 200 = {len(reachable_in_range)/200*100:.1f}%")
print(f"  Magic numbers hit: {sorted(magic_hit)} ({len(magic_hit)}/{len(magic_numbers)})")
magic_miss = magic_set - reachable
if magic_miss:
    print(f"  Magic numbers missed: {sorted(magic_miss)}")

# Check if ALL magic numbers are reachable
print(f"\n  All 7 magic numbers reachable: {magic_set.issubset(reachable)}")

# How many random sets of 7 from [1,200] would be fully reachable?
import random
random.seed(42)
n_trials = 100000
full_hit_count = 0
for _ in range(n_trials):
    rand_set = set(random.sample(range(1, 201), 7))
    if rand_set.issubset(set(reachable_in_range)):
        full_hit_count += 1

print(f"  Random baseline: {full_hit_count}/{n_trials} random 7-element sets fully reachable = {full_hit_count/n_trials*100:.1f}%")
print(f"  This means the decomposition is {'constraining' if full_hit_count/n_trials < 0.5 else 'NOT constraining'}")

# More restrictive: only products of exactly two dims (tighter constraint)
strict_reachable = set()
for d1 in dims_2I:
    for d2 in dims_2I:
        strict_reachable.add(d1 * d2)

strict_in_range = sorted([x for x in strict_reachable if 1 <= x <= 200])
print(f"\n  STRICT (products of 2 dims only):")
print(f"  Reachable: {strict_in_range}")
print(f"  Count: {len(strict_in_range)} / 200 = {len(strict_in_range)/200*100:.1f}%")
print(f"  Magic numbers hit: {sorted(magic_set.intersection(strict_reachable))}")

# ============================================================
# TASK 2e: EIGENVALUE RATIOS TO 12
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2e: EIGENVALUE RATIOS TO 12 (PENTAGONAL STRUCTURE)")
print("=" * 80)

print(f"\n  λ/(12) ratios:")
for val, mult in evals_sorted:
    if val != 0:
        ratio = val / 12
        # Check against cos(kπ/5)
        pentagonal = []
        for k in range(1, 5):
            c = np.cos(k * np.pi / 5)
            if abs(ratio - c) / max(abs(ratio), 0.001) * 100 < 2:
                pentagonal.append((k, c))
        pent_str = ""
        if pentagonal:
            pent_str = f" = cos({pentagonal[0][0]}π/5)"
        print(f"  {val:8.4f}/12 = {ratio:8.5f}{pent_str}  (mult {mult})")

print(f"\n  Exact pentagonal ratios:")
print(f"  (3+3√5)/12 = 3(1+√5)/12 = (1+√5)/4 = φ/2 = cos(π/5) = {phi/2:.6f}")
print(f"  (3-3√5)/12 = 3(1-√5)/12 = (1-√5)/4 = -1/(2φ) = cos(4π/5) = {-1/(2*phi):.6f}")
print(f"  Actual cos(π/5) = {np.cos(np.pi/5):.6f}")
print(f"  Actual cos(2π/5) = {np.cos(2*np.pi/5):.6f}")

# Check: (2+2√5)/12 
val_check = (2 + 2*sqrt5)/12
print(f"\n  (2+2√5)/12 = {val_check:.6f} = 2(1+√5)/12 = (1+√5)/6 = φ/3 = {phi/3:.6f}")
# Is φ/3 a pentagonal quantity?
print(f"  φ/3 = 2cos(π/5)/3 — NOT a standard pentagonal ratio")

# ============================================================
# TASK 2f: MULTIPLICITY STRUCTURE
# ============================================================
print("\n\n" + "=" * 80)
print("TASK 2f: MULTIPLICITY STRUCTURE — V⊗V AND SHELL MODEL")
print("=" * 80)

# Shell model degeneracies
# Harmonic oscillator shells: N=0,1,2,3,4,5
# Degeneracy = (N+1)(N+2)/2
ho_shells = [(N, (N+1)*(N+2)//2) for N in range(7)]
print("\nHarmonic oscillator shell degeneracies:")
for N, deg in ho_shells:
    print(f"  N={N}: degeneracy = {deg} (cumulative: {sum(d for _, d in ho_shells[:N+1])})")

# With spin: multiply by 2
print("\nWith spin (×2):")
for N, deg in ho_shells:
    print(f"  N={N}: 2 × {deg} = {2*deg} (cumulative: {sum(2*d for _, d in ho_shells[:N+1])})")

# Compare with 600-cell multiplicities
print("\n600-cell multiplicities: 1, 4, 9, 16, 25, 36, 9, 16, 4")
print("These are k² for k = 1,2,3,4,5,6,3,4,2")
print("Total: 120 = |2I|")

# Shell model magic numbers from harmonic oscillator
ho_magic = [2, 8, 20, 40, 70, 112]
print(f"\nHarmonic oscillator magic numbers: {ho_magic}")
print(f"Observed magic numbers: {magic_numbers}")
print(f"Agreement up to: 20 (then diverge — spin-orbit needed)")

# Connection: cumulative multiplicities
cum_mult = []
s = 0
for val, mult in evals_sorted:
    s += mult
    cum_mult.append(s)
print(f"\n600-cell cumulative multiplicities: {cum_mult}")
print(f"Note: 1, 5, 14, 30, 55, 91, 100, 116, 120")
# Check against magic numbers
print(f"Overlap with magic numbers: {set(cum_mult).intersection(set(magic_numbers))}")

# Triangular numbers check
print(f"\nTriangular number check:")
for i, c in enumerate(cum_mult):
    # Is c a triangular number?
    n = (-1 + np.sqrt(1 + 8*c)) / 2
    if abs(n - round(n)) < 0.001:
        print(f"  Cumulative {c} = T({int(round(n))}) (triangular number)")
    # Is c a binomial coefficient?
    for k in range(2, 10):
        for m in range(k, 20):
            from math import comb
            if comb(m, k) == c:
                print(f"  Cumulative {c} = C({m},{k})")

print("\n\n" + "=" * 80)
print("COMPUTATION COMPLETE")
print("=" * 80)
