"""Prepare image assets for the profile cards.
Usage:  python make_assets.py 1.png 2.png [wave.mp4]
 - 1.png : character on a white background (hero + ID badge)
 - 2.png : pointing character on dark background (connect card)
 - wave.mp4 (optional): short clip; every frame is extracted to frames/ and
   background-matted so build.py plays it inside hero.svg.
"""
import sys, os, subprocess, glob, shutil
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
os.makedirs(A, exist_ok=True)

def matte_white(im, grow=2, blur=1.2):
    """Remove a flat white background by flood-filling from the border.
    The cartoon's dark outline stops the fill, so white hoodies stay opaque."""
    a = np.array(im.convert("RGBA"))
    rgb = a[..., :3].astype(int)
    mn, mx = rgb.min(2), rgb.max(2)
    near_white = (mn >= 236) & ((mx - mn) < 14)
    lab, _ = ndi.label(near_white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    bg = ndi.binary_dilation(bg, iterations=grow)           # shave the white fringe
    alpha = Image.fromarray((~bg).astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(blur))
    a[..., 3] = np.array(alpha)
    return Image.fromarray(a)

def to_png8(im, path, colors=255):
    """Palette PNG with alpha: small, and still a real PNG (never WebP)."""
    q = im.convert("RGBA").quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    q.save(path, optimize=True)
    print(os.path.basename(path), os.path.getsize(path) // 1024, "KB", im.size)

def main():
    src1, src2 = sys.argv[1], sys.argv[2]
    video = sys.argv[3] if len(sys.argv) > 3 else None

    c1 = matte_white(Image.open(src1))
    W, H = c1.size
    # hero still (bottom edge is cropped in the source art, so trim it)
    hero = c1.crop((0, 0, W, int(H * 0.93)))
    to_png8(hero.resize((760, int(760 * hero.height / hero.width)), Image.LANCZOS), f"{A}/hero_still.png")
    # badge portrait: just the head and shoulders
    face = c1.crop((int(W * .22), int(H * .02), int(W * .76), int(H * .46)))
    to_png8(face.resize((330, int(330 * face.height / face.width)), Image.LANCZOS), f"{A}/badge_face.png")

    # pointing character: crop, erase baked-in neon text, keep the dark art
    im2 = Image.open(src2).convert("RGB")
    crop = im2.crop((120, 100, 1560, 2330))
    arr = np.array(crop).astype(float)
    x0, y0, x1, y1 = 930 - 120, 300 - 100, 1560 - 120, 612 - 100
    # fill vertically between clean rows above and below the sign, heavily smoothed
    T = ndi.gaussian_filter1d(np.median(arr[y0 - 14:y0 - 4, x0:x1], axis=0), 40, axis=0)
    B = ndi.gaussian_filter1d(np.median(arr[y1 + 4:y1 + 12, x0:x1], axis=0), 40, axis=0)
    for i in range(y1 - y0):
        t = i / (y1 - y0)
        arr[y0 + i, x0:x1] = 0.4 * ((1 - t) * T + t * B) + 0.6 * np.array([19, 23, 36])
    erased = Image.fromarray(arr.astype(np.uint8))
    m = Image.new("L", crop.size, 0)
    m.paste(255, (x0, y0, x1, y1))
    m = m.filter(ImageFilter.GaussianBlur(14))
    crop = Image.composite(erased, crop, m)
    small = crop.resize((520, int(520 * crop.height / crop.width)), Image.LANCZOS)
    q = small.quantize(colors=200, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    q.save(f"{A}/pointing.png", optimize=True)
    print("pointing.png", os.path.getsize(f"{A}/pointing.png") // 1024, "KB", small.size)

    if video:
        fr = os.path.join(HERE, "frames")
        shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        subprocess.check_call(["ffmpeg", "-loglevel", "error", "-i", video, "-vf", "fps=12", f"{fr}/raw_%03d.png"])
        for i, f in enumerate(sorted(glob.glob(f"{fr}/raw_*.png"))):
            fm = matte_white(Image.open(f))
            fm = fm.crop((0, 0, fm.width, int(fm.height * .93)))
            to_png8(fm.resize((380, int(380 * fm.height / fm.width)), Image.LANCZOS), f"{fr}/f{i:03d}.png", colors=128)
            os.remove(f)
        print("frames:", len(glob.glob(f"{fr}/f*.png")))

if __name__ == "__main__":
    main()
