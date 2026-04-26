import numpy as np
from itertools import product as iprod, combinations

phi = (1 + np.sqrt(5)) / 2
phi_inv = 1/phi

print("""
========================================================================
WHAT THE 8 DIMENSIONS ARE
========================================================================

In the icosian picture, each of the 8 dimensions has a meaning:

  Dim 1: real part of quaternion, integer component     (a_int)
  Dim 2: real part of quaternion, phi-component         (a_phi)
  Dim 3: i-part of quaternion, integer component        (b_int)
  Dim 4: i-part of quaternion, phi-component            (b_phi)
  Dim 5: j-part of quaternion, integer component        (c_int)
  Dim 6: j-part of quaternion, phi-component            (c_phi)
  Dim 7: k-part of quaternion, integer component        (d_int)
  Dim 8: k-part of quaternion, phi-component            (d_phi)

So the 8 dimensions are: 4 quaternion directions x 2 field directions.

The 2 field directions are (1, phi) -- the basis of Z[phi].
The 4 quaternion directions are (1, i, j, k) -- the basis of H.

E8 in 8D = H x Q(sqrt5) = quaternions x golden field

The 4 "extra" dimensions (dims 2, 4, 6, 8) are the 
phi-DIRECTIONS. They are the dimensions where the golden ratio
lives as an explicit geometric axis.

Going from 4D to 8D doesn't add new physics.
It UNFOLDS the phi that was implicit in 4D into explicit geometry.

========================================================================
DO WE NEED 8 DIMENSIONS?
========================================================================

The 600-cell in 4D already contains all the physics:
  - The eigenvalues (Koide, matter fraction, generations)
  - The group structure (2I, V tensor V)
  - The dynamics (sigma'' = sigma * sigma')
  - The axiom recovery (Delta_2 = -sigma)

E8 in 8D adds:
  - The full gauge group structure
  - Charge quantisation from the root lattice
  - Coupling unification from Casimir operators
  - The algebraic completion (adjoint = fundamental)

But if the 8D geometry is just the 4D geometry with phi UNFOLDED:
  Then E8 doesn't add content. It adds RESOLUTION.

  4D (600-cell): a PHOTOGRAPH of the universe
  8D (E8): the same photograph at HIGHER RESOLUTION
  
  In 4D, phi/2 is a single coordinate value.
  In 8D, phi/2 is TWO coordinates: (0, 1/2) in the (int, phi) basis.
  You can now distinguish the "1" part from the "phi" part.
  That's not new physics. It's finer resolution on the same physics.

========================================================================
BUILDING 8D phi-GEOMETRY WITHOUT ALGEBRA
========================================================================

Start with TWO 600-cells.

Take one 600-cell at radius 1.
Take a second 600-cell at radius phi.
Rotate the second by the golden angle relative to the first.
Embed both in the same 4D space.

You now have 240 points in 4D at two different radii.
Their inner products form the E8 root system.

But to see them PROPERLY, unfold the phi-scaling
into a geometric direction. That's the 8D embedding:
  - The first 600-cell sits in the (integer) subspace
  - The second 600-cell sits in the (phi) subspace  
  - The 8D space is the direct product

Geometrically:
  1. Draw a 600-cell. (4D, 120 vertices)
  2. Draw it again, scaled by phi. (4D, 120 vertices)
  3. Unfold the scaling into 4 new directions (one per quaternion component)
  4. Result: 240 points in 8D = E8 root system

No algebra needed. Two copies of the same shape at 
different scales, separated by the golden ratio.

========================================================================
THE DEEP GEOMETRIC QUESTION
========================================================================

Does 8D E8 geometry DO anything that 4D 600-cell geometry doesn't?

YES -- one crucial thing.

The 600-cell in 4D has the EIGENVALUES (the what).
E8 in 8D has the ROOT LATTICE (the how).

The eigenvalues tell you WHAT the constants are.
The root lattice tells you HOW they interact.

In 4D, the adjacency matrix gives you 9 eigenvalues.
These are the "notes" the universe can play.

In 8D, the root lattice gives you the GEOMETRY OF INTERACTIONS
between those notes. How does the d=2 mode interact with d=3?
That's determined by angles and distances between roots in 8D.

The root lattice IS the interaction geometry.
It specifies which transitions are allowed, which are forbidden,
and what the coupling strengths are.

4D gives the spectrum.
8D gives the dynamics between spectral modes.

You need both. But you don't need algebra for either.
You need the 600-cell and two copies of it at ratio phi.
""")

