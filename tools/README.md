# tools

Everything in the repo root (`*.svg`) is generated from here. Fonts, icons and images are embedded as base64,
so the cards need no network and look identical everywhere.

    pip install -r requirements.txt
    python update_stats.py     # refresh repos / stars / followers from your public profile
    python build.py            # rewrite all five cards

Other scripts
- `make_assets.py 1.png 2.png [wave.mp4]`: re-cut the character art, and (optionally) extract and matte every frame of a video for the hero.
- `check.py hero.svg 0.5,2,3.5`: render a card in headless Chromium at those SMIL times, plus `<img>` mode and an animation-stripped mode.

Edit your details (name, links, location, pitch) in `common.py`, the `CFG` block.
Icons: Simple Icons (CC0). Fonts: Unbounded and JetBrains Mono (SIL OFL 1.1) via Fontsource.
