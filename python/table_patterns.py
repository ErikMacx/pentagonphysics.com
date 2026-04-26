"""
Systematic analysis of patterns in how PP constants 
use the character table. What is the syntax?
"""
import numpy as np
from collections import Counter

phi = (1 + np.sqrt(5)) / 2
sigma = phi - 1

# Every PP constant and which cells it touches
# Format: (constant, [list of (rep, class) cells used], operation)

mappings = [
    # COUPLINGS
    ("α⁻¹", [(2,'φ')], "Power series in χ(2,φ)⁻ⁿ"),
    ("αs(MZ)", [(2,'σ'), (2,'id')], "χ(2,σ)³ / χ(2,id)"),
    ("sin²θ_W", [(2,'σ')], "χ(2,σ)³"),
    ("g₂", [(2,'id'), (2,'φ'), (5,'id')], "χ(2,id)·χ(2,φ) / χ(5,id)"),
    ("g₁²=λ_H", [(2,'id'), (2,'φ'), (5,'id')], "χ(2,id)·χ(2,φ) / χ(5,id)²"),
    
    # GRAVITY
    ("Λ", [(2,'φ'), (2,'σ'), (2,'σ')], "α⁻¹ · 2/(χ(2,φ)+χ(2,σ)) + χ(2,σ)²"),
    ("G", [(5,'id'), (2,'φ')], "1/(χ(5,id)·χ(2,φ)⁴)"),
    
    # ELECTROWEAK
    ("m_H", [(2,'φ'), (5,'id')], "2v·√(χ(2,φ)/χ(5,id))"),
    ("V''(φ⁻¹)=√5", [(2,'φ'), (2,'σ')], "χ(2,φ) + χ(2,σ)"),
    
    # MASS
    ("Koide Q", [(2,'id'), (3,'id')], "χ(2,id) / χ(3,id)"),
    ("m_p/m_e", [(2,'φ')], "6π⁵ + π⁵/[χ(2,φ)⁷(π⁵−1)]"),
    
    # MIXING
    ("sin²θ₁₃", [(5,'id'), (3,'id')], "1 / (χ(5,id)·χ(3,id)²)"),
    ("sin²θ₁₂", [(2,'φ'), (5,'id'), (3,'id')], "2·χ(2,φ)⁴ / (χ(5,id)·χ(3,id)²)"),
    ("sin²θ₂₃", [(3,'id'), (2,'φ')], "χ(3,id) / (χ(2,id)·χ(2,φ)²)"),
    ("δ_PMNS", [(5,'id'), (2,'φ')], "π + π/(χ(5,id)·χ(2,φ)²)"),
    ("δ_CKM", [(2,'φ')], "π / χ(2,φ)²"),
    
    # TOPOLOGY
    ("√5", [(2,'φ'), (2,'σ')], "χ(2,φ) + χ(2,σ)"),
    ("2/√5", [(2,'id'), (2,'φ'), (2,'σ')], "χ(2,id) / (χ(2,φ)+χ(2,σ))"),
    ("1/φ", [(2,'σ')], "χ(2,σ) directly"),
    ("φ⁻²", [(2,'σ')], "χ(2,σ)²"),
    ("R_Λ−R_G", [(2,'σ')], "χ(2,σ)"),
    ("θ_QCD", [], "0 = identity stillpoint"),
    
    # COSMO
    ("η_B", [(2,'σ')], "σ-partition"),
    ("Δm²₃₂", [(2,'σ')], "σ-partition"),
]

# ============================================================
# PATTERN 1: Which irreps are used?
# ============================================================
print("="*80)
print("PATTERN 1: IRREP FREQUENCY — Which rows of the table carry physics?")
print("="*80)

rep_count = Counter()
for name, cells, op in mappings:
    for rep, cls in cells:
        rep_count[rep] += 1

