"""
Step 2: 2I-restricted ablation of the Pentagon formula.

Claim tested:
  In the restricted search space of formulas
     α⁻¹ = c_2/φ^2 + c_3/φ^3 + c_5/φ^5 + c_7/φ^7
  where:
    - exponents are restricted to {2, 3, 5, 7} (first four primes,
      = prime factors of μ_7 = Tr(A^7)/1440 = 2^5·3^2·5^2·7 for
      the 600-cell adjacency matrix),
    - c_2 is fixed at 360 (angular convention: the first term is
      the golden angle in degrees, 360/φ^2 = 137.508°),
    - c_3, c_5, c_7 are drawn from a 2I-derivable coefficient pool,
  the four-term formula (c_3, c_5, c_7) = (-2, 1/3^5, 1/7^7)
  is uniquely preferred.

Restricted coefficient pool P:
  P = {0} ∪ {±k : k = 1..MAX_INT}          # eigenvalue-style integers
      ∪ {±1/(m^n) : m ∈ [2..7], n ∈ [1..7]}  # self-referential p^(-q) forms

The integer range 1..20 covers:
  - Irrep dimensions of 2I: {1, 2, 2, 3, 3, 4, 4, 5, 6}
  - Absolute values of eigenvalues: {0, 2, 3, 12} and rounded {2.47, 3.71, 6.47, 9.71}
  - Laplacian eigenvalues: {0, 9, 12, 14, 15}
  - Small multiplicities: {1, 4, 9, 16, 25, 36} (perfect squares)

The 1/(m^n) family with m ∈ [2..7] covers p^(-p) forms:
  m=3, n=5:  1/243  ← Pentagon T5 coefficient
  m=7, n=7:  1/823543 ← Pentagon T7 coefficient
"""
import mpmath
from mpmath import mpf, mp, sqrt
import itertools
import json

mp.dps = 50

phi = (1 + sqrt(5)) / 2
alpha_inv_morel = mpf("137.035999206")
sigma_morel    = mpf("0.000000011")

# Pentagon benchmark
T2_pentagon = mpf(360) / phi**2
T3_pentagon = mpf(-2) / phi**3
T5_pentagon = mpf(1) / (mpf(3)**5 * phi**5)
T7_pentagon = mpf(1) / (mpf(7)**7 * phi**7)
pentagon = T2_pentagon + T3_pentagon + T5_pentagon + T7_pentagon
pentagon_dev = abs(pentagon - alpha_inv_morel)
pentagon_sigma = pentagon_dev / sigma_morel

# ---------- Build the restricted coefficient pool P ----------
MAX_INT = 20  # covers all irrep dims, eigenvalues, and small structural integers
MAX_BASE = 7  # largest prime in μ_7 factorisation
MAX_EXP = 7   # matches the prime-power range in the formula

def build_restricted_pool():
    """
    Returns list of mpf values drawn ONLY from 2I-derivable quantities.
    Each entry is accompanied by a human-readable label for traceability.
    """
    entries = []  # list of (value, label)

    # Zero (allows dropping a term — fewer-term formulas)
    entries.append((mpf(0), "0"))

    # Signed integers up to MAX_INT (eigenvalue / dimension / multiplicity values)
    for k in range(1, MAX_INT + 1):
        entries.append((mpf(k),  f"+{k}"))
        entries.append((mpf(-k), f"-{k}"))

    # 1/(m^n) forms with 2 ≤ m ≤ MAX_BASE and 1 ≤ n ≤ MAX_EXP
    # Deduplicate by value.
    seen_vals = set()
    for m in range(2, MAX_BASE + 1):
        for n in range(1, MAX_EXP + 1):
            val = mpf(1) / (mpf(m) ** n)
            key = mpmath.nstr(val, 30)
            if key in seen_vals:
                continue
            seen_vals.add(key)
            entries.append(( val, f"+1/{m}^{n}"))
            entries.append((-val, f"-1/{m}^{n}"))

    return entries

pool = build_restricted_pool()
print(f"Restricted 2I-derivable coefficient pool: {len(pool)} entries")
print(f"(integers ±1..{MAX_INT}, 1/(m^n) with m∈[2,{MAX_BASE}], n∈[1,{MAX_EXP}], plus 0 and signs)")
print()

# Confirm Pentagon correction coefficients are in the pool
pentagon_corrections = {
    "c_3": (mpf(-2),             "-2"),
    "c_5": (mpf(1)/(mpf(3)**5),  "+1/3^5"),
    "c_7": (mpf(1)/(mpf(7)**7),  "+1/7^7"),
}
print("Pentagon correction coefficients, lookup in pool:")
for name, (val, label) in pentagon_corrections.items():
    found = any(abs(v - val) < mpf("1e-40") for v, _ in pool)
    print(f"  {name} = {label:<12}  in pool? {found}")
print()

# ---------- Factored ablation ----------
#
# For α⁻¹ = 360/φ² + c3/φ³ + c5/φ⁵ + c7/φ⁷ to match α⁻¹_morel,
# we need   c3/φ³ + c5/φ⁵ + c7/φ⁷ = α⁻¹_morel - 360/φ² = target_corr.
# Factor:   for each (c5, c7) pair, compute residual r = target_corr - c5/φ⁵ - c7/φ⁷.
#           then c3 must satisfy  c3/φ³ = r,  i.e. c3 = r · φ³.
# Search the pool for the entry closest to r·φ³ and record the match quality.
#
# Complexity: |pool|² ≈ 1.6·10⁴  + binary search in sorted pool = very fast.

target_corr = alpha_inv_morel - T2_pentagon
phi3 = phi**3
phi5 = phi**5
phi7 = phi**7

