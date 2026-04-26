#!/usr/bin/env python3
"""
OMML Injector for Solving Alpha V5.

Replaces each [[EQ:name]] placeholder paragraph with a properly structured
<m:oMathPara><m:oMath>...</m:oMath></m:oMathPara> containing hand-crafted
stacked OMML with Cambria Math font on every run.

Renders correctly in Word, LibreOffice, and Google Docs.
"""

import re
import sys
from pathlib import Path

# ===== OMML building blocks =====
# Every run carries explicit Cambria Math font + italic-off for upright style.

MATH_FONT_PR_PLAIN = (
    '<m:rPr><m:sty m:val="p"/></m:rPr>'
    '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    '<w:sz w:val="26"/></w:rPr>'
)
MATH_FONT_PR_ITALIC = (
    '<m:rPr><m:sty m:val="i"/></m:rPr>'
    '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    '<w:i/><w:sz w:val="26"/></w:rPr>'
)
# ctrlPr contains only <w:rPr>, not <m:rPr>
CTRL_RPR = (
    '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
    '<w:i/><w:sz w:val="26"/></w:rPr>'
)


def r(text, italic=False, preserve=False):
    """A math run. Default = upright (numbers/operators)."""
    props = MATH_FONT_PR_ITALIC if italic else MATH_FONT_PR_PLAIN
    space = ' xml:space="preserve"' if preserve or (text and text[0] in ' \t') or (text and text[-1] in ' \t') else ''
    return f'<m:r>{props}<m:t{space}>{text}</m:t></m:r>'


def ri(text, preserve=False):
    """A math run in italic (for variables like φ, α, c, p)."""
    return r(text, italic=True, preserve=preserve)


def frac(num, den):
    """Stacked fraction."""
    return f'<m:f><m:fPr><m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:fPr><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'


def sup(base, exp):
    """Superscript."""
    return f'<m:sSup><m:sSupPr><m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:sSupPr><m:e>{base}</m:e><m:sup>{exp}</m:sup></m:sSup>'


def sub(base, subscript):
    """Subscript."""
    return f'<m:sSub><m:sSubPr><m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:sSubPr><m:e>{base}</m:e><m:sub>{subscript}</m:sub></m:sSub>'


def rad(inner, degree=None):
    """Square root (or nth root if degree given)."""
    if degree is None:
        return f'<m:rad><m:radPr><m:degHide m:val="1"/><m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:radPr><m:deg/><m:e>{inner}</m:e></m:rad>'
    else:
        return f'<m:rad><m:radPr><m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:radPr><m:deg>{degree}</m:deg><m:e>{inner}</m:e></m:rad>'


def d(open_c, close_c, inner):
    """Delimiter (parens, brackets)."""
    return (f'<m:d><m:dPr><m:begChr m:val="{open_c}"/><m:endChr m:val="{close_c}"/>'
            f'<m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:dPr><m:e>{inner}</m:e></m:d>')


def nary(op, lim_low, lim_high, body, limloc="undOvr"):
    """N-ary operator (Σ, Π, etc). limloc: 'undOvr' (under/over) or 'subSup'."""
    sub_part = f'<m:sub>{lim_low}</m:sub>' if lim_low else '<m:sub/>'
    sup_part = f'<m:sup>{lim_high}</m:sup>' if lim_high else '<m:sup/>'
    return (f'<m:nary><m:naryPr><m:chr m:val="{op}"/><m:limLoc m:val="{limloc}"/>'
            f'<m:subHide m:val="{"1" if not lim_low else "0"}"/>'
            f'<m:supHide m:val="{"1" if not lim_high else "0"}"/>'
            f'<m:ctrlPr>{CTRL_RPR}</m:ctrlPr></m:naryPr>'
            f'{sub_part}{sup_part}<m:e>{body}</m:e></m:nary>')


# Convenience: φ^n
def phi_n(n):
    return sup(ri('φ'), r(str(n)))


# ===== Equation definitions =====

EQS = {}

# 1. Partition: 1/φ + 1/φ² = 1
EQS['partition'] = (
    frac(r('1'), ri('φ'))
    + r(' + ', preserve=True)
    + frac(r('1'), phi_n(2))
    + r(' = 1', preserve=True)
)

# bridge_partition (same as partition)
EQS['bridge_partition'] = EQS['partition']

