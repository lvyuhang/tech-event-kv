#!/usr/bin/env python3
"""设计资料库索引与查询。

    python scripts/library_index.py                         # 重新生成 library/INDEX.md
    python scripts/library_index.py --tag 玻璃 --verdict good # 查询（输出匹配条目）
    python scripts/library_index.py --type AI --board out.jpg # 查询并把命中条目拼成对照板

条目：library/items/<id>/note.md（YAML front matter，见 library/TEMPLATE.md）+ cover.jpg
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent / "library"
DIMS = ["概念", "冲击", "融合", "字体", "排版系统", "图文一体", "克制", "时代感与识别度"]


def load_items():
    items = []
    for note in sorted((ROOT / "items").glob("*/note.md")):
        text = note.read_text(encoding="utf-8")
        if not text.startswith("---"):
            print(f"⚠ 缺少 front matter: {note}", file=sys.stderr); continue
        _, fm, body = text.split("---", 2)
        try:
            meta = yaml.safe_load(fm) or {}
        except yaml.YAMLError as e:
            print(f"⚠ YAML 格式错误，已跳过 {note}：{str(e).splitlines()[0]}（含引号、冒号的值请整体加单引号）", file=sys.stderr); continue
        meta["_dir"] = note.parent
        cover = next((p for p in note.parent.iterdir() if p.stem == "cover"), None)
        meta["_cover"] = cover
        meta["_body"] = body.strip()
        sc = meta.get("scores") or {}
        vals = [sc.get(d, 0) or 0 for d in DIMS]
        meta["_total"] = sum(vals) if all(vals) else None
        items.append(meta)
    return items


def match(it, a):
    if a.verdict and it.get("verdict") != a.verdict: return False
    if a.type and a.type not in str(it.get("event_type", "")): return False
    if a.tier and a.tier != it.get("brand_tier"): return False
    if a.tag and not all(t in (it.get("tags") or []) for t in a.tag): return False
    if a.system and a.system != it.get("type_system"): return False
    return True


def write_index(items):
    lines = ["# 设计资料库索引", "", "> 自动生成：`python scripts/library_index.py`。不要手改。", "",
             f"共 {len(items)} 条。", "",
             "| id | 判定 | 类型 | 品牌层级 | 手法 | 直白度 | 排版 | 总分 | 标签 |", "|---|---|---|---|---|---|---|---|---|"]
    for it in items:
        c = it.get("concept") or {}
        lines.append("| [{id}](items/{id}/note.md) | {v} | {t} | {tier} | {op} | {lit} | {sys} | {tot} | {tags} |".format(
            id=it.get("id", it["_dir"].name), v=it.get("verdict", ""), t=it.get("event_type", ""), tier=it.get("brand_tier", ""),
            op=c.get("operator", ""), lit=c.get("literalness", ""), sys=it.get("type_system", ""),
            tot=it["_total"] if it["_total"] is not None else "—", tags="、".join(it.get("tags") or [])))
    (ROOT / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(ROOT / "INDEX.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", action="append")
    ap.add_argument("--verdict", choices=["good", "bad", "near", "process"])
    ap.add_argument("--type")
    ap.add_argument("--tier")
    ap.add_argument("--system")
    ap.add_argument("--board", help="把命中条目的 cover 拼成对照板（调用 moodboard.py）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = load_items()
    querying = any([a.tag, a.verdict, a.type, a.tier, a.system, a.board])
    if not querying:
        write_index(items); return
    hits = [it for it in items if match(it, a)]
    for it in hits:
        c = it.get("concept") or {}
        if a.json:
            print(json.dumps({k: v for k, v in it.items() if not k.startswith("_")}, ensure_ascii=False, default=str))
        else:
            print(f"- {it.get('id')} [{it.get('verdict')}] {it.get('title', '')} · {c.get('operator', '')} {c.get('literalness', '')} · 总分 {it['_total'] or '—'}")
            print(f"  {it['_dir'] / 'note.md'}")
    if not hits:
        print("没有匹配的条目")
    if a.board and hits:
        lst = [{"file": str(it["_cover"]), "title": f"{it.get('id')} [{it.get('verdict')}]",
                "note": (it.get("concept") or {}).get("thesis", "")} for it in hits if it["_cover"]]
        tmp = Path(a.board).with_suffix(".list.json")
        tmp.write_text(json.dumps(lst, ensure_ascii=False), encoding="utf-8")
        subprocess.run([sys.executable, str(Path(__file__).parent / "moodboard.py"), str(tmp), "--out", a.board], check=True)


if __name__ == "__main__":
    main()
