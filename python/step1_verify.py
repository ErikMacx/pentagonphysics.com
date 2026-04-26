"""
Step 1: Verify the Pentagon formula at 50-digit precision.
Establish baseline accuracy against Morel 2020.
"""
import mpmath
from mpmath import mpf, mp, sqrt

mp.dps = 50

phi = (1 + sqrt(5)) / 2

# Morel 2020 measurement
alpha_inv_morel = mpf("137.035999206")
sigma_morel = mpf("0.000000011")

# Pentagon formula
T2 = mpf(360) / phi**2
T3 = mpf(-2) / phi**3
T5 = mpf(1) / (mpf(3)**5 * phi**5)
T7 = mpf(1) / (mpf(7)**7 * phi**7)

alpha_inv_pentagon = T2 + T3 + T5 + T7

print("=" * 70)
print("PENTAGON FORMULA VERIFICATION")
print("=" * 70)
print(f"T2 = 360/phi^2       = {T2}")
print(f"T3 = -2/phi^3        = {T3}")
print(f"T5 = 1/(3^5 phi^5)   = {T5}")
print(f"T7 = 1/(7^7 phi^7)   = {T7}")
print()
print(f"Pentagon sum    = {alpha_inv_pentagon}")
print(f"Morel 2020      = {alpha_inv_morel}")
print(f"Difference      = {alpha_inv_pentagon - alpha_inv_morel}")
print(f"In sigma (Morel)= {(alpha_inv_pentagon - alpha_inv_morel) / sigma_morel}")
print()

# Pre-compute target correction (what the non-leading terms must sum to)
target_full = alpha_inv_morel           # what the 4 terms should sum to
target_after_T2 = alpha_inv_morel - T2  # what T3+T5+T7 should equal
print(f"Target correction (T3+T5+T7) = α⁻¹ - 360/phi^2 = {target_after_T2}")
print()

# Also check cumulative precision
cum = mpf(0)
for i, (name, val) in enumerate([("T2", T2), ("T3", T3), ("T5", T5), ("T7", T7)]):
    cum += val
    diff = cum - alpha_inv_morel
    print(f"After {name}: α⁻¹ ≈ {cum}  (off by {float(diff):+.3e})")
