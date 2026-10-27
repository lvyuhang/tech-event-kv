# tech-event-kv

为程序 / 技术类运营活动（开发者大会、技术峰会、黑客松、发布会、AI 大会、技术沙龙）构思并产出 KV 主视觉物料的 Claude skill。

**核心思路：图文分层。** 外部生图模型只生成不含文字的主图；标题、日期、logo 由 HTML 模板排版，再用 Playwright 批量导出多尺寸。

## 结构

```
SKILL.md                    主流程：brief → 符号提炼 → 风格方向 → 主图提示词 → 排版 → 延展 → 自检
references/
  brief.md                  brief 字段、活动类型 → 默认调性
  motif.md                  主视觉符号提炼方法、技术隐喻素材库、俗套禁用清单
  directions.md             8 个技术活动风格方向配方
  prompt-recipes.md         6 段式主图提示词、版式 → 留白构图句
  layout-type.md            信息层级、L1–L4 版式、字体、安全区
  sizes.md                  延展尺寸表与主图分配规则
  qa-checklist.md           自检清单
  case-studies.md           参考案例拆解（Alibaba / WDCC / TCL TIC）
templates/
  kv.html                   配置驱动的排版模板
  config.example.json       配置示例
scripts/
  image_model.py            生图模型适配器（接你自己的模型）
  render.py                 多尺寸渲染 + 总览图
  placeholder.py            占位主图，用于预览版式
```

## 快速开始

```bash
pip install playwright pillow && python -m playwright install chromium

mkdir -p demo && cp templates/config.example.json demo/config.json
python scripts/placeholder.py --ratio 16:9 --focal 0.68,0.5 --out demo/heroes/hero_16x9.png
python scripts/placeholder.py --ratio 9:16 --focal 0.5,0.7 --out demo/heroes/hero_9x16.png
python scripts/render.py demo/config.json --out demo/out
```

## 接入生图模型

二选一：

- 设置环境变量 `KV_IMAGE_ENDPOINT`（以及可选的 `KV_IMAGE_API_KEY`、`KV_IMAGE_MODEL`），走通用 HTTP 接口；
- 或直接改写 `scripts/image_model.py` 里的 `generate()`。

未配置时 skill 会把提示词交给用户手动生成。

## 状态

v0.1。已知差距与 v2 计划：标题字设计、图文穿插（三层合成）、概念发散与独特性筛选、主图后期、审美评分。
