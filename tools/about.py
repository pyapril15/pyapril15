import math, textwrap
from common import *

W, H, P = 1000, 470, "a"
LX, RX, CW = 0, 512, 488          # left / right card origin and width
LOOP = 16.0


# ---------------------------------------------------------------- left: fake browser + capabilities
def left():
    o = [card(P, LX, 0, CW, H, 28, glow=[(60, 30, 300, CYAN, .13), (470, 460, 320, VIOLET, .16)], key="L")]
    bx, by, bw, bh = 24, 24, 440, 220
    o.append(f'<defs><clipPath id="{P}win"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16"/></clipPath></defs>')
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="#08090f" stroke="#fff" stroke-opacity=".1"/>')
    o.append(f'<g clip-path="url(#{P}win)"><rect x="{bx}" y="{by}" width="{bw}" height="34" fill="#fff" fill-opacity=".045"/>')
    for i, c in enumerate((PINK, VIOLET, CYAN)):
        o.append(f'<circle cx="{bx+20+i*16}" cy="{by+17}" r="5" fill="{c}" fill-opacity=".85"/>')
    ux, uw = bx + 84, bw - 100
    url = CFG["portfolio"]
    o.append(f'<rect x="{ux}" y="{by+7}" width="{uw}" height="20" rx="10" fill="#fff" fill-opacity=".07"/>'
             f'<path transform="translate({ux+11} {by+11})" d="M2 5V3.6a2.6 2.6 0 0 1 5.2 0V5 M1 5h7.2v5H1z" stroke="{CYAN}" stroke-width="1.2" stroke-linejoin="round"/>'
             f'<text x="{ux+28}" y="{by+21}" class="m" font-size="12" fill="{INK}" fill-opacity=".9">{url}</text>'
             f'<rect x="{f(ux+28+text_w(url,"m4",12)+3)}" y="{by+10}" width="7" height="14" fill="{CYAN}">{anim("opacity",[1,1,0,0],1.1,[0,.5,.5,1],calc="discrete")}</rect>')
    # illustration: code editor (left) and phone (right)
    ix, iy = bx, by + 34
    o.append(f'<rect x="{ix}" y="{iy}" width="{bw}" height="{bh-34}" fill="url(#{P}dots)"/>')
    o.append(f'<defs><radialGradient id="{P}ph"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".4"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient></defs>'
             f'<ellipse cx="{ix+342}" cy="{iy+92}" rx="130" ry="95" fill="url(#{P}ph)"/>')
    lines = [(0, 90, CYAN), (0, 130, VIOLET), (1, 110, PINK), (1, 70, INK), (2, 140, CYAN), (2, 90, VIOLET), (1, 60, PINK), (0, 40, INK), (0, 110, VIOLET)]
    for k, (ind, ln, col) in enumerate(lines):
        y = iy + 20 + k * 17
        o.append(f'<text x="{ix+18}" y="{y+8}" class="m" font-size="9" fill="{FAINT}">{k+1:>2}</text>'
                 f'<rect x="{ix+42+ind*16}" y="{y}" width="{ln}" height="8" rx="4" fill="{col}" fill-opacity=".8">{ent("width", 0, ln, .3 + k * .12, .7)}</rect>')
    # phone
    px, py, pw, ph = ix + 292, iy + 14, 100, 150
    o.append(f'<g>{tent("translate", "0 18", "0 0", .5, 1.0)}{ent("opacity", 0, 1, .5, .8)}'
             f'<rect x="{px}" y="{py}" width="{pw}" height="{ph+14}" rx="16" fill="#0d0e16" stroke="{VIOLET}" stroke-opacity=".7" stroke-width="1.6"/>'
             f'<rect x="{px+34}" y="{py+6}" width="32" height="4" rx="2" fill="#fff" fill-opacity=".18"/>'
             f'<rect x="{px+8}" y="{py+18}" width="{pw-16}" height="34" rx="9" fill="url(#{P}aurd)" fill-opacity=".85"/>'
             f'{icon("flutter", px+16, py+26, 18, "#fff")}'
             f'<rect x="{px+42}" y="{py+28}" width="36" height="5" rx="2.5" fill="#fff" fill-opacity=".85"/><rect x="{px+42}" y="{py+38}" width="24" height="4" rx="2" fill="#fff" fill-opacity=".5"/>')
    for k in range(3):
        yy = py + 60 + k * 27
        o.append(f'<rect x="{px+8}" y="{yy}" width="{pw-16}" height="22" rx="7" fill="#fff" fill-opacity=".06"/>'
                 f'<circle cx="{px+21}" cy="{yy+11}" r="6" fill="{(CYAN, PINK, VIOLET)[k]}" fill-opacity=".85"/>'
                 f'<rect x="{px+32}" y="{yy+6}" width="{40-k*6}" height="4" rx="2" fill="#fff" fill-opacity=".55"/><rect x="{px+32}" y="{yy+13}" width="{28}" height="3" rx="1.5" fill="#fff" fill-opacity=".25"/>')
    o.append(f'<circle cx="{px+pw-4}" cy="{py+22}" r="7" fill="{PINK}"><animate attributeName="r" values="7;8.5;7" dur="2s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{px+pw-4}" cy="{py+22}" r="7" fill="none" stroke="{PINK}" opacity="0">{anim("r", [7, 18], 2, [0, 1])}{anim("opacity", [.8, 0], 2, [0, 1])}</circle></g>')
    o.append('</g>')
    # capability rows
    rows = [("flutter", "Mobile apps", "Flutter, React Native, Dart", CYAN),
            ("react", "Web interfaces", "React, Next.js, Tailwind CSS", VIOLET),
            ("fastapi", "Backends and APIs", "Node.js, FastAPI, Firebase, Supabase", PINK)]
    for k, (ic, t, sub, col) in enumerate(rows):
        y = 262 + k * 62
        o.append(f'<g>{tent("translate", "-24 0", "0 0", .9 + k * .18, .9)}{ent("opacity", 0, 1, .9 + k * .18, .7)}'
                 f'{glass(24, y, 440, 52, 16, .04, .08)}'
                 f'<rect x="36" y="{y+6}" width="40" height="40" rx="12" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>'
                 f'{icon(ic, 46, y+16, 20, col)}'
                 f'<text x="92" y="{y+23}" class="dm" font-size="14" fill="{INK}">{t}</text>'
                 f'<text x="92" y="{y+40}" class="m" font-size="12" fill="{MUTE}">{esc(sub)}</text>'
                 f'<rect x="{464-26}" y="{y+22}" width="8" height="8" rx="4" fill="{col}">{anim("opacity",[.35,1,.35],2.4,[0,.5,1],begin=f"{-k*.8}s")}</rect></g>')
    return "".join(o)