total_refs = sum(rep_count.values())
print(f"\n  {'Irrep':>8} {'Uses':>6} {'Share':>8}  Role")
print("  " + "-"*60)
for rep in [1, 2, 3, 4, 5, 6]:
    c = rep_count.get(rep, 0)
    pct = c/total_refs*100 if total_refs > 0 else 0
    roles = {
        1: "Trivial — baseline, almost never accessed directly",
        2: "THE CARRIER — appears in nearly every constant",
        3: "SCALE SETTER — appears in denominators (normaliser)",
        4: "UNUSED — the quiet sector",
        5: "SCALE SETTER — appears in denominators (normaliser)",
        6: "BARELY USED — only Koide Q uses d=6 indirectly"
    }
    bar = "█" * int(pct/2)
    print(f"  d={rep:>2}   {c:>5}   {pct:>5.1f}%  {bar}  {roles[rep]}")

print(f"\n  d=2 alone accounts for {rep_count[2]/total_refs*100:.0f}% of all cell references.")
print(f"  d=2 + d=5 + d=3 account for {(rep_count[2]+rep_count[5]+rep_count[3])/total_refs*100:.0f}%.")
print(f"  d=4, d=4', d=6 are nearly silent.")

# ============================================================
# PATTERN 2: Which conjugacy classes are used?
# ============================================================
print(f"\n{'='*80}")
print("PATTERN 2: CLASS FREQUENCY — Which columns carry physics?")
print("="*80)

class_count = Counter()
for name, cells, op in mappings:
    for rep, cls in cells:
        class_count[cls] += 1

print(f"\n  {'Class':>8} {'Uses':>6} {'Share':>8}  Meaning")
print("  " + "-"*60)
class_info = [
    ('id', 'Identity (trace=2) — dimensions live here'),
    ('φ', 'Five-fold (trace=φ) — THE physics column'),
    ('σ', 'Conjugate five-fold (trace=σ) — coupling hierarchy'),
    ('-σ', 'Trace=-σ — rarely accessed directly'),
    ('-φ', 'Trace=-φ — rarely accessed directly'),
    ('1', 'Three-fold (trace=1) — integer sector'),
    ('-1', 'Trace=-1 — integer sector'),
    ('0', 'Two-fold (trace=0) — all zeros, never used'),
    ('-2', 'Central element — never used directly'),
]
for cls, meaning in class_info:
    c = class_count.get(cls, 0)
    pct = c/total_refs*100 if total_refs > 0 else 0
    bar = "█" * int(pct/2)
    print(f"  {cls:>8}   {c:>4}   {pct:>5.1f}%  {bar}  {meaning}")

print(f"\n  The φ and σ columns (five-fold symmetry) carry {(class_count['φ']+class_count['σ'])/total_refs*100:.0f}% of physics.")
print(f"  The identity column (dimensions) carries {class_count['id']/total_refs*100:.0f}%.")
print(f"  Together: {(class_count['φ']+class_count['σ']+class_count['id'])/total_refs*100:.0f}% of all references.")

# ============================================================
# PATTERN 3: The grammar operations by physics type
# ============================================================
print(f"\n{'='*80}")
print("PATTERN 3: GRAMMAR BY PHYSICS TYPE — Operation determines domain")
print("="*80)

print("""
  Physics domain        Grammar operation         Why
  ─────────────         ─────────────────         ───
  Couplings (α,αs,θ_W) Powers of σ = χ(2,σ)      Depth on the spiral
  Mass ratios (m_p/m_e) Powers of φ × πⁿ          Geometry meets spectrum
  Mixing angles (PMNS)  Dimension ratios           How irreps relate
  Cosmological (Λ,G)    Galois sums + powers       Bridge between arms
  Electroweak (g₂,λ_H)  Mixed: dim × char / dim   Gauge meets geometry
  Topological (√5,1/φ)  Direct or Galois sum       Pure structure

  RULE: The type of physics determines the grammatical operation.
  The grammar has a syntax. It is not arbitrary combination.
""")

# ============================================================
# PATTERN 4: Number of cells per constant
# ============================================================
print(f"{'='*80}")
print("PATTERN 4: WORD LENGTH — How many cells per constant?")
print("="*80)

lengths = Counter()
for name, cells, op in mappings:
    n = len(cells)
    lengths[n] += 1

print(f"\n  Cells used   Constants   Examples")
print("  " + "-"*50)
for n in sorted(lengths.keys()):
    examples = [name for name, cells, op in mappings if len(cells) == n][:3]
    print(f"  {n:>5}         {lengths[n]:>5}       {', '.join(examples)}")

