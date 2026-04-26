#!/usr/bin/env python3
"""
Complete enumeration stress-test for CKM paper.
Tests: density, complexity, robustness, irrational substitution.
"""
import numpy as np
from math import sin, pi, log2, sqrt
import random

PHI = (1 + sqrt(5)) / 2
TARGET_VUS = 0.2243  # PDG 2024 average
TARGET_DELTA = 68.5   # degrees, CKMfitter

# ═══════════════════════════════════════════════════════
# TEST 1: Base enumeration (k<n, n∈[1,12], m∈[0,5])
# ═══════════════════════════════════════════════════════
def enumerate_expressions(phi_val, k_max=12, n_max=12, m_max=5):
    results = []
    for n in range(1, n_max+1):
        for k in range(1, n):
            for m in range(0, m_max+1):
                val = sin(k * pi / n) / phi_val**m
                cost = log2(max(k,1)) + log2(n) + m
                results.append({
                    'k': k, 'n': n, 'm': m,
                    'value': val, 'cost': cost,
                    'error_pct': abs(val - TARGET_VUS) / TARGET_VUS * 100
                })
    return results

print("=" * 60)
print("TEST 1: BASE ENUMERATION (n≤12, m≤5)")
print("=" * 60)

base = enumerate_expressions(PHI)
print(f"Total expressions: {len(base)}")

# Unique values (some may coincide due to trig identities)
vals = np.array([r['value'] for r in base])
unique_vals = np.unique(np.round(vals, 10))
print(f"Unique values: {len(unique_vals)}")

# Sub-percent matches
sub1 = [r for r in base if r['error_pct'] < 1.0]
sub01 = [r for r in base if r['error_pct'] < 0.1]
print(f"Sub-1% matches: {len(sub1)}")
for r in sub1:
    print(f"  sin({r['k']}π/{r['n']})/φ^{r['m']} = {r['value']:.6f} ({r['error_pct']:.4f}%, cost={r['cost']:.2f})")
print(f"Sub-0.1% matches: {len(sub01)}")
for r in sub01:
    print(f"  sin({r['k']}π/{r['n']})/φ^{r['m']} = {r['value']:.6f} ({r['error_pct']:.4f}%, cost={r['cost']:.2f})")

# ═══════════════════════════════════════════════════════
# TEST 2: DENSITY NEAR TARGET
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("TEST 2: LOCAL DENSITY NEAR 0.2243")
print("=" * 60)

positive_vals = sorted([v for v in vals if 0 < v < 1])
for eps in [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002]:
    count = sum(1 for v in positive_vals if abs(v - TARGET_VUS) < eps)
    print(f"  Within ±{eps} of {TARGET_VUS}: {count} expressions")

# ECDF: what's the local density at 0.2243?
nearby = sorted([v for v in positive_vals if 0.15 < v < 0.30])
print(f"\n  Values in [0.15, 0.30]: {len(nearby)}")
print(f"  Values in [0.20, 0.25]: {sum(1 for v in nearby if 0.20 < v < 0.25)}")
print(f"  Values in [0.22, 0.23]: {sum(1 for v in nearby if 0.22 < v < 0.23)}")

# Minimum spacing near target
if nearby:
    spacings = np.diff(nearby)
    min_sp = np.min(spacings) if len(spacings) > 0 else float('inf')
    # Find spacing around our hit
    for i, v in enumerate(nearby):
        if abs(v - TARGET_VUS) < 0.001:
            left = nearby[i-1] if i > 0 else None
            right = nearby[i+1] if i < len(nearby)-1 else None
            print(f"\n  Nearest neighbors to best match ({v:.6f}):")
            if left: print(f"    Left:  {left:.6f} (gap: {v-left:.6f})")
            if right: print(f"    Right: {right:.6f} (gap: {right-v:.6f})")

# ═══════════════════════════════════════════════════════
# TEST 3: COMPLEXITY RANKING
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("TEST 3: COMPLEXITY RANKING")
print("=" * 60)

