"""
Step 3 (optimized): Permissive ablation with numpy float64.
Float64 gives ~10⁻¹⁵ precision, ample for the 10⁻¹¹-level discrimination.
"""
import numpy as np
import itertools, bisect, json

phi = (1.0 + np.sqrt(5.0)) / 2.0
alpha_inv_morel = 137.035999206
sigma_morel = 0.000000011

pentagon = 360/phi**2 - 2/phi**3 + 1/(3**5 * phi**5) + 1/(7**7 * phi**7)
pentagon_dev = abs(pentagon - alpha_inv_morel)

# Permissive rational pool: ±a/b with a ∈ [0..30], b ∈ [1..30]
# Plus small integers up to 500 (covers 360)
def build_permissive_pool(N_NUM=30, N_DEN=30, MAX_INT=500):
    vals = set()
    vals.add(0.0)
    for k in range(1, MAX_INT + 1):
        vals.add(float(k))
        vals.add(-float(k))
    for a in range(1, N_NUM + 1):
        for b in range(2, N_DEN + 1):
            v = a / b
            vals.add(v)
            vals.add(-v)
    arr = np.array(sorted(vals))
    return arr

pool = build_permissive_pool()
print(f"Permissive pool size: {len(pool):,} values")

# Small pool for c_2, c_3 (kept small for runtime)
small_pool_vals = set()
small_pool_vals.add(0.0)
for k in range(1, 15):
    small_pool_vals.add(float(k))
    small_pool_vals.add(-float(k))
for a in range(1, 10):
    for b in range(2, 10):
        v = a/b
        small_pool_vals.add(v)
        small_pool_vals.add(-v)
small_pool = np.array(sorted(small_pool_vals))
print(f"Small pool (c2, c3): {len(small_pool)}")

# Labels for top matches
def label(v):
    if v == 0: return "0"
    sign = "+" if v > 0 else "-"
    av = abs(v)
    # integer?
    if abs(av - round(av)) < 1e-14:
        return f"{sign}{int(round(av))}"
    # simple fraction?
    for b in range(2, 31):
        a = av * b
        if abs(a - round(a)) < 1e-12 and round(a) <= 30:
            return f"{sign}{int(round(a))}/{b}"
    return f"{sign}{av:.6e}"

exp_choices = list(range(1, 11))
exp_tuples = list(itertools.combinations(exp_choices, 4))

lead_pool = np.array([60, 120, 180, 240, 360, 400, 720] + list(range(1, 10)), dtype=float)

thresholds = {
    "0.1σ": 0.1 * sigma_morel,
    "1σ":   sigma_morel,
    "10σ":  10 * sigma_morel,
    "100σ": 100 * sigma_morel,
    "1ppb": alpha_inv_morel * 1e-9,
    "1ppm": alpha_inv_morel * 1e-6,
}
counts = {k: 0 for k in thresholds}
top_matches = []

n_tuples = len(exp_tuples)
print(f"Exponent tuples: {n_tuples}")
print(f"Total formula evaluations: {n_tuples * len(lead_pool) * len(small_pool)**2:,}")
print()

def nearest_pool(x, arr=pool):
    """Return (value, index, diff) for nearest pool entry."""
    idx = np.searchsorted(arr, x)
    # candidates
    best_d = np.inf
    best_v = 0.0
    best_i = -1
    for i in (idx-1, idx):
        if 0 <= i < len(arr):
            d = abs(arr[i] - x)
            if d < best_d:
                best_d = d
                best_v = arr[i]
                best_i = i
    return best_v, best_i, best_d

