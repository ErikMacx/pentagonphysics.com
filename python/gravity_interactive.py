import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

plt.rcParams['font.family'] = 'DejaVu Serif'

# ── Constants ──────────────────────────────────────────────────────────────────
DARK_BG   = '#0A0A0B'
PANEL_BG  = '#0D0D12'
GOLD      = '#D4A843'
BLUE      = '#5B9BC4'
RED       = '#C44B4B'
TEXT      = '#E8E4DC'
TEXT_DIM  = '#787470'
BORDER    = '#2A2A35'

# ── Figure layout ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 10), facecolor=DARK_BG)
fig.suptitle('Gravity: Two Models', fontsize=16, color=TEXT, y=0.98)

gs = gridspec.GridSpec(
    3, 3,
    figure=fig,
    left=0.04, right=0.96,
    top=0.93, bottom=0.04,
    hspace=0.08, wspace=0.12,
    height_ratios=[1, 0.06, 0.06]
)

ax_left  = fig.add_subplot(gs[0, 0])
ax_right = fig.add_subplot(gs[0, 1])
ax_ctrl  = fig.add_subplot(gs[0, 2])

for ax in [ax_left, ax_right]:
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-4.2, 4.2)
    ax.set_aspect('equal')
    ax.axis('off')

ax_ctrl.set_facecolor(PANEL_BG)
ax_ctrl.axis('off')

# Panel titles
ax_left.set_title('Standard Model\n(inward curvature)',
                  color=TEXT_DIM, fontsize=10, pad=8)
ax_right.set_title('Pentagon Physics\n(outward depletion)',
                   color=TEXT_DIM, fontsize=10, pad=8)
ax_ctrl.set_title('Controls', color=TEXT_DIM, fontsize=10, pad=8)

# ── Sliders ────────────────────────────────────────────────────────────────────
slider_specs = [
    ('separation',  'Mass separation',   0.8, 3.5, 2.0),
    ('m1_mass',     'Left mass (M\u2081)',        0.3, 3.0, 1.0),
    ('m2_mass',     'Right mass (M\u2082)',       0.3, 3.0, 1.0),
    ('orbit_ecc',   'Orbit eccentricity', 0.0, 0.7, 0.25),
    ('speed',       'Orbit speed',        0.2, 3.0, 1.0),
]

sliders = {}
slider_y_start = 0.82
slider_height  = 0.025
slider_gap     = 0.072

for i, (key, label, vmin, vmax, vinit) in enumerate(slider_specs):
    y = slider_y_start - i * slider_gap
    ax_s  = fig.add_axes([0.70, y, 0.22, slider_height], facecolor='#1A1A22')
    sl    = Slider(ax_s, label, vmin, vmax, valinit=vinit,
                   color=GOLD, track_color='#2A2A35',
                   handle_style={'facecolor': GOLD, 'edgecolor': TEXT, 'size': 8})
    sl.label.set_color(TEXT_DIM)
    sl.label.set_fontsize(8)
    sl.valtext.set_color(GOLD)
    sl.valtext.set_fontsize(8)
    sliders[key] = sl

# Reset button
ax_btn = fig.add_axes([0.77, 0.10, 0.08, 0.035], facecolor='#1A1A22')
btn_reset = Button(ax_btn, 'Reset', color='#1A1A22', hovercolor='#2A2A35')
btn_reset.label.set_color(TEXT)
btn_reset.label.set_fontsize(9)

# ── State ──────────────────────────────────────────────────────────────────────
orbit_angle = [0.0]   # mutable for closure

# ── Grid ──────────────────────────────────────────────────────────────────────
N = 22
xg = np.linspace(-4.0, 4.0, N)
yg = np.linspace(-4.0, 4.0, N)
Xg, Yg = np.meshgrid(xg, yg)

# ── Cached plot objects ────────────────────────────────────────────────────────
# We'll clear and redraw each frame for clarity
drawn = {'left': [], 'right': []}

def get_params():
    sep   = sliders['separation'].val
    m1    = sliders['m1_mass'].val
    m2    = sliders['m2_mass'].val
    ecc   = sliders['orbit_ecc'].val
    spd   = sliders['speed'].val
    return sep, m1, m2, ecc, spd

