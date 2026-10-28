#!/usr/bin/env python3
"""把 config.json 渲染成多尺寸 KV PNG，并生成总览图 contact_sheet.png。

用法:
    python scripts/render.py config.json --out out/ [--only screen_16x9,square]

依赖: playwright (python -m playwright install chromium), Pillow
config 中的相对路径（hero、hero_fg、logo_image、fonts.files）都相对 config.json 所在目录解析。

渲染前会从主图自动取色（accent / glow / shade），config.color_from_hero=false 可关闭。
渲染时检测字体是否真的加载，未加载会打印 ⚠ 警告——不要忽略。
"""
import argparse
import colorsys
import json
import math
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "kv.html"


def to_uri(p, base):
    if not p or str(p).startswith(("http://", "https://", "data:", "file://")):
        return p
    path = (base / p).resolve()
    if not path.exists():
        sys.exit(f"找不到文件: {path}")
    return path.as_uri()


def resolve_paths(cfg, base):
    cfg = json.loads(json.dumps(cfg))
    for holder in [cfg] + list(cfg.get("sizes", [])):
        for k in ("hero", "hero_fg", "mark_texture"):
            if holder.get(k):
                holder[k] = to_uri(holder[k], base)
    t = cfg.get("text", {})
    if t.get("logo_image"):
        t["logo_image"] = to_uri(t["logo_image"], base)
    files = (cfg.get("fonts") or {}).get("files") or {}
    for fam, src in files.items():
        items = src if isinstance(src, list) else [src]
        out = []
        for it in items:
            if isinstance(it, str):
                out.append(to_uri(it, base))
            else:
                it = dict(it); it["src"] = to_uri(it["src"], base); out.append(it)
        files[fam] = out
    return cfg


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(int(max(0, min(255, c))) for c in rgb)


def palette_from_image(path, theme="dark"):
    """从主图提取 accent（主色相）、glow（第二色相）、shade（暗部/底色）。

    只统计鲜艳像素（饱和度、亮度够高）的色相直方图，避免大面积背景把主体颜色淹没。
    """
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((240, 240))
    px = list(im.get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.getdata())
    bins = [[0.0, 0.0, 0.0, 0.0] for _ in range(12)]  # weight, r, g, b
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s < 0.18 or v < 0.3:
            continue
        w = s * v * v
        k = int(h * 12) % 12
        bins[k][0] += w; bins[k][1] += r * w; bins[k][2] += g * w; bins[k][3] += b * w

    def color(k, vmin):
        w, r, g, b = bins[k]
        h, s, v = colorsys.rgb_to_hsv(r / w / 255, g / w / 255, b / w / 255)
        r, g, b = colorsys.hsv_to_rgb(h, min(1, max(s, 0.35) * 1.1), max(v, vmin))
        return _hex((r * 255, g * 255, b * 255))

    res = {}
    order = sorted(range(12), key=lambda k: bins[k][0], reverse=True)
    if bins[order[0]][0] > 0:
        a = order[0]
        res["accent"] = color(a, 0.92 if theme == "dark" else 0.5)
        far = [k for k in order[1:] if bins[k][0] > bins[a][0] * 0.02 and min(abs(k - a), 12 - abs(k - a)) >= 2]
        res["glow"] = color(far[0], 0.9 if theme == "dark" else 0.55) if far else res["accent"]
    lum = sorted(px, key=lambda p: 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2])
    part = lum[: max(1, len(lum) // 4)] if theme == "dark" else lum[-max(1, len(lum) // 4):]
    avg = [sum(p[i] for p in part) / len(part) for i in range(3)]
    res["shade"] = _hex(avg)
    res["bg"] = res["shade"]
    return res


def contact_sheet(files, out_path, gap=24, col_w=640):
    from PIL import Image, ImageDraw
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        if im.width > im.height * 1.2:
            scale = col_w / im.width
        else:
            scale = (col_w * 0.62) / im.height * (im.height / im.width if im.width < im.height else 1)
        thumbs.append((f.stem, im.resize((int(im.width * scale), int(im.height * scale)))))
    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    row_h = [max(t.height for _, t in thumbs[r * cols:(r + 1) * cols]) + 28 for r in range(rows)]
    W = cols * col_w + (cols + 1) * gap
    H = sum(row_h) + (rows + 1) * gap
    sheet = Image.new("RGB", (W, H), (236, 236, 240))
    d = ImageDraw.Draw(sheet)
    y = gap
    for r in range(rows):
        x = gap
        for name, t in thumbs[r * cols:(r + 1) * cols]:
            sheet.paste(t, (x, y))
            d.text((x, y + t.height + 6), name, fill=(60, 60, 70))
            x += col_w + gap
        y += row_h[r] + gap
    sheet.save(out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", default="out")
    ap.add_argument("--only", default="", help="逗号分隔的尺寸 name，只渲染这些")
    args = ap.parse_args()

    cfg_path = Path(args.config).resolve()
    base = cfg_path.parent
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg = resolve_paths(raw, base)
    out = Path(args.out)
    if not out.is_absolute():
        out = Path.cwd() / out
    out.mkdir(parents=True, exist_ok=True)

    sizes = cfg.get("sizes") or []
    if args.only:
        keep = set(args.only.split(","))
        sizes = [s for s in sizes if s["name"] in keep]
    if not sizes:
        sys.exit("config.sizes 为空")

    # 每张不同的主图各取一次色
    pal_cache = {}

    def auto_for(s):
        src = s.get("hero") or cfg.get("hero")
        theme = s.get("theme", cfg.get("theme", "dark"))
        if not src or not str(src).startswith("file://") or cfg.get("color_from_hero") is False:
            return {}
        key = (src, theme)
        if key not in pal_cache:
            from urllib.parse import unquote, urlparse
            pal_cache[key] = palette_from_image(unquote(urlparse(src).path), theme)
            print(f"  取色 {Path(unquote(urlparse(src).path)).name}: {pal_cache[key]}")
        return {"palette": pal_cache[key]}

    template = TEMPLATE.read_text(encoding="utf-8")
    files, warned = [], set()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in sizes:
            payload = json.dumps({"config": cfg, "size": s, "auto": auto_for(s)}, ensure_ascii=False)
            html = template.replace("</head>", f"<script>window.KV = {payload};</script>\n</head>", 1)
            tmp = out / f".{s['name']}.html"
            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": s["w"], "height": s["h"]}, device_scale_factor=s.get("dpr", 1))
            page.on("pageerror", lambda e: print("  页面脚本错误:", e, file=sys.stderr))
            page.goto(tmp.as_uri())
            page.wait_for_selector("body[data-ready='1']", state="attached", timeout=30000)
            for w in page.evaluate("window.KV_WARN || []"):
                if w not in warned:
                    warned.add(w); print(f"  ⚠ {w}")
            dest = out / f"{s['name']}_{s['w']}x{s['h']}.png"
            page.screenshot(path=str(dest))
            page.close()
            tmp.unlink()
            files.append(dest)
            print(f"✓ {dest}")
        browser.close()

    sheet = out / "contact_sheet.png"
    contact_sheet(files, sheet)
    print(f"✓ {sheet}")


if __name__ == "__main__":
    main()
