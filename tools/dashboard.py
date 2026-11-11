import math, random
from common import *

W, H, P = 1000, 560, "d"
PX, PY = 165, 10                    # lanyard pivot (top of the strap, in card coords)
T = 8.0                             # one-shot drop + swing timeline


# ---------------------------------------------------------------- physics -> keyframes
def physics():
    """Gravity drop, two decaying rebounds, then a damped pendulum (theta'' = -w^2 theta - 2 z w theta')."""
    g, h0 = 2600.0, 600.0
    th = math.sqrt(2 * h0 / g)                 # time of impact
    ts = [i / 60 for i in range(int(1.6 * 60))] + [1.6 + i / 30 for i in range(int((T - 1.6) * 30) + 1)]
    ys, angs = [], []
    A, zeta, period = 9.0, .22, 2.3
    w = 2 * math.pi / period
    for t in ts:
        if t < th:
            y = -h0 + .5 * g * t * t
        else:
            tau = t - th
            y = 0
            for amp, dur, start in ((20, .34, 0), (6, .2, .34)):       # rebounds
                if start <= tau < start + dur:
                    u = (tau - start) / dur
                    y = -amp * 4 * u * (1 - u)
        ang = 0.0
        if t >= th:
            tau = t - th
            ang = A * math.exp(-zeta * w * tau) * math.sin(w * tau) * min(1, tau / .08)
        ys.append(y); angs.append(ang)
    ys[-1] = 0; angs[-1] = 0
    return ts, ys, angs


