"""Key a chroma-green image to a transparent WebP.

usage: python tools/key.py <in.png> <out.webp> [--max 900] [--split N]
Alpha comes from the colour distance to the background (sampled at the corners), so darker or
yellower greens (leaves, stems) survive; green spill on the edges is pulled back to neutral.
--split N cuts a row of N separate objects into <out>-1.webp ... <out>-N.webp.
"""
import argparse
import numpy as np
from PIL import Image


def key(img, hard=False):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    s = max(8, min(h, w) // 40)
    bg = np.median(np.concatenate([a[:s, :s], a[:s, -s:], a[-s:, :s], a[-s:, -s:]]).reshape(-1, 3), axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(-1))
    alpha = np.clip((d - 38) / (95 - 38), 0, 1)                   # soft edge between the two thresholds
    if hard:  # objects with no green of their own: any green-dominant pixel (incl. cast shadows) goes
        exc = a[..., 1] - np.maximum(a[..., 0], a[..., 2])
        alpha = np.minimum(alpha, np.clip(1 - (exc - 4) / 26, 0, 1))
    # spill suppression: green can't exceed the brighter of red/blue by much near the edge
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    limit = np.maximum(r, b) + 12
    edge = alpha < 1
    g = np.where(edge | (g > limit * 1.15), np.minimum(g, limit), g)
    if hard:  # translucent petals pick up green from behind: pull green down to the red/blue average
        g = np.minimum(g, (r + b) / 2 + 6)
    out = np.dstack([r, g, b, alpha * 255]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def crop(im, pad=0.04):
    box = im.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    w, h = im.size
    p = int(max(w, h) * pad)
    return im.crop((max(0, box[0] - p), max(0, box[1] - p), min(w, box[2] + p), min(h, box[3] + p)))


def save(im, path, mx):
    im.thumbnail((mx, mx), Image.LANCZOS)
    im.save(path, "WEBP", quality=86, method=6)
    print(path, im.size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--max", type=int, default=900)
    ap.add_argument("--split", type=int, default=0)
    ap.add_argument("--hard", action="store_true", help="object has no green parts: also remove green shadows")
    a = ap.parse_args()
    im = key(Image.open(a.src), a.hard)
    if a.split:
        al = np.asarray(im.getchannel("A")) > 12
        cols = al.any(0)
        runs, start = [], None
        for x, on in enumerate(list(cols) + [False]):
            if on and start is None: start = x
            if not on and start is not None:
                runs.append((start, x)); start = None
        runs = sorted(runs, key=lambda r: r[1] - r[0], reverse=True)[: a.split]
        for i, (x0, x1) in enumerate(sorted(runs), 1):
            save(crop(im.crop((x0, 0, x1, im.height))), a.dst.replace(".webp", f"-{i}.webp"), a.max)
    else:
        save(crop(im), a.dst, a.max)
