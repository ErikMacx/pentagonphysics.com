"""
Step 4 — Ablation C: 2I-restricted coefficients with FREE exponents.

If the restricted coefficient pool alone is enough to pin Pentagon down,
this ablation must rank Pentagon (2,3,5,7) first among all exponent tuples
drawn from {1..12}.
"""
import numpy as np
import itertools, json

phi = (1.0 + np.sqrt(5.0)) / 2.0
alpha_inv_morel = 137.035999206
sigma_morel = 0.000000011
pentagon = 360/phi**2 - 2/phi**3 + 1/(3**5 * phi**5) + 1/(7**7 * phi**7)
pentagon_dev = abs(pentagon - alpha_inv_morel)

# 2I-restricted coefficient pool (same as step 2)
def build_restricted_pool(MAX_INT=20, MAX_BASE=7, MAX_EXP=7):
    vals_float = []
    labels = []
    # zero
    vals_float.append(0.0); labels.append("0")
    # signed integers
    for k in range(1, MAX_INT+1):
        vals_float.append(float(k));  labels.append(f"+{k}")
        vals_float.append(float(-k)); labels.append(f"-{k}")
    # 1/(m^n)
    seen = set()
    for m in range(2, MAX_BASE+1):
        for n in range(1, MAX_EXP+1):
            v = 1.0/(m**n)
            key = round(v, 12)
            if key in seen: continue
            seen.add(key)
            vals_float.append(v);  labels.append(f"+1/{m}^{n}")
            vals_float.append(-v); labels.append(f"-1/{m}^{n}")
    order = np.argsort(vals_float)
    arr = np.array(vals_float)[order]
    lbl = [labels[i] for i in order]
    return arr, lbl

pool_arr, pool_lbl = build_restricted_pool()
print(f"2I-restricted pool: {len(pool_arr)} entries")

# Leading-term options (angular convention 360 + structural 2I integers)
lead_options = [360, 720, 180, 240, 120, 60]

# Free exponents from {2..12}, 4-tuple distinct sorted
exp_range = list(range(2, 13))  # 11 choices → 330 4-tuples
exp_tuples = list(itertools.combinations(exp_range, 4))

print(f"Exponent 4-tuples from {{2..12}}: {len(exp_tuples)}")
print(f"Leading candidates: {len(lead_options)}")
print(f"Formula search: {len(exp_tuples) * len(lead_options) * len(pool_arr)**3:,}")
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

# For each (exps, lead), enumerate (c_b, c_c) from pool; solve for c_d; snap.
# c_a = lead (fixed per iteration).
#
# formula: α⁻¹ = lead/φ^p1 + c_b/φ^p2 + c_c/φ^p3 + c_d/φ^p4
# → c_d = (α⁻¹ - lead/φ^p1 - c_b/φ^p2 - c_c/φ^p3) × φ^p4

top_matches = []
pentagon_rank = None
pentagon_dev_in_restricted = None

P = len(pool_arr)
# pre-flatten c_b, c_c
cb_flat = np.repeat(pool_arr, P)  # (P²,)
cc_flat = np.tile  (pool_arr, P)  # (P²,)
cb_lbl_flat = np.repeat(np.arange(P), P)
cc_lbl_flat = np.tile  (np.arange(P), P)

best_overall = None

for ti, (p1, p2, p3, p4) in enumerate(exp_tuples):
    phi_p = np.array([phi**p1, phi**p2, phi**p3, phi**p4])
    for lead in lead_options:
        T1 = lead / phi_p[0]
        T2_flat = cb_flat / phi_p[1]
        T3_flat = cc_flat / phi_p[2]
        residual = alpha_inv_morel - T1 - T2_flat - T3_flat
        c_d_needed = residual * phi_p[3]
        # snap to pool_arr
        idxs = np.searchsorted(pool_arr, c_d_needed)
        idxs = np.clip(idxs, 1, P-1)
        da = pool_arr[idxs-1]; db = pool_arr[idxs]
        choose_b = np.abs(db - c_d_needed) < np.abs(da - c_d_needed)
        c_d = np.where(choose_b, db, da)
        d_idx = np.where(choose_b, idxs, idxs-1)
        trial = T1 + T2_flat + T3_flat + c_d / phi_p[3]
        absdev = np.abs(trial - alpha_inv_morel)
        # counts
        for k, tol in thresholds.items():
            counts[k] += int(np.sum(absdev <= tol))
        # best-of-batch
        j = int(np.argmin(absdev))
        if best_overall is None or absdev[j] < best_overall[0]:
            best_overall = (absdev[j], (p1,p2,p3,p4), lead,
                            pool_lbl[cb_lbl_flat[j]],
                            pool_lbl[cc_lbl_flat[j]],
                            pool_lbl[d_idx[j]])
        # top matches (within 10σ)
        mask10 = absdev <= thresholds["10σ"]
        if mask10.any():
            for j in np.nonzero(mask10)[0]:
                top_matches.append((absdev[j], (p1,p2,p3,p4), lead,
                                    pool_lbl[cb_lbl_flat[j]],
                                    pool_lbl[cc_lbl_flat[j]],
                                    pool_lbl[d_idx[j]]))

top_matches.sort(key=lambda x: x[0])

# Check Pentagon presence
for i, entry in enumerate(top_matches):
    absdev, exps, lead, c_b, c_c, c_d = entry
    if exps == (2,3,5,7) and lead == 360 and c_b == "-2" and c_c == "+1/3^5" and c_d == "+1/7^7":
        pentagon_rank = i + 1
        break

print()
print("=" * 80)
print("ABLATION C: 2I-restricted coefficients, FREE exponents in {2..12}")
print("=" * 80)
print()
print("Count of formulas matching α⁻¹ to within tolerance:")
for k, tol in thresholds.items():
    print(f"  within {k:<6} (|Δα⁻¹| ≤ {tol:.2e}):  {counts[k]:,}")
print()
print(f"Pentagon formula rank in this space: {pentagon_rank}")
print()
print("Top 15 matches:")
print("-" * 100)
print(f"{'rank':<5} {'|Δα⁻¹|':<12} {'σ':<8} {'exponents':<16} {'c1':<6} {'c2':<10} {'c3':<12} {'c4':<12}")
print("-" * 100)
for i, entry in enumerate(top_matches[:15]):
    absdev, exps, lead, cb_lbl, cc_lbl, cd_lbl = entry
    marker = "  ← PENTAGON" if (exps == (2,3,5,7) and lead == 360 and
                                 cb_lbl == "-2" and cc_lbl == "+1/3^5" and cd_lbl == "+1/7^7") else ""
    print(f"{i+1:<5} {absdev:<12.3e} {absdev/sigma_morel:<8.3f} "
          f"{str(exps):<16} {lead:<6} {cb_lbl:<10} {cc_lbl:<12} {cd_lbl:<12}{marker}")

with open('/home/claude/alpha_v5/ablation_C_results.json', 'w') as f:
    json.dump({
        "pool_size": len(pool_arr),
        "exp_tuples": len(exp_tuples),
        "lead_options": lead_options,
        "counts": {k: counts[k] for k in thresholds},
        "pentagon_rank": pentagon_rank,
        "top_30": [
            {"rank": i+1, "abs_dev": float(e[0]), "sigma": float(e[0]/sigma_morel),
             "exps": list(e[1]), "lead": int(e[2]),
             "cb": e[3], "cc": e[4], "cd": e[5]}
            for i, e in enumerate(top_matches[:30])
        ],
    }, f, indent=2)
print("\nResults saved.")
