"""
Step 5b — Ablation B (proper): PERMISSIVE coefficients for ALL terms,
PRIME-fixed exponents (2,3,5,7).

This tests: does the prime-exponent restriction alone isolate Pentagon,
or do we need the coefficient pool restriction as well?

Full permissive pool: a/b with a ∈ [1..30], b ∈ [2..30] plus integers up to 500
(includes 360 and ±500).  Note 1/3^5 = 1/243 is NOT in this pool (b > 30),
so we augment with prime-power reciprocals {1/m^n : m ∈ [2,12], n ∈ [1,10]}
so that Pentagon's coefficients themselves are in the search space.
"""
import numpy as np
import json

phi = (1.0 + np.sqrt(5.0)) / 2.0
alpha_inv_morel = 137.035999206
sigma_morel = 0.000000011

pentagon = 360/phi**2 - 2/phi**3 + 1/(3**5 * phi**5) + 1/(7**7 * phi**7)
pentagon_dev = abs(pentagon - alpha_inv_morel)

# Expanded permissive pool that INCLUDES the Pentagon coefficients
def build_expanded_permissive_pool():
    vals = set()
    vals.add(0.0)
    # integers up to 500
    for k in range(1, 501):
        vals.add(float(k)); vals.add(-float(k))
    # rationals a/b with a ≤ 30, b ≤ 30
    for a in range(1, 31):
        for b in range(2, 31):
            v = a/b
            vals.add(v); vals.add(-v)
    # prime-power reciprocals 1/m^n (so that 1/3^5, 1/7^7, etc., are in)
    for m in range(2, 13):
        for n in range(1, 11):
            v = 1.0 / (m**n)
            vals.add(v); vals.add(-v)
    return np.array(sorted(vals))

pool = build_expanded_permissive_pool()
print(f"Expanded permissive pool: {len(pool):,}  (includes 1/3^5, 1/7^7 etc.)")

# Confirm Pentagon coefficients are in pool
for name, v in [("360", 360.0), ("-2", -2.0), ("+1/3^5", 1.0/243), ("+1/7^7", 1.0/823543)]:
    present = np.any(np.abs(pool - v) < 1e-12)
    print(f"  {name} in pool? {present}")
print()

# Fixed exponents (2, 3, 5, 7), c1 = 360
p1, p2, p3, p4 = 2, 3, 5, 7
phi_p = [phi**p for p in (p1,p2,p3,p4)]
T1 = 360 / phi_p[0]

P = len(pool)
print(f"Search: {P}² = {P*P:,} formulas")
print("(factored over c_2, c_3; c_4 solved and snapped)")
print()

thresholds = {
    "0.1σ": 0.1 * sigma_morel,
    "1σ":   sigma_morel,
    "10σ":  10 * sigma_morel,
    "100σ": 100 * sigma_morel,
    "1ppb": alpha_inv_morel * 1e-9,
    "1ppm": alpha_inv_morel * 1e-6,
}
counts = {k: 0 for k in thresholds}
top_matches = []  # (absdev, c2, c3, c4)

# Process in chunks to manage memory (~P² floats = ~90M for P=9.6k)
CHUNK = 500
for start in range(0, P, CHUNK):
    end = min(start + CHUNK, P)
    c2_chunk = pool[start:end]                     # (c,)
    T2_chunk = c2_chunk / phi_p[1]                 # (c,)
    # broadcast against full pool for c3
    residuals = alpha_inv_morel - T1 - T2_chunk[:, None] - pool[None, :] / phi_p[2]  # (c, P)
    c4_needed = residuals * phi_p[3]                                          # (c, P)
    flat = c4_needed.ravel()
    idxs = np.searchsorted(pool, flat)
    idxs = np.clip(idxs, 1, P-1)
    cand_a = pool[idxs-1]
    cand_b = pool[idxs]
    choose_b = np.abs(cand_b - flat) < np.abs(cand_a - flat)
    c4 = np.where(choose_b, cand_b, cand_a)
    trial = (T1
             + np.repeat(T2_chunk, P)
             + np.tile  (pool, end-start) / phi_p[2]
             + c4 / phi_p[3])
    absdev = np.abs(trial - alpha_inv_morel)
    for k, tol in thresholds.items():
        counts[k] += int(np.sum(absdev <= tol))
    # track 10σ hits
    mask10 = absdev <= thresholds["10σ"]
    if mask10.any():
        c2_grid = np.repeat(c2_chunk, P)
        c3_grid = np.tile  (pool,      end-start)
        for j in np.nonzero(mask10)[0]:
            top_matches.append((float(absdev[j]),
                                float(c2_grid[j]),
                                float(c3_grid[j]),
                                float(c4[j])))

top_matches.sort(key=lambda x: x[0])

print("Counts matching α⁻¹ within tolerance:")
for k, tol in thresholds.items():
    print(f"  within {k:<6} (|Δα⁻¹| ≤ {tol:.2e}):  {counts[k]:,}")
print()

def flabel(v):
    if v == 0: return "0"
    s = "+" if v > 0 else "-"
    av = abs(v)
    if abs(av - round(av)) < 1e-12 and round(av) <= 1000:
        return f"{s}{int(round(av))}"
    # look for 1/m^n
    for m in range(2, 13):
        for n in range(1, 11):
            if abs(av - 1.0/(m**n)) < 1e-14:
                return f"{s}1/{m}^{n}"
    # simple fraction?
    for b in range(2, 31):
        a = av*b
        if abs(a - round(a)) < 1e-10 and round(a) <= 30:
            return f"{s}{int(round(a))}/{b}"
    return f"{s}{av:.6g}"

print(f"Pentagon benchmark: |Δ| = {pentagon_dev:.3e}  ({pentagon_dev/sigma_morel:.3f}σ)")
print(f"                    c = (360, -2, +1/3^5, +1/7^7)")
print()
print("Top 15 matches (PERMISSIVE coefs, fixed prime exps (2,3,5,7)):")
print("-" * 100)
print(f"{'rank':<5} {'|Δα⁻¹|':<12} {'σ':<8} {'c_1':<6} {'c_2':<10} {'c_3':<12} {'c_4':<14}")
print("-" * 100)
for i, (absdev, c2, c3, c4) in enumerate(top_matches[:15]):
    marker = "  ← PENTAGON" if (abs(c2 + 2) < 1e-12 and abs(c3 - 1/243) < 1e-14 and abs(c4 - 1/823543) < 1e-16) else ""
    print(f"{i+1:<5} {absdev:<12.3e} {absdev/sigma_morel:<8.3f} "
          f"{'360':<6} {flabel(c2):<10} {flabel(c3):<12} {flabel(c4):<14}{marker}")

with open('/home/claude/alpha_v5/ablation_B_proper_results.json', 'w') as f:
    json.dump({
        "pool_size": P,
        "counts": {k: counts[k] for k in thresholds},
        "top_30": [
            {"rank": i+1, "abs_dev": t[0], "sigma": t[0]/sigma_morel,
             "c1": 360.0, "c2": t[1], "c3": t[2], "c4": t[3]}
            for i, t in enumerate(top_matches[:30])
        ],
    }, f, indent=2)
print("\nResults saved.")
