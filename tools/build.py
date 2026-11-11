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
