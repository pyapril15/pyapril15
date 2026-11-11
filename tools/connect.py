from PIL import Image
from common import *

W, H, P = 1000, 400, "c"


def build():
    iw, ih = Image.open(f"{ASSETS}/pointing.png").size
    imh = 372; imw = imh * iw / ih; ix, iy = 22, 14
    o = [svg_open(W, H, P, ("d7", "d5", "m4", "m7"))]
    o.append(card(P, 0, 0, W, H, 28, glow=[(120, 220, 300, VIOLET, .2), (800, 60, 340, CYAN, .13), (900, 380, 300, PINK, .13)]))

    # character: edges feathered by a blurred inset mask so the art melts into the card
    o.append(f'<defs><filter id="{P}fb" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="11"/></filter>'
             f'<mask id="{P}pm" maskUnits="userSpaceOnUse" x="{ix-10}" y="{iy-10}" width="{f(imw+20)}" height="{imh+20}">'
             f'<rect x="{ix+16}" y="{iy+14}" width="{f(imw-32)}" height="{imh-26}" rx="12" fill="#fff" filter="url(#{P}fb)"/></mask></defs>'
             f'<g mask="url(#{P}pm)"><g>{tanim("translate", ["0 0", "0 -4", "0 0"], 5, [0, .5, 1], splines=["0.37 0 0.63 1"] * 2)}'
             f'<image x="{ix}" y="{iy}" width="{f(imw)}" height="{imh}" href="data:image/png;base64,{b64file(f"{ASSETS}/pointing.png")}"/></g></g>')

    # neon sign (native SVG, so it stays crisp), the character points at it
    sx, sy = 300, 90
    sign = f'@{CFG["handle"]}'
    o.append(f'<defs><filter id="{P}glow" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>'
             f'<linearGradient id="{P}neon" gradientUnits="userSpaceOnUse" x1="{sx}" y1="0" x2="{sx+380}" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>'
             f'<g>{ent("opacity", 0, 1, .3, .8)}'
             f'<text x="{sx}" y="{sy}" class="d" font-size="46" fill="url(#{P}neon)" filter="url(#{P}glow)" opacity=".75">{sign}'
             f'{anim("opacity", [.75, .75, .45, .75, .6, .75, .75], 7, [0, .6, .62, .64, .66, .68, 1])}</text>'
             f'<text x="{sx}" y="{sy}" class="d" font-size="46" fill="none" stroke="url(#{P}neon)" stroke-width="2" stroke-linejoin="round">{sign}</text>'
             f'<text x="{sx}" y="{sy}" class="d" font-size="46" fill="#fff" fill-opacity=".14">{sign}</text></g>'
             f'<text x="{sx+2}" y="122" class="m" font-size="13" fill="{MUTE}">Open to collabs. Ask me about Flutter, React or REST APIs.</text>')

    # link cards
    cards = [("LinkedIn", "praveenyadavme", CYAN, "in"), ("Portfolio", CFG["portfolio"], VIOLET, "link"),
             ("Instagram", "praveen.yadav.in", PINK, "instagram"), ("Email", CFG["email"], CYAN, "gmail")]
    cx0, cw, ch, gap = 300, 332, 100, 16
    for k, (title, sub, col, ic) in enumerate(cards):
        x = cx0 + (k % 2) * (cw + gap); y = 150 + (k // 2) * (ch + gap)
        d = .5 + k * .15
        if ic == "in": g = linkedin_glyph(x + 30, y + 30, 26, col)
        elif ic == "link": g = f'<g transform="translate({x+30} {y+30}) scale(1.6)"><path d="M6.8 9.2a2.6 2.6 0 0 0 3.7 0l2.2-2.2a2.6 2.6 0 0 0-3.7-3.7L8.2 4.1 M9.2 6.8a2.6 2.6 0 0 0-3.7 0L3.3 9a2.6 2.6 0 0 0 3.7 3.7l.8-.8" stroke="{col}" stroke-width="1.5" stroke-linecap="round" fill="none"/></g>'
        else: g = icon(ic, x + 30, y + 30, 26, col if ic != "gmail" else "#f87171")
        sw = 8 if k == 0 else 0
        o.append(f'<g>{tent("translate", "40 0", "0 0", d, .9)}{ent("opacity", 0, 1, d, .7)}'
                 f'{glass(x, y, cw, ch, 20, .045, .1)}'
                 f'<rect x="{x+.5}" y="{y+.5}" width="{cw-1}" height="{ch-1}" rx="19.5" stroke="{col}" stroke-opacity=".28"/>'
                 f'<rect x="{x+18}" y="{y+18}" width="64" height="64" rx="18" fill="{col}" fill-opacity=".13" stroke="{col}" stroke-opacity=".5"/>'
                 f'{g}'
                 f'<text x="{x+98}" y="{y+44}" class="dm" font-size="16" fill="{INK}">{title}</text>'
                 f'<text x="{x+98}" y="{y+66}" class="m" font-size="{11.5 if text_w(sub, "m4", 12) > 170 else 12}" fill="{MUTE}">{esc(sub)}</text>'
                 f'<g transform="translate({x+cw-46} {y+ch/2-9})">{tanim("translate", [f"{x+cw-46} {y+ch/2-9}", f"{x+cw-46} {y+ch/2-9}", f"{x+cw-37} {y+ch/2-9}", f"{x+cw-46} {y+ch/2-9}", f"{x+cw-46} {y+ch/2-9}"], 2.8, [0, .05 + k * .07, .25 + k * .07, .5 + k * .07, 1])}'
                 f'{arrow(0, 0, col, 18, 2.2)}</g></g>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("connect.svg", build())