# ---------------------------------------------------------------- right: hobby carousel
def ball():
    g = []
    pent = lambda cx, cy, r, rot=-90: " ".join(f"{f(cx + r*math.cos(math.radians(rot+72*k)))},{f(cy + r*math.sin(math.radians(rot+72*k)))}" for k in range(5))
    g.append(f'<clipPath id="{P}ballc"><circle r="60"/></clipPath><circle r="60" fill="#f1f2fa"/><g clip-path="url(#{P}ballc)" fill="#12131d" stroke="#12131d" stroke-linejoin="round">'
             f'<polygon points="{pent(0,0,19)}" stroke-width="2"/>')
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        g.append(f'<line x1="{f(19*math.cos(a))}" y1="{f(19*math.sin(a))}" x2="{f(46*math.cos(a))}" y2="{f(46*math.sin(a))}" stroke-width="3"/>'
                 f'<polygon points="{pent(58*math.cos(a), 58*math.sin(a), 17, -90+72*k+36)}" stroke-width="2"/>')
    g.append(f'</g><circle r="60" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>')
    return "".join(g)


def art_football():
    return (f'<ellipse cx="220" cy="176" rx="90" ry="9" fill="#000" opacity=".45"/>'
            f'<path d="M30 150 C 90 40, 150 40, 190 80" stroke="{CYAN}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round">'
            f'{anim("stroke-dashoffset",[0,-40],2,[0,1])}</path>'
            f'<path d="M420 130 C 380 60, 340 60, 300 84" stroke="{PINK}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round">'
            f'{anim("stroke-dashoffset",[0,40],2,[0,1])}</path>'
            f'<g transform="translate(220 96)"><g>{tanim("rotate",["0 0 0","360 0 0"],14)}{ball()}</g></g>'
            f'<g stroke="#fff" stroke-opacity=".1"><path d="M0 188H440M40 170H400M90 152H350"/></g>')


