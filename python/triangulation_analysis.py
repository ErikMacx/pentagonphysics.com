import math
import random

phi = (1 + math.sqrt(5)) / 2
sqrt5 = math.sqrt(5)
alpha_inv = 137.035999206

# The actual targets
targets = {
    'alpha': -2.137,      # log10(α) ≈ log10(1/137) 
    'Lambda': -122.951,   # log10(ρ_Λ)
    'G': -38.2286,        # log10(α_G)
}

# The template: log10(g) = -α⁻¹ R - φ⁻² + Δ
# For each constant, we need to find R and Δ from Q(√5)

# How many bridge ratios of the form a*φ^n / (b*√5^m) with small a,b,n,m
# can approximate a given target?

# Generate all "simple" bridge ratios from Q(√5)
bridge_ratios = set()
for a in [1, 2, 3, 4]:
    for n in range(-4, 5):
        for b in [1, 2, 3, 4, 5]:
            for m in [0, 1, 2]:
                R = a * phi**n / (b * sqrt5**m)
                if 0.01 < R < 10:  # reasonable range
                    bridge_ratios.add(round(R, 10))

bridge_list = sorted(bridge_ratios)
print(f"Distinct bridge ratios in range [0.01, 10]: {len(bridge_list)}")

# For each bridge ratio, what exponent does the template produce?
# E = -α⁻¹ R - φ⁻² + Δ
# Without correction: E₀ = -α⁻¹ R - φ⁻²

exponents_no_correction = []
for R in bridge_list:
    E0 = -alpha_inv * R - phi**(-2)
    exponents_no_correction.append(E0)

print(f"\nLeading-order exponents range: [{min(exponents_no_correction):.1f}, {max(exponents_no_correction):.1f}]")
print(f"Number of distinct leading-order values: {len(exponents_no_correction)}")

# Now: what fraction of "random" target exponents in [-150, 0] can be 
# approximated to within 0.1% by SOME bridge ratio?
# This tests whether the template can fit anything

n_random = 100000
n_hits = 0
tolerance = 0.001  # 0.1% relative error on the exponent

for _ in range(n_random):
    target = random.uniform(-150, -1)
    # Find best bridge ratio
    best_err = float('inf')
    for E0 in exponents_no_correction:
        err = abs(E0 - target) / abs(target)
        if err < best_err:
            best_err = err
    if best_err < tolerance:
        n_hits += 1

print(f"\nFraction of random exponents matchable to 0.1% (no correction): {n_hits/n_random:.4f}")

# Now with corrections from the same family
corrections = set()
corrections.add(0.0)
for sign in [+1, -1]:
    for a in [1, 2, 3, 4]:
        for n in range(1, 11):
            for b in [1, 5, 25]:
                for m in [0, 1, 2, 3]:
                    val = sign * a / (b * phi**n * 5**m)
                    corrections.add(round(val, 12))

corr_list = sorted(corrections)
print(f"\nDistinct corrections: {len(corr_list)}")

# With corrections, how many targets can we match?
n_hits_corr = 0
for _ in range(n_random):
    target = random.uniform(-150, -1)
    best_err = float('inf')
    for R in bridge_list:
        E0 = -alpha_inv * R - phi**(-2)
        for delta in corr_list:
            E = E0 + delta
            err = abs(E - target) / abs(target)
            if err < best_err:
                best_err = err
            if best_err < tolerance:
                break
        if best_err < tolerance:
            break
    if best_err < tolerance:
        n_hits_corr += 1

print(f"Fraction of random exponents matchable to 0.1% (with corrections): {n_hits_corr/n_random:.4f}")

# THE KEY QUESTION: What's the probability that THREE specific targets
# are ALL matched to their observed precision?
# α: within 0.05σ ≈ 0.004% of measurement
# Λ: within 0.05% 
# G: within 0.021%

# For each, compute: how many bridge+correction combos land within the observed error?
print("\n=== TRIANGULATION ANALYSIS ===")

actual_cases = [
    ('α (inverse)', -2.137, 0.00004),   # 0.004% = 0.05σ precision
    ('Λ (log₁₀ρ)', -122.951, 0.0005),   # 0.05% relative
    ('G (log₁₀αG)', -38.2286, 0.00021),  # 0.021% = 208ppm
]

for name, target, tol in actual_cases:
    hits = 0
    total = 0
    for R in bridge_list:
        E0 = -alpha_inv * R - phi**(-2)
        for delta in corr_list:
            E = E0 + delta
            total += 1
            err = abs(E - target) / abs(target)
            if err < tol:
                hits += 1
    print(f"{name}: {hits} hits out of {total} combos (fraction {hits/total:.6f}) matching to {tol*100:.3f}%")

# Joint probability (assuming independence)
fractions = []
for name, target, tol in actual_cases:
    hits = 0
    total = 0
    for R in bridge_list:
        E0 = -alpha_inv * R - phi**(-2)
        for delta in corr_list:
            total += 1
            E = E0 + delta
            err = abs(E - target) / abs(target)
            if err < tol:
                hits += 1
    f = hits / total
    fractions.append(f)

joint = 1.0
for f in fractions:
    joint *= f
print(f"\nJoint probability (independent): {joint:.2e}")
print(f"That's 1 in {1/joint:.0f}")

# AND: the bridge identity R_Λ - R_G = 1/φ exactly
# What fraction of bridge ratio PAIRS satisfy an exact algebraic identity?
print("\n=== BRIDGE IDENTITY TEST ===")
exact_hits = 0
pair_count = 0
for i, R1 in enumerate(bridge_list):
    for j, R2 in enumerate(bridge_list):
        if R1 > R2:
            pair_count += 1
            diff = R1 - R2
            # Check if diff is a "simple" Q(√5) number
            for a in [1, 2, 3, 4]:
                for n in range(-3, 4):
                    test = a * phi**n
                    if abs(diff - test) < 1e-10:
                        exact_hits += 1
                        break

print(f"Bridge pairs with exact Q(√5) difference: {exact_hits} out of {pair_count}")
print(f"Fraction: {exact_hits/pair_count:.4f}")

# Combined: joint probability × bridge identity
# The bridge identity is an ADDITIONAL constraint
print(f"\n=== COMBINED EVIDENCE ===")
print(f"Three-constant match probability: {joint:.2e}")
print(f"Bridge identity probability: ~{exact_hits/pair_count:.3f}")
combined = joint * (exact_hits/pair_count)
print(f"Combined: {combined:.2e}")
print(f"That's 1 in {1/combined:.0f}")
