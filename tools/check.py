"""Render an SVG in headless Chromium and save screenshots.
   python check.py hero.svg 0.4,1.5,3.2     -> shots at those SMIL times, plus <img> mode and animation-stripped mode
"""
import os, re, sys
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "/home/claude/build/shots"; os.makedirs(OUT, exist_ok=True)


def dims(svg):
    m = re.search(r'<svg[^>]*width="(\d+)"[^>]*height="(\d+)"', svg)
    return int(m.group(1)), int(m.group(2))


def strip_anim(svg):
    svg = re.sub(r"<animate(?:Transform|Motion)?\b[^>]*/>", "", svg)
    svg = re.sub(r"<(animate(?:Transform|Motion)?)\b[^>]*>.*?</\1>", "", svg, flags=re.S)
    return svg


def run(name, times, scale=1):
    path = os.path.join(ROOT, name); svg = open(path, encoding="utf-8").read(); w, h = dims(svg)
    base = os.path.splitext(name)[0]
    stat = os.path.join(OUT, f"{base}_static.svg"); open(stat, "w", encoding="utf-8").write(strip_anim(svg))
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
        pg.on("console", lambda m: errs.append(m.text) if m.type in ("error", "warning") else None)
        pg.on("requestfailed", lambda r: errs.append("REQ FAIL " + r.url[:80]))
        pg.goto("file://" + path); pg.evaluate("document.fonts.ready.then(()=>1)"); pg.wait_for_timeout(400)
        for t in times:
            pg.evaluate(f"(()=>{{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime({t});}})()")
            pg.wait_for_timeout(120)
            pg.screenshot(path=f"{OUT}/{base}_t{t}.png")
        # <img> mode, exactly how a README embeds it (no JS, fonts must come from the data: URIs)
        for tag, src, wait in (("img", path, 3000), ("static", stat, 800)):
            hp = os.path.join(OUT, f"{base}_{tag}.html")
            open(hp, "w").write(f'<body style="margin:0;background:#0d1117"><img src="file://{src}" width="{w}" height="{h}">')
            pgx = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            pgx.goto("file://" + hp); pgx.wait_for_timeout(wait); pgx.screenshot(path=f"{OUT}/{base}_{tag}.png")
        b.close()
    print(name, f"{w}x{h}", "console:", errs[:5] or "clean")


if __name__ == "__main__":
    run(sys.argv[1], [x for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else ["1"], float(sys.argv[3]) if len(sys.argv) > 3 else 1)
