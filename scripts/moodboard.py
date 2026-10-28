#!/usr/bin/env python3
"""把调研收集的参考图拼成一张带标注的情绪板。

用法:
    python scripts/moodboard.py refs/ --out refs/moodboard.jpg
    python scripts/moodboard.py refs/list.json --out refs/moodboard.jpg [--cols 4] [--width 2400]

list.json: [{"file": "01_xxx.jpg", "title": "某大会 2025", "note": "借：光溢出；避：玻璃字形"}]
（file 相对 list.json 所在目录）。传目录时用文件名作为标题。
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    import glob
    for p in glob.glob("/usr/share/fonts/**/*CJK*.tt*", recursive=True):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def collect(src):
    src = Path(src)
    if src.is_dir():
        return [{"file": str(p), "title": p.stem, "note": ""} for p in sorted(src.iterdir())
                if p.suffix.lower() in EXTS and p.stem != "moodboard"]
    items = json.loads(src.read_text(encoding="utf-8"))
    for it in items:
        it["file"] = str((src.parent / it["file"]).resolve())
    return items


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for ch in text:
        if draw.textlength(cur + ch, font=font) > width:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default="moodboard.jpg")
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--width", type=int, default=2400)
    a = ap.parse_args()
    items = [it for it in collect(a.src) if Path(it["file"]).exists()]
    if not items:
        raise SystemExit("没有找到图片")
    gap = 28
    cw = (a.width - gap * (a.cols + 1)) // a.cols
    ft, fn = load_font(26), load_font(21)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    tiles = []
    for i, it in enumerate(items, 1):
        im = Image.open(it["file"]).convert("RGB")
        im = im.resize((cw, int(im.height * cw / im.width)))
        title = f"{i:02d}  {it.get('title', '')}"
        notes = wrap(probe, it.get("note", ""), fn, cw) if it.get("note") else []
        cap_h = 56 + 30 * len(notes)
        tile = Image.new("RGB", (cw, im.height + cap_h), (250, 250, 252))
        tile.paste(im, (0, 0))
        d = ImageDraw.Draw(tile)
        d.text((0, im.height + 10), title, font=ft, fill=(20, 20, 28))
        for j, ln in enumerate(notes):
            d.text((0, im.height + 44 + 30 * j), ln, font=fn, fill=(95, 95, 110))
        tiles.append(tile)
    # 瀑布流：每张放进当前最矮的一栏
    heights = [gap] * a.cols
    pos = []
    for t in tiles:
        c = heights.index(min(heights))
        pos.append((gap + c * (cw + gap), heights[c]))
        heights[c] += t.height + gap
    board = Image.new("RGB", (a.width, max(heights)), (236, 236, 240))
    for t, p in zip(tiles, pos):
        board.paste(t, p)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    board.save(a.out, quality=88)
    print(a.out)


if __name__ == "__main__":
    main()