# ---------------------------------------------------------------- badge
def badge():
    ts, ys, angs = physics()
    kt = [t / T for t in ts]; kt[-1] = 1
    o = []
    # dark lanyard hardware gradients
    o.append(f'<defs>'
             f'<linearGradient id="{P}metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f5fb"/><stop offset=".35" stop-color="#8d92ad"/><stop offset=".6" stop-color="#e3e5f1"/><stop offset="1" stop-color="#6c7090"/></linearGradient>'
             f'<linearGradient id="{P}gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7dc84"/><stop offset=".5" stop-color="#c8962e"/><stop offset="1" stop-color="#f1dd9a"/></linearGradient>'
             f'<linearGradient id="{P}strap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
             f'<linearGradient id="{P}holo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="{CYAN}" stop-opacity=".5"/><stop offset=".4" stop-color="{VIOLET}" stop-opacity=".5"/><stop offset=".6" stop-color="{PINK}" stop-opacity=".5"/><stop offset=".8" stop-color="#fde68a" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<filter id="{P}blur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5"/></filter>'
             f'<clipPath id="{P}bd"><rect x="45" y="150" width="240" height="380" rx="22"/></clipPath>'
             f'<clipPath id="{P}pf"><rect x="75" y="198" width="180" height="152" rx="18"/></clipPath></defs>')
    # drop
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="{";".join("0 "+f(y) for y in ys)}" '
             f'keyTimes="{";".join(f(k) for k in kt)}" dur="{T}s" begin="0s" fill="freeze"/>')
    # pendulum, pivoting at the top of the strap
    o.append(f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f(a)+f" {PX} {PY}" for a in angs)}" '
             f'keyTimes="{";".join(f(k) for k in kt)}" dur="{T}s" begin="0s" fill="freeze"/>')
    # ambient sway keeps it alive after it settles
    o.append(f'<g>{tanim("rotate", [f"{a} {PX} {PY}" for a in (0, .7, 0, -.7, 0)], 6, [0, .25, .5, .75, 1], splines=["0.37 0 0.63 1"] * 4)}')

    # strap with printed text (extends far above the card; the card clips it)
    o.append(f'<rect x="{PX-18}" y="-700" width="36" height="822" fill="url(#{P}strap)"/>'
             f'<rect x="{PX-18}" y="-700" width="3" height="822" fill="#fff" fill-opacity=".25"/><rect x="{PX+15}" y="-700" width="3" height="822" fill="#000" fill-opacity=".18"/>'
             f'<text transform="translate({PX+4} 8) rotate(90)" class="mb" font-size="10" letter-spacing="1.2" fill="#0d0e16" fill-opacity=".78">@PYAPRIL15</text>')
    # metal clasp
    o.append(f'<rect x="{PX-15}" y="112" width="30" height="16" rx="5" fill="url(#{P}metal)" stroke="#000" stroke-opacity=".35"/>'
             f'<rect x="{PX-3}" y="127" width="6" height="12" rx="2" fill="url(#{P}metal)"/>'
             f'<circle cx="{PX}" cy="148" r="11" stroke="url(#{P}metal)" stroke-width="4.5"/>'
             f'<path d="M{PX-8} 123h16" stroke="#000" stroke-opacity=".3"/>')
    # card
    o.append(f'<rect x="45" y="150" width="240" height="380" rx="22" fill="#10111b"/>'
             f'<g clip-path="url(#{P}bd)"><rect x="45" y="150" width="240" height="380" fill="url(#{P}dots)"/>'
             f'<circle cx="165" cy="250" r="150" fill="{VIOLET}" fill-opacity=".10"/><circle cx="260" cy="520" r="120" fill="{PINK}" fill-opacity=".09"/>'
             f'<rect x="45" y="150" width="240" height="46" fill="#fff" fill-opacity=".03"/></g>'
             f'<rect x="45.6" y="150.6" width="238.8" height="378.8" rx="21.4" stroke="url(#{P}hair)" stroke-width="1.2"/>'
             f'<rect x="147" y="160" width="36" height="9" rx="4.5" fill="#05060a" stroke="#fff" stroke-opacity=".15"/>'
             f'<circle cx="{PX}" cy="148" r="11" stroke="url(#{P}metal)" stroke-width="4.5" clip-path="url(#{P}ringclip)"/>'
             f'<clipPath id="{P}ringclip"><rect x="{PX-20}" y="120" width="40" height="38"/></clipPath>'
             f'<text x="165" y="187" text-anchor="middle" class="m" font-size="10" letter-spacing="2" fill="{MUTE}">DEVELOPER ID</text>')
    # portrait with a travelling light
    o.append(f'<rect x="75" y="198" width="180" height="152" rx="18" fill="url(#{P}aurd)" fill-opacity=".28"/>'
             f'<g clip-path="url(#{P}pf)"><image x="75" y="198" width="180" height="152" preserveAspectRatio="xMidYMin slice" href="data:image/png;base64,{b64file(f"{ASSETS}/badge_face.png")}"/></g>'
             f'<rect x="75" y="198" width="180" height="152" rx="18" stroke="#fff" stroke-opacity=".14" stroke-width="1.5"/>'
             f'<rect x="75" y="198" width="180" height="152" rx="18" pathLength="100" stroke="url(#{P}aurd)" stroke-width="5" stroke-linecap="round" stroke-dasharray="16 84" filter="url(#{P}blur)" opacity=".9">'
             f'{anim("stroke-dashoffset", [0, -100], 3.6, [0, 1])}</rect>'
             f'<rect x="75" y="198" width="180" height="152" rx="18" pathLength="100" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="10 90">'
             f'{anim("stroke-dashoffset", [0, -100], 3.6, [0, 1])}</rect>')
    # identity
    nm = CFG["name"].upper()
    o.append(f'<text x="165" y="382" text-anchor="middle" class="d" font-size="{15 if text_w(nm, "d7", 15) < 205 else 13}" fill="{INK}">{nm}</text>'
             f'<text x="165" y="401" text-anchor="middle" class="m" font-size="11.5" fill="{MUTE}">Full Stack and Mobile Dev</text>')
    # gold chip
    o.append(f'<rect x="75" y="420" width="44" height="34" rx="7" fill="url(#{P}gold)" stroke="#fff" stroke-opacity=".3"/>'
             f'<path d="M75 432h14v10H75 M119 432h-14v10h14 M89 420v34 M105 420v34 M89 437h16" stroke="#7a5a14" stroke-opacity=".65" fill="none" stroke-width="1.2"/>')
    # barcode (seeded so it never changes)
    rnd = random.Random(15); x = 136; bars = []
    while x < 253:
        wdt = rnd.choice((1.2, 1.2, 2, 3)); bars.append(f'<rect x="{f(x)}" y="420" width="{wdt}" height="34" fill="{INK}" fill-opacity=".85"/>'); x += wdt + rnd.choice((1.5, 2, 2.6))
    o.append("".join(bars))
    o.append(f'<text x="165" y="478" text-anchor="middle" class="m" font-size="11" letter-spacing="1" fill="{MUTE}">@{CFG["handle"]}</text>'
             f'<rect x="75" y="494" width="180" height="1" fill="#fff" fill-opacity=".1"/>'
             f'<text x="165" y="513" text-anchor="middle" class="m" font-size="10.5" fill="{FAINT}">MCA, Lovely Professional University</text>')
    # holographic foil sweep (clipped to the card)
    o.append(f'<g clip-path="url(#{P}bd)"><g>{tanim("translate", ["0 0", "0 0", "420 0", "420 0"], 6.5, [0, .2, .62, 1])}'
             f'<rect x="-130" y="120" width="76" height="440" fill="url(#{P}holo)" transform="rotate(18 -90 340)"/></g></g>')
    o.append("</g></g></g>")
    return "".join(o)