# Sort by cost, show best sub-1% by complexity
sub1_sorted = sorted(sub1, key=lambda r: r['cost'])
print("Sub-1% matches ranked by complexity (lower = simpler):")
for r in sub1_sorted:
    print(f"  Cost={r['cost']:.2f}: sin({r['k']}π/{r['n']})/φ^{r['m']} = {r['value']:.6f} ({r['error_pct']:.4f}%)")

# What's the simplest expression overall that's close?
all_sorted = sorted(base, key=lambda r: (r['cost'], r['error_pct']))
print(f"\nSimplest 10 expressions (any accuracy):")
for r in all_sorted[:10]:
    print(f"  Cost={r['cost']:.2f}: sin({r['k']}π/{r['n']})/φ^{r['m']} = {r['value']:.6f} ({r['error_pct']:.3f}%)")

# Among low-complexity (cost < 5), what's the best?
low_cost = [r for r in base if r['cost'] < 5]
low_cost_best = sorted(low_cost, key=lambda r: r['error_pct'])
print(f"\nBest matches with cost < 5 ({len(low_cost)} expressions):")
for r in low_cost_best[:5]:
    print(f"  Cost={r['cost']:.2f}: sin({r['k']}π/{r['n']})/φ^{r['m']} = {r['value']:.6f} ({r['error_pct']:.4f}%)")

# ═══════════════════════════════════════════════════════
# TEST 4: ROBUSTNESS TO EXPANDED GRAMMAR
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("TEST 4: GRAMMAR EXPANSION ROBUSTNESS")
print("=" * 60)

for n_max, m_max in [(12, 5), (15, 5), (20, 5), (12, 7), (15, 7), (20, 7), (20, 10)]:
    expanded = enumerate_expressions(PHI, k_max=n_max, n_max=n_max, m_max=m_max)
    n_total = len(expanded)
    n_sub1 = sum(1 for r in expanded if r['error_pct'] < 1.0)
    n_sub01 = sum(1 for r in expanded if r['error_pct'] < 0.1)
    best_err = min(r['error_pct'] for r in expanded)
    print(f"  n≤{n_max:2d}, m≤{m_max:2d}: {n_total:5d} total, {n_sub1:2d} sub-1%, {n_sub01:2d} sub-0.1%, best={best_err:.4f}%")

# ═══════════════════════════════════════════════════════
# TEST 5: RANDOM QUADRATIC IRRATIONAL SUBSTITUTION
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("TEST 5: QUADRATIC IRRATIONAL SUBSTITUTION (Monte Carlo)")
print("=" * 60)

random.seed(42)
np.random.seed(42)

# Generate quadratic irrationals: (a + sqrt(D)) / b for small a, b, D
def quadratic_irrationals(N=200):
    """Generate N distinct quadratic irrationals > 1."""
    irr = set()
    for D in range(2, 50):
        if int(sqrt(D))**2 == D: continue  # skip perfect squares
        for a in range(-5, 6):
            for b in range(1, 6):
                val = (a + sqrt(D)) / b
                if 1.0 < val < 5.0:
                    irr.add(round(val, 12))
    return sorted(irr)

irrationals = quadratic_irrationals()
print(f"Testing {len(irrationals)} quadratic irrationals (range (1, 5))")
print(f"φ = {PHI:.10f}")

sub01_counts = []
sub1_counts = []
best_errors = []

for phi_test in irrationals:
    results = enumerate_expressions(phi_test, k_max=12, n_max=12, m_max=5)
    n1 = sum(1 for r in results if r['error_pct'] < 1.0)
    n01 = sum(1 for r in results if r['error_pct'] < 0.1)
    best = min(r['error_pct'] for r in results)
    sub1_counts.append(n1)
    sub01_counts.append(n01)
    best_errors.append(best)

sub01_counts = np.array(sub01_counts)
sub1_counts = np.array(sub1_counts)
best_errors = np.array(best_errors)

