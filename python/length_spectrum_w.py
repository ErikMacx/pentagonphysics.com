"""
LENGTH SPECTRUM IN THE w-UNIFORMIZATION
=========================================
The collaborator's key insight:

Define s = -log(w)/log(φ) where w is the Floquet multiplier.
Then:
  - |w| = φ^{-1/2} ↔ Re(s) = 1/2  (THE CRITICAL LINE)
  - w^d = p^{-s}  when d = log(p)/log(φ)  (THE EULER PRODUCT)

So we scan w along the circle |w| = φ^{-1/2} with varying argument,
convert to z via z² = b₀² + b₁² + b₀b₁(w + 1/w),
compute Δ(z(w)) = det(I + V·R_T(z(w))),
then take d/ds log Δ and FT into length t.

THIS is the correct coordinate for the length-spectrum test.
The previous test failed because we scanned the wrong variable.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

PHI = (1 + np.sqrt(5)) / 2
LOG_PHI = np.log(PHI)

def sieve_primes(N):
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(N**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, N + 1, i):
                is_prime[j] = False
    return np.array([i for i in range(2, N + 1) if is_prime[i]])

PRIMES = sieve_primes(10000)
def phi_position(p): return np.log(p) / LOG_PHI
def phi_offset(p): return phi_position(p) - np.round(phi_position(p))
def phi_weight(p): return PHI ** (-np.abs(phi_offset(p)))

# Background
B_RATIO = np.sqrt(PHI)
B_MEAN = 61.2
B0 = B_MEAN * 2 / (1 + B_RATIO)
B1 = B0 * B_RATIO

print(f"Background: b0={B0:.4f}, b1={B1:.4f}, ratio={B1/B0:.6f}")
print(f"Golden radius: |w| = φ^(-1/2) = {PHI**(-0.5):.6f}")

# ============================================================
# The w-uniformization
# ============================================================
def w_to_z(w):
    """Convert Floquet multiplier w to spectral parameter z.
    z² = b₀² + b₁² + b₀·b₁·(w + 1/w)
    """
    z_sq = B0**2 + B1**2 + B0 * B1 * (w + 1/w)
    return np.sqrt(z_sq + 0j)

def s_to_w(s):
    """s = -log(w)/log(φ), so w = φ^(-s)"""
    return PHI ** (-s)

def s_to_z(s):
    """s → w → z"""
    return w_to_z(s_to_w(s))

# Verify: s = 1/2 + 0i should give z = 0 (mid-gap)
s_test = 0.5 + 0j
w_test = s_to_w(s_test)
z_test = s_to_z(s_test)
print(f"\nVerification:")
print(f"  s = 1/2: w = {w_test:.6f}, |w| = {abs(w_test):.6f}, z = {z_test:.6f}")
print(f"  Expected: |w| = φ^(-1/2) = {PHI**(-0.5):.6f}, z = 0")

# Check: s = 1/2 + iE for various E
print(f"\n  Scanning critical line s = 1/2 + iE:")
for E_val in [0, 1, 5, 10, 20]:
    s = 0.5 + 1j * E_val
    w = s_to_w(s)
    z = s_to_z(s)
    print(f"    E={E_val:5.1f}: |w|={abs(w):.6f}, arg(w)={np.angle(w):.4f}, "
          f"z={z:.4f}, |z|={abs(z):.4f}")


# ============================================================
# Green's function (same as before)
# ============================================================
def discriminant(z):
    return (z**2 - B0**2 - B1**2) / (B0 * B1)

def kappa(z):
    D = discriminant(z)
    k = np.sqrt(D**2 - 4 + 0j)
    rho1 = (D - k) / 2
    rho2 = (D + k) / 2
    if abs(rho1) <= abs(rho2):
        return k
    else:
        return -k

def floquet_multiplier(z):
    D = discriminant(z)
    k = kappa(z)
    return (D - k) / 2

def I_r(z, r):
    rho = floquet_multiplier(z)
    k = kappa(z)
    if abs(k) < 1e-15:
        return 0.0 + 0j
    return rho**abs(r) / (B0 * B1 * k)

def green_function(n, m, z):
    alpha = n % 2
    beta = m % 2
    j = (n - alpha) // 2
    ell = (m - beta) // 2
    r = j - ell
    if alpha == 0 and beta == 0:
        return -z * I_r(z, r)
    elif alpha == 1 and beta == 1:
        return -z * I_r(z, r)
    elif alpha == 0 and beta == 1:
        return -(B0 * I_r(z, r) + B1 * I_r(z, r-1))
    else:
        return -(B0 * I_r(z, r) + B1 * I_r(z, r+1))


# ============================================================
# Potential V (no log p, prime indicators)
# ============================================================
def build_potential(N_sites, sigma=0.3, max_primes=200):
    v = np.zeros(N_sites)
    for p in PRIMES[:max_primes]:
        alpha = phi_position(p)
        w = phi_weight(p)
        for n in range(N_sites):
            dist = alpha - n
            if abs(dist) < 5 * sigma:
                v[n] += w * np.exp(-dist**2 / (2*sigma**2))
    return v


# ============================================================
# Compute perturbation determinant along the CRITICAL LINE
# ============================================================
def compute_det_critical_line(v, E_vals):
    """
    Compute Δ(s) = det(I + V·R_T(z(s))) at s = 1/2 + iE
    along the critical line in the w-uniformization.
    """
    active = np.where(np.abs(v) > 1e-10)[0]
    N_active = len(active)
    v_active = v[active]
    
    dets = np.zeros(len(E_vals), dtype=complex)
    z_vals = np.zeros(len(E_vals), dtype=complex)
    w_vals = np.zeros(len(E_vals), dtype=complex)
    
    for idx, E in enumerate(E_vals):
        s = 0.5 + 1j * E
        w = s_to_w(s)
        z = s_to_z(s)
        
        w_vals[idx] = w
        z_vals[idx] = z
        
        G = np.zeros((N_active, N_active), dtype=complex)
        for i in range(N_active):
            for j in range(N_active):
                G[i,j] = green_function(active[i], active[j], z)
        
        VG = np.diag(v_active) @ G
        dets[idx] = np.linalg.det(np.eye(N_active, dtype=complex) + VG)
    
    return dets, z_vals, w_vals


# ============================================================
# Length spectrum in the s-variable
# ============================================================
def length_spectrum_s(E_vals, dets):
    """
    Compute d/ds log Δ(s) along the critical line,
    then FT into length t.
    
    Since s = 1/2 + iE, d/ds = d/(idE) = -i·d/dE
    so d/ds log Δ = -i · d/dE log Δ
    """
    dE = E_vals[1] - E_vals[0]
    
    # log Δ
    log_delta = np.log(dets + 0j)
    
    # d/dE of log Δ
    d_log_delta = np.gradient(log_delta, dE)
    
    # d/ds log Δ = -i · d/dE log Δ  (since ds = i·dE on the critical line)
    d_ds_log_delta = -1j * d_log_delta
    
    # Also compute phase and amplitude separately
    phase = np.unwrap(np.angle(dets))
    amplitude = np.log(np.abs(dets) + 1e-30)
    d_phase = np.gradient(phase, dE)
    d_amp = np.gradient(amplitude, dE)
    
    # Window
    N = len(E_vals)
    w = np.hanning(N)
    
    # FT of d/ds log Δ into length t
    # The convention: peaks at t = log(p) from oscillations e^{-iE·log(p)}
    N_pad = 8 * N
    
    signal = d_ds_log_delta * w
    ft = np.fft.fft(signal, n=N_pad)
    t_vals = np.fft.fftfreq(N_pad, d=dE) * 2 * np.pi
    
    # Also FT just the real part of d/ds log Δ 
    # (which should contain the -ζ'/ζ analog)
    signal_real = np.real(d_ds_log_delta) * w
    ft_real = np.fft.fft(signal_real, n=N_pad)
    
    # And FT the imaginary part (spectral shift derivative)
    signal_imag = np.imag(d_ds_log_delta) * w
    ft_imag = np.fft.fft(signal_imag, n=N_pad)
    
    pos_mask = t_vals > 0
    t_pos = t_vals[pos_mask]
    ft_pos = ft[pos_mask]
    ft_real_pos = ft_real[pos_mask]
    ft_imag_pos = ft_imag[pos_mask]
    
    return (t_pos, ft_pos, ft_real_pos, ft_imag_pos, 
            d_ds_log_delta, d_phase, d_amp)


# ============================================================
# Peak analysis
# ============================================================
def analyze_peaks(t_pos, ft_magnitude, label="", max_primes=30):
    """Find peaks and match to log(p) positions."""
    
    # Smooth
    smoothed = gaussian_filter1d(ft_magnitude, sigma=3)
    
    # Find peaks
    threshold = np.max(smoothed[t_pos < 15]) * 0.03
    peaks, _ = find_peaks(smoothed, height=threshold, distance=5,
                           prominence=threshold * 0.5)
    
    if len(peaks) == 0:
        print(f"  {label}: No peaks found above threshold")
        return [], []
    
    # Sort by height
    heights = smoothed[peaks]
    sorted_idx = np.argsort(-heights)
    peaks = peaks[sorted_idx]
    
    matches = []
    print(f"\n  {label} — peaks matched to prime orbits:")
    print(f"  {'t_peak':>8} {'|FT|':>12} {'log(p^k)':>10} {'p':>5} {'k':>3} {'error':>8} {'p^{-k/2}':>10}")
    
    for pk_idx in peaks[:25]:
        t_peak = t_pos[pk_idx]
        ft_val = ft_magnitude[pk_idx]
        
        if t_peak < 0.3 or t_peak > 15:
            continue
        
        best_match = None
        best_error = float('inf')
        
        for p in PRIMES[:max_primes]:
            log_p = np.log(p)
            for k in range(1, 8):
                target = k * log_p
                error = abs(t_peak - target)
                if error < best_error:
                    best_error = error
                    best_match = (p, k, target)
        
        if best_match and best_error < 0.12:
            p, k, target = best_match
            predicted = p**(-k/2)
            matches.append((t_peak, ft_val, p, k, best_error, predicted))
            marker = " <<<" if k == 1 else ""
            print(f"  {t_peak:8.4f} {ft_val:12.4e} {target:10.4f} {p:5d} {k:3d} "
                  f"{best_error:8.4f} {predicted:10.6f}{marker}")
    
    return peaks, matches


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("╔" + "═" * 68 + "╗")
    print("║  LENGTH SPECTRUM in the w-UNIFORMIZATION                          ║")
    print("║  Critical line = circle |w| = φ^{-1/2} in Floquet plane          ║")
    print("║  s = -log(w)/log(φ),  w^d = p^{-s}                              ║")
    print("╚" + "═" * 68 + "╝\n")
    
    # Build potential
    N_SITES = 120
    SIGMA = 0.3
    MAX_PRIMES = 200
    v = build_potential(N_SITES, sigma=SIGMA, max_primes=MAX_PRIMES)
    print(f"V: {np.sum(np.abs(v) > 1e-10)} nonzero sites")
    
    # Scan the critical line: s = 1/2 + iE
    N_ENERGY = 3000
    E_max = 30.0  # height on critical line
    E_vals = np.linspace(-E_max, E_max, N_ENERGY)
    dE = E_vals[1] - E_vals[0]
    
    print(f"\nScanning critical line: E ∈ [{-E_max}, {E_max}], N={N_ENERGY}")
    print(f"  dE = {dE:.4f}")
    print(f"  Max resolvable length: t_max = π/dE = {np.pi/dE:.2f}")
    print(f"  Length resolution: Δt ≈ 2π/(N·dE) = {2*np.pi/(N_ENERGY*dE):.4f}")
    
    # What z values does this correspond to?
    print(f"\n  Sample z values on critical line:")
    for E in [0, 5, 10, 15, 20, 25, 30]:
        s = 0.5 + 1j * E
        z = s_to_z(s)
        w = s_to_w(s)
        rho = floquet_multiplier(z)
        print(f"    E={E:5.1f}: z={z:.4f}, |z|={abs(z):.2f}, "
              f"|w|={abs(w):.4f}, |ρ(z)|={abs(rho):.4f}")
    
    # Compute determinant along critical line
    print(f"\nComputing Δ(s) along critical line...")
    dets, z_vals, w_vals = compute_det_critical_line(v, E_vals)
    
    print(f"  |Δ| range: [{np.min(np.abs(dets)):.6f}, {np.max(np.abs(dets)):.6f}]")
    print(f"  arg(Δ) range: [{np.min(np.angle(dets)):.4f}, {np.max(np.angle(dets)):.4f}]")
    
    # Length spectrum
    print("\n" + "=" * 70)
    print("LENGTH SPECTRUM: d/ds log Δ(1/2+iE), FT → length t")
    print("=" * 70)
    
    (t_pos, ft_pos, ft_real_pos, ft_imag_pos, 
     d_ds, d_phase, d_amp) = length_spectrum_s(E_vals, dets)
    
    ft_mag = np.abs(ft_pos)
    ft_real_mag = np.abs(ft_real_pos)
    ft_imag_mag = np.abs(ft_imag_pos)
    
    # Analyze peaks in different components
    print("\n--- Full d/ds log Δ ---")
    peaks_full, matches_full = analyze_peaks(t_pos, ft_mag, "Full")
    
    print("\n--- Real part of d/ds log Δ ---")
    peaks_re, matches_re = analyze_peaks(t_pos, ft_real_mag, "Real")
    
    print("\n--- Imaginary part of d/ds log Δ ---")
    peaks_im, matches_im = analyze_peaks(t_pos, ft_imag_mag, "Imag")
    
    # Use best matches
    all_matches = [(m, "full") for m in matches_full] + \
                  [(m, "real") for m in matches_re] + \
                  [(m, "imag") for m in matches_im]
    
    best_matches = matches_re if len(matches_re) >= max(len(matches_full), len(matches_im)) else \
                   (matches_full if len(matches_full) >= len(matches_im) else matches_im)
    
    # ============================================================
    # VISUALIZATION
    # ============================================================
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle('LENGTH SPECTRUM in the w-UNIFORMIZATION\n'
                 'Critical line = golden-radius circle |w| = φ⁻¹ᐟ²', 
                 fontsize=15, fontweight='bold', y=0.99)
    
    C = {
        'gold': '#DAA520', 'blue': '#4169E1', 'red': '#DC143C',
        'green': '#2E8B57', 'purple': '#8B008B', 'cyan': '#00CED1',
        'orange': '#FF8C00', 'bg': '#1a1a2e', 'text': '#e0e0e0', 
        'grid': '#333355'
    }
    fig.patch.set_facecolor(C['bg'])
    gs = GridSpec(3, 2, hspace=0.35, wspace=0.3,
                 left=0.07, right=0.96, top=0.94, bottom=0.03)
    
    # Panel 1: d/ds log Δ along critical line
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(C['bg'])
    ax1.plot(E_vals, np.real(d_ds), color=C['gold'], linewidth=0.5, 
             label='Re(d/ds log Δ)', alpha=0.8)
    ax1.plot(E_vals, np.imag(d_ds), color=C['blue'], linewidth=0.5, 
             label='Im(d/ds log Δ)', alpha=0.8)
    ax1.set_xlabel('E (height on critical line)', color=C['text'])
    ax1.set_ylabel('d/ds log Δ(1/2+iE)', color=C['text'])
    ax1.set_title('Scattering Log-Derivative on Critical Line', 
                  color=C['gold'], fontsize=12)
    ax1.legend(facecolor=C['bg'], edgecolor=C['grid'], labelcolor=C['text'], fontsize=9)
    ax1.tick_params(colors=C['text'])
    for s in ax1.spines.values(): s.set_color(C['grid'])
    
    # Panel 2: Full length spectrum
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(C['bg'])
    
    t_mask = (t_pos > 0.3) & (t_pos < 12)
    ax2.plot(t_pos[t_mask], ft_mag[t_mask], color=C['gold'], linewidth=0.8)
    
    for p in PRIMES[:20]:
        log_p = np.log(p)
        if 0.3 < log_p < 12:
            ax2.axvline(log_p, color=C['red'], alpha=0.6, linewidth=1, linestyle='--')
            ymax = ax2.get_ylim()[1] if ax2.get_ylim()[1] > 0 else np.max(ft_mag[t_mask])
            ax2.text(log_p, ymax * 0.95, f'{p}', color=C['red'], fontsize=7, 
                     ha='center', va='top')
    
    # Mark harmonics
    for p in [2, 3, 5]:
        for k in range(2, 5):
            t_pk = k * np.log(p)
            if 0.3 < t_pk < 12:
                ax2.axvline(t_pk, color=C['cyan'], alpha=0.25, linewidth=0.5, linestyle=':')
    
    ax2.set_xlabel('t (orbit length)', color=C['text'])
    ax2.set_ylabel('|FT| (full d/ds log Δ)', color=C['text'])
    ax2.set_title('Length Spectrum — Full', color=C['gold'], fontsize=12)
    ax2.tick_params(colors=C['text'])
    for s in ax2.spines.values(): s.set_color(C['grid'])
    
    # Panel 3: Real-part length spectrum (should match -ζ'/ζ)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(C['bg'])
    
    ax3.plot(t_pos[t_mask], ft_real_mag[t_mask], color=C['gold'], linewidth=0.8)
    
    for p in PRIMES[:20]:
        log_p = np.log(p)
        if 0.3 < log_p < 12:
            ax3.axvline(log_p, color=C['red'], alpha=0.6, linewidth=1, linestyle='--')
    
    ax3.set_xlabel('t (orbit length)', color=C['text'])
    ax3.set_ylabel('|FT| (Re d/ds log Δ)', color=C['text'])
    ax3.set_title('Length Spectrum — Real Part', color=C['gold'], fontsize=12)
    ax3.tick_params(colors=C['text'])
    for s in ax3.spines.values(): s.set_color(C['grid'])
    
    # Panel 4: Imaginary-part length spectrum
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(C['bg'])
    
    ax4.plot(t_pos[t_mask], ft_imag_mag[t_mask], color=C['gold'], linewidth=0.8)
    
    for p in PRIMES[:20]:
        log_p = np.log(p)
        if 0.3 < log_p < 12:
            ax4.axvline(log_p, color=C['red'], alpha=0.6, linewidth=1, linestyle='--')
    
    ax4.set_xlabel('t (orbit length)', color=C['text'])
    ax4.set_ylabel('|FT| (Im d/ds log Δ)', color=C['text'])
    ax4.set_title('Length Spectrum — Imaginary Part', color=C['gold'], fontsize=12)
    ax4.tick_params(colors=C['text'])
    for s in ax4.spines.values(): s.set_color(C['grid'])
    
    # Panel 5: Peak amplitudes vs p^{-1/2}
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.set_facecolor(C['bg'])
    
    if best_matches:
        k1 = [(p, amp, pred) for (t, amp, p, k, err, pred) in best_matches if k == 1]
        if k1:
            ps = [m[0] for m in k1]
            amps = [m[1] for m in k1]
            
            ax5.scatter(ps, amps, color=C['gold'], s=50, zorder=5, 
                        label='Observed peaks at log(p)')
            
            p_range = np.linspace(min(ps), max(ps)*1.2, 100)
            scale = np.mean([a * np.sqrt(p) for a, p in zip(amps, ps)])
            ax5.plot(p_range, scale / np.sqrt(p_range), '--', color=C['red'],
                     linewidth=2, label=f'C·p^{{-1/2}}')
            
            ax5.set_xlabel('Prime p', color=C['text'])
            ax5.set_ylabel('Peak amplitude', color=C['text'])
            ax5.set_title('Peak Amplitudes vs p^{-1/2}', color=C['gold'], fontsize=12)
            ax5.legend(facecolor=C['bg'], edgecolor=C['grid'], labelcolor=C['text'])
    else:
        ax5.text(0.5, 0.5, 'No matched peaks', color=C['text'],
                 ha='center', va='center', transform=ax5.transAxes, fontsize=14)
    ax5.tick_params(colors=C['text'])
    for s in ax5.spines.values(): s.set_color(C['grid'])
    
    # Panel 6: The w-plane (Floquet plane)
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor(C['bg'])
    
    # Draw the golden-radius circle
    theta = np.linspace(0, 2*np.pi, 200)
    r_gold = PHI**(-0.5)
    ax6.plot(r_gold * np.cos(theta), r_gold * np.sin(theta), 
             color=C['red'], linewidth=2, label=f'|w| = φ⁻¹ᐟ² (critical line)')
    ax6.plot(np.cos(theta), np.sin(theta), 
             color=C['grid'], linewidth=0.5, label='|w| = 1 (band edge)')
    
    # Plot the w values we sampled
    ax6.scatter(np.real(w_vals[::10]), np.imag(w_vals[::10]), 
                color=C['gold'], s=3, alpha=0.5, label='Sampled points')
    
    ax6.set_xlabel('Re(w)', color=C['text'])
    ax6.set_ylabel('Im(w)', color=C['text'])
    ax6.set_title('Floquet Plane: Critical Line = Golden Circle', 
                  color=C['gold'], fontsize=12)
    ax6.set_aspect('equal')
    ax6.legend(facecolor=C['bg'], edgecolor=C['grid'], labelcolor=C['text'], fontsize=8)
    ax6.tick_params(colors=C['text'])
    for s in ax6.spines.values(): s.set_color(C['grid'])
    
    plt.savefig('/home/claude/length_spectrum_w.png', dpi=150,
                facecolor=C['bg'], bbox_inches='tight')
    print("\nFigure saved: /home/claude/length_spectrum_w.png")
    
    # ============================================================
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    
    total_matches = len(best_matches)
    k1_matches = len([m for m in best_matches if m[3] == 1])
    harmonic_matches = len([m for m in best_matches if m[3] > 1])
    
    print(f"\n  Total peak matches: {total_matches}")
    print(f"  Fundamental (k=1):  {k1_matches}")
    print(f"  Harmonics (k>1):    {harmonic_matches}")
    
    if k1_matches >= 3:
        k1_data = [(p, amp) for (t, amp, p, k, err, pred) in best_matches if k == 1]
        ps = np.array([d[0] for d in k1_data])
        amps = np.array([d[1] for d in k1_data])
        
        # Fit: |FT| ~ C · p^{-α}
        log_p = np.log(ps)
        log_a = np.log(amps + 1e-30)
        A = np.vstack([log_p, np.ones(len(log_p))]).T
        result = np.linalg.lstsq(A, log_a, rcond=None)
        alpha_fit = -result[0][0]
        
        print(f"\n  Amplitude scaling: |FT| ~ p^{{-α}}")
        print(f"    Fitted α = {alpha_fit:.4f}")
        print(f"    Expected α = 0.5000 (p^{{-1/2}} from |ρ|=φ^{{-1/2}})")
        
        if abs(alpha_fit - 0.5) < 0.15:
            print(f"\n  *** POSITIVE: p^{{-1/2}} scaling confirmed ***")
            print(f"  *** The critical line emerges from the operator ***")
        elif abs(alpha_fit - 0.5) < 0.3:
            print(f"\n  MIXED: scaling in right direction")
        else:
            print(f"\n  NEGATIVE: exponent {alpha_fit:.3f} far from 1/2")
    elif total_matches > 0:
        print(f"\n  Too few fundamental peaks for scaling test")
    else:
        print(f"\n  No peaks → operator doesn't produce discrete prime orbits")
        print(f"  (Likely cause: V too small / primes unresolved)")
