import math
from common import *

W, H, P = 1000, 600, "s"
CX, CY = 318, 300                 # orbit scene centre
CORE_R = 42                       # glowing core radius
MOON_ORBIT, MOON_R, REACT_R = 36, 11, 19


def orbit(rx, ry, tilt, icons, dur, ccw=False, col=VIOLET, tag=""):
    """One tilted elliptical orbit. icons = [(slug, size, phase)].  The tilt lives on the group; each rider is counter-rotated so it stays upright."""
    o = [f'<g transform="translate({CX} {CY}) rotate({tilt})">',
         f'<ellipse rx="{rx}" ry="{ry}" stroke="{col}" stroke-opacity=".3" stroke-dasharray="2 7" stroke-linecap="round"/>']
    for slug, size, ph in icons:
        ang = ph * 2 * math.pi
        x0, y0, d = orbit_path(rx, ry, ang)
        if ccw: d = d.replace(" 0 0 1 ", " 0 0 0 ")
        extra = ""
        if slug == "react":
            extra = moons(tilt)
        o.append(f'<g transform="translate({f(x0)} {f(y0)})"><g transform="rotate({-tilt})">'
                 f'<circle r="{size/2+7}" fill="#0d0e16" stroke="{legible(ICONS[slug]["hex"])}" stroke-opacity=".55" stroke-width="1.4"/>'
                 f'<circle r="{size/2+7}" fill="{legible(ICONS[slug]["hex"])}" fill-opacity=".08"/>'
                 f'{icon(slug, -size/2, -size/2, size)}{extra}</g>'
                 f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}"/></g>')
    o.append("</g>")
    return "".join(o)


def moons(tilt):
    """Two small moons that orbit the React icon (they travel with it because they are its children)."""
    out = []
    for slug, per, ph, ccw in (("tailwindcss", 4.2, .1, False), ("typescript", 6.4, .62, True)):
        ang = ph * 2 * math.pi
        x0, y0, d = orbit_path(MOON_ORBIT, MOON_ORBIT, ang)
        if ccw: d = d.replace(" 0 0 1 ", " 0 0 0 ")
        out.append(f'<circle r="{MOON_ORBIT}" stroke="#fff" stroke-opacity=".12" stroke-dasharray="1 5"/>'
                   f'<g transform="translate({f(x0)} {f(y0)})"><circle r="{MOON_R+3}" fill="#0d0e16" stroke="{legible(ICONS[slug]["hex"])}" stroke-opacity=".7"/>'
                   f'{icon(slug, -7, -7, 14)}<animateMotion dur="{per}s" repeatCount="indefinite" path="{d}"/></g>')
    return "".join(out)


def clearance_check(orbits):
    """Assert the moons can never touch the core: sample React's orbit and the moon circle."""
    rx, ry, tilt = orbits
    worst = 1e9
    for k in range(720):
        a = k / 720 * 2 * math.pi
        x, y = rx * math.cos(a), ry * math.sin(a)
        t = math.radians(tilt)
        px, py = x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)   # centre of the React icon
        worst = min(worst, math.hypot(px, py) - (MOON_ORBIT + MOON_R + 3))               # nearest a moon can get
    gap = worst - CORE_R
    assert gap > 18, f"moons would crowd the core (gap {gap:.1f})"
    return gap


