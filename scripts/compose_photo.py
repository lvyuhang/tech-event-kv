#!/usr/bin/env python3
"""把生图模型出的"玻璃 / 透明物体"照片和排版好的内容（代码、文字、图案）合成在一起。

生图模型画不出准确的文字，但很会画玻璃、光和阴影。做法是分工：
  - 模型只出"透明物体放在空白纸面上"的照片（光、阴影、焦散、高光都来自照片）
  - 内容页（如代码页）由排版生成
  - 本脚本把内容页"印"在照片的纸面上，并在透明物体内部做折射

用法:
    python scripts/compose_photo.py --photo heroes/drop_16x9.png \
        --outside heroes/page_A.png [--inside heroes/page_B.png] --out heroes/hero_16x9.png \
        [--circle 0.5,0.42,0.18] [--mag 1.5] [--debug heroes/detect.png]

--circle cx,cy,r（cx/cy 相对宽高，r 相对高度）不给时自动检测：
找照片里边缘最强的圆形区域。**一定用 --debug 输出的检测图确认位置**，不准就手动给 --circle。
内容页尺寸会被缩放到和照片一致；内容页的底色应接近纸面颜色（脚本按纸面颜色归一化）。
"""
import argparse

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def load(p, size=None):
    im = Image.open(p).convert("RGB")
    if size and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255


def paper_color(P):
    b = np.concatenate([P[:8].reshape(-1, 3), P[-8:].reshape(-1, 3), P[:, :8].reshape(-1, 3), P[:, -8:].reshape(-1, 3)])
    return np.median(b, 0)


def detect_circle(P):
    g = P.mean(-1)
    g = ndimage.gaussian_filter(g, 1.2)
    mag = np.hypot(ndimage.sobel(g, 0), ndimage.sobel(g, 1))
    thr = np.quantile(mag, 0.985)
    ys, xs = np.nonzero(mag > thr)
    if len(xs) < 30:
        raise SystemExit("没检测到明显的透明物体边缘，请用 --circle 手动指定")
    # 最大连通块
    lab, n = ndimage.label(ndimage.binary_dilation(mag > thr, iterations=3))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    keep = lab[ys, xs] == (np.argmax(sizes) + 1)
    xs, ys = xs[keep].astype(float), ys[keep].astype(float)
    # 代数最小二乘拟合圆
    A = np.c_[2 * xs, 2 * ys, np.ones_like(xs)]
    b = xs ** 2 + ys ** 2
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    r = np.sqrt(c + cx ** 2 + cy ** 2)
    return cx, cy, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True)
    ap.add_argument("--outside", required=True)
    ap.add_argument("--inside")
    ap.add_argument("--out", required=True)
    ap.add_argument("--circle")
    ap.add_argument("--mag", type=float, default=1.5)
    ap.add_argument("--fringe", type=float, default=0.01)
    ap.add_argument("--ink", type=float, default=1.0, help="内容的浓度（印在纸上的深浅）")
    ap.add_argument("--debug")
    a = ap.parse_args()

    P = load(a.photo)
    H, W, _ = P.shape
    A = load(a.outside, (W, H))
    B = load(a.inside, (W, H)) if a.inside else A
    if a.circle:
        cx, cy, r = map(float, a.circle.split(",")); cx, cy, R = cx * W, cy * H, r * H
    else:
        cx, cy, R = detect_circle(P)
        R *= 0.985
    print(f"circle: cx={cx / W:.3f} cy={cy / H:.3f} r={R / H:.3f}")

    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = xs - cx, ys - cy
    rr = np.clip(np.hypot(dx, dy) / R, 0, 1)
    inside = np.clip((R - np.hypot(dx, dy)) / 1.5 + 0.5, 0, 1)
    k = (1 / a.mag) * (1 + 0.28 * rr ** 2.5) + 0.10 * np.clip((rr - 0.86) / 0.14, 0, 1) ** 2
    chans = []
    for c, f in enumerate([1 + a.fringe * rr ** 4, 1.0, 1 - a.fringe * rr ** 4]):
        chans.append(ndimage.map_coordinates(B[..., c], [cy + dy * k * f, cx + dx * k * f], order=1, mode="nearest"))
    refr = np.stack(chans, -1)
    content = A * (1 - inside[..., None]) + refr * inside[..., None]

    # 内容按"油墨"印在纸面上：相对底色的变暗量乘到照片上
    paper = paper_color(P)
    base = paper_color(A)
    ink = np.clip(content / np.maximum(base, 1e-3), 0, 1.2)
    ink = 1 - (1 - ink) * a.ink
    out = np.clip(P * ink, 0, 1)
    Image.fromarray((out * 255).astype(np.uint8)).save(a.out)
    print(a.out)
    if a.debug:
        im = Image.fromarray((P * 255).astype(np.uint8)); d = ImageDraw.Draw(im)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(255, 0, 80), width=3)
        d.line([cx - 12, cy, cx + 12, cy], fill=(255, 0, 80), width=2); d.line([cx, cy - 12, cx, cy + 12], fill=(255, 0, 80), width=2)
        im.save(a.debug)


if __name__ == "__main__":
    main()
