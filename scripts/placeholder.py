#!/usr/bin/env python3
"""生成占位主图，用于在真实主图出来之前预览版式和留白。

用法:
    python scripts/placeholder.py --ratio 16:9 --focal 0.7,0.5 --theme dark --out heroes/hero_16x9.png
占位图在 focal 位置画一团柔光色块代表主体，方便检查文字会不会压到主体。
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SIZES = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratio", default="16:9")
    ap.add_argument("--focal", default="0.68,0.5")
    ap.add_argument("--theme", default="dark", choices=["dark", "light"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    W, H = SIZES[a.ratio]
    fx, fy = (float(v) for v in a.focal.split(","))
    bg = (12, 8, 26) if a.theme == "dark" else (246, 247, 250)
    im = Image.new("RGB", (W, H), bg)
    layer = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(layer)
    r = min(W, H) * 0.32
    cx, cy = W * fx, H * fy
    colors = [(124, 92, 255), (255, 138, 61), (61, 255, 176), (255, 77, 154)]
    for i, c in enumerate(colors):
        ox = (i - 1.5) * r * 0.45
        oy = ((i % 2) - 0.5) * r * 0.5
        d.ellipse([cx + ox - r * 0.6, cy + oy - r * 0.6, cx + ox + r * 0.6, cy + oy + r * 0.6], fill=c)
    layer = layer.filter(ImageFilter.GaussianBlur(min(W, H) * 0.06))
    im = Image.blend(im, layer, 0.9)
    d2 = ImageDraw.Draw(im)
    d2.line([cx - 20, cy, cx + 20, cy], fill=(255, 255, 255), width=2)
    d2.line([cx, cy - 20, cx, cy + 20], fill=(255, 255, 255), width=2)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    im.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
