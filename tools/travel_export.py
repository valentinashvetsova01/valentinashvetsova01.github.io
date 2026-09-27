"""Export the chosen travel photos to assets/travel/<place>/NN.webp (graded, resized, black bars cropped).

The selection lives in SELECT below: place folder -> list of source file stems in slide order.
"""
import pathlib
import numpy as np
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "assets" / "raw" / "travel"
OUT = ROOT / "assets" / "travel"

SELECT = {
    "Sri Lanka": ["IMG_0772", "IMG_0931", "IMG_1203", "IMG_1312", "IMG_1713", "IMG_1758", "IMG_2843", "IMG_2837",
                  "IMG_1782", "IMG_1951", "IMG_2078", "IMG_2169", "IMG_2389"],
    "Iceland": ["IMG_8998", "IMG_9011", "IMG_9092", "IMG_9207", "IMG_9245"],
    "Turkey": ["IMG_6545", "IMG_6527", "IMG_7083", "IMG_7630", "IMG_7242", "IMG_6522"],
    "Liguria": ["15ed2dc2d3f6efef378f64ff00c9be19", "8cbed90403d5bbe028e5e6e1dbe36d8a", "IMG_5305", "IMG_5320", "IMG_5323", "IMG_5338", "IMG_5886"],
    "Garda": ["IMG_3738", "IMG_3741", "3880e66ac72e62b202959c11fdec9544", "IMG_3825", "IMG_4442", "e3a7475ba678aa79caa42db7f97f46e4", "ed73c8f2863e33c7534905f5faa4016b"],
    "Madrid": ["1fba1979ec7448110b887315800fc3ef", "IMG_1480", "IMG_1682", "IMG_1683", "IMG_1709", "IMG_1728", "IMG_1738"],
    "Florence": ["IMG_1174", "IMG_1181", "IMG_1227", "IMG_1232"],
    "Budapest": ["fe206129b19c0a7a00f7dc76afcc6e2f", "a0b934ead09793d2f2b5796ed7d7a7a5", "IMG_20241130_142615", "IMG_20241130_124449", "IMG_6566", "IMG-20241202-WA0061"],
}


def grade(im, warm=0.3, sat=0.93, lift=4):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    g = a.mean(-1, keepdims=True); a = g + (a - g) * sat
    a[..., 0] *= 1 + 0.035 * warm; a[..., 1] *= 1 + 0.012 * warm; a[..., 2] *= 1 - 0.05 * warm
    a = a * (1 - lift / 255) + lift
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def unbar(im):                              # phone screenshots come with black bars above and below
    a = np.asarray(im.convert("L"))
    rows = np.where(a.mean(1) > 14)[0]
    return im.crop((0, rows[0], im.width, rows[-1] + 1)) if len(rows) else im


for place, stems in SELECT.items():
    d = OUT / place.lower().replace(" ", "-"); d.mkdir(parents=True, exist_ok=True)
    for i, stem in enumerate(stems, 1):
        im = ImageOps.exif_transpose(Image.open(RAW / place / (stem + ".jpg")))
        im = grade(unbar(im) if stem.startswith("IMG_28") else im); im.thumbnail((1300, 1300), Image.LANCZOS)
        out = d / f"{i:02d}.webp"; im.save(out, "WEBP", quality=72, method=6)
        print(out.relative_to(ROOT), im.size, "wide" if im.width > im.height else "", out.stat().st_size // 1024, "KB")