# 2. Pentagon: α⁻¹ = 360/φ² − 2/φ³ + 1/(3⁵φ⁵) + 1/(7⁷φ⁷)
EQS['pentagon'] = (
    sup(ri('α'), r('−1'))
    + r(' = ', preserve=True)
    + frac(r('360'), phi_n(2))
    + r(' − ', preserve=True)
    + frac(r('2'), phi_n(3))
    + r(' + ', preserve=True)
    + frac(r('1'), sup(r('3'), r('5')) + phi_n(5))
    + r(' + ', preserve=True)
    + frac(r('1'), sup(r('7'), r('7')) + phi_n(7))
)

# 3. Zeta-rung: α⁻¹ = 360/φ² − 2/φ³ + 2ζ(3)/(360 φ⁶) − 16ζ(5)/(360² φ¹⁰)
EQS['zeta_rung'] = (
    sup(ri('α'), r('−1'))
    + r(' = ', preserve=True)
    + frac(r('360'), phi_n(2))
    + r(' − ', preserve=True)
    + frac(r('2'), phi_n(3))
    + r(' + ', preserve=True)
    + frac(r('2 ζ(3)'), r('360 ') + phi_n(6))
    + r(' − ', preserve=True)
    + frac(r('16 ζ(5)'), sup(r('360'), r('2')) + r(' ') + phi_n(10))
)

# 4. Bridge identity: 27 ζ(3) / (20 φ) = 1.00293
EQS['bridge_identity'] = (
    frac(r('27 ζ(3)'), r('20 ') + ri('φ'))
    + r(' = 1.002 93', preserve=True)
)

# 5. μ₇ = Tr(A⁷)/1440 = 50 400 = 2⁵ · 3² · 5² · 7
EQS['mu7'] = (
    sub(ri('μ'), r('7'))
    + r(' = ', preserve=True)
    + frac(r('Tr') + d('(', ')', sup(ri('A'), r('7'))), r('1440'))
    + r(' = 50 400 = ', preserve=True)
    + sup(r('2'), r('5')) + r(' · ', preserve=True)
    + sup(r('3'), r('2')) + r(' · ', preserve=True)
    + sup(r('5'), r('2')) + r(' · 7', preserve=True)
)

# 6. Generic four-term: α⁻¹ = c₁/φ^p₁ + c₂/φ^p₂ + c₃/φ^p₃ + c₄/φ^p₄
def term_ci_over_phi_pi(i):
    return frac(
        sub(ri('c'), r(str(i))),
        sup(ri('φ'), sub(ri('p'), r(str(i))))
    )

EQS['generic_four'] = (
    sup(ri('α'), r('−1'))
    + r(' = ', preserve=True)
    + term_ci_over_phi_pi(1)
    + r(' + ', preserve=True)
    + term_ci_over_phi_pi(2)
    + r(' + ', preserve=True)
    + term_ci_over_phi_pi(3)
    + r(' + ', preserve=True)
    + term_ci_over_phi_pi(4)
)

# 7. Complete series: α⁻¹ = 360/φ² − 2/φ³ + (1/φ²) Σ_{k=1}^{∞} (−1)^(k+1) 2^(k²) ζ(2k+1) w^k
EQS['complete_series'] = (
    sup(ri('α'), r('−1'))
    + r(' = ', preserve=True)
    + frac(r('360'), phi_n(2))
    + r(' − ', preserve=True)
    + frac(r('2'), phi_n(3))
    + r(' + ', preserve=True)
    + frac(r('1'), phi_n(2))
    + r(' · ', preserve=True)
    + nary('∑', ri('k') + r('=1'), r('∞'),
           sup(r('(−1)'), ri('k') + r('+1'))
           + r(' · ', preserve=True)
           + sup(r('2'), sup(ri('k'), r('2')))
           + r(' · ζ', preserve=True)
           + d('(', ')', r('2') + ri('k') + r('+1'))
           + r(' · ', preserve=True)
           + sup(ri('w'), ri('k')))
)

# 8. rung7: +C₇ ζ(7) / (360³ φ¹⁴)
EQS['rung7'] = (
    r('+ ', preserve=True)
    + frac(
        sub(ri('C'), r('7')) + r(' · ζ(7)'),
        sup(r('360'), r('3')) + r(' ') + phi_n(14)
    )
)

