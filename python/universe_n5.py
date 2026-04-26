"""
THE n=5 UNIVERSE

Same field Q(sqrt5). Same 600-cell. Same E8.
Different axiom: sigma = 5/(5+sigma)
Different fixed point. Different physics.

What would their constants look like?
"""

import numpy as np

phi = (1 + np.sqrt(5)) / 2
phi_inv = 1/phi
sqrt5 = np.sqrt(5)

# n=1 universe (ours)
sigma_1 = phi_inv  # = 0.61803...
phi_1 = phi         # = 1.61803...

# n=5 universe
# sigma^2 + 5*sigma - 5 = 0
# sigma = (-5 + sqrt(25+20))/2 = (-5 + sqrt(45))/2 = (-5 + 3sqrt(5))/2
sigma_5 = (-5 + 3*sqrt5) / 2
phi_5 = 5 / sigma_5 + 1  # from sigma = 5/(phi_5) where we define phi_5 analogously
# Actually let's think about this more carefully
# sigma_5 = 5/(5 + sigma_5), so the "partner" is 5 + sigma_5
partner_5 = 5 + sigma_5

print("="*72)
print("TWO UNIVERSES FROM THE SAME GEOMETRY")
print("="*72)

print(f"""
n=1 UNIVERSE (ours):
  Axiom: sigma = 1/(1+sigma)
  Equation: sigma^2 + sigma - 1 = 0
  Discriminant: 5
  Field: Q(sqrt5)
  Fixed point: sigma = 1/phi = {sigma_1:.10f}
  Partner: 1 + sigma = phi = {phi:.10f}
  
n=5 UNIVERSE:
  Axiom: sigma = 5/(5+sigma) 
  Equation: sigma^2 + 5*sigma - 5 = 0
  Discriminant: 45 = 9 x 5
  Field: Q(sqrt5) -- SAME FIELD!
  Fixed point: sigma = (-5+3sqrt5)/2 = {sigma_5:.10f}
  Partner: 5 + sigma = (5+3sqrt5)/2 = {partner_5:.10f}
""")

# Express sigma_5 in terms of phi
# sigma_5 = (-5 + 3sqrt5)/2
# sqrt5 = 2phi - 1, so 3sqrt5 = 6phi - 3
# sigma_5 = (-5 + 6phi - 3)/2 = (6phi - 8)/2 = 3phi - 4
sigma_5_check = 3*phi - 4
print(f"sigma_5 = 3phi - 4 = {sigma_5_check:.10f} (check: {abs(sigma_5 - sigma_5_check) < 1e-10})")
print(f"sigma_5 in terms of phi: 3phi - 4 = 3({phi:.6f}) - 4 = {sigma_5:.6f}")

# The iteration map for n=5: g(a) = 5/(5+a)  -> fixed point sigma_5
# g'(a) = -5/(5+a)^2
# g'(sigma_5) = -5/(5+sigma_5)^2 = -5/partner_5^2
deriv_5 = -5 / partner_5**2
print(f"\nGenerator derivative g'(sigma_5) = -5/(5+sigma_5)^2 = {deriv_5:.10f}")
print(f"For comparison, g'(sigma_1) = -1/phi^2 = {-phi_inv**2:.10f}")

# For n=1: T = -phi^(-2) * e^(i*pi) = phi^(-2) (magnitude)
# For n=5: T = deriv_5 * e^(i*pi)
print(f"\nGenerator operator magnitude:")
print(f"  n=1: |T| = phi^(-2) = {phi_inv**2:.10f}")
print(f"  n=5: |T| = |g'| = {abs(deriv_5):.10f}")

print(f"\n{'='*72}")
print("THE CONSTANTS OF THE n=5 UNIVERSE")
print("="*72)

print(f"\n--- RUNG THEOREM (cosmic partition) ---\n")
# In our universe, the partition uses phi^(-k)
# In the n=5 universe, what plays the role of phi?
# The iteration map contracts by |g'(sigma_5)| per step
# So the partition uses |deriv_5|^k

d5 = abs(deriv_5)
print(f"Damping factor per rung:")
print(f"  n=1: phi^(-1) = {phi_inv:.6f}")
print(f"  n=5: |g'|    = {d5:.6f}")