# ---------------------------------------------------------------- odometer count-up
_cid = [0]


def odometer(x, base, text, size, color, delay):
    """Rolling digits that land on `text`. Final transform is the base state; SMIL rolls up from 0."""
    cw = max(text_w(str(d), "d7", size) for d in range(10)) + 1
    lh = size * 1.25
    out = []
    for i, ch in enumerate(text):
        cx = x + i * cw
        extra = 10 if i == len(text) - 1 else (0 if len(text) > 1 else 10)
        n = int(ch); final = -(n + extra) * lh
        _cid[0] += 1; cid = f"{P}od{_cid[0]}"
        strip = "".join(f'<text x="{f(cw/2)}" y="{f(k*lh)}" text-anchor="middle" class="d" font-size="{size}" fill="{color}">{k % 10}</text>' for k in range(20))
        out.append(f'<clipPath id="{cid}"><rect x="{f(cx)}" y="{f(base-size*.98)}" width="{f(cw)}" height="{f(lh)}"/></clipPath>'
                   f'<g clip-path="url(#{cid})"><g transform="translate({f(cx)} {f(base)})"><g transform="translate(0 {f(final)})">{strip}'
                   f'{tent("translate", "0 0", f"0 {f(final)}", delay + i * .12, 1.7)}</g></g></g>')
    return "".join(out)