def chips():
    groups = [("Mobile and frontend", CYAN, [("flutter", "Flutter"), ("dart", "Dart"), ("react", "React"), ("nextdotjs", "Next.js"), ("tailwindcss", "Tailwind"), ("vite", "Vite")]),
              ("Backend and APIs", VIOLET, [("nodedotjs", "Node.js"), ("express", "Express"), ("fastapi", "FastAPI"), ("django", "Django"), ("postman", "Postman"), ("swagger", "Swagger")]),
              ("Data and BaaS", PINK, [("firebase", "Firebase"), ("supabase", "Supabase"), ("mongodb", "MongoDB"), ("mysql", "MySQL"), ("postgresql", "Postgres"), ("appwrite", "Appwrite")]),
              ("Tools and cloud", CYAN, [("git", "Git"), ("github", "GitHub"), ("jenkins", "Jenkins"), ("vercel", "Vercel"), ("netlify", "Netlify"), ("pandas", "Pandas")])]
    gx, gw = 636, 332
    total = sum(len(g[2]) for g in groups); idx = 0; period = 10.0
    o = []; y = 58
    for gi, (title, col, items) in enumerate(groups):
        o.append(f'<text x="{gx}" y="{y}" class="dm" font-size="13" fill="{INK}">{title}</text>'
                 f'<rect x="{gx}" y="{y+8}" width="22" height="2.5" rx="1.25" fill="{col}"/>')
        x, yy = gx, y + 22
        for slug, label in items:
            cw = 34 + text_w(label, "m4", 12) + 6
            if x + cw > gx + gw:
                x, yy = gx, yy + 34
            # each chip's border glows in turn: all timelines start at 0s, keyTimes carry the stagger
            a = idx / total; b = min(a + 1.4 / total, .999)
            o.append(f'<g><rect x="{x}" y="{yy}" width="{f(cw)}" height="28" rx="14" fill="#fff" fill-opacity=".035"/>'
                     f'<rect x="{x+.5}" y="{yy+.5}" width="{f(cw-1)}" height="27" rx="13.5" stroke="{col}" stroke-width="1.3" stroke-opacity=".35">'
                     f'{anim("stroke-opacity", [.3, 1, .3, .3], period, [0, a, b, 1]) if a > 0 else anim("stroke-opacity", [1, .3, .3], period, [0, b, 1])}'
                     f'{anim("stroke-width", [1.2, 2, 1.2, 1.2], period, [0, a, b, 1]) if a > 0 else anim("stroke-width", [2, 1.2, 1.2], period, [0, b, 1])}</rect>'
                     f'{icon(slug, x+10, yy+7, 14)}<text x="{f(x+30)}" y="{yy+18.5}" class="m" font-size="12" fill="{INK}" fill-opacity=".9">{label}</text></g>')
            x += cw + 8; idx += 1
        y = yy + 34 + 28
    return "".join(o)


def build():
    o = [svg_open(W, H, P)]
    o.append(card(P, 0, 0, W, H, 28, glow=[(CX, CY, 330, VIOLET, .22), (CX, CY, 150, CYAN, .12), (900, 560, 300, PINK, .14)]))
    # divider between scene and chips
    o.append(f'<path d="M612 40V560" stroke="#fff" stroke-opacity=".08"/>')

    orbits = [(158, 66, 22, VIOLET), (262, 118, -28, CYAN), (284, 164, 66, PINK)]
    gap = clearance_check(orbits[1][:3])
    # orbit riders (React rides the middle orbit alone with its moons)
    o.append(orbit(*orbits[2][:3], [("firebase", 20, .05), ("supabase", 20, .22), ("mongodb", 20, .39), ("fastapi", 20, .56), ("mysql", 20, .73), ("git", 20, .9)], 34, col=orbits[2][3]))
    o.append(orbit(*orbits[1][:3], [("react", REACT_R * 2 - 4, .15), ("flutter", 24, .62)], 26, ccw=True, col=orbits[1][3]))
    o.append(orbit(*orbits[0][:3], [("python", 20, .0), ("cplusplus", 20, .2), ("openjdk", 20, .4), ("dart", 20, .6), ("javascript", 20, .8)], 18, col=orbits[0][3]))

    # glowing core
    o.append(f'<g transform="translate({CX} {CY})">'
             f'<defs><radialGradient id="{P}core"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".25" stop-color="{CYAN}" stop-opacity=".9"/><stop offset=".7" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient></defs>'
             f'<circle r="{CORE_R+30}" fill="url(#{P}core)" opacity=".28">{anim("r", [CORE_R+26, CORE_R+36, CORE_R+26], 4, [0, .5, 1])}</circle>'
             f'<circle r="{CORE_R}" fill="#0d0e16" stroke="url(#{P}aurd)" stroke-width="2"/>'
             f'<circle r="{CORE_R-8}" fill="url(#{P}core)" opacity=".55"/>'
             f'<circle r="{CORE_R+8}" stroke="{CYAN}" stroke-opacity=".5" stroke-dasharray="4 10" stroke-linecap="round">{tanim("rotate", ["0", "360"], 14)}</circle>'
             f'<text y="6" text-anchor="middle" class="d" font-size="17" fill="#fff">PY</text></g>')
    o.append(f'<text x="34" y="52" class="dm" font-size="16" fill="{INK}">Tech stack</text>'
             f'<text x="34" y="72" class="m" font-size="12" fill="{MUTE}">what I reach for, in orbit</text>')
    o.append(f'<text x="{636}" y="560" class="m" font-size="11" fill="{FAINT}">icons: Simple Icons</text>')
    o.append(chips())
    o.append("</svg>")
    print(f"stack: React/moon clearance from core = {gap:.1f}px")
    return "".join(o)


if __name__ == "__main__":
    write("stack.svg", build())
