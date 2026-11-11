"""Make web-sized copies of the paintings for the site.

Usage: python3 tools/build_images.py

Reads the original photos (paths below, relative to this repo's parent
folders) and writes assets/works/<slug>-800.jpg and <slug>-1600.jpg.
Camera metadata (including GPS) is dropped; the color profile is kept so
colors match the originals.
"""

import os

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
PRO = os.path.dirname(SITE)                       # .../professional artist
PORTFOLIO = os.path.join(os.path.dirname(PRO), "portfolio")
OUT = os.path.join(SITE, "assets", "works")

WORKS = {
    "uncles-old-house": os.path.join(PORTFOLIO, "Thesis1-uncles_old_house.jpeg"),
    "goojingin-undur": os.path.join(PORTFOLIO, "Thesis2-goojingin_undur.jpeg"),
    "disconnected": os.path.join(PORTFOLIO, "thesis3-connected.jpeg"),
    "the-way-back": os.path.join(PORTFOLIO, "thesis4-the_way_back.jpeg"),
    "palace-grill": os.path.join(PORTFOLIO, "thesis5-palace_grill.jpeg"),
    "reach": os.path.join(PRO, "Munkhjargal_1.jpeg"),
    "flow": os.path.join(PRO, "Munkhjargal_2.jpeg"),
    "expand": os.path.join(PRO, "Munkhjargal_3.jpeg"),
    "climb": os.path.join(PRO, "Munkhjargal_4.jpeg"),
    "settle": os.path.join(PRO, "Munkhjargal_5.jpeg"),
    "narrow": os.path.join(PRO, "small-moments-narrow.jpeg"),
}
SIZES = (800, 1600)


def save(im, path, icc):
    im.save(path, "JPEG", quality=84, optimize=True, progressive=True, icc_profile=icc)


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, src in WORKS.items():
        with Image.open(src) as original:
            icc = original.info.get("icc_profile")
            im = ImageOps.exif_transpose(original).convert("RGB")
        print(f"{slug}: {im.width}x{im.height}")
        for size in SIZES:
            copy = im.copy()
            copy.thumbnail((size, size), Image.LANCZOS)
            save(copy, os.path.join(OUT, f"{slug}-{size}.jpg"), icc)

    # Social preview: 1200x630 crop of the home page painting.
    with Image.open(WORKS["uncles-old-house"]) as original:
        icc = original.info.get("icc_profile")
        im = ImageOps.exif_transpose(original).convert("RGB")
    share = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
    save(share, os.path.join(SITE, "assets", "share.jpg"), icc)


if __name__ == "__main__":
    main()