# ---------------------------------------------------------------- dashboard
def dashboard():
    X0, CWD = 354, 646
    o = [card(P, X0, 0, CWD, H, 28, glow=[(X0 + 600, 40, 320, CYAN, .12), (X0 + 40, 540, 320, VIOLET, .14)], key="D")]
    o.append(f'<text x="{X0+32}" y="52" class="dm" font-size="16" fill="{INK}">GitHub at a glance</text>'
             f'<text x="{X0+32}" y="72" class="m" font-size="12" fill="{MUTE}">@{CFG["handle"]}, snapshot {STATS["asof"]}</text>')
    kp = [("Repositories", str(STATS["repos"]), CYAN), ("Stars earned", str(STATS["stars"]), PINK),
          ("Followers", str(STATS["followers"]), VIOLET), ("Languages", str(STATS["languages"]), CYAN)]
    tw, gap = (CWD - 64 - 3 * 14) / 4, 14
    for k, (lab, val, col) in enumerate(kp):
        x = X0 + 32 + k * (tw + gap); y = 92
        o.append(f'<g>{ent("opacity", 0, 1, .2 + k * .12, .6)}{glass(f(x), y, f(tw), 92, 16, .04, .09)}'
                 f'<rect x="{f(x+16)}" y="{y+14}" width="22" height="3" rx="1.5" fill="{col}"/>'
                 f'<text x="{f(x+16)}" y="{y+38}" class="m" font-size="11.5" fill="{MUTE}">{lab}</text>'
                 f'{odometer(x+16, y+78, val, 34, INK, .5 + k * .15)}</g>')
    # bar chart: most-starred repos, single hue, values labelled
    top = STATS["top"]; vmax = max(v for _, v in top) or 1
    py = 204
    o.append(f'{glass(X0+32, py, CWD-64, 200, 18, .03, .08)}<text x="{X0+52}" y="{py+30}" class="dm" font-size="13" fill="{INK}">Most-starred repositories</text>'
             f'<text x="{X0+CWD-52}" y="{py+30}" text-anchor="end" class="m" font-size="11.5" fill="{MUTE}">stars</text>')
    lx, bx0 = X0 + 52, X0 + 232; bmax = X0 + CWD - 100 - bx0
    for k, (name, v) in enumerate(top):
        y = py + 52 + k * 28; wdt = bmax * v / vmax
        nm = name if len(name) <= 17 else name[:16] + "."
        o.append(f'<text x="{lx}" y="{y+13}" class="m" font-size="12.5" fill="{INK}" fill-opacity=".9">{esc(nm)}</text>'
                 f'<rect x="{bx0}" y="{y}" width="{f(bmax)}" height="18" rx="9" fill="#fff" fill-opacity=".05"/>'
                 f'<rect x="{bx0}" y="{y}" width="{f(wdt)}" height="18" rx="9" fill="{CYAN}" fill-opacity=".9">{ent("width", 0, f(wdt), .9 + k * .12, 1.0)}</rect>'
                 f'<text x="{f(bx0+wdt+10)}" y="{y+13.5}" class="mb" font-size="13" fill="{INK}">{v}{ent("opacity", 0, 1, 1.6 + k * .12, .5)}</text>')
    # "now" panel
    ny = 424
    o.append(f'{glass(X0+32, ny, CWD-64, 114, 18, .04, .09)}'
             f'<circle cx="{X0+54}" cy="{ny+27}" r="4" fill="{PINK}"/><circle cx="{X0+54}" cy="{ny+27}" r="4" fill="none" stroke="{PINK}">{anim("r",[4,12],2,[0,1])}{anim("opacity",[.8,0],2,[0,1])}</circle>'
             f'<text x="{X0+68}" y="{ny+31}" class="dm" font-size="13" fill="{INK}">Now</text>')
    lines = ["studying MCA at Lovely Professional University", "building Flutter and Firebase apps", "practising DSA in C++, Java and Python"]
    for k, ln in enumerate(lines):
        y = ny + 56 + k * 22
        o.append(f'<g>{ent("opacity", 0, 1, 1.4 + k * .35, .6)}<text x="{X0+54}" y="{y}" class="mb" font-size="12.5" fill="{CYAN}">&gt;</text>'
                 f'<text x="{X0+72}" y="{y}" class="m" font-size="12.5" fill="{INK}" fill-opacity=".88">{ln}</text></g>')
    ey = ny + 56 + 2 * 22
    o.append(f'<rect x="{f(X0+72+text_w(lines[-1],"m4",12.5)+5)}" y="{ey-11}" width="7" height="14" fill="{CYAN}">{anim("opacity",[1,1,0,0],1.1,[0,.5,.5,1],calc="discrete")}</rect>')
    return "".join(o)


def build():
    o = [svg_open(W, H, P, ("d7", "d5", "m4", "m7"))]
    o.append(card(P, 0, 0, 330, H, 28, glow=[(165, 300, 260, VIOLET, .16), (60, 40, 200, CYAN, .10)], key="B"))
    o.append(f'<clipPath id="{P}lc"><rect x="0" y="0" width="330" height="{H}" rx="28"/></clipPath><g clip-path="url(#{P}lc)">{badge()}</g>')
    o.append(dashboard())
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("id-dashboard.svg", build())