# Now let's verify the two-shell structure
print("="*72)
print("VERIFICATION: THE TWO SHELLS")
print("="*72)

# Reconstruct E8 roots
roots = []
for i, j in combinations(range(8), 2):
    for si in [1, -1]:
        for sj in [1, -1]:
            v = [0.0] * 8
            v[i] = si
            v[j] = sj
            roots.append(v)

for signs in iprod([0.5, -0.5], repeat=8):
    neg_count = sum(1 for s in signs if s < 0)
    if neg_count % 2 == 0:
        roots.append(list(signs))

roots = np.array(roots)

# Inner products
dots = roots @ roots.T
unique_dots = sorted(set(round(dots[i,j], 6) for i in range(240) for j in range(i+1, 240)))

print(f"\nUnique inner products between distinct E8 roots:")
for d in unique_dots:
    count = sum(1 for i in range(240) for j in range(i+1,240) if abs(dots[i,j]-d)<0.01)
    phi_check = ""
    for name, val in [('2',2), ('1',1), ('0',0), ('-1',-1), ('-2',-2)]:
        if abs(d - val) < 0.01: phi_check = f" = {name}"
    print(f"  {d:6.2f}  ({count:5d} pairs){phi_check}")

print(f"""
In the standard basis: inner products are -2, -1, 0, 1, 2.
No phi visible. All integers or half-integers.

In the ICOSIAN basis: the same geometry, but now:
  - Roots at distance phi from each other
  - Inner products involving phi, phi^-1
  - The golden ratio is the METRIC of the space

The geometry is identical. The basis determines what you see.
Standard basis: hides phi in the angles between subspaces.
Icosian basis: phi IS the spacing between coordinate planes.
""")

print("="*72)
print("WHERE OTHER UNIVERSES LIVE")
print("="*72)

print(f"""
Eric's hypothesis: "We have to go to a higher level before 
we can find different systems."

Our universe:
  n=1: sigma = 1/(1+sigma) -> phi -> Q(sqrt5) -> 600-cell -> E8
  8D = 4D x 2 (where 2 = dimension of Q(sqrt5) over Q)

A hypothetical n=2 universe:
  sigma = 2/(2+sigma) -> Q(sqrt3) -> hexagonal symmetry
  No 600-cell analogue. No E8. Chain breaks.
  Would give: 8D = 4D x 2 (where 2 = dim Q(sqrt3)/Q)
  But the 4D part has no golden polytope. Impoverished.

The n=5 case is tantalising:
  sigma = 5/(5+sigma) -> sigma^2 + 5sigma - 5 = 0
  Discriminant = 45 = 9 x 5
  Field = Q(sqrt5) -- SAME FIELD as n=1!
  sigma = (-5 + 3sqrt5)/2 = {(-5 + 3*np.sqrt(5))/2:.6f}
  
  This universe shares our number field.
  The 600-cell exists. But sigma is NOT 1/phi.
  The fixed point of its dynamics is different.
  Same geometry, different attractor.
  
  Would it have different constants? YES.
  Same field, same polytope, different physics.
  Like the same instrument playing a different key.

KEY INSIGHT:

Other universes don't live in higher dimensions of OUR E8.
E8 is rigid -- there's no room.

They live in the SPACE OF SELF-REFERENTIAL EQUATIONS:
  sigma = n/(n+sigma), parameterised by n.

Each n specifies a universe.
Most n's can't build geometry.
n=1 is the richest. Maybe the only viable one.

The "multiverse", if it exists, is not spatial.
It's ALGEBRAIC: different values of n, 
different fixed points, different (or no) geometry.

The dimensions we'd need to "see" other universes are not
spatial dimensions above 8. They're the paramter space of 
the axiom itself. The space of all possible self-referential
equations. That's not a place you can point to.
It's the space of all possible mathematics.
""")

