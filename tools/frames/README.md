Drop your waving clip here as `wave.mp4`, then run from the `tools/` folder:

    python make_assets.py path/to/1.png path/to/2.png frames/wave.mp4
    python build.py

Every frame is extracted at 12 fps, background-matted and embedded; `hero.svg` then plays the clip
inside the viewfinder (play once, hold the last frame, fade, repeat). With no frames here, the hero
shows your still portrait instead.
