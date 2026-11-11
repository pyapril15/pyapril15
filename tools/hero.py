import glob, os
from PIL import Image
from common import *

W, H, P = 1000, 440, "h"
ROLES = ["Full Stack & Mobile Developer", "Flutter and React, shipped end to end", "Node.js, FastAPI and Firebase backends"]
LOOP = 4.0                      # viewfinder loop: play ~2s, hold last frame ~1.4s, fade, repeat
FX, FY, FW, FH = 604, 40, 348, 360   # viewfinder frame


def frames():
    fr = sorted(glob.glob(os.path.join(HERE, "frames", "f*.png")))
    return fr or [os.path.join(ASSETS, "hero_still.png")]


def build():
    fl = frames(); n = len(fl); live = n > 1
    iw, ih = Image.open(fl[0]).size
    imw = 350; imh = imw * ih / iw
    imx, imy = FX + (FW - imw) / 2, FY + 6
    o = [svg_open(W, H, P, ("d7", "m4", "m7"))]
    o.append(card(P, 0, 0, W, H, 28, glow=[(130, 40, 380, CYAN, .15), (900, 420, 430, VIOLET, .2), (780, 150, 300, PINK, .13)]))

    # ---- open to collabs pill
    pw = 40 + text_w("open to collabs", "m4", 13) + 18
    o.append(f'<g>{glass(52, 44, f(pw), 30, 15, .05, .12)}'
             f'<circle cx="71" cy="59" r="4.5" fill="{CYAN}"/>'
             f'<circle cx="71" cy="59" r="4.5" fill="none" stroke="{CYAN}" stroke-width="1.5" opacity="0">'
             f'{anim("r", [4.5, 13], 2.2, [0, 1])}{anim("opacity", [.7, 0], 2.2, [0, 1])}</circle>'
             f'<text x="88" y="64" class="m" font-size="13" fill="{INK}">open to collabs</text>'
             f'{ent("opacity", 0, 1, 0, .6)}</g>')

    # ---- typed greeting
    s1 = "Hi there, I’m"; cw = text_w("a", "m4", 20); d0, step = .5, .06
    tot = d0 + len(s1) * step + .4
    xs = [0] + [cw * (k + 1) for k in range(len(s1))]
    kt = [0] + [(d0 + k * step) / tot for k in range(len(s1))]
    vals = [0] + xs[1:]
    kt2 = kt + [1]; vals2 = vals + [vals[-1]]
    o.append(f'<clipPath id="{P}typ"><rect x="52" y="96" width="{f(cw*len(s1)+2)}" height="30">'
             f'{anim("width", [f(v) for v in vals2], tot, kt2, loop=False, calc="discrete")}</rect></clipPath>'
             f'<text x="52" y="118" class="m" font-size="20" fill="{MUTE}" clip-path="url(#{P}typ)">{esc(s1)}</text>'
             f'<rect x="{f(52+cw*len(s1))}" y="101" width="9" height="19" fill="{CYAN}" opacity="0">'
             f'{anim("x", [f(52+v) for v in vals2], tot, kt2, loop=False, calc="discrete")}'
             f'{anim("opacity", [1, 1, 0], tot, [0, (d0+len(s1)*step)/tot+.1, (d0+len(s1)*step)/tot+.1+.001], loop=False, calc="discrete")}</rect>')

    # ---- name: gradient + rising mask
    o.append(f'<linearGradient id="{P}ng" gradientUnits="userSpaceOnUse" x1="52" y1="0" x2="452" y2="0" spreadMethod="repeat">'
             f'<stop offset="0" stop-color="{CYAN}"/><stop offset=".33" stop-color="{VIOLET}"/><stop offset=".66" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>'
             f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;400 0" dur="6s" repeatCount="indefinite"/></linearGradient>'
             f'<mask id="{P}nm" maskUnits="userSpaceOnUse" x="30" y="130" width="560" height="160">'
             f'<rect x="30" y="130" width="560" height="160" fill="#fff">{ent("y", 290, 130, 1.0, 1.1)}{ent("height", 0, 160, 1.0, 1.1)}</rect></mask>'
             f'<g mask="url(#{P}nm)"><g>{tent("translate", "0 22", "0 0", 1.0, 1.1)}'
             f'<text x="50" y="198" class="d" font-size="72" fill="url(#{P}ng)" letter-spacing="-1">{CFG["first"]}</text>'
             f'<text x="50" y="270" class="d" font-size="72" fill="url(#{P}ng)" letter-spacing="-1">{CFG["last"]}</text></g></g>')

    # ---- cycling role lines
    nr = len(ROLES); per = 9.0
    for i, r in enumerate(ROLES):
        kt, op, xo = cycle_pts(nr, i, fade=.035, off=14)
        o.append(f'<g opacity="{1 if i == 0 else 0}"><g>'
                 f'<text x="52" y="318" class="mb" font-size="18" fill="{CYAN}">&gt;</text>'
                 f'<text x="76" y="318" class="mb" font-size="18" fill="{INK}">{esc(r)}</text>'
                 f'{tanim("translate", [f"{v} 0" for v in xo], per, kt)}</g>'
                 f'{anim("opacity", op, per, kt)}</g>')

    # ---- pitch
    o.append(f'<text x="52" y="354" class="m" font-size="14" fill="{MUTE}">{esc(CFG["pitch"])}{ent("opacity", 0, 1, 1.9, .8)}</text>')

    # ---- meta row with drawn icons
    items = [("pin", CFG["location"], CYAN), ("building", CFG["company"], VIOLET),
             ("star", f'{STATS["stars"]} stars', PINK), ("repo", f'{STATS["repos"]} repos', CYAN)]
    x = 52
    for k, (ic, tx, col) in enumerate(items):
        o.append(stroke_icon(ic, x, 380, col, delay=1.6 + k * .25))
        o.append(f'<text x="{f(x+24)}" y="393" class="m" font-size="13" fill="{INK}" fill-opacity=".85">{esc(tx)}</text>')
        x += 24 + text_w(tx, "m4", 13) + 26

    # ---- viewfinder
    o.append(f'<defs><clipPath id="{P}vf"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="20"/></clipPath>'
             f'<radialGradient id="{P}vmg" gradientUnits="userSpaceOnUse" cx="{FX+FW/2}" cy="{FY+FH*.5}" r="205" '
             f'gradientTransform="translate({FX+FW/2} {FY+FH*.5}) scale(1 1.04) translate({-(FX+FW/2)} {-(FY+FH*.5)})">'
             f'<stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#fff"/><stop offset=".97" stop-color="#000"/></radialGradient>'
             f'<mask id="{P}vm" maskUnits="userSpaceOnUse" x="{FX}" y="{FY}" width="{FW}" height="{FH}"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="url(#{P}vmg)"/></mask>'
             f'<radialGradient id="{P}vglow" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".38"/><stop offset=".6" stop-color="{CYAN}" stop-opacity=".08"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="{P}scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>')
    o.append(f'<g clip-path="url(#{P}vf)">'
             f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="#07080e" fill-opacity=".55"/>'
             f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="url(#{P}vglow)"/>'
             f'<g stroke="#fff" stroke-opacity=".08" stroke-dasharray="3 6">'
             f'<path d="M{FX+FW/3} {FY}V{FY+FH}M{FX+2*FW/3} {FY}V{FY+FH}M{FX} {FY+FH/3}H{FX+FW}M{FX} {FY+2*FH/3}H{FX+FW}"/></g>')
    # character (frames or still), melted into the card by the radial mask
    o.append(f'<g mask="url(#{P}vm)"><g>{tanim("translate", ["0 0", "0 -3", "0 0"], 4, [0, .5, 1]) if not live else ""}')
    if live:
        o.append("<g>")
        for i, fp in enumerate(fl):
            a, b = i / n * .5, (i + 1) / n * .5
            if i == 0: kts, v = [0, b], [1, 0]
            elif i == n - 1: kts, v = [0, a, .88], [0, 1, 0]
            else: kts, v = [0, a, b], [0, 1, 0]
            o.append(f'<image x="{f(imx)}" y="{f(imy)}" width="{imw}" height="{f(imh)}" opacity="{1 if i == n-1 else 0}" '
                     f'href="data:image/png;base64,{b64file(fp)}">{anim("opacity", v, LOOP, kts, calc="discrete")}</image>')
        o.append(f'{anim("opacity", [0, 1, 1, 0, 0], LOOP, [0, .06, .88, .97, 1])}</g>')
    else:
        o.append(f'<image x="{f(imx)}" y="{f(imy)}" width="{imw}" height="{f(imh)}" href="data:image/png;base64,{b64file(fl[0])}"/>')
    o.append('</g></g>')
    # scrims so the label row and scrubber stay legible over the artwork
    o.append(f'<defs><linearGradient id="{P}scb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07080e" stop-opacity="0"/><stop offset="1" stop-color="#07080e" stop-opacity=".92"/></linearGradient>'
             f'<linearGradient id="{P}sct" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#07080e" stop-opacity="0"/><stop offset="1" stop-color="#07080e" stop-opacity=".7"/></linearGradient></defs>'
             f'<rect x="{FX}" y="{FY+FH-96}" width="{FW}" height="96" fill="url(#{P}scb)"/>'
             f'<rect x="{FX}" y="{FY}" width="{FW}" height="64" fill="url(#{P}sct)"/>')
    # scan line
    o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="46" fill="url(#{P}scan)" opacity=".55">'
             f'{anim("y", [FY-46, FY+FH], LOOP, [0, 1])}</rect></g>')
    # corner brackets that draw in
    L = 30; ins = 12
    br = [(FX + ins, FY + ins, 1, 1, CYAN), (FX + FW - ins, FY + ins, -1, 1, VIOLET),
          (FX + FW - ins, FY + FH - ins, -1, -1, PINK), (FX + ins, FY + FH - ins, 1, -1, VIOLET)]
    for k, (cx, cy, sx, sy, col) in enumerate(br):
        d = f"M{cx} {cy+sy*L}V{cy+sy*8}Q{cx} {cy} {cx+sx*8} {cy}H{cx+sx*L}"
        o.append(f'<path d="{d}" pathLength="1" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="0">'
                 f'{ent("stroke-dashoffset", 1, 0, .2 + k * .12, .8)}</path>')
    # REC + timecode
    rx_, ry_ = FX + 42, FY + 36
    o.append(f'<circle cx="{rx_}" cy="{ry_}" r="9" fill="{PINK}" opacity=".22">{anim("opacity", [.28, .04, .28], 1.2, [0, .5, 1])}</circle>'
             f'<circle cx="{rx_}" cy="{ry_}" r="5" fill="{PINK}">{anim("opacity", [1, .15, 1], 1.2, [0, .5, 1])}</circle>'
             f'<text x="{rx_+14}" y="{ry_+4.5}" class="mb" font-size="12" fill="{PINK}">REC</text>')
    tc = ["00:00", "00:01", "00:02"]
    for i, t in enumerate(tc):
        kts = [[0, .25], [0, .25, .5], [0, .5, 1]][i]
        vv = [[1, 0], [0, 1, 0], [0, 1, 0]][i]
        base = 1 if i == 2 else 0
        o.append(f'<text x="{FX+FW-42}" y="{ry_+4.5}" text-anchor="end" class="m" font-size="12" fill="{INK}" fill-opacity=".8" opacity="{base}">{t}'
                 f'{anim("opacity", vv, LOOP, kts, calc="discrete")}</text>')
    # filename + scrubber (synced to the 4s loop)
    sx0, sx1 = FX + 30, FX + FW - 30; sl = sx1 - sx0; sy = FY + FH - 28
    o.append(f'<text x="{sx0}" y="{sy-12}" class="m" font-size="12" fill="{MUTE}">praveen_wave.mov</text>'
             f'<text x="{sx1}" y="{sy-12}" text-anchor="end" class="m" font-size="12" fill="{FAINT}">12 fps</text>'
             f'<rect x="{sx0}" y="{sy}" width="{sl}" height="4" rx="2" fill="#fff" fill-opacity=".13"/>'
             f'<rect x="{sx0}" y="{sy}" width="{sl}" height="4" rx="2" fill="url(#{P}aur)">'
             f'{anim("width", [0, sl, sl, 0, 0], LOOP, [0, .5, .9, .97, 1])}</rect>'
             f'<circle cx="{sx1}" cy="{sy+2}" r="6" fill="#fff">'
             f'{anim("cx", [sx0, sx1, sx1, sx0, sx0], LOOP, [0, .5, .9, .97, 1])}</circle>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    write("hero.svg", build())
