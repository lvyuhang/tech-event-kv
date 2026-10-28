#!/usr/bin/env python3
"""从主图生成前景抠图 hero_fg（带透明通道的 PNG），用于文字从主体后面穿过。

用法:
    python scripts/cutout.py heroes/hero_16x9.png                       # 自动选择方法
    python scripts/cutout.py heroes/hero_16x9.png --mask heroes/mask.png  # 已有黑白蒙版（白 = 主体）
    python scripts/cutout.py heroes/hero_16x9.png --method luma --threshold 0.35
输出默认为 <原名>_fg.png。

方法优先级:
  1. --mask：生图工具或 3D 软件导出的蒙版，质量最好
  2. rembg：已安装 rembg（pip install rembg）时自动使用
  3. luma：亮度键，适合"暗背景 + 发光主体"；浅色背景加 --invert
抠图后用 Read 检查边缘：主体边缘应干净，倒影和背景光晕不应被抠进来。
"""
import argparse
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


def from_mask(img, mask_path, feather):
    m = Image.open(mask_path).convert("L").resize(img.size)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA"); out.putalpha(m); return out


def from_rembg(img):
    from rembg import remove  # noqa
    return remove(img.convert("RGBA"))


def from_luma(img, threshold, softness, invert, feather):
    g = ImageOps.grayscale(img)
    if invert:
        g = ImageOps.invert(g)
    lo, hi = int(255 * threshold), int(255 * min(1, threshold + softness))
    lut = [0 if v <= lo else 255 if v >= hi else int((v - lo) / max(1, hi - lo) * 255) for v in range(256)]
    m = g.point(lut).filter(ImageFilter.MedianFilter(5))
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    out = img.convert("RGBA"); out.putalpha(m); return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--out")
    ap.add_argument("--mask")
    ap.add_argument("--method", choices=["auto", "rembg", "luma"], default="auto")
    ap.add_argument("--threshold", type=float, default=0.32)
    ap.add_argument("--softness", type=float, default=0.12)
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--feather", type=float, default=1.2)
    a = ap.parse_args()
    img = Image.open(a.image).convert("RGB")
    out_path = Path(a.out) if a.out else Path(a.image).with_name(Path(a.image).stem + "_fg.png")
    if a.mask:
        res, how = from_mask(img, a.mask, a.feather), "mask"
    else:
        res = None
        if a.method in ("auto", "rembg"):
            try:
                res, how = from_rembg(img), "rembg"
            except ImportError:
                if a.method == "rembg":
                    raise SystemExit("未安装 rembg：pip install rembg")
        if res is None:
            res, how = from_luma(img, a.threshold, a.softness, a.invert, a.feather), "luma"
    res.save(out_path)
    print(f"{out_path}  (method: {how})")


if __name__ == "__main__":
    main()
