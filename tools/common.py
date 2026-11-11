"""Shared building blocks: palette, embedded fonts, card chrome, SMIL helpers, icons."""
import base64, json, math, os
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.dirname(HERE)          # repo root: where the .svg files are written

# ---------------------------------------------------------------- profile data
CFG = dict(
    name="Praveen Yadav", first="Praveen", last="Yadav", handle="pyapril15",
    email="praveen885127@gmail.com", location="Phagwara, Punjab", company="ex-KryptoAd",
    role="Full Stack & Mobile Developer",
    pitch="I turn ideas into clean, fast, user-friendly products.",
    linkedin="linkedin.com/in/praveenyadavme", instagram="instagram.com/praveen.yadav.in",
    portfolio="praveenyadavdev.vercel.app",
)
CFG.update(json.load(open(f"{HERE}/profile.json", encoding="utf-8")))   # edit profile.json to change any text
STATS = json.load(open(f"{ASSETS}/stats.json"))
ICONS = json.load(open(f"{ASSETS}/icons.json"))

# midnight glass + aurora
BG, CYAN, VIOLET, PINK = "#0d0e16", "#22d3ee", "#a78bfa", "#f472b6"
INK, MUTE, FAINT = "#e7e9f5", "#8a8fab", "#4b4f6b"

# ---------------------------------------------------------------- fonts
FONTS = {  # key -> (family, weight, file)
    "d5": ("PY Display", 500, "unbounded-latin-500-normal"),
    "d7": ("PY Display", 700, "unbounded-latin-700-normal"),
    "m4": ("PY Mono", 400, "jetbrains-mono-latin-400-normal"),
    "m7": ("PY Mono", 700, "jetbrains-mono-latin-700-normal"),
}
_ft = {k: TTFont(f"{ASSETS}/fonts/{v[2]}.woff2") for k, v in FONTS.items()}


def text_w(text, key, size, ls=0.0):
    """Advance width of `text` in px (no kerning; good enough for layout)."""
    t = _ft[key]; cmap = t.getBestCmap(); hm = t["hmtx"]; u = t["head"].unitsPerEm
    return sum(hm[cmap[ord(c)]][0] for c in text) * size / u + ls * len(text)