def field(px, py, mass, X, Y, outward):
    dx = X - px
    dy = Y - py
    r  = np.sqrt(dx**2 + dy**2) + 1e-6
    strength = mass / (r**2)
    sign = 1.0 if outward else -1.0
    return sign * (dx/r) * strength, sign * (dy/r) * strength

def mask_near(U, V, X, Y, centres, radius=0.5):
    for cx, cy in centres:
        dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
        near = dist < radius
        U[near] = 0; V[near] = 0

def draw_panel(ax, m1x, m2x, m1, m2, outward, angle):
    ax.cla()
    ax.set_facecolor(PANEL_BG)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-4.2, 4.2)
    ax.set_aspect('equal')
    ax.axis('off')

    centres = [(m1x, 0), (m2x, 0)]

    # Field vectors
    U1, V1 = field(m1x, 0, m1, Xg, Yg, outward)
    U2, V2 = field(m2x, 0, m2, Xg, Yg, outward)
    U = U1 + U2
    V = V1 + V2
    mask_near(U, V, Xg, Yg, centres)

    mag = np.sqrt(U**2 + V**2) + 1e-10
    Un  = U / mag
    Vn  = V / mag
    col_vals = np.log1p(mag) / (np.log1p(mag).max() + 1e-10)

    cmap = plt.cm.YlOrBr if outward else plt.cm.Blues_r
    colors = cmap(col_vals.ravel())

    ax.quiver(Xg, Yg, Un, Vn,
              color=colors.reshape(N, N, 4).reshape(-1, 4),
              scale=30, width=0.0025, headwidth=4, headlength=5,
              alpha=0.65, pivot='mid', zorder=2)

    if outward:
        # Equilibrium zone: perpendicular bisector weighted by mass ratio
        # x_eq such that m1/(x_eq - m1x)^2 = m2/(m2x - x_eq)^2
        # For equal masses: x_eq = (m1x + m2x)/2
        # General: solve sqrt(m1)*(m2x - x_eq) = sqrt(m2)*(x_eq - m1x)
        x_eq = (np.sqrt(m1)*m2x + np.sqrt(m2)*m1x) / (np.sqrt(m1) + np.sqrt(m2))
        by = np.linspace(-3.8, 3.8, 120)
        bx = np.full_like(by, x_eq)
        ax.plot(bx, by, color=BLUE, linewidth=1.4, alpha=0.7,
                linestyle='--', zorder=4)
        ax.fill_betweenx(by, x_eq - 0.15, x_eq + 0.15,
                         alpha=0.10, color=BLUE, zorder=3)
        ax.text(x_eq, 3.6, 'equilibrium', color=BLUE,
                fontsize=7.5, ha='center', style='italic', zorder=9)

        # Orbit: ellipse centred on the equilibrium point
        sep_len = abs(m2x - m1x)
        a = sep_len * 0.48           # semi-major
        ecc = sliders['orbit_ecc'].val
        b = a * np.sqrt(1 - ecc**2)  # semi-minor
        ot = np.linspace(0, 2*np.pi, 300)
        ox = x_eq + a * np.cos(ot)
        oy = b * np.sin(ot)
        ax.plot(ox, oy, color=RED, linewidth=1.3, alpha=0.85, zorder=5)

        # Orbiting body
        bx_pos = x_eq + a * np.cos(angle)
        by_pos = b * np.sin(angle)
        ax.plot(bx_pos, by_pos, 'o', color=RED, markersize=7,
                zorder=8, alpha=0.95)
        # Trail
        trail_t = np.linspace(angle - 0.8, angle, 40)
        tx = x_eq + a * np.cos(trail_t)
        ty = b * np.sin(trail_t)
        for j in range(len(tx)-1):
            alpha = 0.12 + 0.6 * (j / len(tx))
            ax.plot(tx[j:j+2], ty[j:j+2], color=RED,
                    linewidth=1.0, alpha=alpha, zorder=6)

    else:
        # Standard model: show inward spiral tendency
        # Small body orbiting m1 in the inward model
        r_orb = abs(m1x) * 0.65
        bx_pos = m1x + r_orb * np.cos(-angle * 1.2)
        by_pos = r_orb * np.sin(-angle * 1.2)
        ax.plot(bx_pos, by_pos, 'o', color=BLUE, markersize=7,
                zorder=8, alpha=0.85)
        ot = np.linspace(0, 2*np.pi, 200)
        ax.plot(m1x + r_orb*np.cos(ot), r_orb*np.sin(ot),
                color=BLUE, linewidth=0.9, alpha=0.4, zorder=4)

    # Masses
    for (cx, cy), mass_val, lbl in zip(centres, [m1, m2], ['M\u2081', 'M\u2082']):
        r = 0.18 + 0.08 * mass_val
        circ = plt.Circle((cx, cy), r, color=GOLD, zorder=7)
        ax.add_patch(circ)
        glow = plt.Circle((cx, cy), r * 2.0,
                           color=GOLD, alpha=0.10, zorder=6)
        ax.add_patch(glow)
        ax.text(cx, cy - r - 0.32, lbl,
                color=GOLD, fontsize=10, ha='center',
                style='italic', zorder=9)

    # Bottom caption
    if outward:
        ax.text(0, -3.9,
                'Space curves out. Objects fall toward least dense geometry.',
                color=TEXT_DIM, fontsize=7.5, ha='center', style='italic')
    else:
        ax.text(0, -3.9,
                'Mass curves spacetime inward. Objects fall toward the drain.',
                color=TEXT_DIM, fontsize=7.5, ha='center', style='italic')