# Vectorised per exponent-tuple
for ti, (p1, p2, p3, p4) in enumerate(exp_tuples):
    phi_p = np.array([phi**p1, phi**p2, phi**p3, phi**p4])
    for lead in lead_pool:
        T1 = lead / phi_p[0]
        # Vectorise over c2, c3
        # Broadcast to flat (P*P,) arrays
        c2_flat = np.repeat(small_pool, len(small_pool))    # (P*P,)
        c3_flat = np.tile  (small_pool, len(small_pool))    # (P*P,)
        T2_flat = c2_flat / phi_p[1]
        T3_flat = c3_flat / phi_p[2]
        residual = alpha_inv_morel - T1 - T2_flat - T3_flat
        flat_c4_needed = residual * phi_p[3]
        # Snap each to pool using searchsorted
        idxs = np.searchsorted(pool, flat_c4_needed)
        idxs = np.clip(idxs, 1, len(pool)-1)
        c4a = pool[idxs - 1]
        c4b = pool[idxs]
        choose_b = np.abs(c4b - flat_c4_needed) < np.abs(c4a - flat_c4_needed)
        c4 = np.where(choose_b, c4b, c4a)
        # full α⁻¹
        trial = T1 + T2_flat + T3_flat + c4 / phi_p[3]
        absdev = np.abs(trial - alpha_inv_morel)
        # Bucket counts
        for k, tol in thresholds.items():
            counts[k] += int(np.sum(absdev <= tol))
        # Track best within 10σ for top matches table
        mask10 = absdev <= thresholds["10σ"]
        if mask10.any():
            for j in np.nonzero(mask10)[0]:
                top_matches.append((absdev[j],
                                    (p1,p2,p3,p4),
                                    float(lead),
                                    float(c2_flat[j]),
                                    float(c3_flat[j]),
                                    float(c4[j])))
    if (ti+1) % 30 == 0:
        print(f"  processed {ti+1}/{n_tuples} tuples")

top_matches.sort(key=lambda x: x[0])

print()
print("=" * 80)
print("PERMISSIVE ABLATION RESULTS")
print("=" * 80)
print(f"Exponents:  any 4 distinct from (1..10)       [{len(exp_tuples)} tuples]")
print(f"Leading c1: {len(lead_pool)} candidates (including 360)")
print(f"c2, c3:     small rationals ±a/b (a≤14, b≤9)  [{len(small_pool)} values]")
print(f"c4:        snapped to permissive pool          [{len(pool):,} rationals]")
print()
print("Count of distinct (exponents, coeffs) matching α⁻¹ to within tolerance:")
for k, tol in thresholds.items():
    print(f"  within {k:<6} (|Δα⁻¹| ≤ {tol:.2e}):  {counts[k]:,}")
print()
print("Pentagon benchmark: |Δ| = {:.3e}  ({:.3f}σ)   exps=(2,3,5,7)  c=(360,-2,1/3⁵,1/7⁷)".format(
    pentagon_dev, pentagon_dev/sigma_morel))
print()
print("Top 15 permissive matches (any exponents from 1..10):")
print("-" * 110)
print(f"{'rank':<5} {'|Δα⁻¹|':<12} {'σ':<8} {'exps':<18} {'c1':<8} {'c2':<10} {'c3':<10} {'c4':<16}")
print("-" * 110)
for i, entry in enumerate(top_matches[:15]):
    absdev, exps, lead, c2, c3, c4 = entry
    print(f"{i+1:<5} {absdev:<12.3e} {absdev/sigma_morel:<8.3f} "
          f"{str(exps):<18} {lead:<8.0f} {label(c2):<10} {label(c3):<10} {label(c4):<16}")

# Look at whether any permissive match has exps = (2,3,5,7)
pentagonish = [e for e in top_matches if e[1] == (2,3,5,7)]
print()
print(f"Permissive matches with exponents EXACTLY (2,3,5,7):  {len(pentagonish)}")
for i, (absdev, exps, lead, c2, c3, c4) in enumerate(pentagonish[:5]):
    print(f"  #{i+1}: |Δ|={absdev:.3e} ({absdev/sigma_morel:.2f}σ)  c=({lead:.0f}, {label(c2)}, {label(c3)}, {label(c4)})")

with open('/home/claude/alpha_v5/ablation_permissive_results.json', 'w') as f:
    json.dump({
        "pool_size": len(pool),
        "exp_tuples": len(exp_tuples),
        "small_pool_size": len(small_pool),
        "counts": {k: counts[k] for k in thresholds},
        "pentagon_dev": pentagon_dev,
        "top_30": [
            {"rank": i+1, "abs_dev": float(e[0]), "sigma": float(e[0]/sigma_morel),
             "exps": list(e[1]), "c1": float(e[2]),
             "c2": float(e[3]), "c3": float(e[4]), "c4": float(e[5])}
            for i, e in enumerate(top_matches[:30])
        ],
    }, f, indent=2)
print("\nResults saved.")
