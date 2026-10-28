#!/usr/bin/env python3
"""玻璃透镜 / 水滴后期：在成品 KV 上放一滴有折射、阴影、焦散的玻璃。

适合"看见 / 放大 / 透明 / 预见"类概念，也适合延续"玻璃"品牌资产（如 Liquid Glass）。
透镜内可以显示另一张图（--inside），用来表达"透过它看到的是另一种状态"（例如补全后的代码）。

用法:
    python scripts/glass_lens.py --outside out/kv_A.png [--inside out/kv_B.png] \
        --cx 0.78 --cy 0.42 --r 0.19 --out out/kv.png [--mag 1.55] [--light -0.6,-0.8]

坐标 cx / cy 是相对画面宽 / 高的比例，r 是相对画面高度的比例。
outside 和 inside 应该是同尺寸、同排版的两次渲染，只在透镜要"变"的地方不同。
"""
import argparse

import numpy as np
from PIL import Image
from scipy import ndimage


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255


def sample(img, xs, ys):
    return np.stack([ndimage.map_coordinates(img[..., c], [ys, xs], order=1, mode="nearest") for c in range(3)], -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outside", required=True)
    ap.add_argument("--inside")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cx", type=float, required=True)
    ap.add_argument("--cy", type=float, required=True)
    ap.add_argument("--r", type=float, required=True)
    ap.add_argument("--mag", type=float, default=1.55, help="中心放大倍数")
    ap.add_argument("--light", default="-0.6,-0.8", help="光源方向（屏幕坐标，左上为负）")
    ap.add_argument("--fringe", type=float, default=0.012, help="边缘色散强度，0 关闭")
    ap.add_argument("--shadow", type=float, default=0.16)
    a = ap.parse_args()

    A = load(a.outside)
    B = load(a.inside) if a.inside else A
    H, W, _ = A.shape
    cx, cy, R = a.cx * W, a.cy * H, a.r * H
    lx, ly = map(float, a.light.split(",")); ln = np.hypot(lx, ly); lx, ly = lx / ln, ly / ln
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = xs - cx, ys - cy
    d = np.hypot(dx, dy); r = d / R
    inside = r < 1

    # 1. 纸面上的阴影与焦散（光从 light 方向来，阴影落在反方向）
    sx, sy = -lx * R * 0.16, -ly * R * 0.16
    ds = np.hypot(xs - (cx + sx), ys - (cy + sy)) / R
    shadow = (ds < 0.97).astype(np.float32)
    shadow = ndimage.gaussian_filter(shadow, R * 0.07) * a.shadow
    caustic = np.exp(-(np.hypot(xs - (cx + sx * 2.2), ys - (cy + sy * 2.2)) / (R * 0.28)) ** 2) * 0.07
    base = A * (1 - shadow[..., None]) + caustic[..., None] * (1 - shadow[..., None] * 2)

    # 2. 折射：中心放大、边缘强烈弯折（球冠近似）
    rr = np.clip(r, 0, 1)
    k = (1 / a.mag) * (1 + 0.28 * rr ** 2.5) + 0.10 * np.clip((rr - 0.86) / 0.14, 0, 1) ** 2
    def refract(f):
        return cx + dx * k * f, cy + dy * k * f
    xr, yr = refract(1 + a.fringe * rr ** 4)
    xg, yg = refract(1.0)
    xb, yb = refract(1 - a.fringe * rr ** 4)
    lens = np.stack([
        ndimage.map_coordinates(B[..., 0], [yr, xr], order=1, mode="nearest"),
        ndimage.map_coordinates(B[..., 1], [yg, xg], order=1, mode="nearest"),
        ndimage.map_coordinates(B[..., 2], [yb, xb], order=1, mode="nearest"),
    ], -1)

    # 3. 玻璃本身的明暗：受光侧边缘亮、背光侧内缘暗、左上高光
    ndx, ndy = dx / np.maximum(d, 1e-3), dy / np.maximum(d, 1e-3)
    facing = -(ndx * lx + ndy * ly)            # 1 = 朝向光源
    rim = np.clip((rr - 0.93) / 0.07, 0, 1) ** 2
    band = np.clip((rr - 0.78) / 0.22, 0, 1)
    lens = lens * (1 - 0.10 * band * np.clip(-facing, 0, 1) - 0.05 * band)[..., None]
    lens = lens * (1 - 0.025 * (1 - rr))[..., None]  # 玻璃体本身极轻的吸收，让它看起来有厚度
    lens = lens + (0.45 * rim * np.clip(facing, 0, 1) ** 1.5)[..., None]
    hx, hy = cx + lx * R * 0.55, cy + ly * R * 0.55
    ang = np.arctan2(ly, lx) + np.pi / 2
    ux, uy = (xs - hx) * np.cos(ang) + (ys - hy) * np.sin(ang), -(xs - hx) * np.sin(ang) + (ys - hy) * np.cos(ang)
    spec = np.exp(-((ux / (R * 0.26)) ** 2 + (uy / (R * 0.055)) ** 2))  # 沿边缘的细长高光
    lens = lens + (spec * 0.32)[..., None]
    # 背光侧内缘的一道细亮线（玻璃内部反射），让体积更像实物
    inner = np.exp(-((rr - 0.9) / 0.03) ** 2) * np.clip(-facing, 0, 1) * 0.18
    lens = lens + inner[..., None]

    # 4. 抗锯齿合成 + 外缘一圈极细的暗线
    edge = np.clip((R - d) / 1.5 + 0.5, 0, 1)
    ring = np.exp(-((d - R) / 1.4) ** 2) * 0.30
    out = base * (1 - edge[..., None]) + np.clip(lens, 0, 1) * edge[..., None]
    out = out * (1 - ring[..., None] * (1 - edge[..., None]))
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
