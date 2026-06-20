#!/usr/bin/env python3
"""Create Tyler cutout PNG/WebP from fw-banner.png for contact section."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Images" / "fw-banner.png"
OUT_PNG = ROOT / "Images" / "fw-banner-cutout.png"
OUT_WEBP = ROOT / "Images" / "fw-banner-cutout.webp"


def trim_alpha(img: Image.Image, pad: int = 12) -> Image.Image:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    if not bbox:
        return img
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(img.width, bbox[2] + pad)
    bottom = min(img.height, bbox[3] + pad)
    return img.crop((left, top, right, bottom))


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source image: {SRC}")

    raw = remove(SRC.read_bytes())
    img = Image.open(BytesIO(raw)).convert("RGBA")
    img = trim_alpha(img, pad=16)

    img = trim_alpha(img, pad=16)

    # Crop to Tyler only — equipment sits on the right of the banner art.
    w, h = img.size
    person_right = int(w * 0.58)
    img = img.crop((0, 0, person_right, h))
    img = trim_alpha(img, pad=12)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PNG, "PNG", optimize=True)
    img.save(OUT_WEBP, "WEBP", quality=88, method=6, lossless=False)

    print(f"Wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes)")
    print(f"Wrote {OUT_WEBP} ({OUT_WEBP.stat().st_size} bytes) — {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
