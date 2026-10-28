# 设计资料库（标注范例）

这里存放**经过设计师标注**的 KV 范例：正例、反例和过程稿。它是 skill 审美判断的锚点，用在三个地方：

1. **参考调研**（SKILL 第 1.5 步）：先查资料库，再上网搜。资料库里的条目有设计师的判断，比搜索结果可靠。
2. **评分校准**（第 7 步）：打分时把成品和资料库里同类型的正例并排比较（`scripts/moodboard.py`）。
3. **经验沉淀**：反例里设计师写的"差在哪"，归纳后进入 `references/lessons.md`。

## 目录结构

```
library/
├── README.md               本文件
├── TEMPLATE.md             标注模板（复制后填写）
├── INDEX.md                自动生成的索引（不要手改）
└── items/
    └── <id>/               一个范例一个文件夹，id 用 "年份-活动-简称"，如 2025-devday-dumbar
        ├── note.md         标注（按 TEMPLATE.md）
        ├── cover.jpg       成品主图（必需）
        ├── sizes/          延展尺寸（可选）
        └── process/        过程稿、分层、主图原图（可选，非常有价值）
```

## 添加一条

```bash
mkdir -p library/items/2025-xxx && cp library/TEMPLATE.md library/items/2025-xxx/note.md
# 放入 cover.jpg，填写 note.md
python scripts/library_index.py            # 重新生成 INDEX.md
python scripts/library_index.py --tag 玻璃 --verdict good     # 按条件查询
```

## 标注要点

- **好在哪 / 差在哪用设计师自己的话写**，越具体越好（"标题和主体之间的留白刚好是一个字高"比"排版舒服"有用得多）。
- **反例和正例一样重要**：特别是"差一点"的作品——构图对了但字体不对、概念对了但执行老气，这类最能帮 skill 校准。
- **过程稿最有价值**：主图原图 vs 成品，能直接看出后期做了什么。
- **评分用 qa-checklist 的 8 个维度**（1–5 分），方便和 skill 的自评对齐。
- 版权：范例只用于内部学习和对照，不进入交付物，不作为生图模型的参考图输入。
