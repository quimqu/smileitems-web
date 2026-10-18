"""Genera les imatges de la web a partir dels originals de raw/.

Els originals són les fotos dels productes i els bàners de la botiga de
Smile Items a Amazon (són nostres). Ús, des de l'arrel del projecte:

    py -3 tools/images.py
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
OUT = ROOT / "public" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def webp(src, dst, max_w, quality=80):
    im = Image.open(RAW / src).convert("RGB")
    im.thumbnail((max_w, max_w * 2))
    im.save(OUT / dst, "WEBP", quality=quality, method=6)
    print(dst, im.size)


def logo():
    """Logo negre sobre transparent: la tinta passa a ser l'alfa."""
    gray = Image.open(RAW / "store-logo.png").convert("L")
    alpha = ImageOps.invert(gray)
    ink = Image.new("RGBA", gray.size, (17, 17, 17, 255))
    ink.putalpha(alpha)
    # Files 158-683: paraula + somriure. 748-829: el lema en anglès.
    mark = ink.crop((0, 140, 1040, 700)).crop(ink.crop((0, 140, 1040, 700)).getbbox())
    mark.thumbnail((480, 480))
    mark.save(OUT / "logo.png", optimize=True)
    print("logo.png", mark.size)

    # Icona quadrada per a Apple / xarxes: logo sobre groc de marca.
    sq = Image.new("RGBA", (512, 512), (255, 201, 40, 255))
    m = mark.copy()
    m.thumbnail((400, 400))
    sq.alpha_composite(m, ((512 - m.width) // 2, (512 - m.height) // 2))
    sq.convert("RGB").resize((180, 180), Image.LANCZOS).save(ROOT / "public" / "apple-touch-icon.png")
    sq.convert("RGB").save(OUT / "icon-512.png")


def og():
    """Imatge per compartir (1200x630): la foto de la festa."""
    im = Image.open(RAW / "store-hero.png").convert("RGB")
    w, h = im.size
    target = 1200 / 630
    new_w = int(h * target)
    left = (w - new_w) // 2
    im = im.crop((left, 0, left + new_w, h)).resize((1200, 630), Image.LANCZOS)
    im.save(OUT / "og.jpg", quality=82, optimize=True)
    print("og.jpg", im.size)


if __name__ == "__main__":
    logo()
    og()
    webp("store-hero.png", "festa.webp", 1600, 78)
    webp("store-hero.png", "festa-800.webp", 800, 78)
    for name in ["smiley-1", "caca-1", "cubos-1", "laberintos-1",
                 "libros-2", "wc-1"]:
        webp(f"{name}.jpg", f"{name}.webp", 720)