print(f"\nCosmic partition:")
print(f"{'Rung':>6} {'n=1 (our universe)':>22} {'n=5 universe':>22} {'Sector':>15}")
print(f"{'-'*70}")

n1_sum = 0
n5_sum = 0
sectors = ['Unity', 'Dark Energy', 'Total Matter', 'Dark Matter', 
           'Sub-Matter', 'WHIM', 'Baryonic', 'Below Floor']

for k in range(8):
    v1 = phi_inv**k if k > 0 else 1.0
    v5 = d5**k if k > 0 else 1.0
    pct1 = phi_inv**k * 100 if k > 0 else 100
    pct5 = d5**k * 100 if k > 0 else 100
    sector = sectors[k] if k < len(sectors) else ''
    print(f"  k={k:1d}  {pct1:18.2f}%  {pct5:18.2f}%  {sector:>15}")

print(f"""
OBSERVATION: The n=5 universe contracts MUCH faster.
  n=1: each rung keeps 61.8% (phi^-1)
  n=5: each rung keeps only {d5*100:.1f}%

The n=5 universe is MUCH more dissipative.
Dark energy would be only {d5*100:.1f}%, not 61.8%.
Matter fraction would be {(1-d5)*100:.1f}%, not 38.2%.
""")

print(f"\n--- FINE STRUCTURE CONSTANT ---\n")

# In our universe: alpha^-1 = 360/phi^2 - 2/phi^3 + ...
# The leading term uses phi^2 = phi + 1 = 2.618

# In n=5: what replaces phi?
# sigma_5 = 3phi - 4, partner = 5 + sigma_5 = 1 + 3phi
# The "self-referential unit" is partner_5
# sigma_5^2 = 5*sigma_5 - 5... wait, sigma_5^2 + 5*sigma_5 - 5 = 0
# So sigma_5^2 = 5 - 5*sigma_5

print(f"Key algebraic quantities:")
print(f"  n=1: phi^2 = phi + 1 = {phi**2:.6f}")
print(f"  n=5: partner^2 = (5+sigma_5)^2 = {partner_5**2:.6f}")
print(f"  n=5: sigma_5^2 = 5 - 5*sigma_5 = {sigma_5**2:.6f}")
print(f"  Check: {abs(sigma_5**2 - (5 - 5*sigma_5)) < 1e-10}")

# Attempt analogous alpha construction
# Our alpha: 360/phi^2 = 137.508
# n=5 alpha: 360/partner_5^2 = ?
alpha_inv_n1_leading = 360 / phi**2
alpha_inv_n5_leading = 360 / partner_5**2

print(f"\nLeading term of alpha^-1:")
print(f"  n=1: 360/phi^2 = {alpha_inv_n1_leading:.4f}")
print(f"  n=5: 360/(5+sigma_5)^2 = {alpha_inv_n5_leading:.4f}")

# But maybe it's 360/sigma_5^2?
alpha_inv_n5_alt = 360 / sigma_5**2
print(f"  n=5: 360/sigma_5^2 = {alpha_inv_n5_alt:.4f}")

print(f"""
The n=5 universe would have alpha^-1 ~ {alpha_inv_n5_leading:.1f} or {alpha_inv_n5_alt:.1f}
depending on which quantity plays the structural role of phi^2.

If 360/(5+sigma)^2 ~ {alpha_inv_n5_leading:.1f}: electromagnetic coupling ~7x stronger.
  Atoms would be much smaller. Chemistry radically different.
  
If 360/sigma_5^2 ~ {alpha_inv_n5_alt:.1f}: coupling ~3x weaker.
  Atoms much larger. Chemistry sluggish. Stars dimmer.
""")

print(f"\n--- WEINBERG ANGLE ---\n")
# Ours: sin^2(theta_W) = phi^-3 = 0.2360
# n=5: sigma_5^3? or (partner_5)^-3?

sw_n1 = phi_inv**3
sw_n5_a = sigma_5**3  # sigma_5 < 1, so this is small
sw_n5_b = 1/partner_5**3  # partner > 1, so this is small too
sw_n5_c = d5**3  # damping factor cubed