def art_khokho():
    g = [f'<path d="M50 100H390" stroke="#fff" stroke-opacity=".28" stroke-width="2"/>']
    for k in range(8):
        x = 96 + k * 36
        up = k % 2 == 0
        g.append(f'<rect x="{x-9}" y="{100-27 if up else 100+9}" width="18" height="18" rx="5" fill="{VIOLET}" fill-opacity="{.85 if up else .5}"/>'
                 f'<path d="M{x} 100V{100-9 if up else 100+9}" stroke="#fff" stroke-opacity=".28" stroke-width="2"/>')
    for x in (50, 390):
        g.append(f'<circle cx="{x}" cy="100" r="8" fill="#0d0e16" stroke="{CYAN}" stroke-width="2.5"/>')
    path = "M0 0 c20 -40 60 -40 80 0 c20 40 60 40 80 0 c20 -40 60 -40 80 0 c20 40 60 40 80 0 l-320 0"
    g.append(f'<g transform="translate(60 100)"><circle r="16" fill="{PINK}" opacity=".18"/><circle r="8" fill="{PINK}"/>'
             f'<animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></g>'
             f'<g transform="translate(60 100)"><circle r="7" fill="{CYAN}"/>'
             f'<animateMotion dur="7s" repeatCount="indefinite" path="M0 0 l320 0 l-320 0"/></g>')
    return "".join(g)


def art_apps():
    g = [f'<circle cx="220" cy="100" r="40" fill="none" stroke="{CYAN}" opacity="0">{anim("r",[40,110],3,[0,1])}{anim("opacity",[.5,0],3,[0,1])}</circle>',
         f'<path d="M120 60L180 90M320 60L260 90M120 150L180 120M320 150L260 120" stroke="#fff" stroke-opacity=".25" stroke-dasharray="3 5">{anim("stroke-dashoffset",[0,-16],1.2,[0,1])}</path>',
         f'<rect x="170" y="14" width="100" height="172" rx="20" fill="#0d0e16" stroke="{CYAN}" stroke-width="2"/>'
         f'<rect x="178" y="26" width="84" height="148" rx="12" fill="url(#{P}aurd)" fill-opacity=".9"/>'
         f'{icon("flutter", 200, 62, 40, "#fff")}<rect x="192" y="124" width="56" height="6" rx="3" fill="#fff" fill-opacity=".85"/><rect x="200" y="138" width="40" height="5" rx="2.5" fill="#fff" fill-opacity=".5"/>']
    for k, (ic, x, y, col, ph) in enumerate((("dart", 68, 40, CYAN, 0), ("firebase", 316, 40, "#FFCA28", 1.1), ("nodedotjs", 68, 118, "#8CC84B", 2.2), ("supabase", 316, 118, "#3ECF8E", 3.3))):
        g.append(f'<g transform="translate({x} {y})"><g>{tanim("translate",["0 0","0 -7","0 0"],3.6,[0,.5,1],begin=f"{-ph}s")}'
                 f'<rect width="56" height="56" rx="16" fill="#0d0e16" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>{icon(ic, 14, 14, 28, col)}</g></g>')
    return "".join(g)


def art_dsa():
    nodes = {8: (220, 32), 3: (140, 80), 10: (300, 80), 1: (96, 130), 6: (184, 130), 14: (348, 130), 4: (150, 176), 7: (218, 176)}
    edges = [(8, 3), (8, 10), (3, 1), (3, 6), (10, 14), (6, 4), (6, 7)]
    path = [8, 3, 6, 4]
    g = []
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#fff" stroke-opacity=".22" stroke-width="2"/>')
    pts = [nodes[v] for v in path]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    g.append(f'<path d="{d}" pathLength="1" stroke="url(#{P}aur)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="0">'
             f'{anim("stroke-dashoffset",[1,0,0,1],5,[0,.45,.9,1])}</path>')
    for v, (x, y) in nodes.items():
        on = v in path; i = path.index(v) if on else 0
        g.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#0d0e16" stroke="{CYAN if on else "#fff"}" stroke-opacity="{1 if on else .35}" stroke-width="2"/>'
                 f'<text x="{x}" y="{y+4.5}" text-anchor="middle" class="mb" font-size="13" fill="{INK}">{v}</text>')
        if on:
            g.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{CYAN}" opacity="0">{anim("opacity",[0,.45,0,0],5,[0,(.1+i*.11),(.2+i*.11),1])}</circle>')
    g.append(f'<text x="420" y="40" text-anchor="end" class="mb" font-size="15" fill="{PINK}">O(log n)</text>'
             f'<text x="420" y="60" text-anchor="end" class="m" font-size="12" fill="{MUTE}">search(4)</text>')
    return "".join(g)


