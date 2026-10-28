#!/usr/bin/env python3
"""生成式图层：由真实代码字符组成的"流"。

用于"汇聚 / 流动 / 涌现"类概念：散落的代码片段 → 单个字符 → 光点 → 一条发光的流。
近看能读出代码，远看是一条完整的形，大尺寸下细节撑得住。

用法:
    python scripts/glyph_flow.py --w 1920 --h 1080 --out heroes/flow_16x9 \
        --path "0.02,1.02 0.28,0.80 0.52,0.66 0.70,0.46 0.84,0.22 0.98,-0.04" \
        --accent "#D4FF3A" [--code src.txt] [--n 9000] [--seed 3]

输出:
    <out>_hero.png     底 + 字符流的合成图，没有生图主图时直接作为 hero
    <out>_fg.png       只含汇聚段的透明图层，作为 hero_fg：发光的流从文字前面穿过，散落的片段留在文字后面
    <out>_layer.png    完整的透明字符流，叠加在生图主图上使用
    <out>_bg.png       深色底 + 细点阵，作为 hero（没有生图主图时使用）
    <out>_texture.png  密排代码纹理，作为巨字填充（title_fill: texture）

--path 是归一化坐标的控制点（x,y，左上为 0,0），按流动方向排列：起点散开，终点汇聚。
--code 用真实、与活动相关的代码；不提供时用内置示例。
"""
import argparse
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

DEFAULT_CODE = """
import { galaxy } from "@galaxy/sdk"
const stars = await galaxy.collect({ from: "every-developer" })
for (const line of stars) { river.merge(line) }
git commit -m "first line" && git push origin main
export default function build(idea) { return ship(idea) }
model.generate({ prompt, tokens: 4096 }).then(deploy)
fn main() { let mut river = Stream::new(); river.flow(); }
def converge(points): return sum(points) / len(points)
while (true) { listen(); learn(); light(); }
SELECT * FROM commits WHERE author = 'you' ORDER BY created_at;
kubectl apply -f galaxy.yaml --namespace devcon-2026
npm create galaxy@latest && cd galaxy && npm run dev
"""

MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "C:/Windows/Fonts/consola.ttf",
]


