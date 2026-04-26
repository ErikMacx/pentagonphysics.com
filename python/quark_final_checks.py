"""Final consolidated numerics for the paper."""
import numpy as np
phi=(1+np.sqrt(5))/2; sig=1/phi; s5=np.sqrt(5)

# PDG 2024 central values (GeV)
mu, md, ms = 2.16e-3, 4.67e-3, 93.4e-3
mc, mb, mt = 1.2730, 4.183, 172.57
# PDG uncertainties (approximate symmetric)
Eu, Ed, Es = 0.4e-3, 0.3e-3, 6e-3
Ec, Eb, Et = 0.046, 0.007, 0.29

def circulant(tri):
    s = np.sqrt(np.array(tri, dtype=float))
    A = np.mean(s)
    x = (s[0]-A)/A; y = (s[1]-A)/A
    r = np.hypot(x, -(2*y + x)/np.sqrt(3))
    delta = np.arctan2(-(2*y + x)/np.sqrt(3), x)
    Q = np.sum(s**2)/np.sum(s)**2
    return Q, r, delta

Qu, ru, du = circulant((mu, mc, mt))
Qd, rd, dd = circulant((md, ms, mb))

# Predicted values assuming identities exact:
Qsum_target = np.sqrt(5/2)
Qprod_shape = Qu*Qd  # just observed
cos_prod_target = 1/3

print("="*70)
print("Pentagon Physics quark spectral structure: numerics for the paper")
print("="*70)
print(f"\nInputs (PDG 2024 averages, GeV):")
print(f"  u = {mu:.5f} ± {Eu:.5f}")
print(f"  d = {md:.5f} ± {Ed:.5f}")
print(f"  s = {ms:.5f} ± {Es:.5f}")
print(f"  c = {mc:.4f} ± {Ec:.4f}")
print(f"  b = {mb:.3f} ± {Eb:.3f}")
print(f"  t = {mt:.2f} ± {Et:.2f}")

print("\nTwo Koide circulants (one per type):")
print(f"  UP-type  (u, c, t):  Q = {Qu:.6f}   r = {ru:.6f}   cos δ = {np.cos(du):+.6f}")
print(f"  DOWN-type(d, s, b):  Q = {Qd:.6f}   r = {rd:.6f}   cos δ = {np.cos(dd):+.6f}")
print(f"\n  Charged leptons:     Q = 0.666667   r = 1.414214  cos δ = -0.678571")
print(f"                         = 2/3         = √2            = -19/28")

print("\n--- Two suggested structural identities ---")
print(f"[I1]  Q_up + Q_down = sqrt(5/2)")
print(f"      observed:    {Qu+Qd:.6f}")
print(f"      predicted:   {Qsum_target:.6f}")
print(f"      residual:    {(Qu+Qd-Qsum_target)*1e4:+.2f} × 10^-4  ({(Qu+Qd-Qsum_target)/Qsum_target*100:+.3f}%)")

print(f"\n[I2]  cos δ_up · cos δ_down = 1/3")
print(f"      observed:    {np.cos(du)*np.cos(dd):.6f}")
print(f"      predicted:   {1/3:.6f}")
print(f"      residual:    {(np.cos(du)*np.cos(dd)-1/3)*1e4:+.2f} × 10^-4  ({(np.cos(du)*np.cos(dd)-1/3)/(1/3)*100:+.3f}%)")

print("\n--- Monte Carlo sensitivity ---")
np.random.seed(1)
N = 50000
Is1 = []; Is2 = []
for _ in range(N):
    u_ = np.random.normal(mu, Eu); d_ = np.random.normal(md, Ed); s_ = np.random.normal(ms, Es)
    c_ = np.random.normal(mc, Ec); b_ = np.random.normal(mb, Eb); t_ = np.random.normal(mt, Et)
    if min(u_, d_, s_, c_, b_, t_) <= 0: continue
    Qu_, _, du_ = circulant((u_, c_, t_))
    Qd_, _, dd_ = circulant((d_, s_, b_))
    Is1.append(Qu_ + Qd_); Is2.append(np.cos(du_)*np.cos(dd_))
Is1, Is2 = np.array(Is1), np.array(Is2)
print(f"  [I1] Q_up+Q_down mean ± sigma : {Is1.mean():.5f} ± {Is1.std():.5f}")
print(f"       distance to sqrt(5/2)    : {(Is1.mean()-np.sqrt(5/2))/Is1.std():+.2f} σ_exp")
print(f"  [I2] cos*cos mean ± sigma     : {Is2.mean():.5f} ± {Is2.std():.5f}")
print(f"       distance to 1/3          : {(Is2.mean()-1/3)/Is2.std():+.2f} σ_exp")

# Derived r values if identities exact:
# Koide identity: r^2 = 2(3Q - 1). So r_up^2 + r_down^2 = 2(3(Q_up+Q_down) - 2) = 6√(5/2)-4
r2sum_pred = 6*np.sqrt(5/2) - 4
print(f"\n--- Consequences of [I1] ---")
print(f"  r_up² + r_down² = 6√(5/2) - 4 = {r2sum_pred:.5f}")
print(f"  observed        = {ru**2 + rd**2:.5f}  (rel err {(ru**2+rd**2-r2sum_pred)/r2sum_pred*100:+.3f}%)")

print("\n--- Bridge anchor (from Why_137, McLean) ---")
# The bottom quark is predicted at 4.607 GeV from the bridge half-gap (sin pi/10)
# This anchors the absolute scale for the down-type circulant.
m_b_bridge = 4.607  # GeV, from Why_137 (0.04% match to 1S-kinetic average 4.605 GeV)
print(f"  m_b (bridge half-gap) = {m_b_bridge:.3f} GeV")
print(f"  m_b (PDG MSbar)       = {mb:.3f} GeV")
print(f"  m_b (1S+kinetic avg)  = 4.605 ± 0.018 GeV")

print("\n--- Combined with the two identities, the system reduces ---")
print("  Six PDG quark masses are replaced by:")
print("   - One absolute scale (m_b at the bridge midpoint)")
print("   - Q_up ∈ [lower, sqrt(5/2)]  (one dof, gives Q_down by [I1])")
print("   - cos δ_up × cos δ_down = 1/3  (two phases, one constraint)")
print("  Net: from 6 lattice parameters → 1 anchored scale + 3 dof + 2 constraints.")
print("  Further reduction requires independent derivations of Q_up (or Q_down) ")
print("  and δ_up (or δ_down) from the character table of 2I.")
