"""Build every card.   cd tools && python build.py"""
import os
import hero, about, stack, dashboard, connect
from common import write, OUT

write("hero.svg", hero.build())
write("about-life.svg", about.build())
write("stack.svg", stack.build())
write("id-dashboard.svg", dashboard.build())
write("connect.svg", connect.build())

# Placeholder so the README image is never broken before the first workflow run.
# The yoshi389111/github-profile-3d-contrib action overwrites this exact path.
os.makedirs(f"{OUT}/profile-3d-contrib", exist_ok=True)
open(f"{OUT}/profile-3d-contrib/profile-night-view.svg", "w").write(
    '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="260" viewBox="0 0 1000 260" fill="none">'
    '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee" stop-opacity=".7"/><stop offset=".5" stop-color="#a78bfa" stop-opacity=".35"/><stop offset="1" stop-color="#f472b6" stop-opacity=".7"/></linearGradient></defs>'
    '<rect width="1000" height="260" rx="28" fill="#0d0e16"/><rect x=".6" y=".6" width="998.8" height="258.8" rx="27.4" stroke="url(#g)" stroke-width="1.2"/>'
    '<g fill="#22d3ee" fill-opacity=".25"><rect x="150" y="150" width="40" height="60"/><rect x="200" y="120" width="40" height="90"/><rect x="250" y="160" width="40" height="50"/><rect x="700" y="130" width="40" height="80"/><rect x="750" y="100" width="40" height="110"/><rect x="800" y="150" width="40" height="60"/></g>'
    '<text x="500" y="122" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="18" fill="#e7e9f5">Your 3D contribution city appears here</text>'
    '<text x="500" y="150" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="#8a8fab">Actions tab, run "GitHub-Profile-3D-Contrib" once. It refreshes daily after that.</text></svg>')
print("profile-3d-contrib/profile-night-view.svg (placeholder)")

# ---- README: live "Latest repositories" table + automatic cache-busting (?v=<content hash>)
import hashlib, json, re
from common import STATS
rd = f"{OUT}/README.md"
txt = open(rd, encoding="utf-8").read()
rows = []
for r in STATS.get("recent", []):
    desc = (r["desc"] or "No description yet").replace("|", "/").strip()
    desc = desc if len(desc) <= 110 else desc[:107] + "..."
    rows.append(f"| [**{r['name']}**](https://github.com/{STATS['user']}/{r['name']}) | {desc} | {r['lang'] or '-'} | {r['stars']} |")
table = "| Repository | About | Language | Stars |\n| :-- | :-- | :-- | --: |\n" + "\n".join(rows)
txt = re.sub(r"(<!--REPOS:START-->).*?(<!--REPOS:END-->)", lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}", txt, flags=re.S)

def bust(m):
    p = m.group(1)
    h = hashlib.md5(open(f"{OUT}/{p[2:]}", "rb").read()).hexdigest()[:8]
    return f"{p}?v={h}"
txt = re.sub(r"(\./[\w\-/]+\.svg)\?v=\w+", bust, txt)
open(rd, "w", encoding="utf-8").write(txt)
print("README refreshed (latest repos + cache-bust)")