def right():
    o = [card(P, RX, 0, CW, H, 28, glow=[(480, 40, 300, PINK, .13), (40, 440, 320, CYAN, .13)], key="R")]
    o.append(f'<text x="{RX+24}" y="50" class="dm" font-size="16" fill="{INK}">Off the keyboard</text>')
    slides = [("Football", "First place, U-19 Football Championship, Jaipur Regional, 2019.", art_football, CYAN),
              ("Kho-Kho", "Second place twice, in the U-14 and U-17 championships.", art_khokho, VIOLET),
              ("Building apps", "Flutter and Firebase projects, from NoteIt to the Minati payment app.", art_apps, CYAN),
              ("Problem solving", "Data structures and algorithms in C++, Java and Python.", art_dsa, PINK)]
    n = len(slides)
    # Instagram-style segmented progress
    sx, sw_, gap = RX + 24, (440 - 3 * 6) / 4, 6
    for i in range(n):
        x = sx + i * (sw_ + gap)
        a, b = i / n, (i + 1) / n
        kt = [0, a, b, 1] if i else [0, b, 1]
        v = [0, 0, sw_, sw_] if i else [0, sw_, sw_]
        o.append(f'<rect x="{f(x)}" y="68" width="{f(sw_)}" height="3.5" rx="1.75" fill="#fff" fill-opacity=".16"/>'
                 f'<rect x="{f(x)}" y="68" width="{f(sw_)}" height="3.5" rx="1.75" fill="url(#{P}aur)">{anim("width", v, LOOP, kt)}</rect>')
    # slides
    o.append(f'<defs><clipPath id="{P}car"><rect x="{RX+24}" y="84" width="440" height="296"/></clipPath></defs><g clip-path="url(#{P}car)">')
    for i, (t, sub, art, col) in enumerate(slides):
        kt, op, xo = cycle_pts(n, i, fade=.04, off=44)
        o.append(f'<g opacity="{1 if i == 0 else 0}"><g transform="translate(0 0)">'
                 f'<g transform="translate({RX+24} 86)">'
                 f'<rect width="440" height="200" rx="20" fill="#08090f" stroke="#fff" stroke-opacity=".09"/>'
                 f'<clipPath id="{P}sl{i}"><rect width="440" height="200" rx="20"/></clipPath>'
                 f'<g clip-path="url(#{P}sl{i})"><rect width="440" height="200" fill="url(#{P}dots)"/>'
                 f'<circle cx="220" cy="100" r="150" fill="{col}" fill-opacity=".07"/>{art()}</g></g>'
                 f'<text x="{RX+24}" y="326" class="d" font-size="18" fill="{INK}">{t}</text>'
                 + "".join(f'<text x="{RX+24}" y="{350+j*17}" class="m" font-size="12.5" fill="{MUTE}">{esc(ln)}</text>' for j, ln in enumerate(textwrap.wrap(sub, 54))) +
                 f'{tanim("translate", [f"{v} 0" for v in xo], LOOP, kt)}</g>'
                 f'{anim("opacity", op, LOOP, kt)}</g>')
    o.append('</g>')
    # daily rings
    rings = [("Build", CYAN, 82), ("Move", PINK, 64), ("Learn", VIOLET, 71)]
    for k, (lab, col, pct) in enumerate(rings):
        cx, cy = RX + 24 + 22 + k * 150, 416
        o.append(f'<circle cx="{cx}" cy="{cy}" r="17" stroke="#fff" stroke-opacity=".1" stroke-width="5"/>'
                 f'<g transform="rotate(-90 {cx} {cy})"><circle cx="{cx}" cy="{cy}" r="17" pathLength="100" stroke="{col}" stroke-width="5" stroke-linecap="round" '
                 f'stroke-dasharray="100 100" stroke-dashoffset="{100-pct}">'
                 f'{anim("stroke-dashoffset", [100, 100-pct, 100-pct, 100], 7, [0, .35, .88, 1], splines=[EASE, LIN, "0.4 0 1 1"])}</circle></g>'
                 f'<text x="{cx+32}" y="{cy-2}" class="dm" font-size="13" fill="{INK}">{lab}</text>'
                 f'<text x="{cx+32}" y="{cy+14}" class="m" font-size="11" fill="{MUTE}">daily goal</text>')
    return "".join(o)


def build():
    return svg_open(W, H, P, ("d5", "d7", "m4", "m7")) + left() + right() + "</svg>"


if __name__ == "__main__":
    write("about-life.svg", build())