# 9. bridge_line: depth = α⁻¹ R + φ⁻²
EQS['bridge_line'] = (
    r('depth', italic=True) + r(' = ', preserve=True)
    + sup(ri('α'), r('−1'))
    + r(' · ', preserve=True)
    + ri('R')
    + r(' + ', preserve=True)
    + sup(ri('φ'), r('−2'))
)

# 10. alpha_from_depth: α⁻¹ = (depth − φ⁻²) / R
EQS['alpha_from_depth'] = (
    sup(ri('α'), r('−1'))
    + r(' = ', preserve=True)
    + frac(
        r('depth', italic=True) + r(' − ', preserve=True) + sup(ri('φ'), r('−2')),
        ri('R')
    )
)

# 11. omega_lambda: Ω_Λ = (8π/3) × 10^(−3 φ⁻²)
EQS['omega_lambda'] = (
    sub(ri('Ω'), ri('Λ'))
    + r(' = ', preserve=True)
    + frac(r('8π'), r('3'))
    + r(' × ', preserve=True)
    + sup(r('10'), r('−3 ') + sup(ri('φ'), r('−2')))
)

# 12. dirichlet: L(1, χ₅) / log(φ) = 2h/√5 = 2/√5
EQS['dirichlet'] = (
    frac(
        ri('L') + r('(1, ') + sub(ri('χ'), r('5')) + r(')'),
        r('log') + d('(', ')', ri('φ'))
    )
    + r(' = ', preserve=True)
    + frac(r('2') + ri('h'), rad(r('5')))
    + r(' = ', preserve=True)
    + frac(r('2'), rad(r('5')))
)


# ===== Replacement logic =====

def build_equation_paragraph(omath_content, indent='      '):
    """Build a full <w:p> containing centered oMathPara > oMath."""
    return (
        f'{indent}<w:p>\n'
        f'{indent}  <w:pPr>\n'
        f'{indent}    <w:spacing w:before="360" w:after="360"/>\n'
        f'{indent}    <w:jc w:val="center"/>\n'
        f'{indent}  </w:pPr>\n'
        f'{indent}  <m:oMathPara>\n'
        f'{indent}    <m:oMathParaPr>\n'
        f'{indent}      <m:jc m:val="center"/>\n'
        f'{indent}    </m:oMathParaPr>\n'
        f'{indent}    <m:oMath>{omath_content}</m:oMath>\n'
        f'{indent}  </m:oMathPara>\n'
        f'{indent}</w:p>'
    )


def inject_omml(doc_xml_path):
    text = Path(doc_xml_path).read_text(encoding='utf-8')

    # Find every paragraph that contains a [[EQ:name]] placeholder and replace the whole <w:p>.
    # Pattern: <w:p>...contains [[EQ:NAME]]...</w:p>
    # We do this by iterating: find each [[EQ:X]] marker, then find the enclosing <w:p>.

    count = 0
    missing = []
    while True:
        m = re.search(r'\[\[EQ:([A-Za-z0-9_]+)\]\]', text)
        if not m:
            break
        name = m.group(1)
        # Find enclosing <w:p>
        p_start = text.rfind('<w:p>', 0, m.start())
        p_start_alt = text.rfind('<w:p ', 0, m.start())
        if p_start_alt > p_start:
            p_start = p_start_alt
        if p_start < 0:
            raise ValueError(f"Can't find enclosing <w:p> for [[EQ:{name}]]")
        p_end = text.index('</w:p>', m.end()) + len('</w:p>')

        if name not in EQS:
            missing.append(name)
            # Mark it so the loop can proceed
            text = text[:m.start()] + f'MISSING_EQ_{name}' + text[m.end():]
            continue

        # Determine indent from the line containing <w:p>
        line_start = text.rfind('\n', 0, p_start) + 1
        indent = text[line_start:p_start]

        new_paragraph = build_equation_paragraph(EQS[name], indent=indent)
        text = text[:p_start] + new_paragraph + text[p_end:]
        count += 1

    if missing:
        print(f"WARNING: missing definitions for: {missing}")

    Path(doc_xml_path).write_text(text, encoding='utf-8')
    return count


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'v5_unpacked/word/document.xml'
    n = inject_omml(target)
    print(f"Injected {n} OMML equations into {target}")
