import math

# Constants
phi = (1 + math.sqrt(5)) / 2
alpha_inv = 137.035999206  # Morel 2020
sqrt5 = math.sqrt(5)

# Template parameters
R_G = 1 / (phi * sqrt5)
floor = phi**(-2)

# CODATA-2022 inputs
hbar = 1.054571817e-34
c = 299792458
m_p = 1.67262192595e-27
G_ref = 6.67430e-11  # CODATA-2022 recommended

# Candidate family: Delta = +/- a / (b * phi^n * 5^m)
# a in {1,2,3,4}, n in {1..10}, b in {1,5,25}, m in {0,1,2,3}
candidates = []

# Zero correction
candidates.append((0, 0.0, "0"))

for sign in [+1, -1]:
    for a in [1, 2, 3, 4]:
        for n in range(1, 11):
            for b in [1, 5, 25]:
                for m in [0, 1, 2, 3]:
                    val = sign * a / (b * phi**n * 5**m)
                    # Build label
                    sign_str = "+" if sign > 0 else "-"
                    num = str(a)
                    den_parts = []
                    if b > 1:
                        den_parts.append(str(b))
                    if n > 0:
                        den_parts.append(f"φ^{n}" if n > 1 else "φ")
                    if m > 0:
                        den_parts.append(f"5^{m}" if m > 1 else "5")
                    den = " ".join(den_parts) if den_parts else "1"
                    label = f"{sign_str}{num}/({den})"
                    candidates.append((sign, val, label))

print(f"Total candidates: {len(candidates)}")

# Evaluate each
results = []
for sign, delta, label in candidates:
    exponent = -alpha_inv * R_G - floor + delta
    alpha_G = 10**exponent
    G_pred = alpha_G * hbar * c / m_p**2
    rel_error = abs(G_pred - G_ref) / G_ref
    # Symbol complexity: count distinct operations
    results.append({
        'delta': delta,
        'label': label,
        'G_pred': G_pred,
        'rel_error': rel_error,
        'exponent': exponent
    })

# Sort by relative error
results.sort(key=lambda x: x['rel_error'])

# Deduplicate: if two candidates have delta within 1e-10, keep simpler label
deduped = []
for r in results:
    is_dup = False
    for d in deduped:
        if abs(r['delta'] - d['delta']) < 1e-10:
            is_dup = True
            break
    if not is_dup:
        deduped.append(r)

print(f"\nDistinct corrections after dedup: {len(deduped)}")
print(f"\nTop 10 distinct results:")
print(f"{'Rank':>4} {'Label':>25} {'Delta':>12} {'G_pred':>16} {'Rel Error':>12} {'Gap':>8}")
print("-" * 85)

best_err = deduped[0]['rel_error']
for i, r in enumerate(deduped[:10]):
    gap = r['rel_error'] / best_err if best_err > 0 else 0
    print(f"{i+1:4d} {r['label']:>25} {r['delta']:12.7f} {r['G_pred']:16.6e} {r['rel_error']*100:11.4f}% {gap:7.1f}x")

# Also check: what does the best result give in ppm?
best = deduped[0]
print(f"\nBest result details:")
print(f"  Delta = {best['delta']:.10f}")
print(f"  G_pred = {best['G_pred']:.6e}")
print(f"  G_ref  = {G_ref:.6e}")
print(f"  Rel error = {best['rel_error']*1e6:.1f} ppm")
print(f"  log10(alpha_G) = {best['exponent']:.6f}")
print(f"  alpha_G = {10**best['exponent']:.6e}")
