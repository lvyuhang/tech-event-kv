#!/usr/bin/env python3
"""把 config.json 渲染成多尺寸 KV PNG，并生成总览图 contact_sheet.png。

用法:
    python scripts/render.py config.json --out out/ [--only screen_16x9,square]

依赖: playwright (python -m playwright install chromium), Pillow
config 中的相对路径（hero、logo_image）都相对 config.json 所在目录解析。
"""
import argparse
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
    if cfg.get("hero"):
        cfg["hero"] = to_uri(cfg["hero"], base)
    t = cfg.get("text", {})
    if t.get("logo_image"):
        t["logo_image"] = to_uri(t["logo_image"], base)
    for s in cfg.get("sizes", []):
        if s.get("hero"):
            s["hero"] = to_uri(s["hero"], base)
    return cfg


def contact_sheet(files, out_path, gap=24, col_w=640):
    from PIL import Image, ImageDraw
    imgs = [(f, Image.open(f).convert("RGB")) for f in files]
    thumbs = []
    for f, im in imgs:
        scale = col_w / im.width if im.width > im.height * 1.2 else (col_w * 0.62) / max(im.width, im.height) * (im.height / im.width if im.width < im.height else 1)
        thumbs.append((f.stem, im.resize((int(im.width * scale), int(im.height * scale)))))
    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    row_h = []
    for r in range(rows):
        row_h.append(max(t.height for _, t in thumbs[r * cols:(r + 1) * cols]) + 28)
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
    cfg = resolve_paths(json.loads(cfg_path.read_text(encoding="utf-8")), base)
    out = Path(args.out)
    if not out.is_absolute():
        out = (Path.cwd() / out)
    out.mkdir(parents=True, exist_ok=True)

    sizes = cfg.get("sizes") or []
    if args.only:
        keep = set(args.only.split(","))
        sizes = [s for s in sizes if s["name"] in keep]
    if not sizes:
        sys.exit("config.sizes 为空")

    template = TEMPLATE.read_text(encoding="utf-8")
    files = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for s in sizes:
            payload = json.dumps({"config": cfg, "size": s}, ensure_ascii=False)
            html = template.replace("</head>", f"<script>window.KV = {payload};</script>\n</head>", 1)
            tmp = out / f".{s['name']}.html"
            tmp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": s["w"], "height": s["h"]}, device_scale_factor=s.get("dpr", 1))
            page.on("pageerror", lambda e: print("  页面脚本错误:", e, file=sys.stderr))
            page.goto(tmp.as_uri())
            page.wait_for_selector("body[data-ready='1']", state="attached", timeout=15000)
            page.wait_for_load_state("networkidle")
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