print(f"\nResults across {len(irrationals)} quadratic irrationals:")
print(f"  Sub-1% hits:  mean={np.mean(sub1_counts):.2f}, median={np.median(sub1_counts):.0f}, max={np.max(sub1_counts)}")
print(f"  Sub-0.1% hits: mean={np.mean(sub01_counts):.2f}, median={np.median(sub01_counts):.0f}, max={np.max(sub01_counts)}")
print(f"  Best error %: mean={np.mean(best_errors):.4f}, median={np.median(best_errors):.4f}, min={np.min(best_errors):.4f}")
print(f"  φ achieved: sub-0.1% = {sum(1 for r in base if r['error_pct'] < 0.1)}, best = {min(r['error_pct'] for r in base):.4f}%")
print(f"  Irrationals matching or beating φ's best error: {sum(1 for e in best_errors if e <= min(r['error_pct'] for r in base))}")

# Distribution of sub-0.1% counts
print(f"\n  Distribution of sub-0.1% hits:")
for c in range(0, max(sub01_counts)+1):
    n = sum(1 for x in sub01_counts if x == c)
    if n > 0:
        print(f"    {c} hits: {n} irrationals ({100*n/len(irrationals):.1f}%)")

# Which irrationals do best?
top_idx = np.argsort(best_errors)[:5]
print(f"\n  Top 5 irrationals by best match:")
for i in top_idx:
    print(f"    {irrationals[i]:.10f} → best error = {best_errors[i]:.4f}%")

print(f"\n  φ = {PHI:.10f} → best error = {min(r['error_pct'] for r in base):.4f}%")

# ═══════════════════════════════════════════════════════
# TEST 6: JOINT PROBABILITY
# ═══════════════════════════════════════════════════════
print(f"\n{'='*60}")
print("TEST 6: JOINT PROBABILITY OF TWO φ-MATCHES")
print("=" * 60)

# For delta: scan pi/phi^a, phi^a * pi/b, etc.
# Simple: delta = pi/phi^2 = 68.754 deg
# CKMfitter: 68.5 ± 2.0
# Match within 0.25 degrees

# Count how many "simple" phi-angles are close to 68.5
delta_candidates = []
for a in range(-5, 6):
    for b in range(1, 13):
        val_rad = pi * PHI**a / b
        val_deg = val_rad * 180 / pi
        if 0 < val_deg < 180:
            delta_candidates.append({'expr': f'π·φ^{a}/{b}', 'deg': val_deg,
                                     'err': abs(val_deg - TARGET_DELTA)})
        # Also: b*pi/phi^a
        val_rad2 = b * pi / PHI**abs(a) if a < 0 else pi / (PHI**a * b)
        val_deg2 = val_rad2 * 180 / pi if val_rad2 > 0 else -1
        if 0 < val_deg2 < 180:
            delta_candidates.append({'expr': f'alt({a},{b})', 'deg': val_deg2,
                                     'err': abs(val_deg2 - TARGET_DELTA)})

# Also simple: k*pi/phi^m
for k in range(1, 6):
    for m in range(0, 6):
        val_deg = k * 180 / PHI**m
        if 0 < val_deg < 180:
            delta_candidates.append({'expr': f'{k}·π/φ^{m}', 'deg': val_deg,
                                     'err': abs(val_deg - TARGET_DELTA)})

# Deduplicate
seen = set()
unique_delta = []
for d in delta_candidates:
    key = round(d['deg'], 6)
    if key not in seen:
        seen.add(key)
        unique_delta.append(d)

unique_delta.sort(key=lambda x: x['err'])
print(f"Delta candidates (simple φ-expressions): {len(unique_delta)}")
print("Best 5:")
for d in unique_delta[:5]:
    print(f"  {d['expr']:20s} = {d['deg']:.3f}° (err = {d['err']:.3f}°)")

sub_half = sum(1 for d in unique_delta if d['err'] < 0.5)
sub_1 = sum(1 for d in unique_delta if d['err'] < 1.0)
print(f"Within 0.5° of 68.5°: {sub_half}")
print(f"Within 1.0° of 68.5°: {sub_1}")

# Joint
p1 = 1 / 151  # Cabibbo: 1 sub-0.1% out of 151
p2 = sub_half / len(unique_delta) if unique_delta else 0.01
print(f"\np_Cabibbo (sub-0.1%) ≈ {p1:.4f}")
print(f"p_delta (sub-0.5°) ≈ {p2:.4f}")
print(f"p_joint (independent) ≈ {p1 * p2:.6f}")
print(f"Equivalent: 1 in {1/(p1*p2):.0f}")