# Sort pool by value for binary search
pool_sorted = sorted(pool, key=lambda x: x[0])
pool_vals = [v for v, _ in pool_sorted]
pool_labels = [lbl for _, lbl in pool_sorted]

import bisect
def nearest_in_pool(target):
    """Return (best_val, best_label, |diff|) finding entry in pool closest to target."""
    # Convert to float for bisect
    tf = float(target)
    idx = bisect.bisect_left([float(v) for v in pool_vals], tf)
    candidates = []
    for i in (idx-1, idx, idx+1):
        if 0 <= i < len(pool_vals):
            candidates.append((pool_vals[i], pool_labels[i], abs(pool_vals[i] - target)))
    candidates.sort(key=lambda x: x[2])
    return candidates[0]

results = []  # (alpha_inv_deviation, c3_lbl, c5_lbl, c7_lbl)

for (c5, lbl5) in pool:
    t5_val = c5 / phi5
    for (c7, lbl7) in pool:
        t7_val = c7 / phi7
        # Required c3:
        c3_needed = (target_corr - t5_val - t7_val) * phi3
        # Snap to nearest pool entry
        c3_actual, lbl3, snap_err = nearest_in_pool(c3_needed)
        # Compute full α⁻¹ for this combo
        alpha_inv_trial = T2_pentagon + c3_actual/phi3 + t5_val + t7_val
        dev = alpha_inv_trial - alpha_inv_morel
        results.append((abs(dev), float(dev), lbl3, lbl5, lbl7))

results.sort(key=lambda x: x[0])

print("=" * 80)
print(f"2I-RESTRICTED ABLATION RESULTS ({len(results):,} formulas tested)")
print("=" * 80)
print(f"Leading term fixed: c_2 = 360 (angular convention)")
print(f"Exponents fixed:    (2, 3, 5, 7) (first four primes, = μ_7 factorisation primes)")
print(f"Pool size: {len(pool)}  |  Search space: {len(pool)}^3 = {len(pool)**3:,}")
print(f"(factored to |pool|^2 = {len(pool)**2:,} via nearest-neighbour on residual)")
print()
print(f"Pentagon formula benchmark: |α⁻¹ - Morel| = {float(pentagon_dev):.3e}  ({float(pentagon_sigma):.3f} σ)")
print()
print("Top 15 formulas ranked by accuracy:")
print("-" * 80)
print(f"{'rank':<5} {'|Δα⁻¹|':<14} {'σ_Morel':<10} {'c3':<12} {'c5':<12} {'c7':<12}")
print("-" * 80)
for i, (absdev, dev, lbl3, lbl5, lbl7) in enumerate(results[:15]):
    sig = absdev / sigma_morel
    marker = "  ← PENTAGON" if (lbl3 == "-2" and lbl5 == "+1/3^5" and lbl7 == "+1/7^7") else ""
    print(f"{i+1:<5} {float(absdev):<14.3e} {float(sig):<10.3f} {lbl3:<12} {lbl5:<12} {lbl7:<12}{marker}")
print()

# Find Pentagon rank
pentagon_rank = None
for i, (absdev, dev, lbl3, lbl5, lbl7) in enumerate(results):
    if lbl3 == "-2" and lbl5 == "+1/3^5" and lbl7 == "+1/7^7":
        pentagon_rank = i + 1
        pentagon_entry = (absdev, lbl3, lbl5, lbl7)
        break
print(f"Pentagon formula rank: {pentagon_rank}")
print(f"Pentagon |Δα⁻¹|      = {float(pentagon_entry[0]):.3e}  ({float(pentagon_entry[0]/sigma_morel):.3f} σ_Morel)")

# Accuracy gap to runner-up (or runner-down)
if pentagon_rank == 1:
    runner_up = results[1]
    gap = runner_up[0] / pentagon_entry[0]
    print(f"Runner-up: c3={runner_up[2]}, c5={runner_up[3]}, c7={runner_up[4]}  |Δ|={float(runner_up[0]):.3e}")
    print(f"Accuracy gap to runner-up: {float(gap):.1f}×")
else:
    winner = results[0]
    print(f"Winner:    c3={winner[2]}, c5={winner[3]}, c7={winner[4]}  |Δ|={float(winner[0]):.3e}")

# Count of formulas matching within various tolerances
print()
print("Count of distinct (c3, c5, c7) formulas matching within various tolerances:")
for tol_label, tol_sigma in [("0.1σ", mpf("0.1")*sigma_morel),
                              ("1σ",   sigma_morel),
                              ("10σ",  mpf(10)*sigma_morel),
                              ("100σ", mpf(100)*sigma_morel),
                              ("1ppb", alpha_inv_morel*mpf("1e-9")),
                              ("1ppm", alpha_inv_morel*mpf("1e-6")),
                              ("0.1%",  alpha_inv_morel*mpf("1e-3"))]:
    cnt = sum(1 for r in results if r[0] <= tol_sigma)
    print(f"  within {tol_label:<6} (|Δα⁻¹| ≤ {float(tol_sigma):.2e}):  {cnt:,}")

# Save top results
with open('/home/claude/alpha_v5/ablation_restricted_results.json', 'w') as f:
    json.dump({
        "pool_size": len(pool),
        "search_space_size": len(pool)**3,
        "pentagon_rank": pentagon_rank,
        "pentagon_deviation": float(pentagon_entry[0]),
        "pentagon_sigma_morel": float(pentagon_entry[0]/sigma_morel),
        "top_20": [
            {"rank": i+1, "abs_dev": float(r[0]), "sigma": float(r[0]/sigma_morel),
             "c3": r[2], "c5": r[3], "c7": r[4]}
            for i, r in enumerate(results[:20])
        ],
    }, f, indent=2)

print("\nResults saved to ablation_restricted_results.json")