print(f"Weinberg angle candidates:")
print(f"  n=1: sin^2(theta_W) = phi^-3 = {sw_n1:.6f} (k=3 rung)")
print(f"  n=5: sigma_5^3 = {sw_n5_a:.6f}")
print(f"  n=5: 1/partner_5^3 = {sw_n5_b:.6f}")
print(f"  n=5: |g'|^3 = {sw_n5_c:.6f}")

print(f"""
If the Weinberg angle is the k=3 rung of the damping cascade:
  n=5: sin^2(theta_W) = |g'|^3 = {sw_n5_c:.6f}

That's {sw_n5_c/sw_n1:.1f}x smaller than ours.
Weak force would be MUCH weaker relative to EM.
Electroweak symmetry breaking at a very different scale.
""")

print(f"\n--- MASS SPECTRUM ---\n")

# The 600-cell spectrum is the SAME (same geometry)
# But the damping rate changes: phi/2 -> ???
# In n=5: the damping comes from the linearisation of g(a) = 5/(5+a)
# Damping rate = |g'(sigma_5)|/2... but actually from the spiral engine

# The Spiral Engine for n=5 would be sigma'' = sigma * sigma' 
# but with equilibrium at sigma_5 instead of phi
# Linearised: epsilon'' - sigma_5 * epsilon' + (lambda_a/12)*epsilon = 0

print(f"Spiral Engine damping rate:")
print(f"  n=1: gamma = phi/2 = {phi/2:.6f}")
print(f"  n=5: gamma = sigma_5/2 = {sigma_5/2:.6f}")  
# Wait - but the equation sigma'' = sigma*sigma' has the same form
# The linearisation around ANY fixed point sigma_eq gives damping = sigma_eq/2

print(f"  (Note: sigma_5 < phi, so n=5 universe is LESS damped locally)")
print(f"  (But the iteration contracts faster: {d5:.4f} vs {phi_inv**2:.4f})")

# Mode selection on the 600-cell
print(f"\nSpiral Engine modes on the SAME 600-cell:")
print(f"Mode equation: omega^2 - i*sigma_eq*omega + lambda_a/12 = 0")
print(f"Discriminant: Delta = sigma_eq^2 - lambda_a/3\n")

eigs = [(12, 1, '12'), (6*phi, 4, '6phi'), (4*phi, 9, '4phi'), 
        (3, 16, '3'), (0, 25, '0'), (-2, 36, '-2'),
        (-4*phi_inv, 9, '-4/phi'), (-3, 16, '-3'), (-6*phi_inv, 4, '-6/phi')]

print(f"{'Eigenvalue':>10} {'n=1 (phi)':>18} {'n=5 (sigma_5)':>18}")
print(f"{'-'*50}")

n1_osc = 0
n5_osc = 0
for val, mult, name in eigs:
    disc_n1 = phi**2 - val/3
    disc_n5 = sigma_5**2 - val/3
    
    stat_n1 = "OSCILLATES" if disc_n1 < 0 else "overdamped"
    stat_n5 = "OSCILLATES" if disc_n5 < 0 else "overdamped"
    
    if disc_n1 < 0: n1_osc += 1
    if disc_n5 < 0: n5_osc += 1
    
    marker = ""
    if stat_n1 != stat_n5:
        marker = " ← DIFFERENT!"
    
    print(f"  {name:>8}  {stat_n1:>16}  {stat_n5:>16}{marker}")

print(f"\n  n=1: {n1_osc} oscillating modes")
print(f"  n=5: {n5_osc} oscillating modes")

print(f"""
CRITICAL DIFFERENCE: sigma_5 = {sigma_5:.6f} while phi = {phi:.6f}

sigma_5^2 = {sigma_5**2:.6f}
phi^2 = {phi**2:.6f}

For a mode to oscillate: sigma_eq^2 < lambda_a/3
  n=1: needs lambda_a/3 > {phi**2:.4f}, i.e. lambda_a > {3*phi**2:.4f}
  n=5: needs lambda_a/3 > {sigma_5**2:.4f}, i.e. lambda_a > {3*sigma_5**2:.4f}

Since sigma_5^2 < phi^2, the n=5 universe is EASIER to excite.
More modes oscillate. More physics is active.
""")