def draw_ctrl():
    ax_ctrl.cla()
    ax_ctrl.set_facecolor(PANEL_BG)
    ax_ctrl.axis('off')
    ax_ctrl.set_title('Legend', color=TEXT_DIM, fontsize=10, pad=8)

    items = [
        (GOLD,  'o', 'Mass bodies'),
        (BLUE,  '--', 'Equilibrium boundary (PP)'),
        (RED,   '-', 'Orbital path (PP)'),
        (BLUE,  'o', 'Orbiting body (SM)'),
    ]
    for i, (col, ls, label) in enumerate(items):
        y = 0.80 - i * 0.18
        if ls == 'o':
            ax_ctrl.plot(0.10, y, 'o', color=col, markersize=7,
                         transform=ax_ctrl.transAxes)
        else:
            ax_ctrl.plot([0.05, 0.18], [y, y], color=col, linestyle=ls,
                         linewidth=1.5, transform=ax_ctrl.transAxes)
        ax_ctrl.text(0.25, y, label, color=TEXT_DIM, fontsize=8,
                     va='center', transform=ax_ctrl.transAxes)

    note = (
        "Sliders:\n"
        "  Separation — distance between masses\n"
        "  M\u2081 / M\u2082 — relative mass sizes\n"
        "  Eccentricity — orbit shape (0=circle)\n"
        "  Speed — orbital period"
    )
    ax_ctrl.text(0.05, 0.22, note, color=TEXT_DIM, fontsize=7.5,
                 va='bottom', transform=ax_ctrl.transAxes,
                 linespacing=1.6)

draw_ctrl()

# ── Animation ──────────────────────────────────────────────────────────────────
def animate(frame):
    sep, m1, m2, ecc, spd = get_params()
    m1x = -sep / 2
    m2x =  sep / 2

    dt = 0.04 * spd
    orbit_angle[0] += dt

    draw_panel(ax_left,  m1x, m2x, m1, m2, outward=False, angle=orbit_angle[0])
    draw_panel(ax_right, m1x, m2x, m1, m2, outward=True,  angle=orbit_angle[0])
    draw_ctrl()

    fig.suptitle('Gravity: Two Models  '
                 f'[sep={sep:.1f}  M\u2081={m1:.1f}  M\u2082={m2:.1f}  ecc={ecc:.2f}]',
                 fontsize=13, color=TEXT, y=0.98)

def reset(event):
    for key, (_, _, vmin, vmax, vinit) in zip(sliders.keys(), slider_specs):
        sliders[key].set_val(vinit)
    orbit_angle[0] = 0.0

btn_reset.on_clicked(reset)

anim = FuncAnimation(fig, animate, interval=60, cache_frame_data=False)

plt.show()