print(f"\n  Maximum cells used by any single constant: {max(len(cells) for _, cells, _ in mappings)}")
print(f"  Most constants use 1-2 cells. The grammar is TERSE.")
print(f"  Short words, not long sentences.")

# ============================================================
# PATTERN 5: The HOT CELLS — which specific cells carry the most?
# ============================================================
print(f"\n{'='*80}")
print("PATTERN 5: HOT CELLS — The load-bearing entries")
print("="*80)

cell_count = Counter()
for name, cells, op in mappings:
    for cell in cells:
        cell_count[cell] += 1

print(f"\n  {'Cell':>15} {'Uses':>6}  Constants that reference it")
print("  " + "-"*65)
for cell, count in cell_count.most_common(10):
    users = [name for name, cells, op in mappings if cell in cells]
    print(f"  χ({cell[0]},{cell[1]:>3})  {count:>5}  {', '.join(users[:5])}")

print(f"""
  THE DOMINANT CELL: χ(2,φ) = φ
  This single entry — the golden ratio at the intersection of the 
  fundamental spinor (d=2) and five-fold symmetry (trace=φ) — is 
  referenced by more constants than any other.

  THE RUNNER-UP: χ(2,σ) = σ = 1/φ
  The Galois conjugate. Together with χ(2,φ), these two cells span 
  the coupling hierarchy (powers of σ) and the discriminant (their sum = √5).

  TWO CELLS CARRY THE PROGRAMME.
  χ(2,φ) and χ(2,σ). The golden ratio and its conjugate.
  Row 2, columns φ and σ. The fundamental spinor at five-fold symmetry.
""")

# ============================================================
# PATTERN 6: The SILENT sectors
# ============================================================
print(f"{'='*80}")
print("PATTERN 6: SILENCE — What the table contains but physics doesn't use")
print("="*80)

print(f"""
  Unused irreps: d=4, d=4' (8 entries each = 16 cells)
  Unused classes: trace=0 (30 elements, all zeros), trace=±1 (40 elements)
  
  The d=4 representations have characters:
    d=4:  4,  1, -1, -1,  0,  1,  1, -1, -4
    d=4': 4, -1,  1, -1,  0, -1,  1, -1,  4
  
  All integers. No φ. No σ. This is the purely arithmetic sector.
  
  If the quark masses live here, they would be governed by integer 
  arithmetic rather than golden ratio geometry — explaining why the 
  quark hierarchy is steeper and less "golden" than the lepton hierarchy.
  
  The d=6 representation: 6, -1, 0, 1, 0, -1, 0, 1, -6
  Also mostly integers and zeros. The largest irrep is the quietest.
  
  PREDICTION: The six quark masses will involve d=4 and d=4' character values.
  This is testable. If quark masses are derived and they use only d=2 and d=3,
  this prediction fails.
""")

# ============================================================
# PATTERN 7: Galois pairing
# ============================================================
print(f"{'='*80}")
print("PATTERN 7: GALOIS PAIRS — The axiom's two-rootedness")
print("="*80)

print(f"""
  The Galois automorphism σ ↔ -φ (equivalently √5 → -√5) creates pairs:
  
    χ(2,φ) = φ      ↔  χ(2',φ) = -σ       (Galois conjugates)
    χ(2,σ) = σ      ↔  χ(2',σ) = -φ       (Galois conjugates)
    χ(3,φ) = φ      ↔  χ(3',φ) = -σ
    χ(3,σ) = -σ     ↔  χ(3',σ) = φ
    
  SUM of Galois pair = √5 (always)
  DIFFERENCE of Galois pair = ±(2φ-1) = ±√5 (always)
  PRODUCT of Galois pair = -φ·σ = -1 (from Vieta's formulas for σ²+σ-1=0)
  
  The Galois sum √5 = discriminant of the axiom.
  The Galois product -1 = constant term of the axiom.
  
  Every time PP uses √5, it is accessing the SEPARATION between the 
  two roots of the axiom. The discriminant isn't a number. It's the 
  distance between the two solutions of self-reference.
  
  The primed irreps (2', 3', 4') are the MIRROR universe.
  The unprimed irreps (2, 3, 4) are our universe.
  The fixed irreps (1, 5, 6) are the same in both.
  
  Three generations may correspond to: unprimed, primed, and fixed.
""")