def find_font(user):
    for p in ([user] if user else []) + MONO_CANDIDATES:
        if p and Path(p).exists():
            return p
    import glob
    hits = glob.glob("/usr/share/fonts/**/*Mono*.tt*", recursive=True)
    if hits:
        return hits[0]
    raise SystemExit("找不到等宽字体，请用 --font 指定")


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def catmull(points, n=3000):
    P = np.array(points, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n // (len(P) - 3), endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2])
    C = np.array(out)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(C, axis=0).T))]
    return C, seg / seg[-1]


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--out", required=True)
    ap.add_argument("--path", default="0.02,1.02 0.28,0.80 0.52,0.66 0.70,0.46 0.84,0.22 0.98,-0.04")
    ap.add_argument("--accent", default="#D4FF3A")
    ap.add_argument("--ink", default="#06070A", help="背景色")
    ap.add_argument("--code")
    ap.add_argument("--font")
    ap.add_argument("--n", type=int, default=9000)
    ap.add_argument("--spread", type=float, default=0.30, help="起点散开的宽度（相对画面高度）")
    ap.add_argument("--core", type=float, default=0.016, help="汇聚后的宽度")
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--fg-from", type=float, default=0.3, help="_fg.png 只保留 t 大于此值的部分（汇聚段），用于从文字前面穿过")
    a = ap.parse_args()
    W, H = a.w, a.h
    S = min(W, H) / 1080
    rng = np.random.default_rng(a.seed)
    font_path = find_font(a.font)
    code = Path(a.code).read_text(encoding="utf-8") if a.code else DEFAULT_CODE
    tokens = [t for t in re.split(r"\s+", code) if t]
    chars = [c for c in code if not c.isspace()]
    accent = np.array(hex_rgb(a.accent), float)
    ink = hex_rgb(a.ink)

    pts = [tuple(map(float, p.split(","))) for p in a.path.split()]
    C, T = catmull([(x * W, y * H) for x, y in pts])
    tang = np.gradient(C, axis=0); tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
    norm = np.stack([-tang[:, 1], tang[:, 0]], 1)

    def at(t):
        i = np.clip(np.searchsorted(T, t), 0, len(T) - 1)
        return C[i], norm[i]

    def width(t):
        # 起点散开 → 汇聚成窄流 → 末端再散开成星（银河）
        return H * (a.spread * (1 - t) ** 2.4 + a.core + 0.11 * smooth(t, 0.80, 1.0) ** 1.5)

    # 采样：越往后越密
    u = rng.random(a.n * 3)
    keep = rng.random(len(u)) < (0.25 + 2.6 * u ** 1.6) / 2.85
    ts = rng.permutation(u[keep])[: a.n]
    ts = ts[np.argsort(-ts)]  # 先画汇聚段，再画散落的个体（个体在上层、互不遮挡）
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fonts = {}

    def F(sz):
        sz = max(6, int(round(sz)))
        if sz not in fonts:
            fonts[sz] = ImageFont.truetype(font_path, sz)
        return fonts[sz]

    ci = ti = 0
    CELL = max(4, int(5 * S))
    occ = np.zeros((H // CELL + 4, W // CELL + 4), bool)  # 占位网格：字符和片段互不重叠

    def free(p, wpx, hpx):
        x0, x1 = int((p[0] - wpx / 2) // CELL) + 2, int((p[0] + wpx / 2) // CELL) + 3
        y0, y1 = int((p[1] - hpx / 2) // CELL) + 2, int((p[1] + hpx / 2) // CELL) + 3
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(occ.shape[1], x1), min(occ.shape[0], y1)
        if x1 <= x0 or y1 <= y0:
            return True
        if occ[y0:y1, x0:x1].any():
            return False
        occ[y0:y1, x0:x1] = True
        return True
    gray0 = np.array([110, 116, 128.0]); gray1 = np.array([214, 218, 224.0]); white = np.array([245, 247, 250.0])
    for t in ts:
        c, nv = at(t)
        w = width(t)
        # 散落段明显稀疏：个体要一个个看得清
        if t < 0.3 and rng.random() > 0.18 + 0.82 * smooth(t, 0.0, 0.3):
            continue
        lat = rng.normal(0, 0.42) if t > 0.15 else rng.uniform(-1.1, 1.1)
        p = c + nv * lat * w
        if not (-60 < p[0] < W + 60 and -60 < p[1] < H + 60):
            continue
        core = math.exp(-(lat / 0.35) ** 2)
        # 颜色：灰（个体）→ 白 → 强调色（汇聚的核心）
        if t < 0.45:
            col = gray0 + (gray1 - gray0) * smooth(t, 0.0, 0.45)
        else:
            col = gray1 + (white - gray1) * smooth(t, 0.45, 0.7)
        col = col + (accent - col) * (core * smooth(t, 0.5, 0.85))
        alpha = (0.55 + 0.45 * smooth(t, 0.0, 0.5)) * (1 - 0.75 * smooth(t, 0.9, 1.0))
        size = (26 * (1 - t) ** 1.25 + 4.2) * S * rng.uniform(0.8, 1.2)
        rgba = tuple(int(v) for v in col) + (int(255 * alpha),)
        if t < 0.22 and rng.random() < 0.5:
            tok = tokens[ti % len(tokens)]
            if not free(p, size * 0.82 * 0.6 * len(tok), size * 0.82):
                continue
            ti += 1
            d.text(tuple(p), tok, font=F(size * 0.82), fill=rgba, anchor="mm")
        elif size > 8.5 * S:
            if not free(p, size * 0.62, size * 0.9):
                continue
            ch = chars[ci % len(chars)]; ci += 1
            d.text(tuple(p), ch, font=F(size), fill=rgba, anchor="mm")
        else:
            r = max(0.7, size * 0.16)
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=rgba)

    # 光晕：只给汇聚段，散落的个体保持清晰
    arr = np.asarray(layer).astype(np.float32) / 255
    rgb, al = arr[..., :3] * arr[..., 3:], arr[..., 3]
    ys, xs = np.mgrid[0:H, 0:W]
    # 估计每个像素对应的 t：用到曲线最近点
    sub = C[::6]; tsub = T[::6]
    from scipy.spatial import cKDTree
    _, idx = cKDTree(sub).query(np.stack([xs.ravel(), ys.ravel()], 1), k=1)
    tmap = tsub[idx].reshape(H, W)
    gmask = (smooth(tmap, 0.5, 0.82) * (1 - 0.6 * smooth(tmap, 0.9, 1.0)))[..., None]
    g1 = ndimage.gaussian_filter(rgb * gmask, (5 * S, 5 * S, 0))
    g2 = ndimage.gaussian_filter(rgb * gmask, (26 * S, 26 * S, 0))
    g3 = ndimage.gaussian_filter(rgb * gmask, (80 * S, 80 * S, 0))
    glow = g1 * 0.55 + g2 * 0.55 + g3 * 0.7
    out_rgb = rgb + glow * (1 - al[..., None])
    out_a = np.clip(al + glow.max(-1) * 1.2, 0, 1)
    out = np.dstack([np.clip(out_rgb / np.maximum(out_a[..., None], 1e-4), 0, 1), out_a])
    Image.fromarray((out * 255).astype(np.uint8), "RGBA").save(a.out + "_layer.png")
    fgm = smooth(tmap, a.fg_from, a.fg_from + 0.12)
    fg = out.copy(); fg[..., 3] *= fgm
    Image.fromarray((fg * 255).astype(np.uint8), "RGBA").save(a.out + "_fg.png")
    # 合成好的主图（底 + 字符流），作为 hero
    base_only = True

    # 背景：墨色 + 细点阵 + 汇聚处极淡的强调色
    bg = np.ones((H, W, 3), np.float32) * np.array(ink, float) / 255
    end = C[int(len(C) * 0.8)]
    rad = np.hypot(xs - end[0], ys - end[1]) / H
    bg += (accent / 255) * (np.exp(-rad * 2.4) * 0.035)[..., None]
    step = max(8, int(24 * S))
    grid = ((xs % step) < 1.5 * S) & ((ys % step) < 1.5 * S)
    bg += grid[..., None] * 0.045
    Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8)).save(a.out + "_bg.png")
    comp = np.clip(bg, 0, 1) * (1 - out[..., 3:]) + out[..., :3] * out[..., 3:]
    Image.fromarray((comp * 255).astype(np.uint8)).save(a.out + "_hero.png")

    # 代码纹理：浅底深字，用作巨字填充（近看是代码，远看是实心字）
    tex = Image.new("RGB", (W, H), (238, 240, 244))
    td = ImageDraw.Draw(tex)
    fs = max(7, int(9 * S)); tf = ImageFont.truetype(font_path, fs)
    lines = [l for l in code.strip().splitlines() if l.strip()]
    y, k = 0, 0
    while y < H:
        line = ""
        while len(line) < W / (fs * 0.55):
            line += lines[k % len(lines)].strip() + "   "; k += 1
        td.text((-(k * 37) % (fs * 8), y), line, font=tf, fill=(206, 210, 218))
        y += int(fs * 1.25)
    tex.save(a.out + "_texture.png")
    print("\n".join(a.out + s for s in ["_hero.png", "_fg.png", "_layer.png", "_bg.png", "_texture.png"]))


if __name__ == "__main__":
    main()
