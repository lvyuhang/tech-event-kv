#!/usr/bin/env python3
"""生图模型适配器 —— 把这里接到你自己的模型上。

skill 只通过这个文件调用生图模型，换模型只改这里。

用法:
    python scripts/image_model.py --prompt-file prompts/hero_16x9.txt --ratio 16:9 --out heroes/hero_16x9.png
    python scripts/image_model.py --check      # 检查是否已配置

提示词文件格式: 正向提示词在前；如有负面提示，另起一行以 "Negative:" 开头。

两种接法，二选一:
  A. 通用 HTTP 接口：设置环境变量即可，不用改代码
       KV_IMAGE_ENDPOINT   POST 地址
       KV_IMAGE_API_KEY    (可选) 作为 Bearer token
       KV_IMAGE_MODEL      (可选) 原样放进请求体 "model"
     请求体: {"model", "prompt", "negative_prompt", "aspect_ratio", "width", "height"}
     响应需包含以下任一字段（支持一层嵌套，如 data[0].b64_json）:
       image_base64 / b64_json / url
  B. 直接改写下面的 generate() 函数，调用你的 SDK。

未配置时退出码为 2，skill 会把提示词交给用户手动生成。
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

RATIO_TO_SIZE = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1536, 1536),
    "3:4": (1152, 1536),
    "4:3": (1536, 1152),
    "21:9": (2520, 1080),
}


class NotConfigured(Exception):
    pass


def parse_prompt_file(path):
    text = Path(path).read_text(encoding="utf-8").strip()
    pos, neg = text, ""
    for marker in ("\nNegative:", "\nnegative:", "\n负面:"):
        if marker in text:
            pos, neg = text.split(marker, 1)
            break
    return " ".join(pos.replace("|", " ").split()), neg.strip()


def _find_image(obj):
    if isinstance(obj, dict):
        for k in ("image_base64", "b64_json", "url"):
            if isinstance(obj.get(k), str):
                return k, obj[k]
        for v in obj.values():
            r = _find_image(v)
            if r:
                return r
    if isinstance(obj, list) and obj:
        return _find_image(obj[0])
    return None


def generate(prompt, negative, ratio, out_path):
    """生成一张图并保存到 out_path。接自有 SDK 时改写这个函数。"""
    endpoint = os.environ.get("KV_IMAGE_ENDPOINT")
    if not endpoint:
        raise NotConfigured("未设置 KV_IMAGE_ENDPOINT，也未改写 generate()")
    w, h = RATIO_TO_SIZE.get(ratio, (1920, 1080))
    body = {
        "model": os.environ.get("KV_IMAGE_MODEL", ""),
        "prompt": prompt,
        "negative_prompt": negative,
        "aspect_ratio": ratio,
        "width": w,
        "height": h,
    }
    headers = {"Content-Type": "application/json"}
    if os.environ.get("KV_IMAGE_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["KV_IMAGE_API_KEY"]
    req = urllib.request.Request(endpoint, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    found = _find_image(data)
    if not found:
        raise RuntimeError("响应里找不到 image_base64 / b64_json / url: " + json.dumps(data)[:300])
    kind, val = found
    if kind == "url":
        with urllib.request.urlopen(val, timeout=300) as r:
            raw = r.read()
    else:
        raw = base64.b64decode(val.split(",", 1)[-1])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_bytes(raw)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-file")
    ap.add_argument("--ratio", default="16:9")
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        ok = bool(os.environ.get("KV_IMAGE_ENDPOINT"))
        print("configured" if ok else "not configured")
        sys.exit(0 if ok else 2)
    pos, neg = parse_prompt_file(a.prompt_file)
    try:
        print(generate(pos, neg, a.ratio, a.out))
    except NotConfigured as e:
        print(f"生图模型未配置：{e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