def b64file(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def font_css(keys=("d7", "m4", "m7")):
    css = ""
    for k in keys:
        fam, wt, fn = FONTS[k]
        css += (f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;"
                f"src:url(data:font/woff2;base64,{b64file(f'{ASSETS}/fonts/{fn}.woff2')}) format('woff2')}}")
    css += (".d{font-family:'PY Display','Segoe UI',Arial,sans-serif;font-weight:700}"
            ".dm{font-family:'PY Display','Segoe UI',Arial,sans-serif;font-weight:500}"
            ".m{font-family:'PY Mono',ui-monospace,Menlo,Consolas,monospace;font-weight:400}"
            ".mb{font-family:'PY Mono',ui-monospace,Menlo,Consolas,monospace;font-weight:700}")
    return css


# ---------------------------------------------------------------- numbers
def f(n):
    s = f"{n:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- SMIL helpers
def _kt(kt):
    return ";".join(f(k) for k in kt)


def anim(attr, values, dur, kt=None, begin="0s", loop=True, splines=None, calc=None, target=""):
    """<animate>. Looping animations repeat forever; one-shots freeze on the last value."""
    a = f'<animate {target}attributeName="{attr}" values="{";".join(str(v) for v in values)}" dur="{f(dur)}s" begin="{begin}"'
    if kt: a += f' keyTimes="{_kt(kt)}"'
    if splines: a += f' calcMode="spline" keySplines="{";".join(splines)}"'
    elif calc: a += f' calcMode="{calc}"'
    a += ' repeatCount="indefinite"/>' if loop else ' fill="freeze"/>'
    return a


def tanim(ttype, values, dur, kt=None, begin="0s", loop=True, splines=None):
    a = f'<animateTransform attributeName="transform" type="{ttype}" values="{";".join(str(v) for v in values)}" dur="{f(dur)}s" begin="{begin}"'
    if kt: a += f' keyTimes="{_kt(kt)}"'
    if splines: a += f' calcMode="spline" keySplines="{";".join(splines)}"'
    a += ' repeatCount="indefinite"/>' if loop else ' fill="freeze"/>'
    return a


EASE = "0.16 1 0.3 1"   # fast-out, soft landing
LIN = "0 0 1 1"


def ent(attr, frm, to, delay, dur):
    """Entrance: hold `frm`, wait `delay`, ease to `to`. Starts at 0s (keyTimes carry the delay).
    The element's own attribute must already hold the final value so a non-animating renderer shows the finished card."""
    tot = delay + dur
    if delay <= 0:
        return anim(attr, [frm, to], tot, [0, 1], loop=False, splines=[EASE])
    return anim(attr, [frm, frm, to], tot, [0, delay / tot, 1], loop=False, splines=[LIN, EASE])


def tent(ttype, frm, to, delay, dur):
    tot = delay + dur
    if delay <= 0:
        return tanim(ttype, [frm, to], tot, [0, 1], loop=False, splines=[EASE])
    return tanim(ttype, [frm, frm, to], tot, [0, delay / tot, 1], loop=False, splines=[LIN, EASE])


def cycle_pts(n, i, fade=0.035, off=40):
    """Crossfading carousel/cycle keyframes for slot i of n. Returns (keyTimes, opacity, x-offset).
    Slot 0 is fully visible at t=0 so a static render shows slot 0."""
    s = [k / n for k in range(n + 1)]
    if i == 0:
        kt = [0, s[1] - fade, s[1], 1 - fade, 1]
        return kt, [1, 1, 0, 0, 1], [0, 0, -off, off, 0]
    if i == n - 1:
        kt = [0, s[i] - fade, s[i], 1 - fade, 1]
        return kt, [0, 0, 1, 1, 0], [off, off, 0, 0, -off]
    kt = [0, s[i] - fade, s[i], s[i + 1] - fade, s[i + 1], 1]
    return kt, [0, 0, 1, 1, 0, 0], [off, off, 0, 0, -off, -off]


def orbit_path(rx, ry, ang):
    """Path (relative to the start point) around an axis-aligned ellipse, starting at angle `ang`.
    Returns (x0, y0, d): put the element at translate(x0,y0) and animateMotion along d."""
    x0, y0 = rx * math.cos(ang), ry * math.sin(ang)
    d = f"M0 0 a{f(rx)} {f(ry)} 0 0 1 {f(-2*x0)} {f(-2*y0)} a{f(rx)} {f(ry)} 0 0 1 {f(2*x0)} {f(2*y0)}"
    return x0, y0, d


# ---------------------------------------------------------------- chrome
def svg_open(w, h, p, fonts=("d7", "m4", "m7"), extra_css=""):
    """Root element + style + shared defs. `p` namespaces every id in the file."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img">'
            f'<style>{font_css(fonts)}{extra_css}</style>'
            f'<defs>'
            f'<linearGradient id="{p}aur" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
            f'<linearGradient id="{p}aurd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>'
            f'<linearGradient id="{p}hair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".75"/><stop offset=".45" stop-color="{VIOLET}" stop-opacity=".35"/><stop offset="1" stop-color="{PINK}" stop-opacity=".7"/></linearGradient>'
            f'<pattern id="{p}dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill="#fff" fill-opacity=".075"/></pattern>'
            f'</defs>')


def card(p, x, y, w, h, r=28, glow=(), key=""):
    """Midnight-glass card: base, aurora glows, dot texture, gradient hairline. `glow` = [(cx,cy,r,color,opacity)...] in card coords."""
    cid = f"{p}clip{key}"
    g = "".join(
        f'<radialGradient id="{p}glow{key}{i}" cx="{cx}" cy="{cy}" r="{rr}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
        for i, (cx, cy, rr, col, op) in enumerate(glow))
    gr = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{p}glow{key}{i})"/>' for i in range(len(glow)))
    return (f'<defs>{g}<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{BG}"/>'
            f'<g clip-path="url(#{cid})">{gr}<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{p}dots)"/></g>'
            f'<rect x="{x+.6}" y="{y+.6}" width="{w-1.2}" height="{h-1.2}" rx="{r-.6}" stroke="url(#{p}hair)" stroke-width="1.2"/>'
            f'<rect x="{x+1.8}" y="{y+1.8}" width="{w-3.6}" height="{h-3.6}" rx="{r-1.8}" stroke="#fff" stroke-opacity=".035"/>')


def glass(x, y, w, h, r=14, op=.04, stroke=.09):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" fill-opacity="{op}" stroke="#fff" stroke-opacity="{stroke}"/>'


def lum(hexs):
    r, g, b = (int(hexs[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b)


def legible(hexs, floor=.22):
    """Brand colours that would vanish on the dark card are lightened toward white until they read."""
    hexs = hexs.lstrip("#")
    for _ in range(14):
        if lum(hexs) >= floor: break
        hexs = "".join(f"{min(255, int(int(hexs[i:i+2], 16) + (255 - int(hexs[i:i+2], 16)) * .18)):02x}" for i in (0, 2, 4))
    return "#" + hexs


def icon(slug, x, y, size, fill=None):
    i = ICONS[slug]
    return f'<path transform="translate({f(x)} {f(y)}) scale({f(size/24)})" d="{i["path"]}" fill="{fill or legible(i["hex"])}"/>'


# the LinkedIn mark was removed from Simple Icons, so draw a plain "in" glyph
def linkedin_glyph(x, y, size, fill):
    s = size / 24
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})" fill="{fill}">'
            f'<rect x="2.5" y="8.5" width="3.6" height="12"/><circle cx="4.3" cy="4.6" r="2.2"/>'
            f'<path d="M9.4 8.5h3.4v1.7c.6-1.1 1.9-2 3.7-2 3.3 0 4 2.1 4 4.9v7.4h-3.6v-6.6c0-1.5-.2-2.7-1.8-2.7s-2.1 1.2-2.1 2.8v6.5H9.4z"/></g>')


def stroke_icon(kind, x, y, color, delay=0.0, size=16):
    """Small outline icons that draw themselves in (pathLength=1 trick)."""
    P = {
        "pin": 'M8 1.6c-2.5 0-4.5 2-4.5 4.5 0 3.3 4.5 8.2 4.5 8.2s4.5-4.9 4.5-8.2C12.5 3.6 10.5 1.6 8 1.6z M8 4.4a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4z',
        "building": 'M3 14.4V3.4c0-.5.4-.9.9-.9h5.2c.5 0 .9.4.9.9v11 M10 6.6h2.1c.5 0 .9.4.9.9v6.9 M1.6 14.4h12.8 M5.4 5.2h1.8 M5.4 8h1.8 M5.4 10.8h1.8',
        "star": 'M8 1.7l1.9 4 4.3.6-3.1 3 .7 4.3L8 11.5l-3.8 2.1.7-4.3-3.1-3 4.3-.6z',
        "repo": 'M3 3.6C3 2.7 3.7 2 4.6 2H13v10H4.6c-.9 0-1.6.7-1.6 1.6v0C3 14.5 3.7 15 4.6 15H13 M6 5h4.2',
        "mail": 'M2 3.8h12v8.4H2z M2.4 4.4L8 9l5.6-4.6',
        "link": 'M6.8 9.2a2.6 2.6 0 0 0 3.7 0l2.2-2.2a2.6 2.6 0 0 0-3.7-3.7L8.2 4.1 M9.2 6.8a2.6 2.6 0 0 0-3.7 0L3.3 9a2.6 2.6 0 0 0 3.7 3.7l.8-.8',
    }
    s = size / 16
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(s)})"><path d="{P[kind]}" pathLength="1" stroke="{color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="0">'
            f'{ent("stroke-dashoffset", 1, 0, delay, .9)}</path></g>')


def arrow(x, y, color, size=16, sw=2):
    """Right-pointing arrow drawn as a path (no font glyph needed)."""
    return (f'<path transform="translate({f(x)} {f(y)})" d="M0 {size/2} H{size-2} M{size*.55} {size*.12} L{size-1} {size/2} L{size*.55} {size*.88}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def write(name, svg):
    path = os.path.join(OUT, name)
    open(path, "w", encoding="utf-8").write(svg)
    print(f"{name:20s} {os.path.getsize(path)/1024:7.1f} KB")
    return path