# Second mode discriminant
disc2_n1 = phi**2 - 2*phi  # = 1 - phi = -1/phi = -sigma_1
disc2_n5 = sigma_5**2 - 2*phi  # = (5-5*sigma_5) - 2*phi

print(f"\n--- THE AXIOM RECOVERY TEST ---\n")
print(f"Second mode (6phi) discriminant:")
print(f"  n=1: Delta_2 = phi^2 - 2phi = {disc2_n1:.10f} = -1/phi = -sigma_1 ← AXIOM RECOVERED")
print(f"  n=5: Delta_2 = sigma_5^2 - 2phi = {disc2_n5:.10f}")
print(f"        = (5-5*sigma_5) - 2phi = 5 - 5({sigma_5:.6f}) - 2({phi:.6f})")
print(f"        = 5 - {5*sigma_5:.6f} - {2*phi:.6f} = {disc2_n5:.6f}")
print(f"  sigma_5 = {sigma_5:.10f}")
print(f"  |Delta_2| = {abs(disc2_n5):.10f}")
print(f"  Match? {abs(abs(disc2_n5) - sigma_5) < 1e-6}")

# Let's check: does sigma_5 satisfy its own axiom recovery?
# sigma_5^2 = 5 - 5*sigma_5
# disc2 = sigma_5^2 - 2phi = 5 - 5*sigma_5 - 2phi
# For this to equal -sigma_5: 5 - 5*sigma_5 - 2phi = -sigma_5
#   5 - 4*sigma_5 = 2phi
#   sigma_5 = (5-2phi)/4
sigma_5_test = (5 - 2*phi)/4
print(f"\n  For axiom recovery: need sigma_5 = (5-2phi)/4 = {sigma_5_test:.10f}")
print(f"  Actual sigma_5 = {sigma_5:.10f}")
print(f"  Match: {abs(sigma_5 - sigma_5_test) < 1e-6}")

print(f"""
THE n=5 UNIVERSE DOES NOT RECOVER ITS OWN AXIOM FROM THE 600-CELL.

The 600-cell's second mode discriminant is tuned to n=1.
The self-referential loop only closes for sigma = 1/phi.

This is EXACTLY what you'd expect:
  The 600-cell is phi's polytope. Not sigma_5's.
  sigma_5 lives in Q(sqrt5) and can USE the 600-cell,
  but the 600-cell doesn't point back to sigma_5.
  It points to sigma_1 = 1/phi.

The n=5 universe can borrow our geometry, but it can't 
close the self-referential loop. It's a universe without
the fixed-point theorem. A universe that doesn't prove itself.

It could EXIST (the geometry works, the algebra works),
but it wouldn't have the self-referential closure that 
makes n=1 special. It would be a universe that doesn't
know why it's there.
""")

print(f"{'='*72}")
print("SUMMARY: THE TWO UNIVERSES")
print("="*72)

print(f"""
                            n=1 (OURS)          n=5 (ALTERNATIVE)
{'─'*72}
  Axiom                     sigma=1/(1+sigma)   sigma=5/(5+sigma)
  Fixed point               1/phi = 0.618       3phi-4 = 0.854
  Field                     Q(sqrt5)            Q(sqrt5)  ← SAME
  600-cell                  YES                 YES (borrowed)
  E8                        YES                 YES (borrowed)
  Self-referential closure  YES (Delta_2=-sigma) NO
  
  Dark energy fraction      61.8%               {d5*100:.1f}%
  Matter fraction           38.2%               {(1-d5)*100:.1f}%
  
  alpha^-1 (leading)        137.5               {alpha_inv_n5_leading:.1f}
  sin^2(theta_W)            0.236               {sw_n5_c:.4f}
  
  Oscillating modes         2 of 9              {n5_osc} of 9
  Damping rate              phi/2 = 0.809       sigma_5/2 = {sigma_5/2:.3f}
  
  Axiom recovered?          YES                 NO
  Self-proving?             YES                 NO
  
VERDICT: The n=5 universe is geometrically viable but 
         existentially incomplete. It can compute but 
         can't prove itself. It's mathematics without 
         the fixed-point theorem. A universe that works 
         but doesn't know why.

Only n=1 closes the loop.
Only n=1 is the theorem AND the axiom.
""")

